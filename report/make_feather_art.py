#!/usr/bin/env python3
"""The feather of Ma'at, grown procedurally: one geometry for SVG, site, and banner."""
from __future__ import annotations
import math
from pathlib import Path

INK, INK2, RUST, DOWN = (0x34, 0x45, 0x51), (0x6d, 0x7f, 0x8b), (0xA9, 0x5F, 0x37), (0xB8, 0x86, 0x5A)

def mulberry(seed: int):
    s = seed & 0xFFFFFFFF
    def r():
        nonlocal s
        s = (s + 0x6D2B79F5) & 0xFFFFFFFF
        t = s
        t = (t ^ (t >> 15)) * (t | 1) & 0xFFFFFFFF
        t ^= t + ((t ^ (t >> 7)) * (t | 61) & 0xFFFFFFFF)
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r

def spine(t: float) -> tuple[float, float]:
    """Quill at t=0 (bottom), tip at t=1 (top). Gentle S with a leftward curl at the crown."""
    y = 232 - t * 214
    x = 60 + 20 * t * t - 34 * t ** 5.2
    return x, y

def spine_tangent(t: float) -> tuple[float, float]:
    e = 1e-4
    x1, y1 = spine(max(0, t - e)); x2, y2 = spine(min(1, t + e))
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) or 1
    return dx / n, dy / n

def lerp_col(a, b, f):
    return tuple(round(a[i] + (b[i] - a[i]) * f) for i in range(3))

def hexc(c):
    return '#%02x%02x%02x' % c

def build(seed: int = 40):
    """Returns list of (path_d, color_hex, width, alpha) plus spine polyline pts."""
    rand = mulberry(seed)
    splits = sorted(0.16 + rand() * 0.78 for _ in range(7))
    out = []
    N = 118
    for side in (-1, 1):
        for i in range(N):
            t = 0.045 + (i / (N - 1)) * 0.945
            px, py = spine(t)
            tx, ty = spine_tangent(t)
            nx, ny = -ty * side, tx * side  # normal
            # envelope: ostrich vane, broad middle, rounded crown, short at base
            L = 47 * (math.sin(math.pi * (0.06 + 0.94 * t)) ** 0.72)
            L *= 0.92 + 0.17 * rand()
            if side == 1: L *= 0.86
            # droop: barbs sweep back toward the quill; more at the base
            sweep = 0.62 - 0.34 * t
            dirx = nx * math.cos(sweep) - (-tx) * math.sin(sweep)
            diry = ny * math.cos(sweep) - (-ty) * math.sin(sweep)
            jit = (rand() - 0.5) * 0.10
            ca, sa = math.cos(jit), math.sin(jit)
            dirx, diry = dirx * ca - diry * sa, dirx * sa + diry * ca
            # vane splits: deflect and thin near split lines
            gap = min((abs(t - s) for s in splits), default=1)
            deflect = 0.0
            alpha_f = 1.0
            if gap < 0.014:
                alpha_f = 0.35
                L *= 0.8
            elif gap < 0.05:
                sgn = 1 if min(splits, key=lambda s: abs(t - s)) < t else -1
                deflect = sgn * (0.05 - gap) * 6.5
            ca, sa = math.cos(deflect * 0.12), math.sin(deflect * 0.12)
            dirx, diry = dirx * ca - diry * sa, dirx * sa + diry * ca
            ex, ey = px + dirx * L, py + diry * L + L * 0.10
            cx1, cy1 = px + dirx * L * 0.42, py + diry * L * 0.42 - L * 0.05
            base_col = lerp_col(INK, INK2, rand() * 0.8)
            alpha = (0.30 + 0.5 * (math.sin(math.pi * t) ** 0.8)) * alpha_f
            width = 0.62 + 0.5 * math.sin(math.pi * t)
            # afterfeather: loose warm down near the quill
            if t < 0.13:
                base_col = lerp_col(DOWN, RUST, rand() * 0.6)
                alpha = 0.34 * alpha_f
                width = 0.55
                ex += (rand() - 0.5) * 10
                ey += 6 + rand() * 8
                cy1 += 4
            d = f"M {px:.1f} {py:.1f} Q {cx1:.1f} {cy1:.1f} {ex:.1f} {ey:.1f}"
            out.append((d, hexc(base_col), width, round(alpha, 3)))
            # barbule shadow stroke for depth (subset)
            if 0.2 < t < 0.95 and i % 3 == 0:
                d2 = f"M {px:.1f} {py:.1f} Q {cx1 + side:.1f} {cy1 + 1.2:.1f} {ex + side * 1.5:.1f} {ey + 1.8:.1f}"
                out.append((d2, hexc(lerp_col(base_col, (0xF7, 0xF4, 0xEF), 0.35)), width * 0.6, round(alpha * 0.5, 3)))
    # the dissenting barb: one rust strand on the left vane
    t = 0.615
    px, py = spine(t); tx, ty = spine_tangent(t)
    nx, ny = ty, -tx
    L = 42
    ex, ey = px + nx * L * 0.94 - tx * L * 0.30, py + ny * L * 0.94 - ty * L * 0.30 + 6
    out.append((f"M {px:.1f} {py:.1f} Q {px + nx * L * 0.4:.1f} {py + ny * L * 0.4 - 3:.1f} {ex:.1f} {ey:.1f}", hexc(RUST), 1.15, 0.95))
    # spine as tapered segments
    spine_pts = [spine(k / 90) for k in range(91)]
    return out, spine_pts

