from __future__ import annotations

import json
import textwrap
from collections import defaultdict
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "report" / "evaluation_systems_snapshot_v1.pdf"
METRICS = BASE / "report" / "v1_metrics_summary.json"
DATA = BASE / "data" / "v1"

PAGE_W, PAGE_H = letter
M = 0.52 * inch
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
for regular, bold in [
    ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
]:
    if Path(regular).exists() and Path(bold).exists():
        pdfmetrics.registerFont(TTFont("CleanSans", regular))
        pdfmetrics.registerFont(TTFont("CleanSans-Bold", bold))
        FONT = "CleanSans"
        FONT_BOLD = "CleanSans-Bold"
        break

IVORY = HexColor("#FBF7EF")
PAPER = HexColor("#FFFDF8")
CHARCOAL = HexColor("#24201D")
MUTED = HexColor("#7B6F65")
LINE = HexColor("#D8CCB9")
RUST = HexColor("#A65437")
RUST_DARK = HexColor("#78351F")
TEAL = HexColor("#244B4A")
PALE_RUST = HexColor("#F0DED4")
PALE_TEAL = HexColor("#DCE8E4")


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


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


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, *, size: float = 9, color=CHARCOAL, font: str = FONT, width: float | None = None, leading: float | None = None) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    leading = leading or size * 1.25
    if width is None:
        c.drawString(x, y, text)
        return y - leading
    yy = y
    for para in text.split("\n"):
        lines = wrap_lines(c, para, width, size, font) or [""]
        for line in lines:
            c.drawString(x, yy, line)
            yy -= leading
    return yy


def label(c: canvas.Canvas, text: str, x: float, y: float, color=MUTED) -> None:
    c.setFont(FONT_BOLD, 7.2)
    c.setFillColor(color)
    c.drawString(x, y, text.upper())


def line(c: canvas.Canvas, x1: float, y1: float, x2: float, y2: float, color=LINE, width=0.7) -> None:
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)


def round_rect(c: canvas.Canvas, x: float, y: float, w: float, h: float, *, fill=PAPER, stroke=LINE, radius=12, sw=0.7) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(sw)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def pill(c: canvas.Canvas, text: str, x: float, y: float, *, fill=PALE_TEAL, color=TEAL) -> float:
    c.setFont(FONT_BOLD, 7.2)
    w = c.stringWidth(text.upper(), FONT_BOLD, 7.2) + 16
    h = 17
    round_rect(c, x, y, w, h, fill=fill, stroke=fill, radius=8.5, sw=0)
    c.setFillColor(color)
    c.drawString(x + 8, y + 5.1, text.upper())
    return w


def metric(c: canvas.Canvas, value: str, title: str, x: float, y: float, w: float, h: float, accent=RUST) -> None:
    round_rect(c, x, y, w, h, fill=PAPER, stroke=LINE, radius=14)
    c.setFillColor(accent)
    c.rect(x, y + h - 4, w, 4, fill=1, stroke=0)
    draw_text(c, value, x + 12, y + h - 30, size=20, color=CHARCOAL, font=FONT_BOLD)
    draw_text(c, title, x + 12, y + 15, size=7.2, color=MUTED, font=FONT_BOLD, width=w - 24, leading=8.4)


def header(c: canvas.Canvas, page: int) -> None:
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    line(c, M, PAGE_H - 0.48 * inch, PAGE_W - M, PAGE_H - 0.48 * inch)
    label(c, "Tarek Etman", M, PAGE_H - 0.35 * inch, color=CHARCOAL)
    c.setFillColor(MUTED)
    c.setFont(FONT, 7.2)
    c.drawRightString(PAGE_W - M, PAGE_H - 0.35 * inch, "tarek.etman@sciencespo.fr | linkedin.com/in/tareketman")
    line(c, M, 0.48 * inch, PAGE_W - M, 0.48 * inch)
    c.setFont(FONT, 7)
    c.setFillColor(MUTED)
    c.drawString(M, 0.31 * inch, "Clinical Model Behavior Evaluation Lab | synthetic public proof artifact")
    c.drawRightString(PAGE_W - M, 0.31 * inch, f"Page {page} of 2")


def sample_bundle() -> tuple[dict, dict, dict, dict, dict]:
    cases = {r["case_id"]: r for r in read_jsonl(DATA / "cases.jsonl")}
    responses = read_jsonl(DATA / "responses.jsonl")
    annotations = read_jsonl(DATA / "annotations.jsonl")
    by_case = defaultdict(list)
    by_response_ann = defaultdict(list)
    for r in responses:
        by_case[r["case_id"]].append(r)
    for a in annotations:
        by_response_ann[a["response_id"]].append(a)
    # Choose a high-signal case with one expert ideal vs one unsafe synthetic pattern.
    case = cases["cmbv1_001"]
    rows = sorted(by_case[case["case_id"]], key=lambda r: r["response_label"])
    anns = {r["response_id"]: sorted(by_response_ann[r["response_id"]], key=lambda a: a["annotation_round"])[0] for r in rows}
    return case, rows[0], rows[1], anns[rows[0]["response_id"]], anns[rows[1]["response_id"]]


