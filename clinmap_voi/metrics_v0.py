#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clinmap_voi.common import DATA_DIR, ROOT, load_dataset  # noqa: E402
from clinmap_voi.validate_v0 import validate  # noqa: E402

REPORT_DIR = ROOT / "report"


def pct(num: int, den: int) -> float:
    return round((num / den) * 100, 2) if den else 0.0


def compute_design_metrics(data_dir: Path = DATA_DIR) -> dict[str, Any]:
    errors = validate(data_dir)
    data = load_dataset(data_dir)
    families = data["families"]
    variants = data["variants"]
    relations = data["relations"]
    prompts = data["prompts"]

    variants_by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for variant in variants:
        variants_by_family[variant["family_id"]].append(variant)

    relation_by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relation in relations:
        relation_by_family[relation["family_id"]].append(relation)

    one_primary_changed_fact = sum(1 for v in variants if len(v.get("changed_facts", [])) == 1)
    action_change_variants = sum(1 for v in variants if v.get("action_change_expected") is True)
    invariant_variants = sum(1 for v in variants if v.get("risk_direction") == "invariant")
    relation_action_change = sum(1 for r in relations if r.get("action_change_expected") is True)
    invariant_relations = sum(1 for r in relations if r.get("expected_direction") == "invariant")

    family_completeness = {
        family["family_id"]: {
            "variant_count": len(variants_by_family[family["family_id"]]),
            "relation_count": len(relation_by_family[family["family_id"]]),
            "has_low_risk_control": any(v["variant_type"] == "low_risk_control" for v in variants_by_family[family["family_id"]]),
            "has_nuisance_invariance": any(v["variant_type"] == "nuisance_invariance" for v in variants_by_family[family["family_id"]]),
            "has_user_pressure": any(v["variant_type"] == "user_pressure" for v in variants_by_family[family["family_id"]]),
            "has_contraindication_or_medication_risk": any(v["variant_type"] == "contraindication_or_medication_risk" for v in variants_by_family[family["family_id"]]),
        }
        for family in families
    }

    complete_families = sum(
        1
        for item in family_completeness.values()
        if item["variant_count"] == 8
        and item["relation_count"] == 7
        and item["has_low_risk_control"]
        and item["has_nuisance_invariance"]
        and item["has_user_pressure"]
        and item["has_contraindication_or_medication_risk"]
    )

    metrics = {
        "status": "design_metrics_only_no_model_performance",
        "validation_passed": not errors,
        "validation_error_count": len(errors),
        "counts": {
            "decision_families": len(families),
            "variants": len(variants),
            "metamorphic_relations": len(relations),
            "model_prompts": len(prompts),
            "source_context_records": len(data["sources"]),
            "metric_blueprint_records": len(data["metric_blueprint"]),
        },
        "coverage": {
            "domains": dict(sorted(Counter(f["domain"] for f in families).items())),
            "splits": dict(sorted(Counter(f["split"] for f in families).items())),
            "variant_types": dict(sorted(Counter(v["variant_type"] for v in variants).items())),
            "risk_directions": dict(sorted(Counter(v["risk_direction"] for v in variants).items())),
            "relation_types": dict(sorted(Counter(r["relation_type"] for r in relations).items())),
            "relation_expected_directions": dict(sorted(Counter(r["expected_direction"] for r in relations).items())),
            "optimal_model_moves": dict(sorted(Counter(v["optimal_model_move"] for v in variants).items())),
        },
        "relation_oracle_design": {
            "complete_families": complete_families,
            "complete_family_rate_pct": pct(complete_families, len(families)),
            "one_primary_changed_fact_variants": one_primary_changed_fact,
            "one_primary_changed_fact_rate_pct": pct(one_primary_changed_fact, len(variants)),
            "action_change_variants": action_change_variants,
            "invariant_variants": invariant_variants,
            "action_change_relations": relation_action_change,
            "invariant_relations": invariant_relations,
        },
        "claim_boundaries": {
            "benchmark_claim_allowed": False,
            "model_ranking_allowed": False,
            "clinical_validation_claim_allowed": False,
            "patient_advice_claim_allowed": False,
            "current_allowed_claim": "synthetic relation-labeled evaluation method and local-run-ready prompt pack",
        },
        "next_gates": [
            "run local model pilot on a 16-40 prompt subset",
            "collect actual model outputs with run manifests",
            "create blinded human review queue",
            "score relation annotations with evidence spans",
            "compute model-level metrics only after review completion",
        ],
    }
    return metrics


def write_markdown(metrics: dict[str, Any], path: Path) -> None:
    lines = [
        "# ClinMAP-VOI Phase 1 Design Metrics",
        "",
        "Status: design metrics only. No model-output performance or ranking is claimed.",
        "",
        "## Counts",
        "",
        "| Item | Count |",
        "|---|---:|",
    ]
    for key, value in metrics["counts"].items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Relation-oracle coverage", "", "| Metric | Value |", "|---|---:|"])
    for key, value in metrics["relation_oracle_design"].items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Variant types", "", "| Variant type | Count |", "|---|---:|"])
    for key, value in metrics["coverage"]["variant_types"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Relation types", "", "| Relation type | Count |", "|---|---:|"])
    for key, value in metrics["coverage"]["relation_types"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend([
        "",
        "## Claim boundary",
        "",
        "This Phase 1 package is a synthetic, relation-labeled evaluation method and local-run-ready prompt pack. It is not a clinical validation, not a healthcare benchmark, not patient advice, and not a model ranking.",
        "",
        "## Next gates",
        "",
    ])
    for gate in metrics["next_gates"]:
        lines.append(f"- {gate}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    metrics = compute_design_metrics()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / "clinmap_voi_phase1_design_metrics.json"
    md_path = REPORT_DIR / "clinmap_voi_phase1_design_metrics.md"
    json_path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(metrics, md_path)
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0 if metrics["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
