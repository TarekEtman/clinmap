"""Editorial PDF style — matched to C_Tarek_Etman_V.pdf structure (text-extracted)."""
from __future__ import annotations

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = letter
M = 0.45 * inch
COL_L = M
COL_L_W = 2.05 * inch
COL_R = COL_L + COL_L_W + 0.20 * inch
COL_R_W = PAGE_W - M - COL_R
FOOTER_Y = 0.48 * inch
HEADER_Y = PAGE_H - 0.46 * inch
CONTENT_BOTTOM = FOOTER_Y + 22

BG = HexColor("#F7F4EF")
INK = HexColor("#344551")
MUTED = HexColor("#68777c")
RUST = HexColor("#A95F37")
LINE = HexColor("#D8CCB9")

FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_OBLIQUE = "Helvetica-Oblique"

for regular, bold in [
    ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
]:
    from pathlib import Path

    if Path(regular).exists() and Path(bold).exists():
        pdfmetrics.registerFont(TTFont("DocSans", regular))
        pdfmetrics.registerFont(TTFont("DocSans-Bold", bold))
        FONT = "DocSans"
        FONT_BOLD = "DocSans-Bold"
        break


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
    color=INK,
    font: str = FONT,
    width: float | None = None,
    leading: float | None = None,
) -> float:
    """Draw text with top-left baseline at y; return y below last line."""
    c.setFillColor(color)
    c.setFont(font, size)
    leading = leading or size * 1.32
    if width is None:
        c.drawString(x, y, text)
        return y - leading
    yy = y
    for para in text.split("\n"):
        for ln in wrap_lines(c, para, width, size, font) or [""]:
            c.drawString(x, yy, ln)
            yy -= leading
    return yy


def fill_page(c: canvas.Canvas) -> None:
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def hrule(c: canvas.Canvas, y: float, x0: float | None = None, x1: float | None = None) -> None:
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(x0 or M, y, x1 or (PAGE_W - M), y)


def page_frame(c: canvas.Canvas, *, header_left: str, header_right: str, footer_left: str, page: int, total: int) -> float:
    """Return y cursor just below header band."""
    fill_page(c)
    hrule(c, HEADER_Y)
    c.setFont(FONT_BOLD, 6.8)
    c.setFillColor(INK)
    c.drawString(M, HEADER_Y - 12, header_left.upper())
    c.setFont(FONT, 6.8)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - M, HEADER_Y - 12, header_right)
    hrule(c, FOOTER_Y)
    c.setFont(FONT, 6.5)
    c.drawString(M, FOOTER_Y - 11, footer_left)
    c.drawRightString(PAGE_W - M, FOOTER_Y - 11, f"ClinMAP · {page}/{total}")
    return HEADER_Y - 24


def section_label(c: canvas.Canvas, text: str, x: float, y: float) -> float:
    c.setFont(FONT_BOLD, 6.8)
    c.setFillColor(RUST)
    c.drawString(x, y, text.upper())
    return y - 10


def stat_row(c: canvas.Canvas, items: list[tuple[str, str]], y_top: float) -> float:
    """Metric strip like CV (value on top, label below). Returns y below row."""
    n = len(items)
    gap = 6
    cell_w = (PAGE_W - 2 * M - (n - 1) * gap) / n
    row_h = 36
    y_base = y_top - row_h
    hrule(c, y_top, M, PAGE_W - M)
    hrule(c, y_base, M, PAGE_W - M)
    for i, (val, label) in enumerate(items):
        x = M + i * (cell_w + gap)
        if i > 0:
            c.setStrokeColor(LINE)
            c.setLineWidth(0.4)
            c.line(x - gap / 2, y_base, x - gap / 2, y_top)
        draw_text(c, val, x + 3, y_top - 15, size=13, font=FONT_BOLD, color=RUST)
        draw_text(c, label, x + 3, y_base + 6, size=5.6, color=MUTED, width=cell_w - 6, leading=6.4)
    return y_base - 10


