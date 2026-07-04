#!/usr/bin/env python3
"""Calculate simple agreement-style metrics for synthetic scored examples."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from statistics import mean


def load_scores(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def quadratic_weight(delta: int) -> float:
    # 0 delta = full agreement, 4-point delta = no agreement.
    return 1.0 - ((delta / 4.0) ** 2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scores", required=True, type=Path)
    args = parser.parse_args()

    rows = load_scores(args.scores)
    exact = 0
    within_one = 0
    deltas: list[int] = []
    weighted: list[float] = []
    primary_distribution: Counter[int] = Counter()
    secondary_distribution: Counter[int] = Counter()

    for row in rows:
        p = int(row["primary_score"])
        s = int(row["secondary_score"])
        delta = abs(p - s)
        deltas.append(delta)
        weighted.append(quadratic_weight(delta))
        if p == s:
            exact += 1
        if delta <= 1:
            within_one += 1
        primary_distribution[p] += 1
        secondary_distribution[s] += 1

    total = len(rows)
    print("Evaluator consistency summary")
    print("=" * 60)
    print(f"Records: {total}")
    print(f"Exact score agreement: {exact}/{total} ({exact / total:.0%})")
    print(f"Within-one agreement: {within_one}/{total} ({within_one / total:.0%})")
    print(f"Mean absolute score delta: {mean(deltas):.2f}")
    print(f"Mean quadratic agreement weight: {mean(weighted):.2f}")
    print("Primary score distribution:", dict(sorted(primary_distribution.items())))
    print("Secondary score distribution:", dict(sorted(secondary_distribution.items())))


if __name__ == "__main__":
    main()