def page1(c: canvas.Canvas, metrics: dict) -> None:
    header(c, 1)
    y = PAGE_H - 0.92 * inch
    label(c, "Neutral proof system", M, y, color=RUST_DARK)
    c.setFont(FONT_BOLD, 26)
    c.setFillColor(CHARCOAL)
    c.drawString(M, y - 32, "Clinical Model Behavior")
    c.drawString(M, y - 62, "Evaluation Lab")
    draw_text(
        c,
        "A reproducible healthcare-domain model-evaluation system: synthetic probes, explicit response provenance, rubric scoring, failure taxonomy, adjudication hooks, and audit-safe claim boundaries.",
        M,
        y - 86,
        size=10.0,
        color=MUTED,
        width=PAGE_W - 2 * M,
        leading=13.2,
    )

    # Candidate fit strip
    strip_y = PAGE_H - 3.25 * inch
    round_rect(c, M, strip_y, PAGE_W - 2 * M, 0.78 * inch, fill=PAPER, stroke=LINE, radius=16)
    label(c, "prepared by", M + 14, strip_y + 0.51 * inch)
    draw_text(c, "Licensed dentist | Global Health MPP | Medical AI / LLM evaluator", M + 14, strip_y + 0.31 * inch, size=10.7, font=FONT_BOLD, color=CHARCOAL)
    draw_text(c, "Focus: clinical safety review, response ranking, rubric calibration, missing-context analysis, and concise evaluator rationales.", M + 14, strip_y + 0.13 * inch, size=8.4, color=MUTED, width=PAGE_W - 2 * M - 28)

    counts = metrics["counts"]
    consistency = metrics["two_pass_consistency"]
    mx = M
    my = PAGE_H - 4.58 * inch
    gap = 0.11 * inch
    mw = (PAGE_W - 2 * M - 2 * gap) / 3
    metric(c, str(counts["cases"]), "synthetic cases", mx, my, mw, 0.70 * inch, accent=TEAL)
    metric(c, str(counts["responses"]), "response records", mx + mw + gap, my, mw, 0.70 * inch, accent=RUST)
    metric(c, str(counts["annotations"]), "annotation records", mx + 2 * (mw + gap), my, mw, 0.70 * inch, accent=TEAL)
    my2 = my - 0.84 * inch
    metric(c, "24 / 24", "preferred A/B balance", mx, my2, mw, 0.70 * inch, accent=RUST)
    metric(c, f"{int(consistency['exact_agreement']['rate'] * 100)}%", "exact two-pass agreement", mx + mw + gap, my2, mw, 0.70 * inch, accent=TEAL)
    metric(c, f"{int(consistency['within_one_agreement']['rate'] * 100)}%", "within-one agreement", mx + 2 * (mw + gap), my2, mw, 0.70 * inch, accent=RUST)

    y2 = PAGE_H - 6.31 * inch
    label(c, "What this proves", M, y2, color=RUST_DARK)
    rows = [
        ("Case design", "Builds health-domain probes that isolate model failure modes instead of relying on generic prompts."),
        ("Rubric calibration", "Uses explicit dimensions, severity, pass/review/fail decisions, and hard caps for unsafe behavior."),
        ("Data architecture", "Separates cases, responses, annotations, adjudications, preferences, manifests, and source anchors."),
        ("Claim discipline", "Labels synthetic fixtures honestly and refuses benchmark, clinical-validation, or independent-rater claims."),
    ]
    table_y = y2 - 0.25 * inch
    row_h = 0.48 * inch
    for i, (head, body) in enumerate(rows):
        yy = table_y - i * row_h
        if i:
            line(c, M, yy + 0.15 * inch, PAGE_W - M, yy + 0.15 * inch)
        draw_text(c, head, M, yy, size=9.1, color=CHARCOAL, font=FONT_BOLD)
        draw_text(c, body, M + 1.48 * inch, yy, size=8.4, color=MUTED, width=PAGE_W - 2 * M - 1.48 * inch, leading=10.2)

    scope_y = 0.82 * inch
    round_rect(c, M, scope_y, PAGE_W - 2 * M, 0.72 * inch, fill=PALE_RUST, stroke=PALE_RUST, radius=14, sw=0)
    draw_text(c, "Boundary", M + 12, scope_y + 0.45 * inch, size=8, color=RUST_DARK, font=FONT_BOLD)
    draw_text(c, "All examples are synthetic. No patient data, platform tasks, client materials, proprietary rubrics, or confidential employer content are used. This is not medical advice or a model benchmark.", M + 12, scope_y + 0.27 * inch, size=7.8, color=RUST_DARK, width=PAGE_W - 2 * M - 24, leading=9.4)


