from pathlib import Path
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import textwrap

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'report' / 'evaluation_systems_snapshot.pdf'
AVATAR = BASE / 'public' / 'assets' / 'tarek-avatar-3d-v1-pdf.jpg'

PAGE_W, PAGE_H = letter
M = 0.48 * inch

FONT = 'Helvetica'
FONT_BOLD = 'Helvetica-Bold'
FONT_BLACK = 'Helvetica-Bold'
font_candidates = [
    ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'),
    ('/Library/Fonts/Arial.ttf', '/Library/Fonts/Arial Bold.ttf'),
]
for regular, bold in font_candidates:
    if Path(regular).exists():
        pdfmetrics.registerFont(TTFont('SnapshotSans', regular))
        FONT = 'SnapshotSans'
    if Path(bold).exists():
        pdfmetrics.registerFont(TTFont('SnapshotSans-Bold', bold))
        FONT_BOLD = 'SnapshotSans-Bold'
        FONT_BLACK = 'SnapshotSans-Bold'
    if FONT != 'Helvetica' and FONT_BOLD != 'Helvetica-Bold':
        break

BG = HexColor('#0C0C0C')
INK = HexColor('#D7E2EA')
INK2 = HexColor('#AAB6C1')
MUTED = HexColor('#7E8792')
PINK = HexColor('#B600A8')
PURPLE = HexColor('#7621B0')
ORANGE = HexColor('#BE4C00')
PANEL = Color(0.07, 0.075, 0.09, alpha=0.86)
PANEL2 = Color(0.10, 0.10, 0.13, alpha=0.74)
LINE = Color(0.84, 0.89, 0.92, alpha=0.22)
WHITE15 = Color(1, 1, 1, alpha=0.15)


def set_fill(c, color):
    c.setFillColor(color)


def set_stroke(c, color, width=0.7):
    c.setStrokeColor(color)
    c.setLineWidth(width)


def bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Soft lab glows
    for i, (x, y, r, col) in enumerate([
        (PAGE_W * 0.56, PAGE_H * 0.62, 250, PINK),
        (PAGE_W * 0.16, PAGE_H * 0.18, 220, ORANGE),
        (PAGE_W * 0.86, PAGE_H * 0.25, 170, PURPLE),
    ]):
        c.saveState()
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.045 if i else 0.07))
        c.circle(x, y, r, fill=1, stroke=0)
        c.restoreState()
    # Grid
    c.saveState()
    c.setStrokeColor(Color(1, 1, 1, alpha=0.035))
    c.setLineWidth(0.25)
    step = 28
    for x in range(0, int(PAGE_W) + step, step):
        c.line(x, 0, x, PAGE_H)
    for y in range(0, int(PAGE_H) + step, step):
        c.line(0, y, PAGE_W, y)
    c.restoreState()


def text(c, s, x, y, size=10, color=INK, font=FONT, leading=None, max_width=None, tracking=0, upper=False):
    if upper:
        s = s.upper()
    c.setFillColor(color)
    c.setFont(font, size)
    if max_width:
        avg = size * 0.48
        width_chars = max(8, int(max_width / avg))
        lines = []
        for para in s.split('\n'):
            lines.extend(textwrap.wrap(para, width=width_chars) or [''])
        if leading is None:
            leading = size * 1.25
        yy = y
        for line in lines:
            c.drawString(x, yy, line)
            yy -= leading
        return yy
    if tracking:
        c.drawString(x, y, s)
    else:
        c.drawString(x, y, s)
    return y - (leading or size * 1.25)


def title(c, s, x, y, size=44, max_width=None):
    c.setFillColor(INK)
    c.setFont(FONT_BLACK, size)
    words = s.split()
    lines = []
    line = ''
    for w in words:
        trial = (line + ' ' + w).strip()
        if max_width and c.stringWidth(trial, FONT_BLACK, size) > max_width and line:
            lines.append(line)
            line = w
        else:
            line = trial
    if line:
        lines.append(line)
    yy = y
    for line in lines:
        c.drawString(x, yy, line.upper())
        yy -= size * 0.95
    return yy


def rounded(c, x, y, w, h, r=18, fill=PANEL, stroke=LINE, sw=0.7):
    c.saveState()
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(sw)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1)
    c.restoreState()


def pill(c, s, x, y, pad_x=10, pad_y=5, size=6.8):
    c.setFont(FONT_BOLD, size)
    w = c.stringWidth(s.upper(), FONT_BOLD, size) + pad_x * 2
    h = size + pad_y * 2
    rounded(c, x, y, w, h, r=h / 2, fill=Color(1,1,1,alpha=0.035), stroke=Color(1,1,1,alpha=0.42), sw=0.55)
    text(c, s.upper(), x + pad_x, y + pad_y - 0.5, size=size, color=INK, font=FONT_BOLD)
    return w


