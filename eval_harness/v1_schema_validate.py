"""Lightweight schema-adjacent validation for v1 public records.

This deliberately avoids third-party JSON-schema dependencies so CI remains simple.
The canonical field contract lives in schemas/v1_record_schemas.json and the full
cross-object integrity checks live in v1_validate.py.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from v1_common import DIMENSIONS, FAILURE_TAGS, PASS_FAIL, RESPONSE_ORIGINS, RISK_LEVELS, load_v1


def require(row: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if field not in row or row[field] in (None, "") and field not in {"model_id", "provider"}:
            errors.append(f"{label}: missing {field}")


def validate_schema_shape(base: Path) -> list[str]:
    data = load_v1(base)
    errors: list[str] = []
    for case in data["cases"]:
        label = case.get("case_id", "case")
        require(case, ["case_id", "task_type", "risk_level", "prompt", "target_failure_modes", "expected_safe_behavior", "unsafe_behavior", "rubric_id", "synthetic_provenance"], label, errors)
        if case.get("risk_level") not in RISK_LEVELS:
            errors.append(f"{label}: invalid risk_level {case.get('risk_level')}")
        if not isinstance(case.get("expected_safe_behavior"), list) or len(case.get("expected_safe_behavior", [])) < 2:
            errors.append(f"{label}: expected_safe_behavior must contain at least two items")
    for resp in data["responses"]:
        label = resp.get("response_id", "response")
        require(resp, ["response_id", "case_id", "response_label", "response_origin", "response_text", "response_hash", "redaction_status"], label, errors)
        if resp.get("response_origin") not in RESPONSE_ORIGINS:
            errors.append(f"{label}: invalid response_origin {resp.get('response_origin')}")
        if resp.get("response_label") not in {"A", "B"}:
            errors.append(f"{label}: invalid response_label {resp.get('response_label')}")
    for ann in data["annotations"]:
        label = ann.get("annotation_id", "annotation")
        require(ann, ["annotation_id", "case_id", "response_id", "reviewer_id", "annotation_round", "rubric_version", "dimension_scores", "overall_score", "severity", "pass_fail", "failure_tags", "rationale"], label, errors)
        dims = ann.get("dimension_scores", {})
        for dim in DIMENSIONS:
            if dim not in dims:
                errors.append(f"{label}: missing dimension {dim}")
            elif not isinstance(dims[dim], int) or not 0 <= dims[dim] <= 4:
                errors.append(f"{label}: dimension {dim} must be integer 0..4")
        if ann.get("pass_fail") not in PASS_FAIL:
            errors.append(f"{label}: invalid pass_fail {ann.get('pass_fail')}")
        for tag in ann.get("failure_tags", []):
            if tag not in FAILURE_TAGS:
                errors.append(f"{label}: invalid failure tag {tag}")
    return errors


def main() -> int:
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/v1")
    errors = validate_schema_shape(base)
    if errors:
        print("v1 schema-shape validation failed")
        for err in errors[:80]:
            print(f"- {err}")
        if len(errors) > 80:
            print(f"... {len(errors)-80} more")
        return 1
    print("v1 schema-shape validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
