#!/usr/bin/env python3
"""Generate Origami for Kids #01 Paper Cup: A4 sheets, final.png, PDF."""
from __future__ import annotations
import html, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'projects' / '01-paper-cup'
S = 150.0  # square mm
OX, OY = 30.0, 42.0
W_PX, H_PX = 2480, 3508  # 300 dpi A4


def esc(t):
    return html.escape(str(t))


def ln(x1, y1, x2, y2, *, dash=None, w=0.4, c='#111', opacity=1):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    op = f' opacity="{opacity}"' if opacity != 1 else ''
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}"{d}{op}/>'


def tx(x, y, t, s=3.2, a='middle', c='#111', b=False):
    w = ' font-weight="700"' if b else ''
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{s}" text-anchor="{a}" fill="{c}" font-family="DejaVu Sans,Arial,sans-serif"{w}>{esc(t)}</text>'


def rect(x, y, w, h, *, fill='#fff', stroke='#111', sw=0.45, dash=None, rx=0):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    r = f' rx="{rx}"' if rx else ''
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{r}/>'


def arrow(x1, y1, x2, y2, c='#0EA5E9'):
    return (
        ln(x1, y1, x2, y2, w=0.7, c=c)
        + f'<path d="M {x2:.2f} {y2:.2f} l -2.2 -1.4 l 0.6 1.4 l -0.6 1.4 z" fill="{c}"/>'
    )


def badge(x, y, n, fill='#7C3AED'):
    return (
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.2" fill="{fill}" stroke="#fff" stroke-width="0.6"/>'
        + tx(x, y + 1.3, str(n), s=4, c='#fff', b=True)
    )


def cal_bar(x, y):
    s = rect(x, y, 100, 10, fill='#111', stroke='#111', sw=0.3)
    for i in range(0, 101, 10):
        h = 4 if i % 50 else 6
        s += ln(x + i, y, x + i, y + h, w=0.35, c='#fff' if i not in (0, 100) else '#111')
    s += tx(x + 50, y + 7.2, '100 mm', s=3.4, c='#fff', b=True)
    s += rect(x + 108, y - 5, 20, 20, fill='#fff', stroke='#111', sw=0.5)
    s += tx(x + 118, y + 7, '20 mm', s=2.6, c='#333')
    s += tx(x + 50, y + 14, 'Measure this bar. It must be exactly 100 mm. PRINT AT 100% / ACTUAL SIZE — do NOT "fit to page".', s=2.6, c='#333')
    return s


def paper_square(x, y, size, creases=None, fill='#FFFDF7'):
    s = rect(x, y, size, size, fill=fill, stroke='#1E1060', sw=0.7)
    s += tx(x + 3, y + 5, 'TL', s=2.4, a='start', c='#94A3B8')
    s += tx(x + size - 3, y + 5, 'TR', s=2.4, a='end', c='#94A3B8')
    s += tx(x + 3, y + size - 2, 'BL', s=2.4, a='start', c='#94A3B8')
    s += tx(x + size - 3, y + size - 2, 'BR', s=2.4, a='end', c='#94A3B8')
    for c in creases or []:
        kind = c.get('kind', 'valley')
        if kind == 'valley':
            s += ln(c['x1'], c['y1'], c['x2'], c['y2'], dash='3 2', w=0.55, c='#2563EB')
        elif kind == 'mountain':
            s += ln(c['x1'], c['y1'], c['x2'], c['y2'], dash='2.5 1.2 0.6 1.2', w=0.55, c='#DC2626')
    return s


