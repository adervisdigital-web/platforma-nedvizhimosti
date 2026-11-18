"""Файлы логотипа «ПЛАТФОРМА НЕДВИЖИМОСТИ»: SVG (текст в кривых), PDF (вектор), PNG (прозрачный фон) + лист-обзор.
Run: py -3 -X utf8 tools/logo_files.py <Manrope[wght].ttf>  →  09_Логотип_файлы/
Пропорции — как в презентации (tools/p_present.py): hlock(64, 19), vlock(230, 40), знак D «Высокая дверь»."""
import os, sys, subprocess, shutil, tempfile
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '09_Логотип_файлы')
FONT = sys.argv[1]
CHROME = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'

NIGHT, MILK, RED, INK, SUB, WHITE = '#0E0E0F', '#F4F2EE', '#F5553C', '#161617', '#8A867F', '#FFFFFF'
ARCH = 'M0 72 V24 A24 24 0 0 1 48 24 V72 H33 V26 A9 9 0 0 0 15 26 V72 Z'
DOT = (67, 63, 9)

# цветовые версии: (имя, знак+ПЛАТФОРМА, точка, НЕДВИЖИМОСТИ, фон для превью, где использовать)
SCHEMES = [
    ('на_тёмном', MILK, RED, SUB, NIGHT, 'основная версия · тёмный фон'),
    ('на_светлом', INK, RED, SUB, MILK, 'светлый фон · сайт, документы, печать'),
    ('на_красном', WHITE, NIGHT, '#FFD9D2', RED, 'красный фон · реклама и соцсети'),
    ('чёрный', INK, INK, INK, WHITE, 'одним цветом · штамп, гравировка, факс'),
    ('белый', WHITE, WHITE, WHITE, NIGHT, 'одним цветом · вывески, тиснение'),
]

_fonts = {}
def inst(w):
    if w not in _fonts:
        _fonts[w] = instantiateVariableFont(TTFont(FONT), {'wght': w})
    return _fonts[w]


def text_path(s, weight, size, track, x0, y_base, anchor='start'):
    """Текст в кривых. track — разрядка в долях кегля (как CSS letter-spacing, без хвоста после последней буквы)."""
    f = inst(weight); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm; k = size / upm
    names = [cmap[ord(c)] for c in s]
    adv = [f['hmtx'][n][0] * k for n in names]
    width = sum(adv) + track * size * (len(s) - 1)
    x = x0 - (width / 2 if anchor == 'middle' else 0)
    sp = SVGPathPen(gs); bp = BoundsPen(gs)
    for n, a in zip(names, adv):
        t = (k, 0, 0, -k, x, y_base)
        gs[n].draw(TransformPen(sp, t)); gs[n].draw(TransformPen(bp, t))
        x += a + track * size
    return sp.getCommands(), bp.bounds, width


def cap_h(weight, size):
    f = inst(weight)
    return f['OS/2'].sCapHeight / f['head'].unitsPerEm * size


def build(layout, c, dot, sub):
    """→ (svg-элементы, bbox x0,y0,x1,y1) в единицах знака (знак 76×72)."""
    els = [f'<path d="{ARCH}" fill="{c}"/>', f'<circle cx="{DOT[0]}" cy="{DOT[1]}" r="{DOT[2]}" fill="{dot}"/>']
    box = [0, 0, 76, 72]
    if layout == 'знак':
        return els, box
    if layout == 'горизонтальный':          # hlock(64, 19): gap .42w, подпись .55 кегля, отступ round(.55 кегля)
        u = 76 / 64; size = 19 * u; sub_s = size * .55; gap_w = round(64 * .42) * u; gap_l = round(19 * .55) * u
        x0 = 76 + gap_w
        ch1, ch2 = cap_h(300, size), cap_h(400, sub_s)
        block = ch1 + gap_l + ch2 + (size - ch1) * .0   # высота блока по прописным
        top = 36 - block / 2
        p1, b1, w1 = text_path('ПЛАТФОРМА', 300, size, .42, x0, top + ch1)
        p2, b2, w2 = text_path('НЕДВИЖИМОСТИ', 400, sub_s, .5, x0, top + ch1 + gap_l + ch2)
    else:                                   # vlock(230, 40): gap .32w, по центру
        u = 76 / 230; size = 40 * u; sub_s = size * .55; gap_w = round(230 * .32) * u; gap_l = round(40 * .55) * u
        ch1, ch2 = cap_h(300, size), cap_h(400, sub_s)
        y1 = 72 + gap_w + ch1
        p1, b1, w1 = text_path('ПЛАТФОРМА', 300, size, .42, 38, y1, 'middle')
        p2, b2, w2 = text_path('НЕДВИЖИМОСТИ', 400, sub_s, .5, 38, y1 + gap_l + ch2, 'middle')
    els += [f'<path d="{p1}" fill="{c}"/>', f'<path d="{p2}" fill="{sub}"/>']
    xs = [0, 76, b1[0], b1[2], b2[0], b2[2]]; ys = [0, 72, b1[1], b1[3], b2[1], b2[3]]
    return els, [min(xs), min(ys), max(xs), max(ys)]


