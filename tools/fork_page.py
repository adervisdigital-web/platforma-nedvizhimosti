"""Развилка «Арки»: тот же знак в 5 палитрах + 5 доработанных знаков в терракоте.
Run: py -3 tools/fork_page.py  → 04_Развилка/index.html (+ PNG через Chrome)."""
import json, math, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '04_Развилка')
os.makedirs(OUT, exist_ok=True)
BEAR = json.load(open(os.path.join(ROOT, 'tools', 'bearings.json'), encoding='utf8'))
F = 'Manrope'
ARCH = 'M0 0 H36 V40 H26 V20 A8 8 0 0 0 10 20 V40 H0 Z'


def svg(w, inner, vb='0 0 36 40', label='Знак'):
    W, H = [float(x) for x in vb.split()[2:]]
    return f'<svg width="{w}" height="{w * H / W:.1f}" viewBox="{vb}" role="img" aria-label="{label}">{inner}</svg>'


def m_arch(w, c):
    return svg(w, f'<path d="{ARCH}" fill="{c}"/>')


_CID = [0]


def m_stones(w, c, filled=7, ghost=None):
    """Arch block cut into 7 stones: 2+2 jamb blocks, 2 shoulders and a keystone (radial joints at 62°/118°)."""
    _CID[0] += 1; cid = f'st{_CID[0]}'
    h = 0.45
    a = 5.36               # radial joints at 75°/105° reach the top edge at 18 ± a
    regions = [
        [(0, 30 + h), (10, 30 + h), (10, 40), (0, 40)],                       # left lower
        [(26, 30 + h), (36, 30 + h), (36, 40), (26, 40)],                     # right lower
        [(0, 13 + h), (10, 13 + h), (10, 30 - h), (0, 30 - h)],               # left upper
        [(26, 13 + h), (36, 13 + h), (36, 30 - h), (26, 30 - h)],             # right upper
        [(0, 0), (18 - a - h, 0), (18 - h, 20), (10, 20), (10, 13 - h), (0, 13 - h)],   # left shoulder
        [(36, 0), (18 + a + h, 0), (18 + h, 20), (26, 20), (26, 13 - h), (36, 13 - h)],  # right shoulder
        [(18 - a + h, 0), (18 + a - h, 0), (18, 19.2)],                       # keystone
    ]
    inner = f'<defs><clipPath id="{cid}"><path d="{ARCH}"/></clipPath></defs>'
    for n, poly in enumerate(regions):
        pts = ' '.join(f'{x:.2f},{y:.2f}' for x, y in poly)
        op = '1' if n < filled else '0.22'
        inner += f'<polygon points="{pts}" fill="{c}" fill-opacity="{op}" clip-path="url(#{cid})"/>'
    return svg(w, inner)


def m_threshold(w, c, light):
    return svg(w, f'<path d="{ARCH}" fill="{c}"/><rect x="10" y="35.5" width="16" height="4.5" fill="{light}"/>')


def m_key(w, c):
    # block with a keyhole-shaped opening reaching the bottom: circle + slot
    path = (f'M0 0 H36 V40 H23 L21.6 24.2 A7.4 7.4 0 1 0 14.4 24.2 L13 40 H0 Z')
    return svg(w, f'<path d="{path}" fill="{c}" fill-rule="evenodd"/>')


def m_window(w, c, photo):
    hole = 'M10 40 V20 A8 8 0 0 1 26 20 V40 Z'
    return svg(w, f'<defs><clipPath id="wn{w}"><path d="{hole}"/></clipPath></defs>'
                  f'<image href="{photo}" x="6" y="10" width="24" height="30" preserveAspectRatio="xMidYMid slice" clip-path="url(#wn{w})"/>'
                  f'<path d="{ARCH}" fill="{c}"/>')


