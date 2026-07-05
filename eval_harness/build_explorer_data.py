"""Build a compact browser data bundle for the static eval explorer."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from v1_common import load_v1

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "explorer" / "data.js"


def main() -> int:
    data = load_v1(ROOT / "data" / "v1")
    anns_by_response = defaultdict(list)
    for ann in data["annotations"]:
        anns_by_response[ann["response_id"]].append(ann)
    responses_by_case = defaultdict(list)
    for resp in data["responses"]:
        first_ann = sorted(anns_by_response[resp["response_id"]], key=lambda a: a["annotation_round"])[0]
        responses_by_case[resp["case_id"]].append({
            "label": resp["response_label"],
            "origin": resp["response_origin"],
            "text": resp["response_text"],
            "score": first_ann["overall_score"],
            "severity": first_ann["severity"],
            "pass_fail": first_ann["pass_fail"],
            "failure_tags": first_ann["failure_tags"],
            "rationale": first_ann["rationale"],
        })
    cases = []
    for case in data["cases"]:
        cases.append({
            "case_id": case["case_id"],
            "task_type": case["task_type"],
            "risk_level": case["risk_level"],
            "prompt": case["prompt"],
            "target_failure_modes": case["target_failure_modes"],
            "expected_safe_behavior": case["expected_safe_behavior"],
            "responses": sorted(responses_by_case[case["case_id"]], key=lambda r: r["label"]),
        })
    bundle = {
        "generated_at": data["manifest"].get("last_updated_at"),
        "counts": {
            "cases": len(data["cases"]),
            "responses": len(data["responses"]),
            "annotations": len(data["annotations"]),
        },
        "claim_boundary": "Synthetic public demo only. Not medical advice, a benchmark, or clinical validation.",
        "cases": cases,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("window.CMB_EXPLORER_DATA = " + json.dumps(bundle, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
