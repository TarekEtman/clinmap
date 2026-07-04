"""Validate v1 separated synthetic evaluation data."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from v1_common import (
    CALIBRATION_ROLES,
    DIMENSIONS,
    FAILURE_TAGS,
    PASS_FAIL,
    RESPONSE_ORIGINS,
    RISK_LEVELS,
    load_v1,
)

REQUIRED_CASE = [
    "case_id", "case_version", "case_family", "task_type", "domain_subdomain", "risk_level", "calibration_role",
    "prompt", "prompt_language", "missing_context_flags", "target_failure_modes", "expected_safe_behavior", "unsafe_behavior",
    "acceptable_variants", "disallowed_response_content", "source_anchor_ids", "rubric_id", "rubric_version", "taxonomy_version",
    "severity_floor", "cap_rules_applicable", "split", "leakage_group_id", "synthetic_provenance", "content_hash",
]
REQUIRED_RESPONSE = [
    "response_id", "case_id", "case_version", "response_label", "response_origin", "model_id", "provider", "model_snapshot",
    "run_id", "system_prompt_id", "temperature", "top_p", "max_tokens", "seed", "tool_access", "retrieval_context",
    "prompt_render_hash", "response_text", "response_hash", "generated_at", "redaction_status", "dedupe_hash",
]
REQUIRED_ANNOTATION = [
    "annotation_id", "case_id", "response_id", "reviewer_id", "reviewer_role", "reviewer_training_version", "blind_status",
    "annotation_round", "rubric_id", "rubric_version", "taxonomy_version", "dimension_scores", "raw_weighted_score",
    "overall_score", "severity", "pass_fail", "failure_tags", "cap_rules_triggered", "evidence_spans", "rationale",
    "safer_behavior", "confidence", "time_spent_sec", "annotated_at", "quality_flags",
]


def missing(row: dict[str, Any], required: list[str]) -> list[str]:
    return [field for field in required if field not in row]


def validate(base: Path) -> list[str]:
    data = load_v1(base)
    errors: list[str] = []
    cases = data["cases"]
    responses = data["responses"]
    annotations = data["annotations"]
    adjudications = data["adjudications"]
    preferences = data["preferences"]
    source_anchors = data["source_anchors"]
    manifest = data["manifest"]

    def unique(rows: list[dict[str, Any]], field: str, label: str) -> set[str]:
        ids = [str(r.get(field, "")) for r in rows]
        for item, count in Counter(ids).items():
            if not item:
                errors.append(f"{label}: missing {field}")
            elif count > 1:
                errors.append(f"{label}: duplicate {field}={item}")
        return set(ids)

    case_ids = unique(cases, "case_id", "cases")
    response_ids = unique(responses, "response_id", "responses")
    annotation_ids = unique(annotations, "annotation_id", "annotations")
    source_ids = unique(source_anchors, "source_anchor_id", "source_anchors")

    if manifest:
        expected_counts = {"case_count": len(cases), "response_count": len(responses), "annotation_count": len(annotations)}
        for key, expected in expected_counts.items():
            if manifest.get(key) != expected:
                errors.append(f"manifest.{key}={manifest.get(key)} but observed {expected}")
        if manifest.get("synthetic_only") is not True:
            errors.append("manifest.synthetic_only must be true")

    for case in cases:
        for field in missing(case, REQUIRED_CASE):
            errors.append(f"case {case.get('case_id')}: missing {field}")
        if case.get("risk_level") not in RISK_LEVELS:
            errors.append(f"case {case.get('case_id')}: invalid risk_level {case.get('risk_level')}")
        if case.get("calibration_role") not in CALIBRATION_ROLES:
            errors.append(f"case {case.get('case_id')}: invalid calibration_role {case.get('calibration_role')}")
        for tag in case.get("target_failure_modes", []):
            if tag not in FAILURE_TAGS:
                errors.append(f"case {case.get('case_id')}: unknown failure tag {tag}")
        for src in case.get("source_anchor_ids", []):
            if src not in source_ids:
                errors.append(f"case {case.get('case_id')}: unknown source_anchor_id {src}")
        prov = case.get("synthetic_provenance", {})
        if prov.get("review_status") not in {"draft", "approved", "rejected"}:
            errors.append(f"case {case.get('case_id')}: invalid synthetic_provenance.review_status")

    responses_by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for resp in responses:
        for field in missing(resp, REQUIRED_RESPONSE):
            errors.append(f"response {resp.get('response_id')}: missing {field}")
        if resp.get("case_id") not in case_ids:
            errors.append(f"response {resp.get('response_id')}: unknown case_id {resp.get('case_id')}")
        if resp.get("response_label") not in {"A", "B", "C", "D"}:
            errors.append(f"response {resp.get('response_id')}: invalid response_label")
        if resp.get("response_origin") not in RESPONSE_ORIGINS:
            errors.append(f"response {resp.get('response_id')}: invalid response_origin {resp.get('response_origin')}")
        if not str(resp.get("response_text", "")).strip():
            errors.append(f"response {resp.get('response_id')}: empty response_text")
        responses_by_case[resp.get("case_id", "")].append(resp)

    for case_id, rows in responses_by_case.items():
        labels = sorted(row["response_label"] for row in rows)
        if labels != ["A", "B"]:
            errors.append(f"case {case_id}: expected exactly A/B responses, found {labels}")

    annotations_by_response: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ann in annotations:
        for field in missing(ann, REQUIRED_ANNOTATION):
            errors.append(f"annotation {ann.get('annotation_id')}: missing {field}")
        if ann.get("case_id") not in case_ids:
            errors.append(f"annotation {ann.get('annotation_id')}: unknown case_id")
        if ann.get("response_id") not in response_ids:
            errors.append(f"annotation {ann.get('annotation_id')}: unknown response_id")
        if ann.get("pass_fail") not in PASS_FAIL:
            errors.append(f"annotation {ann.get('annotation_id')}: invalid pass_fail")
        dims = ann.get("dimension_scores", {})
        for dim in DIMENSIONS:
            if dim not in dims:
                errors.append(f"annotation {ann.get('annotation_id')}: missing dimension {dim}")
            elif not isinstance(dims[dim], int) or not 0 <= dims[dim] <= 4:
                errors.append(f"annotation {ann.get('annotation_id')}: invalid dimension {dim}={dims.get(dim)}")
        for tag in ann.get("failure_tags", []):
            if tag not in FAILURE_TAGS:
                errors.append(f"annotation {ann.get('annotation_id')}: unknown failure tag {tag}")
        annotations_by_response[ann.get("response_id", "")].append(ann)

    for response_id in response_ids:
        rounds = sorted(a.get("annotation_round") for a in annotations_by_response.get(response_id, []))
        if rounds != [1, 2]:
            errors.append(f"response {response_id}: expected annotation rounds [1, 2], found {rounds}")

    adjudicated_response_ids = {adj.get("response_id") for adj in adjudications}
    for response_id, anns in annotations_by_response.items():
        if len(anns) != 2:
            continue
        anns = sorted(anns, key=lambda row: row["annotation_round"])
        delta = abs(int(anns[0]["overall_score"]) - int(anns[1]["overall_score"]))
        if delta > 1 and response_id not in adjudicated_response_ids:
            errors.append(f"response {response_id}: score delta {delta} requires adjudication")
        if anns[0]["pass_fail"] != anns[1]["pass_fail"] and response_id not in adjudicated_response_ids:
            errors.append(f"response {response_id}: pass/fail mismatch requires adjudication")

    pref_labels = Counter(pref.get("preferred_response_label") for pref in preferences)
    total_prefs = sum(pref_labels.values())
    if total_prefs:
        a_share = pref_labels.get("A", 0) / total_prefs
        if not 0.45 <= a_share <= 0.55:
            errors.append(f"pairwise preferred label balance outside 45-55%: A share {a_share:.2%}")
    if len(preferences) != len(cases):
        errors.append(f"preferences count {len(preferences)} does not match case count {len(cases)}")

    for pref in preferences:
        if pref.get("case_id") not in case_ids:
            errors.append(f"preference {pref.get('preference_id')}: unknown case_id")
        for rid in pref.get("response_ids", []):
            if rid not in response_ids:
                errors.append(f"preference {pref.get('preference_id')}: unknown response_id {rid}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="data/v1")
    args = parser.parse_args()
    errors = validate(Path(args.base))
    if errors:
        print("v1 validation failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("v1 validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
