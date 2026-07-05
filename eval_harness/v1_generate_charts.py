"""Generate dependency-free SVG charts for the v1 synthetic demo dataset."""
from __future__ import annotations

import html
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from v1_common import group_by, load_v1

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report" / "v1_charts"
CHARCOAL = "#24201d"
RUST = "#a65437"
TEAL = "#244b4a"
IVORY = "#fbf7ef"
MUTED = "#8b7d72"
LINE = "#ded4c8"


def esc(x: object) -> str:
    return html.escape(str(x))


def svg_wrap(width: int, height: int, title: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">
  <rect width="100%" height="100%" fill="{IVORY}"/>
  <text x="32" y="38" fill="{CHARCOAL}" font-family="Inter, Arial, sans-serif" font-size="20" font-weight="700">{esc(title)}</text>
  {body}
</svg>
'''


def bar_chart(title: str, data: dict[str, int], path: Path, *, width: int = 920, bar_h: int = 24, sort: bool = True, color: str = RUST) -> None:
    items = list(data.items())
    if sort:
        items.sort(key=lambda kv: (-kv[1], kv[0]))
    height = 78 + len(items) * 38
    max_v = max(v for _, v in items) if items else 1
    label_w = 250
    chart_w = width - label_w - 100
    rows = []
    for i, (label, value) in enumerate(items):
        y = 70 + i * 38
        w = int(chart_w * value / max_v)
        rows.append(f'<text x="32" y="{y+18}" fill="{CHARCOAL}" font-family="Inter, Arial, sans-serif" font-size="14">{esc(label)}</text>')
        rows.append(f'<rect x="{label_w}" y="{y}" width="{chart_w}" height="{bar_h}" rx="6" fill="#efe7dd"/>')
        rows.append(f'<rect x="{label_w}" y="{y}" width="{w}" height="{bar_h}" rx="6" fill="{color}"/>')
        rows.append(f'<text x="{label_w + chart_w + 18}" y="{y+17}" fill="{MUTED}" font-family="Inter, Arial, sans-serif" font-size="13">{value}</text>')
    path.write_text(svg_wrap(width, height, title, "\n  ".join(rows)), encoding="utf-8")


def dimension_chart(annotations: Iterable[dict], path: Path) -> None:
    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    for ann in annotations:
        for dim, score in ann["dimension_scores"].items():
            sums[dim] += score
            counts[dim] += 1
    means = {dim: round(sums[dim] / counts[dim], 2) for dim in sums}
    order = [
        "clinical_safety", "escalation", "context_sensitivity", "factuality",
        "uncertainty", "scope_control", "usefulness", "rationale_quality",
    ]
    width = 980
    height = 430
    left = 250
    top = 78
    chart_w = 600
    rows = []
    for i, dim in enumerate(order):
        mean = means[dim]
        y = top + i * 40
        w = int(chart_w * mean / 4)
        label = dim.replace("_", " ")
        rows.append(f'<text x="32" y="{y+18}" fill="{CHARCOAL}" font-family="Inter, Arial, sans-serif" font-size="14">{esc(label)}</text>')
        rows.append(f'<rect x="{left}" y="{y}" width="{chart_w}" height="24" rx="6" fill="#efe7dd"/>')
        rows.append(f'<rect x="{left}" y="{y}" width="{w}" height="24" rx="6" fill="{TEAL}"/>')
        rows.append(f'<text x="{left + chart_w + 18}" y="{y+17}" fill="{MUTED}" font-family="Inter, Arial, sans-serif" font-size="13">{mean} / 4</text>')
    rows.append(f'<text x="32" y="{height-28}" fill="{MUTED}" font-family="Inter, Arial, sans-serif" font-size="12">Mean across two-pass self-calibration annotations. Synthetic demo only; not independent inter-rater reliability.</text>')
    path.write_text(svg_wrap(width, height, "Mean dimension scores", "\n  ".join(rows)), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    b = load_v1(ROOT / "data" / "v1")
    cases = b["cases"]
    responses = b["responses"]
    annotations = b["annotations"]
    anns_by_response = group_by(annotations, "response_id")
    final_annotations = [sorted(rows, key=lambda r: r["annotation_round"])[0] for rows in anns_by_response.values() if rows]

    task_counts = Counter(c["task_type"] for c in cases)
    risk_counts = Counter(c["risk_level"] for c in cases)
    origin_counts = Counter(r["response_origin"] for r in responses)
    outcome_counts = Counter(a["pass_fail"] for a in final_annotations)
    failure_counts = Counter(tag for a in final_annotations for tag in a["failure_tags"])

    bar_chart("Coverage by task type", dict(task_counts), OUT / "coverage_by_task_type.svg", color=TEAL)
    bar_chart("Risk-level coverage", dict(risk_counts), OUT / "risk_level_coverage.svg", color=RUST)
    bar_chart("Response provenance", dict(origin_counts), OUT / "response_provenance.svg", color=TEAL)
    bar_chart("Final response outcomes", dict(outcome_counts), OUT / "response_outcomes.svg", color=RUST)
    bar_chart("Failure-tag frequency", dict(failure_counts), OUT / "failure_tag_frequency.svg", color=RUST)
    dimension_chart(final_annotations, OUT / "dimension_mean_scores.svg")
    print(f"Wrote v1 charts to {OUT}")


if __name__ == "__main__":
    main()
