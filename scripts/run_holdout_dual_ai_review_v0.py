#!/usr/bin/env python3
"""Run dual AI protocol raters on holdout families; writes panel_holdout_reviews.jsonl (honest ai_protocol)."""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLINMAP = ROOT / "clinmap_voi"
if str(CLINMAP) not in sys.path:
    sys.path.insert(0, str(CLINMAP))

from holdout_ai_rater_contract_v0 import annotate as annotate_contract  # noqa: E402
from holdout_ai_rater_escalation_v0 import annotate as annotate_escalation  # noqa: E402

RUN_ID = "hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped"
QUEUE = ROOT / f"model_runs/review_queues/{RUN_ID}_review_queue.csv"
VARIANTS = ROOT / "data/clinmap_voi_v0/variants.jsonl"
OUTPUT = ROOT / "data/clinmap_voi_v0/panel_holdout_reviews.jsonl"
STATUS = ROOT / "data/clinmap_voi_v0/panel_holdout_status.json"
HOLDOUT = {f"CMVOI-{i:03d}" for i in range(33, 41)}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def main() -> int:
    variants = {v["variant_id"]: v for v in read_jsonl(VARIANTS)}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines: list[dict[str, Any]] = []
    with QUEUE.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("family_id") not in HOLDOUT:
                continue
            variant = variants[row["variant_id"]]
            base = {
                "panel_item_id": row["review_item_id"],
                "family_id": row["family_id"],
                "variant_id": row["variant_id"],
                "variant_type": row["variant_type"],
                "primary_observed_decision_label": row["observed_decision_label"],
                "framework_expected_policy_label": row["expected_policy_label"],
                "reviewed_at": now,
            }
            for ann_fn in (annotate_contract, annotate_escalation):
                ann = ann_fn(row, variant)
                lines.append({**base, **ann})

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as out:
        for rec in lines:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    status["layer_c_status"] = "fielded_dual_ai_protocol"
    status["fielded_at"] = now
    status["rater_ids"] = ["ai_protocol_contract_v0", "ai_protocol_escalation_v0"]
    status["rater_type"] = "ai_protocol"
    status["row_count"] = len(lines)
    status["holdout_item_count"] = len(lines) // 2
    status["public_panel_ids_planned"] = []
    STATUS.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "annotations": len(lines),
                "holdout_items": len(lines) // 2,
                "status": status["layer_c_status"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())