def lockup(mark_html, size, ink, sub, word='ПЛАТФОРМА'):
    s = size; ss = max(9, round(size * 0.24))
    W, S = BEAR['Manrope|800'], BEAR['Manrope|500']
    bL = W['П']['lsb'] * s - S['Н']['lsb'] * ss; bR = W['А']['rsb'] * s - S['И']['rsb'] * ss
    letters = ''.join(f'<span>{ch}</span>' for ch in 'НЕДВИЖИМОСТИ')
    words = (f'<div style="display:inline-flex;flex-direction:column;gap:{round(s * .16)}px">'
             f'<span style="font:800 {s}px/0.9 {F},sans-serif;letter-spacing:.04em;margin-right:-.04em;color:{ink};white-space:nowrap">{word}</span>'
             f'<span style="display:flex;justify-content:space-between;width:0;min-width:calc(100% - {bL + bR:.2f}px);margin-left:{bL:.2f}px;font:500 {ss}px/1 {F},sans-serif;color:{sub}">{letters}</span></div>')
    return f'<div style="display:flex;flex-direction:column;align-items:center;gap:{round(s * .55)}px">{mark_html}{words}</div>' if mark_html else words


def letter_lockup(size, ink, acc, sub):
    """Arch built into the word: the «П» of ПЛАТФОРМА is the arch."""
    cap = size * 0.735
    arch = (f'<svg width="{cap * 0.80:.1f}" height="{cap:.1f}" viewBox="0 0 80 100" style="display:inline-block;vertical-align:baseline;margin-right:{size * .05:.1f}px" role="img" aria-label="П">'
            f'<path d="M0 100 V0 H80 V100 H58 V43 A18 18 0 0 0 22 43 V100 Z" fill="{acc}"/></svg>')
    ss = max(9, round(size * 0.24))
    letters = ''.join(f'<span>{ch}</span>' for ch in 'НЕДВИЖИМОСТИ')
    return (f'<div style="display:inline-flex;flex-direction:column;gap:{round(size * .16)}px">'
            f'<span style="font:800 {size}px/0.9 {F},sans-serif;letter-spacing:.04em;margin-right:-.04em;color:{ink};white-space:nowrap">{arch}ЛАТФОРМА</span>'
            f'<span style="display:flex;justify-content:space-between;font:500 {ss}px/1 {F},sans-serif;color:{sub}">{letters}</span></div>')


PALETTES = [
    ('1', 'Терракота', 'как сейчас', '#F2EEE7', '#1F1D1B', '#B4532A', '#7A7368'),
    ('2', 'Глубокий зелёный', 'спокойствие, природа', '#EEEDE6', '#17221C', '#1F4D3A', '#6B7069'),
    ('3', 'Графит и латунь', 'солидно, дороже', '#1E1D1B', '#F2EEE7', '#C9A66B', '#A39C90'),
    ('4', 'Синий и песок', 'надёжно, строго', '#E9E1D3', '#13233A', '#1C3557', '#6E6A60'),
    ('5', 'Красный кирпич', 'энергия, камень', '#F4EFE8', '#1E1B19', '#A3271F', '#76706A'),
]


