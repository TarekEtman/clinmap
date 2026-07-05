#!/usr/bin/env python3
"""Export blinded holdout review pack for independent external panel reviewers."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_ID = "hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped"
QUEUE = ROOT / f"model_runs/review_queues/{RUN_ID}_review_queue.csv"
STATUS = ROOT / "data/clinmap_voi_v0/panel_holdout_status.json"
OUTDIR = ROOT / "model_runs/review_queues/panel_exports"
OUT_CSV = OUTDIR / f"{RUN_ID}_holdout_panel_pack_blinded.csv"
OUT_README = OUTDIR / "PANEL_PACK_README.md"

HOLDOUT = {f"CMVOI-{i:03d}" for i in range(33, 41)}


def main() -> int:
    if not QUEUE.exists():
        raise SystemExit(f"Missing queue: {QUEUE}")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows_out: list[dict[str, str]] = []
    with QUEUE.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("family_id") not in HOLDOUT:
                continue
            rows_out.append(
                {
                    "panel_item_id": row["review_item_id"],
                    "family_id": row["family_id"],
                    "variant_id": row["variant_id"],
                    "variant_type": row["variant_type"],
                    "visible_prompt": row["visible_prompt"],
                    "response_text": row["response_text"],
                    "risk_stratum": row.get("risk_stratum", ""),
                    "panel_observed_decision_label": "",
                    "panel_voi_handling": "",
                    "panel_rationale": "",
                    "panel_reviewer_id": "",
                    "panel_reviewed_at": "",
                }
            )
    fieldnames = list(rows_out[0].keys()) if rows_out else []
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows_out)

    readme = f"""# Holdout panel pack (blinded)

- Source run: `{RUN_ID}`
- Rows: {len(rows_out)} (families CMVOI-033–040)
- **Model ID removed** — reviewers assign policy labels from response text only.
- Do **not** use framework gold columns; reviewers should not see `expected_policy_label`.

## Instructions

1. Assign each reviewer a public ID only: `panel_r01`, `panel_r02`, …
2. Fill `panel_observed_decision_label` using `docs/clinmap_voi_annotation_protocol_v0.md` label set.
3. Merge completed rows into `data/clinmap_voi_v0/panel_holdout_reviews.jsonl` (one JSON object per line).
4. Update `panel_holdout_status.json` → `layer_c_status`: `fielded_external_holdout_panel` after human review is complete.

See `docs/panel_review_strategy.md`.
"""
    OUT_README.write_text(readme, encoding="utf-8")
    print(json.dumps({"holdout_rows": len(rows_out), "csv": str(OUT_CSV), "readme": str(OUT_README)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())