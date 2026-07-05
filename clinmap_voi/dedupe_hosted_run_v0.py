#!/usr/bin/env python3
"""Create a clean latest/best-row JSONL from a hosted ClinMAP-VOI run.

The raw hosted runner appends rows immediately. When --retry-failed is used,
failed/rate-limited attempts remain in the raw audit log and successful retry
rows are appended later. This utility produces a clean corpus with one row per
provider/model/prompt task.

Selection policy:
  1. Prefer status == "ok" over any non-ok status.
  2. If tied on status class, keep the later appended row.

This means a later successful retry replaces an earlier rate_limited/failed row,
while a later rate-limit row cannot overwrite an earlier successful row.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def task_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row.get("provider")), str(row.get("model_id")), str(row.get("prompt_id")))


def rank(row: dict[str, Any], index: int) -> tuple[int, int]:
    return (1 if row.get("status") == "ok" else 0, index)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_jsonl", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    rows = read_jsonl(args.run_jsonl)
    selected: dict[tuple[str, str, str], tuple[int, dict[str, Any]]] = {}
    duplicate_attempts = 0

    for index, row in enumerate(rows):
        key = task_key(row)
        if key in selected:
            duplicate_attempts += 1
            old_index, old_row = selected[key]
            if rank(row, index) >= rank(old_row, old_index):
                selected[key] = (index, row)
        else:
            selected[key] = (index, row)

    clean_rows = [item[1] for item in sorted(selected.values(), key=lambda item: item[0])]

    out_path = args.out or args.run_jsonl.with_name(f"{args.run_jsonl.stem}_deduped.jsonl")
    report_path = args.report or args.run_jsonl.with_name(f"{args.run_jsonl.stem}_dedupe_report.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        for row in clean_rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    report = {
        "source_path": str(args.run_jsonl),
        "deduped_path": str(out_path),
        "raw_rows": len(rows),
        "deduped_rows": len(clean_rows),
        "duplicate_attempt_rows_removed": len(rows) - len(clean_rows),
        "duplicate_keys_seen": duplicate_attempts,
        "status_counts_raw": dict(Counter(str(r.get("status")) for r in rows)),
        "status_counts_deduped": dict(Counter(str(r.get("status")) for r in clean_rows)),
        "provider_counts_deduped": dict(Counter(str(r.get("provider")) for r in clean_rows)),
        "model_counts_deduped": {
            f"{provider}/{alias}/{status}": count
            for (provider, alias, status), count in sorted(
                Counter((str(r.get("provider")), str(r.get("model_alias")), str(r.get("status"))) for r in clean_rows).items()
            )
        },
        "selection_policy": "one row per provider/model_id/prompt_id; prefer ok over non-ok; otherwise later appended row",
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(out_path)
    print(report_path)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
