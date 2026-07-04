#!/usr/bin/env python3
"""Generate simple SVG charts without external dependencies."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
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

LABELS = {
    "clinical_safety": "Clinical safety",
    "escalation": "Escalation",
    "context_sensitivity": "Context",
    "factuality": "Factuality",
    "uncertainty": "Uncertainty",
    "scope_control": "Scope",
    "usefulness": "Usefulness",
    "rationale_quality": "Rationale",
}


def read_scores(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def split_tags(raw: str) -> list[str]:
    return [t.strip() for t in raw.split(";") if t.strip()]


def bar_chart(title: str, items: list[tuple[str, float]], out: Path, x_max: float | None = None) -> None:
    width = 880
    left = 220
    bar_h = 26
    gap = 10
    top = 64
    bottom = 42
    height = top + bottom + len(items) * (bar_h + gap)
    x_max = x_max or max((v for _, v in items), default=1)
    if x_max == 0:
        x_max = 1
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg.append('<rect width="100%" height="100%" fill="#ffffff"/>')
    svg.append(f'<text x="32" y="36" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#17324D">{title}</text>')
    max_bar_w = width - left - 90
    for i, (label, value) in enumerate(items):
        y = top + i * (bar_h + gap)
        bar_w = max_bar_w * (value / x_max)
        svg.append(f'<text x="32" y="{y + 18}" font-family="Arial, sans-serif" font-size="14" fill="#1F2933">{label}</text>')
        svg.append(f'<rect x="{left}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" rx="5" fill="#1F6F78"/>')
        svg.append(f'<text x="{left + bar_w + 8:.1f}" y="{y + 18}" font-family="Arial, sans-serif" font-size="13" fill="#52616B">{value:g}</text>')
    svg.append('</svg>')
    out.write_text("\n".join(svg), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scores", required=True, type=Path)
    parser.add_argument("--dimensions", required=True, type=Path)
    parser.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    scores = read_scores(args.scores)
    dimension_rows = read_scores(args.dimensions)

    failure_counts: Counter[str] = Counter()
    severity_counts: Counter[str] = Counter()
    for row in scores:
        severity_counts[row["severity"]] += 1
        for tag in split_tags(row["failure_tags"]):
            failure_counts[tag] += 1

    failure_items = failure_counts.most_common()
    severity_items = [(f"Severity {k}", severity_counts[k]) for k in sorted(severity_counts, key=int)]
    dimension_items = []
    for dim in DIMENSIONS:
        values = [int(row[dim]) for row in dimension_rows]
        dimension_items.append((LABELS[dim], round(mean(values), 2)))

    bar_chart("Failure tag frequency", failure_items, args.outdir / "failure_tag_frequency.svg")
    bar_chart("Severity distribution", severity_items, args.outdir / "severity_distribution.svg")
    bar_chart("Mean score by dimension", dimension_items, args.outdir / "dimension_means.svg", x_max=4)
    print(f"Wrote charts to {args.outdir}")


if __name__ == "__main__":
    main()
