"""Region-based PDF layout engine — single source of truth for ClinMAP editorial PDFs."""
from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from clinmap_pdf_style_v0 import (
    COL_L,
    COL_L_W,
    COL_R,
    COL_R_W,
    CONTENT_BOTTOM,
    LINE,
    M,
    PAGE_W,
    draw_text,
    hrule,
    page_frame,
    section_label,
)

# Spacing rhythm (pt) — change here, not ad hoc in generators
GAP_SECTION = 8
GAP_BAND = 10
GAP_AFTER_LABEL = 0

DEBUG = os.environ.get("CLINMAP_PDF_DEBUG", "").lower() in {"1", "true", "yes"}


@dataclass
class LayoutPage:
    c: canvas.Canvas
    header_left: str
    header_right: str
    footer_left: str
    page: int
    total: int
    y: float = 0.0
    _bands: list[str] = field(default_factory=list)

    def start(self) -> float:
        self.y = page_frame(
            self.c,
            header_left=self.header_left,
            header_right=self.header_right,
            footer_left=self.footer_left,
            page=self.page,
            total=self.total,
        )
        return self.y

    def _debug_band(self, name: str, y_top: float, y_bottom: float, *, full_width: bool = True) -> None:
        if not DEBUG:
            return
        x0 = M if full_width else COL_L
        x1 = PAGE_W - M if full_width else COL_R + COL_R_W
        self.c.saveState()
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.25)
        self.c.setDash(2, 2)
        self.c.rect(x0, y_bottom, x1 - x0, y_top - y_bottom, fill=0, stroke=1)
        self.c.setFont("Helvetica", 5)
        self.c.drawString(x0 + 2, y_top - 7, name)
        self.c.restoreState()

    def title_band(
        self,
        *,
        title: str,
        subtitle: str,
        hook: str,
        right_rows: list[tuple[str, str]],
    ) -> float:
        """Full-width title block with paired left/right rows (aligned baselines)."""
        y_top = self.y
        from clinmap_pdf_style_v0 import FONT, FONT_BOLD, FONT_OBLIQUE, INK, MUTED, RUST

        c = self.c
        left_rows: list[tuple[str, float, str, Any]] = [
            (title, 17, FONT_BOLD, INK),
            (subtitle, 9, FONT, INK),
            (hook, 8, FONT_OBLIQUE, RUST),
        ]
        y = self.y
        for i, (left, size, font, color) in enumerate(left_rows):
            draw_text(c, left, COL_L, y, size=size, font=font, color=color)
            if i < len(right_rows):
                label, value = right_rows[i]
                c.setFont(FONT, 7 if i else 7.2)
                c.setFillColor(MUTED)
                c.drawRightString(PAGE_W - M, y, f"{label}: {value}" if label else value)
            y -= 13 if i == 0 else 12
        self.y = y - GAP_BAND
        self._debug_band("title", y_top, self.y)
        self._bands.append("title")
        return self.y

    def component(self, draw_fn: Callable[[canvas.Canvas, float], float]) -> float:
        """Full-width block; draw_fn receives (canvas, y_top) and returns y_bottom."""
        y_top = self.y
        self.y = draw_fn(self.c, y_top)
        self._debug_band("full", y_top, self.y)
        self._bands.append("full")
        return self.y

    def two_columns(
        self,
        left_fn: Callable[[canvas.Canvas, float], float],
        right_fn: Callable[[canvas.Canvas, float], float],
        *,
        name: str = "two_col",
    ) -> float:
        """Render paired columns; next band starts below the shorter column."""
        y_top = self.y
        y_l = left_fn(self.c, y_top)
        y_r = right_fn(self.c, y_top)
        col_bottom = min(y_l, y_r)
        mid_x = COL_L + COL_L_W + 0.06 * inch
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.35)
        self.c.line(mid_x, col_bottom, mid_x, y_top)
        self.y = col_bottom - GAP_BAND
        self._debug_band(name, y_top, self.y, full_width=True)
        self._bands.append(name)
        return self.y

    def section(
        self,
        c: canvas.Canvas,
        x: float,
        w: float,
        y: float,
        label: str,
        body_fn: Callable[[canvas.Canvas, float], float],
    ) -> float:
        y = section_label(c, label, x, y) + GAP_AFTER_LABEL
        return body_fn(c, y)

    def overflow(self) -> bool:
        return self.y < CONTENT_BOTTOM

    def assert_fit(self, page_name: str) -> None:
        if self.overflow():
            raise LayoutOverflowError(
                f"{page_name} page {self.page}: content reached y={self.y:.1f}, "
                f"below safe zone ({CONTENT_BOTTOM:.1f}). "
                f"Trim content or edit docs/pdf_layout_brief.md band order."
            )


class LayoutOverflowError(RuntimeError):
    pass