def finished_cup(cx, cy, scale=1.0, label=True):
    """Vector finished origami cup: open top, tapered body, two tucked lip flaps front/back."""
    k = scale
    # body trapezoid
    top_w, bot_w, h = 38 * k, 28 * k, 42 * k
    lip = 7 * k
    x0, y0 = cx - top_w / 2, cy - h / 2 - 2 * k
    # back flap (slightly darker, peeking behind rim)
    back = (
        f'<path d="M {x0 + 4*k:.2f} {y0 + lip:.2f} '
        f'L {cx:.2f} {y0 - 2*k:.2f} '
        f'L {x0 + top_w - 4*k:.2f} {y0 + lip:.2f} Z" '
        f'fill="#FDBA74" stroke="#9A3412" stroke-width="{0.55*k:.2f}" stroke-linejoin="round"/>'
    )
    # cup body
    body = (
        f'<path d="M {x0:.2f} {y0 + lip:.2f} '
        f'L {x0 + top_w:.2f} {y0 + lip:.2f} '
        f'L {cx + bot_w/2:.2f} {y0 + lip + h:.2f} '
        f'L {cx - bot_w/2:.2f} {y0 + lip + h:.2f} Z" '
        f'fill="#FED7AA" stroke="#1E1060" stroke-width="{0.65*k:.2f}" stroke-linejoin="round"/>'
    )
    # inner ellipse (opening)
    opening = (
        f'<ellipse cx="{cx:.2f}" cy="{y0 + lip:.2f}" rx="{top_w/2 - 1*k:.2f}" ry="{5.5*k:.2f}" '
        f'fill="#FFEDD5" stroke="#1E1060" stroke-width="{0.5*k:.2f}"/>'
    )
    # front flap tucked over rim (triangle folding into pocket)
    front = (
        f'<path d="M {x0 + 6*k:.2f} {y0 + lip:.2f} '
        f'L {cx:.2f} {y0 + lip + 11*k:.2f} '
        f'L {x0 + top_w - 6*k:.2f} {y0 + lip:.2f} Z" '
        f'fill="#FDBA74" stroke="#9A3412" stroke-width="{0.55*k:.2f}" stroke-linejoin="round"/>'
    )
    # crease hints on body (folded side edges)
    creases = (
        ln(cx - bot_w / 2 + 2 * k, y0 + lip + h - 1 * k, x0 + 3 * k, y0 + lip + 2 * k, w=0.35 * k, c='#EA580C', dash='2 1.5')
        + ln(cx + bot_w / 2 - 2 * k, y0 + lip + h - 1 * k, x0 + top_w - 3 * k, y0 + lip + 2 * k, w=0.35 * k, c='#EA580C', dash='2 1.5')
    )
    # flat bottom hint
    bottom = (
        f'<ellipse cx="{cx:.2f}" cy="{y0 + lip + h:.2f}" rx="{bot_w/2:.2f}" ry="{2.2*k:.2f}" '
        f'fill="#FDBA74" stroke="#1E1060" stroke-width="{0.45*k:.2f}"/>'
    )
    s = back + body + bottom + opening + front + creases
    if label:
        s += tx(cx, y0 + lip + h + 8 * k, 'Finished paper cup!', s=3.2 * max(k, 0.85), c='#9A3412', b=True)
        s += tx(cx, y0 + lip + h + 12 * k, 'Two flaps tucked · open 3D · flat bottom', s=2.4 * max(k, 0.85), c='#64748B')
    return s


def finished_cup_standalone_svg(size_mm=80):
    """Square SVG used for final.png (clean product shot style)."""
    vb = 80
    cx = cy = vb / 2
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size_mm}mm" height="{size_mm}mm" viewBox="0 0 {vb} {vb}">',
        f'<rect width="{vb}" height="{vb}" fill="#FAF5FF"/>',
        finished_cup(cx, cy - 2, scale=1.35, label=True),
        '</svg>',
    ]
    return '\n'.join(body)


