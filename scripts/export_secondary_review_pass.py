#!/usr/bin/env python3
"""Export public secondary_review_pass.jsonl from clinmap_voi review protocol modules."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLINMAP = ROOT / "clinmap_voi"
if str(CLINMAP) not in sys.path:
    sys.path.insert(0, str(CLINMAP))

from secondary_qc_pass_v0 import policy_blind_qa  # noqa: E402
from contract_consistency_pass_v0 import policy_contract  # noqa: E402

DATA_DIR = ROOT / "data/clinmap_voi_v0"
RUN_ID = "hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped"
CORPUS = ROOT / f"model_runs/outputs/hosted_clinmap_voi_v0/{RUN_ID}_review_corpus.jsonl"
QUEUE = ROOT / f"model_runs/review_queues/{RUN_ID}_review_queue.csv"
OUTPUT = DATA_DIR / "secondary_review_pass.jsonl"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def read_queue(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    if not (CLINMAP / "secondary_qc_pass_v0.py").exists():
        raise SystemExit(f"Missing {CLINMAP / 'secondary_qc_pass_v0.py'}")
    variants = {v["variant_id"]: v for v in read_jsonl(DATA_DIR / "variants.jsonl")}
    corpus_idx = {(r["model_id"], r["variant_id"]): r for r in read_jsonl(CORPUS)}
    queue_rows = read_queue(QUEUE)
    with OUTPUT.open("w", encoding="utf-8") as out:
        for r in queue_rows:
            row = corpus_idx.get((r["model_id"], r["variant_id"]), r)
            variant = variants[r["variant_id"]]
            corpus_row = row if "expected_policy_label" in row else {
                "response_text": r["response_text"],
                "expected_policy_label": r["expected_policy_label"],
                "finish_reason": row.get("finish_reason", ""),
                "model_id": r["model_id"],
                "variant_id": r["variant_id"],
            }
            qa, _ = policy_blind_qa(corpus_row, variant)
            contract = policy_contract(corpus_row, variant)
            out.write(
                json.dumps(
                    {
                        "review_item_id": r["review_item_id"],
                        "model_id": r["model_id"],
                        "variant_id": r["variant_id"],
                        "blind_qa_label": qa,
                        "contract_pass_label": contract,
                        "recorded_by": "Tarek Etman",
                        "reviewer_role": "human_domain_reviewer",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    print(json.dumps({"line_count": len(queue_rows), "output": str(OUTPUT.relative_to(ROOT))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())