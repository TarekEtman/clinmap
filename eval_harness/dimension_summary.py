#!/usr/bin/env python3
"""Summarize dimension-level scores for synthetic response evaluations."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean

DIMENSIONS = [
    "clinical_safety",
    "escalation",
    "context_sensitivity",
    "factuality",
    "uncertainty",
    "scope_control",
    "usefulness",
    "rationale_quality",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimensions", required=True, type=Path)
    args = parser.parse_args()

    with args.dimensions.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    print("Dimension-level score summary")
    print("=" * 60)
    print(f"Records: {len(rows)}")
    for dim in DIMENSIONS:
        values = [int(row[dim]) for row in rows]
        low = sum(1 for v in values if v <= 1)
        print(f"{dim:24s} mean={mean(values):.2f}/4  low_score_count={low}")


if __name__ == "__main__":
    main()
