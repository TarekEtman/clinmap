#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clinmap_voi.common import (  # noqa: E402
    ALLOWED_MOVES,
    DATA_DIR,
    EXPECTED_COUNTS,
    EXPECTED_DIRECTIONS,
    FORBIDDEN_PUBLIC_TOKENS,
    RELATION_TYPES,
    RISK_DIRECTIONS,
    SPLITS,
    VARIANT_TYPES,
    load_dataset,
    require_fields,
)

FAMILY_FIELDS = [
    "family_id",
    "base_case_id",
    "variant_case_ids",
    "framework_version",
    "domain",
    "title",
    "decision_problem",
    "voi_question",
    "metamorphic_operators",
    "expected_relation_enums",
    "risk_directions_covered",
    "voi_slots_required",
    "action_change_expected",
    "source_anchor_ids",
    "split",
    "leakage_group_id",
    "human_review_status",
    "decisive_variables",
    "nuisance_variables",
    "allowed_moves",
    "disallowed_moves",
    "content_hash",
    "synthetic_provenance",
]

VARIANT_FIELDS = [
    "variant_id",
    "family_id",
    "parent_family_id",
    "framework_version",
    "split",
    "variant_type",
    "clinical_axis",
    "risk_direction",
    "risk_stratum",
    "visible_prompt",
    "changed_facts",
    "action_change_expected",
    "expected_safe_behavior_delta",
    "disallowed_generic_response",
    "metamorphic_relation",
    "expected_relation",
    "optimal_model_move",
    "acceptable_model_moves",
    "unsafe_model_moves",
    "utility_table",
    "best_utility",
    "scoring_dimensions",
    "prompt_hash",
    "content_hash",
    "human_review_status",
    "synthetic_provenance",
]

RELATION_FIELDS = [
    "relation_id",
    "family_id",
    "framework_version",
    "source_variant_id",
    "target_variant_id",
    "source_variant_type",
    "target_variant_type",
    "relation_type",
    "expected_direction",
    "expected_behavior_change",
    "action_change_expected",
    "metric_hooks",
    "oracle_status",
    "relation_annotation_schema",
    "content_hash",
]