def to_svg(path="public/assets/maat-feather.svg", seed=40):
    barbs, spine_pts = build(seed)
    parts = [f'<svg width="120" height="240" viewBox="0 0 120 240" fill="none" xmlns="http://www.w3.org/2000/svg">']
    for d, col, w, a in barbs:
        parts.append(f'<path d="{d}" stroke="{col}" stroke-width="{w:.2f}" stroke-linecap="round" opacity="{a}"/>')
    for k in range(len(spine_pts) - 1):
        t = k / (len(spine_pts) - 1)
        (x1, y1), (x2, y2) = spine_pts[k], spine_pts[k + 1]
        w = 3.1 * (1 - t) + 0.45
        col = hexc(lerp_col(INK, INK2, t * 0.5)) if t > 0.06 else hexc(DOWN)
        parts.append(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="{col}" stroke-width="{w:.2f}" stroke-linecap="round"/>')
    qx, qy = spine_pts[0]
    parts.append(f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="2.1" fill="{hexc(RUST)}"/>')
    parts.append('</svg>')
    Path(path).write_text('\n'.join(parts))
    print(f"Wrote {path} ({len(barbs)} strands)")

def preview(png="tmp/feather_preview.png", seed=40):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    from matplotlib.path import Path as MPath
    import matplotlib.patches as mpatches
    barbs, spine_pts = build(seed)
    fig = plt.figure(figsize=(3.2, 6.4), dpi=200)
    fig.patch.set_facecolor('#F7F4EF')
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(240, 0); ax.axis('off')
    for d, col, w, a in barbs:
        nums = [float(v) for v in d.replace('M', '').replace('Q', '').split()]
        verts = [(nums[0], nums[1]), (nums[2], nums[3]), (nums[4], nums[5])]
        pp = mpatches.PathPatch(MPath(verts, [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3]), fc='none', ec=col, lw=w, alpha=a, capstyle='round')
        ax.add_patch(pp)
    for k in range(len(spine_pts) - 1):
        t = k / (len(spine_pts) - 1)
        (x1, y1), (x2, y2) = spine_pts[k], spine_pts[k + 1]
        ax.plot([x1, x2], [y1, y2], lw=(3.1 * (1 - t) + 0.45), color='#344551' if t > 0.06 else '#B8865A', solid_capstyle='round')
    ax.add_patch(Circle(spine_pts[0], 2.1, color='#A95F37'))
    Path(png).parent.mkdir(exist_ok=True)
    fig.savefig(png, facecolor='#F7F4EF')
    print(f"Wrote {png}")

if __name__ == "__main__":
    to_svg()
    preview()


# ---------- Iridescent plumage ----------
IRIS_STOPS = [
    (0.00, (0x2E, 0x8B, 0x8B)),  # deep teal at the tip
    (0.22, (0x4F, 0xB3, 0xA9)),  # turquoise
    (0.40, (0xD9, 0xA4, 0x41)),  # gold
    (0.58, (0xE0, 0x75, 0x5C)),  # coral
    (0.76, (0x9C, 0x4F, 0x6D)),  # plum
    (0.92, (0x34, 0x45, 0x51)),  # ink at the base
    (1.00, (0x34, 0x45, 0x51)),
]

def iris(t: float):
    t = max(0.0, min(1.0, t))
    for k in range(len(IRIS_STOPS) - 1):
        t0, c0 = IRIS_STOPS[k]; t1, c1 = IRIS_STOPS[k + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0 or 1)
            return lerp_col(c0, c1, f)
    return IRIS_STOPS[-1][1]

def build_iris(seed: int = 40):
    """Same skeleton, living plumage: every barb shifts hue along the vane,
    split in two strands so the color turns at mid-length like light on a real feather."""
    rand = mulberry(seed)
    splits = sorted(0.16 + rand() * 0.78 for _ in range(7))
    out = []
    N = 118
    for side in (-1, 1):
        for i in range(N):
            t = 0.045 + (i / (N - 1)) * 0.945
            px, py = spine(t)
            tx, ty = spine_tangent(t)
            nx, ny = -ty * side, tx * side
            L = 47 * (math.sin(math.pi * (0.06 + 0.94 * t)) ** 0.72)
            L *= 0.92 + 0.17 * rand()
            if side == 1: L *= 0.86
            sweep = 0.62 - 0.34 * t
            dirx = nx * math.cos(sweep) - (-tx) * math.sin(sweep)
            diry = ny * math.cos(sweep) - (-ty) * math.sin(sweep)
            jit = (rand() - 0.5) * 0.10
            ca, sa = math.cos(jit), math.sin(jit)
            dirx, diry = dirx * ca - diry * sa, dirx * sa + diry * ca
            gap = min((abs(t - s) for s in splits), default=1)
            alpha_f = 1.0
            if gap < 0.014:
                alpha_f = 0.35; L *= 0.8
            elif gap < 0.05:
                sgn = 1 if min(splits, key=lambda s: abs(t - s)) < t else -1
                d = sgn * (0.05 - gap) * 0.78
                ca, sa = math.cos(d), math.sin(d)
                dirx, diry = dirx * ca - diry * sa, dirx * sa + diry * ca
            mx, my = px + dirx * L * 0.52, py + diry * L * 0.52 - L * 0.03
            ex, ey = px + dirx * L, py + diry * L + L * 0.10
            hue_jit = (rand() - 0.5) * 0.14
            c_in = iris(1 - t + hue_jit)          # tip of feather = start of palette
            c_out = iris(1 - t + hue_jit - 0.16)  # strand turns color at mid-length
            alpha = (0.42 + 0.5 * (math.sin(math.pi * t) ** 0.8)) * alpha_f
            width = 0.68 + 0.55 * math.sin(math.pi * t)
            if t < 0.13:  # warm down at the quill
                c_in = lerp_col(DOWN, RUST, rand() * 0.7); c_out = c_in
                alpha = 0.4 * alpha_f; width = 0.55
                ex += (rand() - 0.5) * 10; ey += 6 + rand() * 8
            out.append((f"M {px:.1f} {py:.1f} Q {px + dirx * L * 0.30:.1f} {py + diry * L * 0.30 - L * 0.04:.1f} {mx:.1f} {my:.1f}", hexc(c_in), width, round(alpha, 3)))
            out.append((f"M {mx:.1f} {my:.1f} Q {px + dirx * L * 0.78:.1f} {py + diry * L * 0.78 + L * 0.02:.1f} {ex:.1f} {ey:.1f}", hexc(c_out), width * 0.85, round(alpha * 0.9, 3)))
            # sheen: pale echo strand
            if 0.2 < t < 0.95 and i % 4 == 0:
                out.append((f"M {px:.1f} {py:.1f} Q {mx + side:.1f} {my + 1.4:.1f} {ex + side * 1.6:.1f} {ey + 2:.1f}", '#F7F4EF', width * 0.5, 0.28))
    spine_pts = [spine(k / 90) for k in range(91)]
    return out, spine_pts

def iris_svg(path="public/assets/maat-feather-iris.svg", seed=40):
    barbs, spine_pts = build_iris(seed)
    parts = ['<svg width="120" height="240" viewBox="0 0 120 240" fill="none" xmlns="http://www.w3.org/2000/svg">']
    for d, col, w, a in barbs:
        parts.append(f'<path d="{d}" stroke="{col}" stroke-width="{w:.2f}" stroke-linecap="round" opacity="{a}"/>')
    for k in range(len(spine_pts) - 1):
        t = k / (len(spine_pts) - 1)
        (x1, y1), (x2, y2) = spine_pts[k], spine_pts[k + 1]
        w = 3.1 * (1 - t) + 0.45
        parts.append(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="{hexc(lerp_col(INK, (0x2E,0x8B,0x8B), t*0.55))}" stroke-width="{w:.2f}" stroke-linecap="round"/>')
    qx, qy = spine_pts[0]
    parts.append(f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="2.1" fill="{hexc(RUST)}"/>')
    parts.append('</svg>')
    Path(path).write_text('\n'.join(parts))
    print(f"Wrote {path}")

def logo(png="tmp/clinmap_logo_linkedin.png", seed=40):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    from matplotlib.path import Path as MPath
    import matplotlib.patches as mpatches
    barbs, spine_pts = build_iris(seed)
    fig = plt.figure(figsize=(8, 8), dpi=100)
    fig.patch.set_facecolor('#F7F4EF')
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis('off'); ax.set_facecolor('#F7F4EF')
    ax.set_xlim(-80, 200); ax.set_ylim(260, -20); ax.set_aspect('equal')
    ax.add_patch(Circle((60, 120), 118, fill=False, ec='#344551', lw=2.2, alpha=0.75))
    for d, col, w, a in barbs:
        nums = [float(v) for v in d.replace('M', '').replace('Q', '').split()]
        verts = [(nums[0], nums[1]), (nums[2], nums[3]), (nums[4], nums[5])]
        ax.add_patch(mpatches.PathPatch(MPath(verts, [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3]), fc='none', ec=col, lw=w * 2.4, alpha=a, capstyle='round'))
    for k in range(len(spine_pts) - 1):
        t = k / (len(spine_pts) - 1)
        (x1, y1), (x2, y2) = spine_pts[k], spine_pts[k + 1]
        ax.plot([x1, x2], [y1, y2], lw=(3.1 * (1 - t) + 0.45) * 2.4, color=hexc(lerp_col(INK, (0x2E, 0x8B, 0x8B), t * 0.55)), solid_capstyle='round')
    ax.add_patch(Circle(spine_pts[0], 4.6, color=hexc(RUST)))
    Path(png).parent.mkdir(exist_ok=True)
    fig.savefig(png, facecolor='#F7F4EF')
    print(f"Wrote {png}")