def page2(c: canvas.Canvas, metrics: dict) -> None:
    header(c, 2)
    case, a, b, ann_a, ann_b = sample_bundle()
    y = PAGE_H - 0.94 * inch
    label(c, "Sample evaluation pass", M, y, color=RUST_DARK)
    c.setFont(FONT_BOLD, 22)
    c.setFillColor(CHARCOAL)
    c.drawString(M, y - 30, "From ambiguous prompt to calibrated ranking")
    draw_text(c, f"Prompt: {case['prompt']}", M, y - 55, size=9.2, color=MUTED, width=PAGE_W - 2 * M, leading=11.2)

    # Response comparison cards
    card_y = PAGE_H - 3.55 * inch
    card_w = (PAGE_W - 2 * M - 0.18 * inch) / 2
    for idx, (resp, ann, accent, title) in enumerate([(a, ann_a, TEAL, "Preferred"), (b, ann_b, RUST, "Downgraded")]):
        x = M + idx * (card_w + 0.18 * inch)
        round_rect(c, x, card_y, card_w, 1.75 * inch, fill=PAPER, stroke=LINE, radius=16)
        c.setFillColor(accent)
        c.rect(x, card_y + 1.75 * inch - 4, card_w, 4, fill=1, stroke=0)
        draw_text(c, f"Response {resp['response_label']} - {title}", x + 12, card_y + 1.45 * inch, size=9.8, color=CHARCOAL, font=FONT_BOLD)
        short = resp["response_text"]
        if len(short) > 360:
            short = short[:357].rsplit(" ", 1)[0] + "..."
        draw_text(c, short, x + 12, card_y + 1.22 * inch, size=7.4, color=MUTED, width=card_w - 24, leading=8.8)
        draw_text(c, f"Score {ann['overall_score']} / 4 | {ann['pass_fail'].upper()} | severity {ann['severity']}", x + 12, card_y + 0.18 * inch, size=8.1, color=accent, font=FONT_BOLD)

    # Rationale and rubric
    mid_y = PAGE_H - 4.45 * inch
    label(c, "Evaluator judgment", M, mid_y, color=RUST_DARK)
    draw_text(
        c,
        "The preferred response preserves uncertainty, recognizes a red-flag pattern, avoids diagnosis, and sets an escalation boundary. The downgraded response sounds calm but falsely reassures, delays review, and fails escalation handling.",
        M,
        mid_y - 18,
        size=9.2,
        color=CHARCOAL,
        width=PAGE_W - 2 * M,
        leading=11.5,
    )

    # Dimensions as pills
    dim_y = PAGE_H - 5.42 * inch
    label(c, "Rubric dimensions", M, dim_y, color=RUST_DARK)
    x = M
    y_pill = dim_y - 25
    dims = [
        "clinical safety", "escalation", "context sensitivity", "factuality",
        "uncertainty", "scope control", "usefulness", "rationale quality",
    ]
    for d in dims:
        w = pill(c, d, x, y_pill, fill=PALE_TEAL, color=TEAL)
        x += w + 6
        if x > PAGE_W - M - 1.3 * inch:
            x = M
            y_pill -= 24

    # Architecture links / files
    box_y = 1.12 * inch
    round_rect(c, M, box_y, PAGE_W - 2 * M, 1.42 * inch, fill=PAPER, stroke=LINE, radius=16)
    label(c, "Inspectable files", M + 12, box_y + 1.10 * inch, color=RUST_DARK)
    files = [
        "eval_spec/clinical_model_behavior_eval_spec_v1.md - protocol, schemas, metrics, release gates",
        "data/v1/ - cases, responses, annotations, adjudications, preferences, manifests",
        "eval_harness/v1_validate.py + v1_metrics.py - reproducible checks and metrics",
        "report/v1_synthetic_demo_report.md + report/v1_charts/ - current report and charts",
    ]
    yy = box_y + 0.88 * inch
    for item in files:
        draw_text(c, item, M + 18, yy, size=7.8, color=MUTED, width=PAGE_W - 2 * M - 36, leading=9.2)
        yy -= 0.21 * inch


def build() -> None:
    metrics = json.loads(METRICS.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("Clinical Model Behavior Evaluation Lab - v1 Snapshot")
    c.setAuthor("Tarek Etman")
    c.setSubject("Synthetic healthcare-domain model behavior evaluation proof artifact")
    c.setCreator("ReportLab")
    page1(c, metrics)
    c.showPage()
    page2(c, metrics)
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