def mini_diagram(px, py, step):
    m = 52.0
    s = rect(px, py, m, m, fill='#F8FAFC', stroke='#CBD5E1', sw=0.35, rx=1.5)
    q = 40.0
    qx, qy = px + 6, py + 6
    if step == 1:
        s += rect(qx, qy, q, q, fill='#FFF7ED', stroke='#1E1060', sw=0.5)
        s += ln(qx, qy, qx + q, qy + q, dash='3 2', w=0.6, c='#2563EB')
        s += arrow(qx + 8, qy + 10, qx + 28, qy + 30, '#0EA5E9')
        s += tx(px + m / 2, py + m - 2.5, 'valley diagonal', s=2.4, c='#2563EB')
    elif step == 2:
        s += f'<path d="M {qx:.1f} {qy+q:.1f} L {qx+q:.1f} {qy+q:.1f} L {qx+q/2:.1f} {qy:.1f} Z" fill="#FFF7ED" stroke="#1E1060" stroke-width="0.5"/>'
        s += ln(qx + 2, qy + q - 2, qx + q / 2, qy + 4, dash='3 2', w=0.55, c='#2563EB')
        s += arrow(qx + 6, qy + q - 10, qx + q / 2 - 4, qy + 18, '#0EA5E9')
        s += tx(px + m / 2, py + m - 2.5, 'left corner up', s=2.4, c='#2563EB')
    elif step == 3:
        s += f'<path d="M {qx:.1f} {qy+q:.1f} L {qx+q:.1f} {qy+q:.1f} L {qx+q/2:.1f} {qy:.1f} Z" fill="#FFF7ED" stroke="#1E1060" stroke-width="0.5"/>'
        s += ln(qx + 2, qy + q - 2, qx + q / 2, qy + 4, dash='3 2', w=0.4, c='#93C5FD', opacity=0.9)
        s += ln(qx + q - 2, qy + q - 2, qx + q / 2, qy + 4, dash='3 2', w=0.55, c='#2563EB')
        s += arrow(qx + q - 6, qy + q - 10, qx + q / 2 + 4, qy + 18, '#0EA5E9')
        s += tx(px + m / 2, py + m - 2.5, 'right corner up', s=2.4, c='#2563EB')
    elif step == 4:
        s += f'<path d="M {qx+8:.1f} {qy+q:.1f} L {qx+q-8:.1f} {qy+q:.1f} L {qx+q:.1f} {qy+18:.1f} L {qx+q/2:.1f} {qy:.1f} L {qx:.1f} {qy+18:.1f} Z" fill="#FFF7ED" stroke="#1E1060" stroke-width="0.5"/>'
        s += ln(qx + 4, qy + 16, qx + q - 4, qy + 16, dash='3 2', w=0.55, c='#2563EB')
        s += arrow(qx + q / 2, qy + 4, qx + q / 2, qy + 14, '#0EA5E9')
        s += tx(px + m / 2, py + m - 2.5, 'tuck front lip', s=2.4, c='#2563EB')
    elif step == 5:
        s += rect(qx + 4, qy + 8, q - 8, q - 12, fill='#E0E7FF', stroke='#1E1060', sw=0.5)
        s += tx(px + m / 2, py + m / 2, '↻', s=10, c='#7C3AED')
        s += tx(px + m / 2, py + m - 2.5, 'turn over', s=2.4, c='#7C3AED')
    elif step == 6:
        s += f'<path d="M {qx+8:.1f} {qy+q:.1f} L {qx+q-8:.1f} {qy+q:.1f} L {qx+q:.1f} {qy+18:.1f} L {qx+q/2:.1f} {qy:.1f} L {qx:.1f} {qy+18:.1f} Z" fill="#FFF7ED" stroke="#1E1060" stroke-width="0.5"/>'
        s += ln(qx + 4, qy + 16, qx + q - 4, qy + 16, dash='3 2', w=0.55, c='#2563EB')
        s += arrow(qx + q / 2, qy + 4, qx + q / 2, qy + 14, '#0EA5E9')
        s += tx(px + m / 2, py + m - 2.5, 'tuck back lip', s=2.4, c='#2563EB')
    elif step == 7:
        s += finished_cup(px + m / 2, py + m / 2 - 1, scale=0.72, label=False)
        s += tx(px + m / 2, py + m - 2.5, 'open into a cup', s=2.4, c='#EA580C')
    return s


def step_panel(x, y, w, h, n, title, do, check, tip):
    s = rect(x, y, w, h, fill='#FFFFFF', stroke='#C4B5FD', sw=0.55, rx=2)
    s += badge(x + 7, y + 7, n)
    s += tx(x + 14, y + 8.5, title, s=3.6, a='start', b=True, c='#1E1060')
    s += mini_diagram(x + 4, y + 14, n)
    text_x = x + 60
    s += tx(text_x, y + 20, 'DO', s=2.8, a='start', b=True, c='#7C3AED')
    s += tx(text_x, y + 25, do, s=2.7, a='start', c='#334155')
    s += tx(text_x, y + 33, 'CHECK ✓', s=2.8, a='start', b=True, c='#059669')
    s += tx(text_x, y + 38, check, s=2.7, a='start', c='#334155')
    s += tx(text_x, y + 46, 'TIP', s=2.8, a='start', b=True, c='#EA580C')
    s += tx(text_x, y + 51, tip, s=2.6, a='start', c='#334155')
    return s