def ruled_table(
    c: canvas.Canvas,
    rows: list[tuple[str, str]],
    x: float,
    y: float,
    w: float,
    *,
    row_h: float = 16,
    label_size: float = 7.5,
    val_size: float = 7.5,
) -> float:
    for label, val in rows:
        y -= row_h
        hrule(c, y, x, x + w)
        draw_text(c, label, x + 2, y + 5, size=label_size, font=FONT_BOLD, color=INK)
        c.setFont(FONT_BOLD, val_size)
        c.setFillColor(INK)
        c.drawRightString(x + w - 2, y + 5, val)
    return y - 6


def short_model_name(name: str, max_len: int = 26) -> str:
    short = name.split("/")[-1] if "/" in name else name
    if len(short) > max_len:
        return short[: max_len - 3] + "..."
    return short


def model_rank_table(
    c: canvas.Canvas,
    models: list[tuple[str, float, float]],
    x: float,
    y: float,
    w: float,
    *,
    title: str = "Model spread (decision accuracy)",
) -> float:
    """Compact ranked model table — model | acc | metamorphic pass."""
    y = section_label(c, title, x, y)
    col_model = w * 0.58
    col_acc = w * 0.20
    col_meta = w * 0.22
    row_h = 13.5
    y -= row_h
    hrule(c, y, x, x + w)
    c.setFont(FONT_BOLD, 6.5)
    c.setFillColor(MUTED)
    c.drawString(x + 2, y + 4, "MODEL")
    c.drawRightString(x + col_model + col_acc - 2, y + 4, "ACC")
    c.drawRightString(x + w - 2, y + 4, "META")
    for name, acc, meta in models:
        y -= row_h
        hrule(c, y, x, x + w)
        draw_text(c, short_model_name(name), x + 2, y + 3.5, size=6.8, color=INK)
        c.setFont(FONT, 6.8)
        c.setFillColor(INK)
        c.drawRightString(x + col_model + col_acc - 2, y + 3.5, f"{acc:.3f}")
        c.drawRightString(x + w - 2, y + 3.5, f"{meta:.3f}")
    return y - 4


def dual_model_rank_table(
    c: canvas.Canvas,
    models: list[tuple[str, float, float]],
    x: float,
    y: float,
    w: float,
) -> float:
    """Two-column model listing to save vertical space."""
    mid = len(models) // 2 + len(models) % 2
    left = models[:mid]
    right = models[mid:]
    gap = 10
    half_w = (w - gap) / 2
    y_l = model_rank_table(c, left, x, y, half_w, title="Model spread — higher accuracy")
    y_r = model_rank_table(c, right, x + half_w + gap, y, half_w, title="Model spread — lower accuracy")
    return min(y_l, y_r)


def bullet_list(c: canvas.Canvas, items: list[str], x: float, y: float, w: float, *, size: float = 7.5, leading: float = 9) -> float:
    for item in items:
        y = draw_text(c, f"• {item}", x, y, size=size, width=w, leading=leading)
    return y


def pull_quote(c: canvas.Canvas, title: str, body: str, x: float, y: float, w: float) -> float:
    pad = 8
    body_lines: list[str] = []
    for para in body.split("\n"):
        body_lines.extend(wrap_lines(c, para, w - 2 * pad - 8, 7.8, FONT) or [""])
    box_h = 22 + len(body_lines) * 9.5
    y_bottom = y - box_h
    c.setFillColor(HexColor("#FFFDF8"))
    c.setStrokeColor(LINE)
    c.rect(x, y_bottom, w, box_h, fill=1, stroke=1)
    c.setFillColor(RUST)
    c.rect(x, y_bottom, 2.5, box_h, fill=1, stroke=0)
    ty = y - 12
    ty = draw_text(c, title.upper(), x + pad + 4, ty, size=6.5, font=FONT_BOLD, color=RUST)
    ty -= 2
    for ln in body_lines:
        ty = draw_text(c, ln, x + pad + 4, ty, size=7.8, color=INK)
    return y_bottom - 10