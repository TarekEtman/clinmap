#!/usr/bin/env python3
"""Build a blinded human-review CSV from a ClinMAP-VOI local model run."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clinmap_voi.common import DATA_DIR, ROOT, read_jsonl  # noqa: E402

DEFAULT_OUT = ROOT / "model_runs" / "review_queues"

REVIEW_COLUMNS = [
    "review_item_id",
    "blind_status",
    "run_id",
    "model_id",
    "family_id",
    "variant_id",
    "variant_type",
    "visible_prompt",
    "response_text",
    "observed_decision_label",
    "decision_correct",
    "voi_handling",
    "required_context_asked",
    "unsafe_shortcuts_present",
    "clinical_safety_score_0_4",
    "escalation_score_0_4",
    "missing_context_score_0_4",
    "medication_safety_score_0_4",
    "uncertainty_score_0_4",
    "scope_control_score_0_4",
    "evidence_span_prompt",
    "evidence_span_response",
    "reviewer_rationale",
    "confidence",
    "needs_adjudication",
    "publication_visibility",
]


def load_variants() -> dict[str, dict[str, Any]]:
    return {row["variant_id"]: row for row in read_jsonl(DATA_DIR / "variants.jsonl")}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_jsonl", type=Path)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--unblind", action="store_true", help="Include oracle fields. Default is blind review.")
    args = parser.parse_args()

    variants = load_variants()
    rows = read_jsonl(args.run_jsonl)
    args.outdir.mkdir(parents=True, exist_ok=True)
    out_path = args.outdir / f"{args.run_jsonl.stem}_review_queue.csv"
    columns = list(REVIEW_COLUMNS)
    if args.unblind:
        columns += ["expected_policy_label", "risk_stratum", "expected_safe_behavior_delta", "must_ask_context", "must_not_claim"]

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for index, row in enumerate(rows, start=1):
            if row.get("status") != "ok":
                continue
            variant = variants[row["variant_id"]]
            item = {
                "review_item_id": f"review_{row['run_id']}_{index:04d}",
                "blind_status": "unblind" if args.unblind else "blind",
                "run_id": row["run_id"],
                "model_id": row["model_id"],
                "family_id": row["family_id"],
                "variant_id": row["variant_id"],
                "variant_type": variant["variant_type"],
                "visible_prompt": variant["visible_prompt"],
                "response_text": row["response_text"],
                "observed_decision_label": "",
                "decision_correct": "",
                "voi_handling": "",
                "required_context_asked": "",
                "unsafe_shortcuts_present": "",
                "clinical_safety_score_0_4": "",
                "escalation_score_0_4": "",
                "missing_context_score_0_4": "",
                "medication_safety_score_0_4": "",
                "uncertainty_score_0_4": "",
                "scope_control_score_0_4": "",
                "evidence_span_prompt": "",
                "evidence_span_response": "",
                "reviewer_rationale": "",
                "confidence": "",
                "needs_adjudication": "",
                "publication_visibility": "",
            }
            if args.unblind:
                item.update(
                    {
                        "expected_policy_label": row["expected_policy_label"],
                        "risk_stratum": row["risk_stratum"],
                        "expected_safe_behavior_delta": variant["expected_safe_behavior_delta"],
                        "must_ask_context": "; ".join(variant.get("must_ask_context", [])),
                        "must_not_claim": "; ".join(variant.get("must_not_claim", [])),
                    }
                )
            writer.writerow(item)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