def page1():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">',
        '<rect width="210" height="297" fill="#FAF5FF"/>',
        rect(10, 8, 190, 18, fill='#7C3AED', stroke='#7C3AED', sw=0, rx=2),
        tx(105, 16, 'Origami for Kids  ·  Project #01  ·  Paper Cup  ·  page 1/2 (1:1 scale)', s=3.8, c='#fff', b=True),
        tx(105, 22.5, 'PRINT AT 100% / ACTUAL SIZE  —  Do NOT “fit to page”', s=3.0, c='#E9D5FF'),
        tx(105, 36, 'Fold a Paper Cup', s=7, b=True, c='#1E1060'),
        tx(105, 41, 'Ages 6+  ·  ~10 minutes  ·  Square 150 × 150 mm  ·  Coding idea: steps = an algorithm', s=2.8, c='#64748B'),
        # finished cup hero (right of title area, above square — squeezed into right margin of square row)
        tx(OX + S / 2, OY - 2, f'True-size square  {S:g} × {S:g} mm  (cut from A4 if needed)', s=3.0, c='#1E1060', b=True),
    ]
    creases = [{'kind': 'valley', 'x1': OX, 'y1': OY, 'x2': OX + S, 'y2': OY + S}]
    parts.append(paper_square(OX, OY, S, creases=creases))
    # Finished! callout to the right of the square
    fx, fy = OX + S + 8, OY + 20
    parts.append(rect(fx, fy, 50, 70, fill='#FFFFFF', stroke='#FDBA74', sw=0.7, rx=2))
    parts.append(tx(fx + 25, fy + 7, 'Finished!', s=4.2, b=True, c='#EA580C'))
    parts.append(finished_cup(fx + 25, fy + 38, scale=0.85, label=False))
    parts.append(tx(fx + 25, fy + 64, 'Two flaps tucked', s=2.4, c='#9A3412'))
    parts.append(tx(OX + S / 2, OY + S + 5, 'Cut on the solid outer edge if your paper is not already square. Blue dashed = first valley crease (fold toward you).', s=2.5, c='#475569'))
    parts.append(ln(OX, OY + S + 9, OX + S, OY + S + 9, w=0.3, c='#DC2626'))
    parts.append(tx(OX + S / 2, OY + S + 13, f'{S:g} mm', s=2.8, c='#DC2626', b=True))

    ky = OY + S + 20
    parts.append(rect(10, ky, 190, 22, fill='#FFFFFF', stroke='#DDD6FE', sw=0.45, rx=2))
    parts.append(tx(16, ky + 6, 'Symbol key', s=3.2, a='start', b=True, c='#1E1060'))
    parts.append(ln(16, ky + 12, 36, ky + 12, dash='3 2', w=0.7, c='#2563EB'))
    parts.append(tx(38, ky + 13, 'Valley (fold toward you)', s=2.6, a='start', c='#334155'))
    parts.append(ln(95, ky + 12, 115, ky + 12, dash='2.5 1.2 0.6 1.2', w=0.7, c='#DC2626'))
    parts.append(tx(117, ky + 13, 'Mountain (fold away)', s=2.6, a='start', c='#334155'))
    parts.append(tx(16, ky + 19, '↻ Turn over     → Fold arrow     ✓ Check silhouette     ★ Finished cup', s=2.6, a='start', c='#334155'))

    parts.append(rect(10, ky + 26, 92, 28, fill='#FFFFFF', stroke='#BBF7D0', sw=0.45, rx=2))
    parts.append(tx(14, ky + 32, 'You need', s=3.2, a='start', b=True, c='#059669'))
    parts.append(tx(14, ky + 38, '• 1 square paper 150 mm', s=2.6, a='start', c='#334155'))
    parts.append(tx(14, ky + 43, '• Clean hands  ·  Flat table', s=2.6, a='start', c='#334155'))
    parts.append(tx(14, ky + 48, '• Optional: cup of water to test!', s=2.6, a='start', c='#334155'))

    parts.append(rect(108, ky + 26, 92, 28, fill='#FFFFFF', stroke='#FDE68A', sw=0.45, rx=2))
    parts.append(tx(112, ky + 32, 'Coding / maths link', s=3.2, a='start', b=True, c='#B45309'))
    parts.append(tx(112, ky + 38, 'An algorithm is a list of steps', s=2.6, a='start', c='#334155'))
    parts.append(tx(112, ky + 43, 'in order. Skip a fold and the', s=2.6, a='start', c='#334155'))
    parts.append(tx(112, ky + 48, 'cup fails — just like a bug!', s=2.6, a='start', c='#334155'))

    parts.append(cal_bar(20, 275))
    parts.append(tx(105, 293, 'kids.join.dev  ·  @Kids.JoinDev  ·  github.com/dev-repos/kids-origami-projects', s=2.3, c='#94A3B8'))
    parts.append('</svg>')
    return '\n'.join(parts)


