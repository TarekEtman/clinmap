#!/usr/bin/env python3
"""Two-page ClinMAP-VOI v0 reviewer snapshot PDF."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "report" / "clinmap_voi_v0_snapshot.pdf"
METRICS = BASE / "report" / "clinmap_voi_v0_performance_metrics.json"
AUDIT = BASE / "report" / "clinmap_voi_review_quality_audit.json"

PAGE_W, PAGE_H = letter
M = 0.52 * inch
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
IVORY = HexColor("#FBF7EF")
PAPER = HexColor("#FFFDF8")
CHARCOAL = HexColor("#24201D")
MUTED = HexColor("#7B6F65")
LINE = HexColor("#D8CCB9")
RUST = HexColor("#A65437")
TEAL = HexColor("#244B4A")


def wrap_lines(c: canvas.Canvas, text: str, width: float, size: float, font: str = FONT) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        trial = f"{line} {word}".strip()
        if c.stringWidth(trial, font, size) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_text(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    *,
    size: float = 9,
    color=CHARCOAL,
    font: str = FONT,
    width: float | None = None,
    leading: float | None = None,
) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    leading = leading or size * 1.25
    if width is None:
        c.drawString(x, y, text)
        return y - leading
    yy = y
    for para in text.split("\n"):
        for line in wrap_lines(c, para, width, size, font) or [""]:
            c.drawString(x, yy, line)
            yy -= leading
    return yy


def round_rect(c: canvas.Canvas, x: float, y: float, w: float, h: float, *, fill=PAPER, stroke=LINE) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, 12, fill=1, stroke=1)


def metric_box(c: canvas.Canvas, value: str, title: str, x: float, y: float, w: float, h: float) -> None:
    round_rect(c, x, y, w, h)
    c.setFillColor(RUST)
    c.rect(x, y + h - 4, w, 4, fill=1, stroke=0)
    draw_text(c, value, x + 12, y + h - 30, size=18, font=FONT_BOLD)
    draw_text(c, title, x + 12, y + 14, size=7, color=MUTED, font=FONT_BOLD, width=w - 24, leading=8)


def header(c: canvas.Canvas, page: int, total: int) -> None:
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(M, PAGE_H - 0.48 * inch, PAGE_W - M, PAGE_H - 0.48 * inch)
    c.setFont(FONT_BOLD, 7.2)
    c.setFillColor(CHARCOAL)
    c.drawString(M, PAGE_H - 0.35 * inch, "TAREK ETMAN · CLINMAP-VOI V0")
    c.setFont(FONT, 7.2)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - M, PAGE_H - 0.35 * inch, f"Page {page} of {total}")
    c.line(M, 0.48 * inch, PAGE_W - M, 0.48 * inch)
    c.drawString(M, 0.31 * inch, "Synthetic metamorphic benchmark · not clinical validation")
    c.drawRightString(PAGE_W - M, 0.31 * inch, "clinical-ai-eval-lab")


def main() -> None:
    metrics = json.loads(METRICS.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    agg = metrics["aggregate"]
    m = audit["metrics"]

    c = canvas.Canvas(str(OUT), pagesize=letter)

    header(c, 1, 2)
    y = PAGE_H - 0.85 * inch
    draw_text(c, "ClinMAP-VOI v0", M, y, size=26, font=FONT_BOLD)
    y -= 28
    draw_text(
        c,
        "Hosted multi-model evaluation on synthetic healthcare metamorphic probes: "
        "human domain review, relation annotations, and post-review QA audit.",
        M,
        y,
        size=10.5,
        width=PAGE_W - 2 * M,
        leading=13,
    )
    y -= 36
    box_w = (PAGE_W - 2 * M - 18) / 4
    for i, (val, title) in enumerate(
        [
            (str(metrics["reviewed_row_count"]), "reviewed rows"),
            (str(agg["model_count"]), "models scored"),
            (f"{agg['mean_decision_accuracy']:.3f}", "mean decision accuracy"),
            (f"{agg['mean_metamorphic_pass_rate']:.3f}", "metamorphic pass rate"),
        ]
    ):
        metric_box(c, val, title, M + i * (box_w + 6), y - 72, box_w, 72)
    y -= 92
    draw_text(c, "Methodology (in repository)", M, y, size=11, font=FONT_BOLD, color=TEAL)
    y -= 16
    bullets = [
        "40 decision families · 320 variants · 280 metamorphic relations",
        "Annotation protocol + 6 policy-relevant dimension scores (0–4)",
        "Holdout QA on families CMVOI-033–040; blind-QA κ in published band",
        "Claim boundary: evaluation engineering demo, not safety certification",
    ]
    for b in bullets:
        y = draw_text(c, f"• {b}", M, y, size=9.2, width=PAGE_W - 2 * M, leading=12)

    y -= 8
    draw_text(c, "Primary artifacts", M, y, size=11, font=FONT_BOLD, color=TEAL)
    y -= 14
    artifacts = textwrap.fill(
        "review_queue.csv · relation_annotations.jsonl · clinmap_voi_v0_performance_metrics.md · "
        "clinmap_voi_review_quality_audit.md · eval_spec/clinmap_voi_eval_spec_v0.md",
        width=95,
    )
    draw_text(c, artifacts, M, y, size=8.8, width=PAGE_W - 2 * M, leading=11)

    c.showPage()

    header(c, 2, 2)
    y = PAGE_H - 0.85 * inch
    draw_text(c, "QA audit summary", M, y, size=18, font=FONT_BOLD)
    y -= 22
    rows = [
        ("Holdout decision accuracy", str(m["holdout_decision_accuracy"])),
        ("Full decision accuracy", str(m["full_decision_accuracy"])),
        ("κ(primary, blind QA)", str(m["cohen_kappa_primary_vs_blind_qa"])),
        ("Relation integrity", str(m["relation_annotation_integrity"])),
        ("Overall QA pass", "YES" if audit.get("overall_pass") else "NO"),
    ]
    for label, val in rows:
        round_rect(c, M, y - 22, PAGE_W - 2 * M, 26)
        draw_text(c, label, M + 10, y - 6, size=9, font=FONT_BOLD)
        c.setFont(FONT_BOLD, 9)
        c.drawRightString(PAGE_W - M - 10, y - 6, val)
        y -= 32

    y -= 6
    draw_text(c, "Reviewer", M, y, size=11, font=FONT_BOLD, color=TEAL)
    y -= 14
    draw_text(c, f"{metrics['primary_reviewer']} · human_domain_reviewer", M, y, size=9.5)
    y -= 20
    draw_text(c, "Run ID", M, y, size=11, font=FONT_BOLD, color=TEAL)
    y -= 14
    draw_text(c, metrics["run_id"], M, y, size=7.8, width=PAGE_W - 2 * M, leading=10)

    y -= 24
    draw_text(c, "Limitations", M, y, size=11, font=FONT_BOLD, color=TEAL)
    y -= 14
    lim = (
        "All probes are synthetic. Metrics reflect rubric policy alignment and metamorphic consistency, "
        "not patient outcomes. Empty model responses were excluded from review. "
        "Public artifacts use collected response text only."
    )
    draw_text(c, lim, M, y, size=9, width=PAGE_W - 2 * M, leading=12)

    c.save()
    public_copy = BASE / "public" / "assets" / "clinmap_voi_v0_snapshot.pdf"
    public_copy.parent.mkdir(parents=True, exist_ok=True)
    public_copy.write_bytes(OUT.read_bytes())
    print(f"Wrote {OUT} and {public_copy}")


if __name__ == "__main__":
    main()