def svg(els, box, pad, bg=None, title='Платформа недвижимости'):
    x0, y0, x1, y1 = box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad
    w, h = x1 - x0, y1 - y0
    b = f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" width="{w * 10:.0f}" height="{h * 10:.0f}">'
            f'<title>{title}</title>{b}{"".join(els)}</svg>'), w, h


def chrome(args):
    ud = os.path.join(tempfile.gettempdir(), 'pn_chrome_logo')
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', f'--user-data-dir={ud}', '--hide-scrollbars',
                    '--allow-file-access-from-files', '--virtual-time-budget=3000', *args],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)


def export(name, svg_text, w, h, png_w):
    for d in ('SVG', 'PDF', 'PNG'):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    sp = os.path.join(OUT, 'SVG', name + '.svg')
    open(sp, 'w', encoding='utf8').write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg_text)
    tmp = os.path.join(tempfile.gettempdir(), 'pn_logo_tmp'); os.makedirs(tmp, exist_ok=True)
    # PDF: страница точно по логотипу, вектор
    pw, ph = w * 4, h * 4   # pt-масштаб: 1 ед. = 4 px
    hp = os.path.join(tmp, 'pdf.html')
    open(hp, 'w', encoding='utf8').write(
        f'<!doctype html><style>@page{{size:{pw:.2f}px {ph:.2f}px;margin:0}}html,body{{margin:0;background:transparent}}'
        f'svg{{display:block;width:{pw:.2f}px;height:{ph:.2f}px}}</style>{svg_text}')
    pdf = os.path.join(OUT, 'PDF', name + '.pdf')
    chrome(['--no-pdf-header-footer', f'--print-to-pdf={pdf}', 'file:///' + hp.replace('\\', '/')])
    # PNG: прозрачный фон
    ph_px = round(png_w * h / w)
    hp2 = os.path.join(tmp, 'png.html')
    open(hp2, 'w', encoding='utf8').write(
        f'<!doctype html><style>html,body{{margin:0;background:transparent}}svg{{display:block;width:{png_w}px;height:{ph_px}px}}</style>{svg_text}')
    png = os.path.join(OUT, 'PNG', f'{name}_{png_w}px.png')
    chrome(['--default-background-color=00000000', f'--window-size={png_w},{ph_px}', f'--screenshot={png}',
            'file:///' + hp2.replace('\\', '/')])
    return sp, pdf, png


if __name__ == '__main__':
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    made, previews = [], []
    LAY = [('горизонтальный', 3000), ('вертикальный', 2000), ('знак', 1600)]
    for li, (lay, pw) in enumerate(LAY, 1):
        for si, (sch, c, dot, sub, bg, note) in enumerate(SCHEMES, 1):
            els, box = build(lay, c, dot, sub)
            s, w, h = svg(els, box, pad=6)
            name = f'{li}.{si}_ПН_{lay}_{sch}'
            made.append(export(name, s, w, h, pw))
            previews.append((lay, sch, note, bg, s))
    # иконка приложения / аватар: квадрат, знак 56 % ширины
    for nm, bg, c, dot in (('на_тёмном', NIGHT, MILK, RED), ('на_красном', RED, WHITE, NIGHT), ('на_светлом', MILK, INK, RED)):
        side = 76 / .56; ox, oy = (side - 76) / 2, (side - 72) / 2
        s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {side:.2f} {side:.2f}" width="1024" height="1024"><title>Платформа недвижимости</title>'
             f'<rect width="{side:.2f}" height="{side:.2f}" fill="{bg}"/><g transform="translate({ox:.2f} {oy:.2f})">'
             f'<path d="{ARCH}" fill="{c}"/><circle cx="{DOT[0]}" cy="{DOT[1]}" r="{DOT[2]}" fill="{dot}"/></g></svg>')
        made.append(export(f'4_ПН_иконка_{nm}', s, side, side, 1024))
    print('\n'.join(os.path.relpath(p, OUT) for t in made for p in t))