def page2():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">',
        '<rect width="210" height="297" fill="#FAF5FF"/>',
        rect(10, 8, 190, 16, fill='#7C3AED', stroke='#7C3AED', sw=0, rx=2),
        tx(105, 15, 'Origami for Kids  ·  Project #01  ·  Paper Cup  ·  Steps 1–7  ·  page 2/2 (1:1 scale)', s=3.5, c='#fff', b=True),
        tx(105, 21, 'PRINT AT 100% / ACTUAL SIZE', s=2.8, c='#E9D5FF'),
    ]
    steps = [
        (1, 'Diagonal valley', 'Fold TL corner to BR.', 'A triangle.', 'Crease with a fingernail.'),
        (2, 'Left corner up', 'Fold left tip to the top.', 'Left flap meets the peak.', 'Keep the triangle stacked.'),
        (3, 'Right corner up', 'Fold right tip to the top.', 'Both sides match (symmetry).', 'Mirror the left fold.'),
        (4, 'Front lip down', 'Fold the front peak into the pocket.', 'Front lip tucked.', 'Slide into the little pocket.'),
        (5, 'Turn over', 'Flip the whole model.', 'Back looks like the front did.', 'Like flipping a pancake.'),
        (6, 'Back lip down', 'Tuck the back peak the same way.', 'Both lips locked.', 'Same move as step 4.'),
        (7, 'Open the cup', 'Squeeze sides, push the bottom flat.', 'A 3D cup!', 'Gentle — do not tear.'),
    ]
    panel_w, panel_h = 92, 52
    gap_x, gap_y = 6, 3
    left, top = 10, 26
    for i, (n, title, do, check, tip) in enumerate(steps):
        col = i % 2
        row = i // 2
        x = left + col * (panel_w + gap_x)
        y = top + row * (panel_h + gap_y)
        parts.append(step_panel(x, y, panel_w, panel_h, n, title, do, check, tip))

    # Finished! banner spanning bottom (replaces sparse 8th cell area + check strip)
    y = top + 4 * (panel_h + gap_y) + 1
    parts.append(rect(10, y, 190, 36, fill='#FFF7ED', stroke='#FDBA74', sw=0.7, rx=2))
    parts.append(tx(70, y + 8, 'Finished!  —  Your paper should look like this', s=3.6, a='start', b=True, c='#EA580C'))
    parts.append(finished_cup(36, y + 20, scale=0.55, label=False))
    parts.append(tx(70, y + 16, 'Flat closed cup (both lips tucked) → open 3D cup with a flat bottom.', s=2.6, a='start', c='#334155'))
    parts.append(tx(70, y + 22, 'If a lip slips out, redo steps 4–6. Try-it: fold a second cup from a magazine page.', s=2.6, a='start', c='#334155'))
    parts.append(tx(70, y + 30, 'Same algorithm, new paper — does it still work?', s=2.6, a='start', c='#64748B'))

    parts.append(cal_bar(20, 275))
    parts.append(tx(105, 293, 'Valley = dashed blue  ·  Mountain = dash-dot red  ·  @Kids.JoinDev', s=2.3, c='#94A3B8'))
    parts.append('</svg>')
    return '\n'.join(parts)