def metric(c, value, label, x, y, w, h):
    rounded(c, x, y, w, h, r=18, fill=PANEL2, stroke=Color(1,1,1,alpha=0.25), sw=0.75)
    text(c, value, x + 14, y + h - 34, size=28, color=INK, font=FONT_BLACK)
    text(c, label, x + 14, y + 16, size=6.8, color=INK2, font=FONT_BOLD, upper=True)


def footer(c, page):
    set_stroke(c, Color(1,1,1,alpha=0.12), 0.45)
    c.line(M, 0.42*inch, PAGE_W - M, 0.42*inch)
    text(c, 'Tarek Etman | dr.tareketman@gmail.com | linkedin.com/in/tareketman | Evaluation Systems Snapshot', M, 0.25*inch, size=6.8, color=MUTED)
    c.setFillColor(MUTED)
    c.setFont(FONT, 6.8)
    c.drawRightString(PAGE_W - M, 0.25*inch, f'Page {page} of 2')


def draw_avatar(c, x, y, w, h):
    if not AVATAR.exists():
        return
    c.saveState()
    # shadow/glow plate behind image
    c.setFillColor(Color(PINK.red, PINK.green, PINK.blue, alpha=0.10))
    c.circle(x + w/2, y + h*0.48, w*0.54, fill=1, stroke=0)
    # clipped rounded portrait
    p = c.beginPath()
    r = min(w, h) * 0.28
    p.roundRect(x, y, w, h, r)
    c.clipPath(p, stroke=0, fill=0)
    img = ImageReader(str(AVATAR))
    c.drawImage(img, x, y, w, h, preserveAspectRatio=True, anchor='c', mask='auto')
    c.restoreState()
    # Fade lower edge with BG overlay
    c.saveState()
    for i in range(8):
        c.setFillColor(Color(BG.red, BG.green, BG.blue, alpha=0.035 + i*0.012))
        c.rect(x, y + i*3, w, 3, fill=1, stroke=0)
    c.restoreState()


def page1(c):
    bg(c)
    # header
    text(c, 'Evaluation Systems Snapshot', M, PAGE_H - 0.55*inch, size=8.5, color=INK2, font=FONT_BOLD, upper=True)
    text(c, 'Tarek Etman', PAGE_W - M - 1.25*inch, PAGE_H - 0.55*inch, size=8.5, color=INK2, font=FONT_BOLD, upper=True)
    # title and subtitle
    yy = title(c, 'Clinical model behavior review', M, PAGE_H - 1.15*inch, size=38, max_width=4.55*inch)
    text(c, 'Evaluation systems for high-stakes healthcare-domain model behavior: controlled probes, operational rubrics, calibrated human judgment, and reproducible error analysis.', M, yy - 0.06*inch, size=11.2, color=INK2, leading=14.4, max_width=4.55*inch)
    # avatar
    draw_avatar(c, PAGE_W - M - 2.35*inch, PAGE_H - 3.18*inch, 2.22*inch, 2.55*inch)

    # candidate strip
    strip_y = PAGE_H - 3.92*inch
    rounded(c, M, strip_y, PAGE_W - 2*M, 0.86*inch, r=20, fill=Color(1,1,1,alpha=0.035), stroke=LINE)
    left_x = M + 0.22*inch
    right_x = M + 4.25*inch
    text(c, 'Prepared by', left_x, strip_y + 0.55*inch, size=7, color=MUTED, font=FONT_BOLD, upper=True)
    text(c, 'Licensed dentist | Global Health MPP', left_x, strip_y + 0.36*inch, size=10.1, color=INK, font=FONT_BOLD)
    text(c, 'Model evaluation specialist | clinical safety and rubric review', left_x, strip_y + 0.18*inch, size=8.1, color=INK2, font=FONT_BOLD)
    text(c, 'Synthetic-only public work sample. No patient data, employer tasks, client content, proprietary rubrics, or confidential materials.', right_x, strip_y + 0.53*inch, size=7.7, color=INK2, leading=9.3, max_width=PAGE_W - M - right_x - 0.22*inch)

    # metrics
    mx = M
    my = PAGE_H - 5.05*inch
    mw = (PAGE_W - 2*M - 0.30*inch) / 4
    for i, (v, lab) in enumerate([
        ('14', 'synthetic case probes'), ('28', 'double-scored outputs'), ('8', 'safety dimensions'), ('93%', 'within-one agreement')
    ]):
        metric(c, v, lab, mx + i*(mw + 0.10*inch), my, mw, 0.88*inch)

    # architecture section
    text(c, 'Evidence architecture', M, PAGE_H - 5.55*inch, size=8, color=INK2, font=FONT_BOLD, upper=True)
    arch_y = PAGE_H - 7.10*inch
    card_w = (PAGE_W - 2*M - 0.18*inch) / 2
    layers = [
        ('Synthetic probes', 'Controlled scenarios targeting boundary failures, missing context, and unsafe certainty.'),
        ('Rubric operations', 'Score anchors, cap rules, severity labels, and reviewer-operable criteria.'),
        ('Human judgment data', 'Double-scored outputs with pass/fail states, failure tags, and concise rationales.'),
        ('Agreement analysis', 'Exact agreement, within-one agreement, dimension summaries, and failure-frequency reporting.'),
    ]
    for i, (h, body) in enumerate(layers):
        col = i % 2
        row = i // 2
        x = M + col * (card_w + 0.18*inch)
        y = arch_y - row * 1.12*inch
        rounded(c, x, y, card_w, 0.92*inch, r=18, fill=Color(0.06,0.065,0.08,alpha=0.82), stroke=Color(1,1,1,alpha=0.20), sw=0.6)
        text(c, h, x + 0.16*inch, y + 0.58*inch, size=11, color=INK, font=FONT_BLACK, upper=True)
        text(c, body, x + 0.16*inch, y + 0.37*inch, size=7.7, color=INK2, leading=9.3, max_width=card_w - 0.32*inch)

    footer(c, 1)


