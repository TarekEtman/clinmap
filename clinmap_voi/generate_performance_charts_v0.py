#!/usr/bin/env python3
"""Generate SVG charts from ClinMAP-VOI v0 performance metrics."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "report/clinmap_voi_v0_performance_metrics.json"
OUTDIR = ROOT / "report/clinmap_voi_v0_charts"


def bar_chart(title: str, labels: list[str], values: list[float], y_max: float = 1.0) -> str:
    w, h, pad = 720, 320, 48
    bar_w = max(12, (w - 2 * pad) // max(len(values), 1) - 8)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'<text x="{pad}" y="24" font-size="16" font-family="system-ui">{title}</text>',
    ]
    for i, (lab, val) in enumerate(zip(labels, values)):
        x = pad + i * (bar_w + 8)
        bh = int((h - 2 * pad) * (val / y_max))
        y = h - pad - bh
        lines.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bh}" fill="#2563eb"/>')
        short = lab.split("/")[-1][:14]
        lines.append(f'<text x="{x}" y="{h-12}" font-size="9" transform="rotate(35 {x},{h-12})">{short}</text>')
    lines.append("</svg>")
    return "\n".join(lines)


def main() -> int:
    data = json.loads(METRICS.read_text(encoding="utf-8"))
    OUTDIR.mkdir(parents=True, exist_ok=True)
    models = list(data["models"].items())[:15]
    labels = [m[0] for m in models]
    acc = [m[1]["decision_accuracy"] for m in models]
    meta = [m[1]["metamorphic_pass_rate"] for m in models]
    (OUTDIR / "decision_accuracy_by_model.svg").write_text(
        bar_chart("Decision accuracy by model", labels, acc), encoding="utf-8"
    )
    (OUTDIR / "metamorphic_pass_by_model.svg").write_text(
        bar_chart("Metamorphic pass rate by model", labels, meta), encoding="utf-8"
    )
    print(f"Wrote charts to {OUTDIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())