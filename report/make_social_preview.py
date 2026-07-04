#!/usr/bin/env python3
"""GitHub social preview banner, 1280x640, brand palette."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon, Circle
from pathlib import Path

CREAM, INK, RUST, MUTED = "#F7F4EF", "#344551", "#A95F37", "#68777c"
fig = plt.figure(figsize=(12.8, 6.4), dpi=100)
fig.patch.set_facecolor(CREAM)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1280); ax.set_ylim(0, 640)
ax.axis("off"); ax.set_facecolor(CREAM)

ax.text(90, 430, "ClinMAP-VOI v0", fontsize=52, fontfamily="serif", color=INK, weight="medium")
ax.text(92, 360, "The dangerous answer is rarely the wrong one.", fontsize=22, fontfamily="serif", style="italic", color=RUST)
ax.text(92, 300, "It is the confident one, given too early.", fontsize=22, fontfamily="serif", style="italic", color=RUST)
ax.text(92, 215, "3,971 reviewed responses  ·  17 models  ·  QA audit pass", fontsize=15.5, color=INK, alpha=0.8)
ax.text(92, 165, "3,219 metamorphic relations  ·  a healthcare-domain model behavior benchmark  ·  Tarek Etman", fontsize=13.5, color=MUTED)
ax.plot([92, 700], [135, 135], color=INK, alpha=0.25, lw=1)
ax.text(92, 100, "github.com/TarekEtman/clinmap  ·  synthetic probes, not clinical validation", fontsize=12, color=MUTED)

# The seal: feather of Ma'at in the circle
import numpy as np
cx, cy, R = 1055, 320, 165
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(cx + R * np.cos(th), cy + R * np.sin(th), lw=3, color=INK, alpha=0.75)
# rachis
ys = np.linspace(cy - 115, cy + 100, 100)
t = (ys - (cy - 115)) / 215
xs = cx + np.sin((t) * 1.25) * 14
ax.plot(xs, ys, lw=3.2, color=INK, solid_capstyle="round")
# barbs
for i in range(12):
    tt = i / 11
    y = cy - 105 + tt * 190
    x = cx + np.sin((tt) * 1.25) * 14
    ln = (16 + 44 * np.sin(np.pi * (0.22 + (1 - tt) * 0.78) * 0.92))
    for side, f in ((-1, 1.0), (1, 0.82)):
        col = RUST if (side == -1 and i == 4) else INK
        a = 0.95 if col == RUST else 0.35 + 0.45 * np.sin(np.pi * (0.12 + (1 - tt) * 0.88))
        bx = np.linspace(x, x + side * ln * f, 20)
        by = y + (bx - x) / (side * ln * f + 1e-9) * (10 + tt * 6) * ((bx - x) / (side * ln * f + 1e-9))
        ax.plot(bx, y + ((bx - x) / (side * ln * f + 1e-9)) ** 1.4 * (12 + tt * 4), lw=1.5, color=col, alpha=float(a), solid_capstyle="round")
ax.add_patch(Circle((cx + np.sin(1.25) * 14, cy + 104), 5.5, color=RUST))
out = Path(__file__).resolve().parents[1] / "tmp" / "clinmap_social_preview.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, facecolor=CREAM)
print(f"Wrote {out}")