def validate(data_dir: Path = DATA_DIR) -> list[str]:
    errors: list[str] = []
    data = load_dataset(data_dir)
    manifest = data["manifest"]
    families = data["families"]
    variants = data["variants"]
    relations = data["relations"]
    prompts = data["prompts"]
    source_ids = {row["source_id"] for row in data["sources"]}

    if manifest.get("family_count") != EXPECTED_COUNTS["families"]:
        errors.append("manifest family_count mismatch")
    if manifest.get("variant_count") != EXPECTED_COUNTS["variants"]:
        errors.append("manifest variant_count mismatch")
    if manifest.get("metamorphic_relation_count") != EXPECTED_COUNTS["relations"]:
        errors.append("manifest metamorphic_relation_count mismatch")
    if manifest.get("prompt_count") != EXPECTED_COUNTS["prompts"]:
        errors.append("manifest prompt_count mismatch")
    for key in ["synthetic_only", "contains_patient_data", "contains_platform_tasks", "contains_proprietary_rubrics"]:
        if key == "synthetic_only" and manifest.get(key) is not True:
            errors.append("manifest must declare synthetic_only true")
        if key != "synthetic_only" and manifest.get(key) is not False:
            errors.append(f"manifest must declare {key} false")
    perf_status = manifest.get("performance_claim_status")
    perf_pre_hosted = "not_available_no_model_outputs"
    perf_hosted = "available_see_clinmap_voi_v0_performance_metrics"
    if perf_status not in (perf_pre_hosted, perf_hosted):
        errors.append("manifest performance_claim_status must be a known claim boundary value")
    elif perf_status == perf_pre_hosted and manifest.get("model_output_status") == "hosted_collection_complete":
        errors.append("manifest inconsistent: hosted collection complete but performance_claim_status is pre-hosted")
    elif perf_status == perf_hosted:
        if manifest.get("model_output_status") != "hosted_collection_complete":
            errors.append("hosted performance claims require model_output_status hosted_collection_complete")
        if manifest.get("human_annotation_status") not in (
            "complete_primary_and_relations",
            "complete_primary_relations_and_qa",
        ):
            errors.append("hosted performance claims require completed human annotation status")

    ids: dict[str, set[str]] = {"families": set(), "variants": set(), "relations": set(), "prompts": set()}
    for f in families:
        require_fields(f, FAMILY_FIELDS, f.get("family_id", "family"), errors)
        fid = f.get("family_id")
        if fid in ids["families"]:
            errors.append(f"duplicate family_id {fid}")
        ids["families"].add(fid)
        if f.get("split") not in SPLITS:
            errors.append(f"{fid}: invalid split")
        if set(f.get("metamorphic_operators", [])) != RELATION_TYPES:
            errors.append(f"{fid}: missing metamorphic operators")
        if len(f.get("variant_case_ids", [])) != 8:
            errors.append(f"{fid}: expected 8 variant ids")
        if f.get("base_case_id") not in set(f.get("variant_case_ids", [])):
            errors.append(f"{fid}: base_case_id not in variant_case_ids")
        if not set(f.get("source_anchor_ids", [])).issubset(source_ids):
            errors.append(f"{fid}: unknown source anchor")
        provenance = f.get("synthetic_provenance", {})
        if provenance.get("contains_patient_data") is not False or provenance.get("contains_platform_tasks") is not False:
            errors.append(f"{fid}: provenance boundary failure")

    variants_by_id = {}
    variants_by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    prompt_hashes: set[str] = set()
    for v in variants:
        require_fields(v, VARIANT_FIELDS, v.get("variant_id", "variant"), errors)
        vid = v.get("variant_id")
        if vid in ids["variants"]:
            errors.append(f"duplicate variant_id {vid}")
        ids["variants"].add(vid)
        variants_by_id[vid] = v
        variants_by_family[v.get("family_id")].append(v)
        if v.get("family_id") not in ids["families"]:
            errors.append(f"{vid}: unknown family_id")
        if v.get("parent_family_id") != v.get("family_id"):
            errors.append(f"{vid}: parent_family_id mismatch")
        if v.get("variant_type") not in VARIANT_TYPES:
            errors.append(f"{vid}: invalid variant_type")
        if v.get("risk_direction") not in RISK_DIRECTIONS:
            errors.append(f"{vid}: invalid risk_direction")
        if v.get("split") not in SPLITS:
            errors.append(f"{vid}: invalid split")
        if v.get("optimal_model_move") not in ALLOWED_MOVES:
            errors.append(f"{vid}: invalid optimal_model_move")
        if not set(v.get("acceptable_model_moves", [])).issubset(ALLOWED_MOVES):
            errors.append(f"{vid}: invalid acceptable_model_moves")
        if "unchanged_facts" not in v:
            errors.append(f"{vid}: missing field unchanged_facts")
        if len(v.get("changed_facts", [])) != 1:
            errors.append(f"{vid}: expected exactly one primary changed fact")
        ph = v.get("prompt_hash")
        if ph in prompt_hashes:
            errors.append(f"{vid}: duplicate prompt_hash")
        prompt_hashes.add(ph)
        prompt = v.get("visible_prompt", "").lower()
        for token in FORBIDDEN_PUBLIC_TOKENS:
            if token in prompt:
                errors.append(f"{vid}: forbidden target-company token in prompt")

    for fid, rows in variants_by_family.items():
        type_counts = Counter(v["variant_type"] for v in rows)
        if set(type_counts) != VARIANT_TYPES:
            errors.append(f"{fid}: missing variant types {VARIANT_TYPES - set(type_counts)}")
        if any(count != 1 for count in type_counts.values()):
            errors.append(f"{fid}: duplicate variant type in family")

    relations_by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in relations:
        require_fields(r, RELATION_FIELDS, r.get("relation_id", "relation"), errors)
        rid = r.get("relation_id")
        if rid in ids["relations"]:
            errors.append(f"duplicate relation_id {rid}")
        ids["relations"].add(rid)
        fid = r.get("family_id")
        relations_by_family[fid].append(r)
        if fid not in ids["families"]:
            errors.append(f"{rid}: unknown family_id")
        if r.get("source_variant_id") not in variants_by_id:
            errors.append(f"{rid}: unknown source_variant_id")
        if r.get("target_variant_id") not in variants_by_id:
            errors.append(f"{rid}: unknown target_variant_id")
        if r.get("relation_type") not in RELATION_TYPES:
            errors.append(f"{rid}: invalid relation_type")
        if r.get("expected_direction") not in EXPECTED_DIRECTIONS:
            errors.append(f"{rid}: invalid expected_direction")
        if r.get("expected_direction") == "invariant" and r.get("action_change_expected") is not False:
            errors.append(f"{rid}: invariant relation cannot expect action change")
        if r.get("expected_direction") == "increase" and r.get("action_change_expected") is not True:
            errors.append(f"{rid}: increase relation must expect action change")
        schema = r.get("relation_annotation_schema", {})
        if schema.get("evidence_spans_required") is not True:
            errors.append(f"{rid}: evidence spans must be required")

    for fid, rows in relations_by_family.items():
        relation_types = Counter(r["relation_type"] for r in rows)
        if set(relation_types) != RELATION_TYPES:
            errors.append(f"{fid}: missing relation types {RELATION_TYPES - set(relation_types)}")
        if any(count != 1 for count in relation_types.values()):
            errors.append(f"{fid}: duplicate relation type")

    for p in prompts:
        require_fields(p, ["prompt_id", "variant_id", "family_id", "system_prompt", "user_prompt", "expected_policy_label", "prompt_hash"], p.get("prompt_id", "prompt"), errors)
        pid = p.get("prompt_id")
        if pid in ids["prompts"]:
            errors.append(f"duplicate prompt_id {pid}")
        ids["prompts"].add(pid)
        vid = p.get("variant_id")
        if vid not in variants_by_id:
            errors.append(f"{pid}: unknown variant_id")
        elif p.get("prompt_hash") != variants_by_id[vid].get("prompt_hash"):
            errors.append(f"{pid}: prompt_hash mismatch")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("ClinMAP-VOI v0 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ClinMAP-VOI v0 validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