def page2(c):
    bg(c)
    text(c, 'Case evidence', M, PAGE_H - 0.62*inch, size=8.5, color=INK2, font=FONT_BOLD, upper=True)
    title(c, 'Four probes, one evaluation stack', M, PAGE_H - 1.17*inch, size=31, max_width=6.8*inch)

    # case cards
    cases = [
        ('01', 'Clinical triage risk', 'Does the model recognize urgency when surface wording looks ordinary?', 'Behavioral safety'),
        ('02', 'Dental medication context', 'Does it handle missing medication and oral-health context safely?', 'Domain constraints'),
        ('03', 'Public-health misinformation', 'Does it preserve uncertainty and evidence strength without amplifying unsupported claims?', 'Evidence quality'),
        ('04', 'Reasoning faithfulness', 'Does the rationale actually support the scoring decision?', 'Auditability'),
    ]
    card_w = (PAGE_W - 2*M - 0.18*inch) / 2
    y0 = PAGE_H - 3.24*inch
    for i, (num, h, q, sig) in enumerate(cases):
        col = i % 2
        row = i // 2
        x = M + col*(card_w + 0.18*inch)
        y = y0 - row*1.28*inch
        rounded(c, x, y, card_w, 1.03*inch, r=18, fill=PANEL, stroke=LINE)
        text(c, num, x + 0.14*inch, y + 0.67*inch, size=23, color=INK, font=FONT_BLACK)
        text(c, h, x + 0.70*inch, y + 0.73*inch, size=11, color=INK, font=FONT_BLACK, upper=True)
        text(c, q, x + 0.70*inch, y + 0.49*inch, size=7.6, color=INK2, leading=9.2, max_width=card_w - 0.86*inch)
        pill(c, sig, x + 0.70*inch, y + 0.14*inch, size=6.1)

    # dimensions and roles
    y = PAGE_H - 6.55*inch
    rounded(c, M, y, PAGE_W - 2*M, 1.35*inch, r=20, fill=Color(1,1,1,alpha=0.035), stroke=LINE)
    text(c, 'Evaluation dimensions', M + 0.18*inch, y + 1.02*inch, size=12, color=INK, font=FONT_BLACK, upper=True)
    dims = ['clinical safety', 'escalation handling', 'context sensitivity', 'factuality', 'uncertainty', 'scope control', 'usefulness', 'rationale quality']
    px = M + 0.18*inch
    py = y + 0.62*inch
    for d in dims:
        w = pill(c, d, px, py, size=5.8)
        px += w + 0.06*inch
        if px > PAGE_W - M - 1.2*inch:
            px = M + 0.18*inch
            py -= 0.28*inch

    y2 = 0.98*inch
    rounded(c, M, y2, PAGE_W - 2*M, 1.05*inch, r=18, fill=Color(0.06,0.065,0.08,alpha=0.86), stroke=LINE)
    text(c, 'Scope', M + 0.18*inch, y2 + 0.72*inch, size=11, color=INK, font=FONT_BLACK, upper=True)
    text(c, 'All examples are synthetic. This is not medical advice, diagnosis, treatment guidance, clinical validation, or production safety certification. Metrics are demonstration summaries, not benchmark claims.', M + 0.18*inch, y2 + 0.48*inch, size=8, color=INK2, leading=9.6, max_width=PAGE_W - 2*M - 0.36*inch)

    footer(c, 2)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle('Evaluation Systems Snapshot')
    c.setAuthor('Tarek Etman')
    c.setSubject('Clinical model behavior evaluation systems snapshot')
    c.setCreator('Tarek Etman')
    page1(c)
    c.showPage()
    page2(c)
    c.save()
    print(OUT)

if __name__ == '__main__':
    build()