def page(photo):
    T, INK, ACC, SUB, BG = '#B4532A', '#1F1D1B', '#B4532A', '#7A7368', '#F2EEE7'
    row1 = ''
    for n, name, note, bg, ink, acc, sub in PALETTES:
        dark = bg == '#1E1D1B'
        chips = ''.join(f'<i style="background:{c};{"border:1px solid #0002;" if c in (bg,) else ""}"></i>' for c in (bg, ink, acc))
        icon = f'<div class="ic" style="background:{acc}">{m_arch(22, bg if not dark else "#1E1D1B")}</div>'
        row1 += (f'<div class="tile" style="background:{bg};color:{ink}">'
                 f'<div class="tag" style="color:{sub}">Цвет {n}</div>'
                 f'<div class="stage">{lockup(m_arch(70, acc), 24, ink, sub)}</div>'
                 f'<div class="foot"><div><b>{name}</b><span style="color:{sub}">{note}</span></div><div class="right">{icon}<div class="chips">{chips}</div></div></div></div>')
    marks = [
        ('А', '7 камней', 'знак собран из 7 камней = 7 этапов стройки; в приложении показывает, сколько готово',
         lockup(m_stones(70, T), 24, INK, SUB) + f'<div class="mini" style="margin-top:16px">{m_stones(26, T, 3)}<span>в приложении: «ваш дом — 3 из 7»</span></div>',
         ''),
        ('Б', 'Порог', 'в проёме светлая ступень — шаг в свой дом',
         lockup(m_threshold(70, T, '#E2B79A'), 24, INK, SUB), ''),
        ('В', 'Ключ', 'проём арки — это замочная скважина: ключи от дома',
         lockup(m_key(70, T), 24, INK, SUB), ''),
        ('Г', 'Буква в слове', 'отдельного значка нет — арка встроена в само слово',
         letter_lockup(25, INK, T, SUB), ''),
        ('Д', 'Окно с жизнью', 'в проёме всегда живой момент: квартира, ремонт, дом',
         lockup(m_window(70, T, photo), 24, INK, SUB), ''),
    ]
    row2 = ''.join(f'<div class="tile" style="background:{BG};color:{INK}"><div class="tag" style="color:{SUB}">Знак {k}</div>'
                   f'<div class="stage">{lk}</div><div class="foot"><div><b>{nm}</b><span style="color:{SUB}">{d}</span></div>{extra}</div></div>'
                   for k, nm, d, lk, extra in marks)
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Развилка «Арки»</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#F7F5F1;--ink:#1F1D1B;--mut:#7A7368;--line:#E4DDD2}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.5 Manrope,system-ui,sans-serif}}
.wrap{{max-width:1440px;margin:0 auto;padding:56px 56px 64px}}
h1{{font:800 44px/1.05 Manrope,sans-serif;letter-spacing:-.02em;margin:0 0 10px}}
p.lead{{margin:0 0 36px;color:var(--mut);max-width:820px;font-size:18px}}
h2{{font:700 22px Manrope,sans-serif;margin:34px 0 6px}}
h2+p{{margin:0 0 16px;color:var(--mut)}}
.row{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px}}
.tile{{border-radius:18px;padding:18px;min-height:340px;display:flex;flex-direction:column;border:1px solid var(--line)}}
.tag{{font:700 12px Manrope,sans-serif;letter-spacing:.12em;text-transform:uppercase}}
.stage{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:26px 0}}
.foot{{display:flex;justify-content:space-between;align-items:flex-end;gap:10px}}
.foot b{{display:block;font:700 15px Manrope,sans-serif}}.foot span{{display:block;font-size:12.5px;line-height:1.4}}
.right{{display:flex;align-items:center;gap:8px;flex:none}}
.ic{{width:46px;height:46px;border-radius:11px;display:flex;align-items:center;justify-content:center}}
.chips{{display:flex;flex-direction:column;gap:3px}}.chips i{{display:block;width:16px;height:12px;border-radius:3px}}
.mini{{display:flex;align-items:center;gap:6px;flex:none;font-size:11px;color:var(--mut)}}
.ask{{margin-top:34px;background:#1F1D1B;color:#F2EEE7;border-radius:18px;padding:22px 26px;font:600 20px/1.4 Manrope,sans-serif}}
.ask span{{color:#E2B79A}}
@media(max-width:900px){{.wrap{{padding:28px 16px}}.row{{grid-template-columns:1fr 1fr}}h1{{font-size:32px}}}}
@media(max-width:560px){{.row{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<h1>«Арка»: что зацепит?</h1>
<p class="lead">Чтобы понять, что не так — цвет или сам знак, — ниже две развилки. В первом ряду тот же логотип в пяти палитрах. Во втором — пять доработанных знаков в нынешней терракоте.</p>
<h2>Тот же знак — разные цвета</h2><p>Если какой-то цвет «оживил» логотип — дело в цвете.</p>
<div class="row">{row1}</div>
<h2>Тот же цвет — разные знаки</h2><p>Если зацепил один из знаков — дело в знаке. Цвет и знак потом можно собрать в любой комбинации.</p>
<div class="row">{row2}</div>
<div class="ask">Ответьте одной строкой: <span>цвет №… и знак …</span> — например, «цвет 2, знак А».</div>
</div></body></html>'''


if __name__ == '__main__':
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(page('kitchen.jpg'))
    import shutil
    shutil.copy(os.path.join(ROOT, '_source', 'gen', 'kv_kitchen.jpg'), os.path.join(OUT, 'kitchen.jpg'))
    print('ok')
