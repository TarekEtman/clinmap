"""Create a manual scoring template for a collected real model-output run."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "v1"

DIMENSIONS = [
    "clinical_safety", "escalation", "context_sensitivity", "factuality",
    "uncertainty", "scope_control", "usefulness", "rationale_quality",
]


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_file", help="JSONL file produced by model_runs/run_openai_compatible.py")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    run_path = Path(args.run_file)
    rows = read_jsonl(run_path)
    cases = {c["case_id"]: c for c in read_jsonl(DATA / "cases.jsonl")}
    out = Path(args.out) if args.out else run_path.with_name(run_path.stem + "_manual_scores.csv")
    fields = [
        "run_id", "case_id", "task_type", "risk_level", "model_id", "overall_score", "severity", "pass_fail",
        *DIMENSIONS, "failure_tags", "cap_rules_triggered", "rationale", "reviewer_id", "annotated_at",
    ]
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            case = cases.get(row["case_id"], {})
            writer.writerow({
                "run_id": row.get("run_id", ""),
                "case_id": row.get("case_id", ""),
                "task_type": case.get("task_type", ""),
                "risk_level": case.get("risk_level", ""),
                "model_id": row.get("model_id", ""),
                "overall_score": "",
                "severity": "",
                "pass_fail": "",
                **{dim: "" for dim in DIMENSIONS},
                "failure_tags": "",
                "cap_rules_triggered": "",
                "rationale": "",
                "reviewer_id": "",
                "annotated_at": "",
            })
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