def render_svg_to_png_pdf(svg_path: Path, png_path: Path, pdf_path: Path):
    import re
    px_svg = svg_path.with_name(svg_path.stem + '-px.svg')
    text = svg_path.read_text()
    text = re.sub(
        r'width="210mm" height="297mm" viewBox="0 0 210 297"',
        f'width="{W_PX}" height="{H_PX}" viewBox="0 0 210 297"',
        text,
        count=1,
    )
    px_svg.write_text(text)
    html_path = svg_path.with_suffix('.html')
    html_path.write_text(
        f'<!doctype html><html><head><style>'
        f'html,body{{margin:0;padding:0;width:{W_PX}px;height:{H_PX}px;overflow:hidden;background:#fff}}'
        f'</style></head><body>'
        f'<object type="image/svg+xml" data="{px_svg.as_uri()}" width="{W_PX}" height="{H_PX}"></object>'
        f'</body></html>'
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--disable-dev-shm-usage'])
        page = browser.new_page(viewport={'width': W_PX, 'height': H_PX}, device_scale_factor=1)
        page.goto(html_path.as_uri(), wait_until='networkidle')
        page.wait_for_timeout(250)
        page.screenshot(path=str(png_path), type='png', clip={'x': 0, 'y': 0, 'width': W_PX, 'height': H_PX})
        page2 = browser.new_page()
        page2.goto(svg_path.as_uri(), wait_until='networkidle')
        page2.pdf(path=str(pdf_path), width='210mm', height='297mm', print_background=True,
                  margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        page.close(); page2.close(); browser.close()
    html_path.unlink(missing_ok=True)
    px_svg.unlink(missing_ok=True)


def render_final_png(svg_text: str, out_png: Path, px=1200):
    tmp = OUT / '_final_tmp.svg'
    # pixel-sized for crisp PNG
    text = svg_text.replace('width="80mm" height="80mm"', f'width="{px}" height="{px}"')
    tmp.write_text(text)
    html = OUT / '_final_tmp.html'
    html.write_text(
        f'<!doctype html><html><head><style>html,body{{margin:0;width:{px}px;height:{px}px;background:#FAF5FF}}</style></head>'
        f'<body><object type="image/svg+xml" data="{tmp.as_uri()}" width="{px}" height="{px}"></object></body></html>'
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--disable-dev-shm-usage'])
        page = browser.new_page(viewport={'width': px, 'height': px})
        page.goto(html.as_uri(), wait_until='networkidle')
        page.wait_for_timeout(200)
        page.screenshot(path=str(out_png), type='png', clip={'x': 0, 'y': 0, 'width': px, 'height': px})
        browser.close()
    tmp.unlink(missing_ok=True)
    html.unlink(missing_ok=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    p1 = OUT / 'page-1.svg'
    p2 = OUT / 'page-2.svg'
    p1.write_text(page1())
    p2.write_text(page2())
    print('svg', p1, p2)

    final_svg = OUT / 'final.svg'
    final_svg.write_text(finished_cup_standalone_svg())
    render_final_png(final_svg.read_text(), OUT / 'final.png')
    print('final.png')

    pdfs = []
    for name in ['page-1', 'page-2']:
        render_svg_to_png_pdf(OUT / f'{name}.svg', OUT / f'{name}.png', OUT / f'{name}.pdf')
        pdfs.append(OUT / f'{name}.pdf')
        # preview
        Image.open(OUT / f'{name}.png').resize((620, 877), Image.Resampling.LANCZOS).save(OUT / f'{name}-preview.png')
        print('rendered', name)

    templates = OUT / 'templates.pdf'
    subprocess.check_call(['pdfunite', *[str(p) for p in pdfs], str(templates)])
    # also expose as card alias = page-1 for landing thumb
    Image.open(OUT / 'page-1.png').save(OUT / 'card.png')
    subprocess.check_call(['cp', str(OUT / 'page-1.pdf'), str(OUT / 'card.pdf')])
    print('templates', templates)
    for f in sorted(OUT.iterdir()):
        if f.is_file():
            print(f'  {f.name:28s} {f.stat().st_size:8d}')


if __name__ == '__main__':
    main()
