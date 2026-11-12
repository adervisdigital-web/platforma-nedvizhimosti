"""Three identity variants (light / dark / bright) for ПЛАТФОРМА НЕДВИЖИМОСТИ.
Each variant: logo board (1440x1540) + style & mockups board (1440x1640)."""
import sys
sys.path.insert(0, 'C:/Users/MSI/AppData/Local/Temp/claude/10d39200edc2b63f/973356bb-8c70-4e3b-b6ae-d636a7404011/scratchpad/v3')
from marks import mark_L, mark_D, mark_Y

OUT = 'C:/Users/MSI/AppData/Local/Temp/claude/10d39200edc2b63f/973356bb-8c70-4e3b-b6ae-d636a7404011/scratchpad/mood/project/'
B = '/_blob/'
IMG = dict(
    build=B + 'a9a387416fc9107965b27f505644a667', brick=B + 'ca00be2acd9690fb9dea9110aaaec783',
    stone=B + '597b77d5921d32365d4391f69448844f', gable=B + 'b471f2a087272c564fa40cb48156b5a1',
    hflat=B + '241aa9c6494b7c64ac1bea49f925807d', kitchen=B + '6eb6b66044bc72cd1c691f54afa97fd2',
    bedroom=B + 'a51f99a2ebaa3290cc815a60538e1744', building=B + '1947ff52209ccab806cd2be3be49c501',
    bath=B + 'e05ef6fc38a92410bfb373f11b4be3cd', after=B + 'ab22bbc0ab515db845d3dee45c8b5d04',
    detail=B + '3472f23568c92d74ff24b6057454790b', process=B + 'de9f3f7fe15a4720d9b574a1e479b7c1')

import json as _json, os as _os
IMG.update({k: '/_blob/' + v for k, v in _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'blobs4.json'), encoding='utf8')).items()})
IMG.update({k: '/_blob/' + v for k, v in _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'blobs2.json'), encoding='utf8')).items()})

def fam(v):
    """Design family of a variant (new arch variants reuse the 'L' layouts) + switch the arch mark shape."""
    import marks as _mk
    _mk.SHAPE = v.get('shape', 'arch')
    _mk.SHAPE_Y = 'module' if v.get('shape') == 'module' else 'assembly'
    if v.get('shape') == 'module':
        _mk.MOD = (v['acc'], v['acc2'])
    return v.get('fam', v['key'])


V = {
 'L': dict(key='L', title='Светлый', name='Арка', file='L',
           gf='family=Manrope:wght@400;500;600;700;800', F='Manrope', FH='Manrope', word_w=800, word_ls='0.04em', word_k=1.0,
           bg='#F2EEE7', panel='#FBF9F5', ink='#1F1D1B', text='#1F1D1B', muted='#7A7368', line='#DED7CB',
           acc='#B4532A', acc_ink='#FFFFFF', sand='#D9CBB5', dir=('#B4532A', '#B4532A', '#B4532A'),
           palette=[('Камень', '#F2EEE7', 40), ('Графит', '#1F1D1B', 26), ('Терракота', '#B4532A', 18), ('Песок', '#D9CBB5', 16)],
           idea='Арка — это буква «П» и вход в дом. Каменная, тёплая, понятная без слов. Платформа открывает дверь: в новую квартиру, в отремонтированную, в свой дом.',
           why=['Одна фигура — читается и в 16 px', 'Арка-окно становится рамкой для всех фото', 'Терракота — цвет кирпича и керамики, тепло без пафоса'],
           type_desc='Manrope — геометричный гротеск с кириллицей. Логотип 800, заголовки 600, текст 400.',
           mood='Спокойно, тепло, «как дома». Много воздуха, светлый камень, один тёплый акцент.'),
 'D': dict(key='D', title='Тёмный', name='Портал', file='D',
           gf='family=Inter+Tight:wght@400;500;600;700', F='Inter Tight', FH='Inter Tight', word_w=600, word_ls='0.02em', word_k=1.0,
           bg='#0E0F11', panel='#17191C', ink='#F2F1EE', text='#F2F1EE', muted='#8D929A', line='#2A2D32',
           acc='#FFB547', acc_ink='#14120E', sand='#A7ACB4', dir=('#FFB547', '#FFB547', '#FFB547'),
           palette=[('Ночь', '#0E0F11', 44), ('Бетон', '#2A2D32', 18), ('Сталь', '#A7ACB4', 14), ('Белый', '#F2F1EE', 14), ('Свет', '#FFB547', 10)],
           idea='Объёмная «П» — дом-портал, в проёме горит тёплый свет. Объём говорит «строим по-настоящему», свет — «вас уже ждут».',
           why=['Объём сразу считывается как здание', 'Свет в проёме — эмоция дома, а не стройки', 'Тёмный фон даёт премиальность без золота'],
           type_desc='Inter Tight — плотный инженерный гротеск. Логотип 600, заголовки 500, текст 400.',
           mood='Уверенно и технологично. Тёмный бетон, сталь и один источник тёплого света.'),
 'Y': dict(key='Y', title='Яркий', name='Сборка', file='Y',
           gf='family=Unbounded:wght@500;600;700&amp;family=Manrope:wght@400;500;600;700', F='Manrope', FH='Unbounded', word_w=600, word_ls='0', word_k=0.86,
           bg='#FFFFFF', panel='#F3F4F8', ink='#14161F', text='#14161F', muted='#6B6F7D', line='#E3E5EC',
           acc='#2E4BFF', acc_ink='#FFFFFF', sand='#F3F4F8', dir=('#2E4BFF', '#FF6B2C', '#18B26B'),
           palette=[('Белый', '#FFFFFF', 40), ('Чернила', '#14161F', 21), ('Квартиры', '#2E4BFF', 13), ('Ремонт', '#FF6B2C', 13), ('Дома', '#18B26B', 13)],
           idea='«П» собрана из трёх частей: слева квартиры, сверху ремонт, справа дома. Вместе — платформа. У каждого направления свой цвет, и он ведёт человека по сайту.',
           why=['Знак объясняет бизнес: три направления — одна компания', 'Цвет = навигация по разделам приложения', 'Энергия массового рынка, как у больших платформ'],
           type_desc='Unbounded — широкий для логотипа и заголовков, Manrope — для текста. Оба с кириллицей.',
           mood='Смело и дружелюбно. Белый фон, три чистых цвета, крупная широкая типографика.'),
 'K': dict(key='K', fam='L', shape='masonry', title='Красный', name='Кладка', file='K',
           gf='family=Manrope:wght@400;500;600;700;800', F='Manrope', FH='Manrope', word_w=800, word_ls='0.04em', word_k=1.0,
           bg='#F4EFE8', panel='#FBF8F3', ink='#1E1B19', text='#1E1B19', muted='#76706A', line='#E2DACE',
           acc='#C8102E', acc_ink='#FFFFFF', sand='#E4D3BF', sand2='#EFE3D3', dir=('#C8102E', '#C8102E', '#C8102E'),
           palette=[('Известь', '#F4EFE8', 40), ('Графит', '#1E1B19', 26), ('Красный', '#C8102E', 18), ('Глина', '#E4D3BF', 16)],
           idea='Та же арка-«П», но сложенная из камня: ряды кладки, клинчатая перемычка и замковый камень. Знак рассказывает, что мы строим сами и на века. В малых размерах кладка убирается — остаётся чистая арка.',
           why=['Детализация видна на вывеске, баннере и упаковке', 'Замковый камень — символ надёжности и завершённой работы', 'Красный — кирпич и энергия, заметен на стройке и в ленте'],
           type_desc='Manrope — геометричный гротеск с кириллицей. Логотип 800, заголовки 600, текст 400.',
           mood='Крепко и по-строительному. Известь, графит и один красный акцент, как кирпич в кладке.'),
 'S': dict(key='S', fam='L', shape='vault', title='Зелёный', name='Свод', file='S',
           gf='family=Geologica:wght@400;500;600;700', F='Geologica', FH='Geologica', word_w=700, word_ls='0.03em', word_k=0.96,
           bg='#F1EEE6', panel='#FAF8F3', ink='#1D2620', text='#1D2620', muted='#6B7069', line='#DCD8CC',
           acc='#2F5D46', acc_ink='#FFFFFF', sand='#D8CDB4', sand2='#E6DDCB', dir=('#2F5D46', '#2F5D46', '#2F5D46'),
           palette=[('Песок', '#F1EEE6', 40), ('Хвоя', '#1D2620', 26), ('Зелень', '#2F5D46', 18), ('Лён', '#D8CDB4', 16)],
           idea='Арка-«П» с дверной рамой и порогом внутри: вход в дом, который уже готов. Двойной контур — аккуратность ремонта, порог — шаг в новую жизнь.',
           why=['Читается как дверь — понятно без слов', 'Зелёный — спокойствие, природа, свой дом за городом', 'Рама и порог дают простую фирменную графику для рамок'],
           type_desc='Geologica — мягкий геометричный гротеск с кириллицей. Логотип 700, заголовки 600, текст 400.',
           mood='Спокойно и природно. Тёплый песок, глубокая зелень и много воздуха.'),
 'M': dict(key='M', fam='Y', shape='module', title='Бирюзовый', name='Модуль', file='M',
           gf='family=Golos+Text:wght@400;500;600;700;800', F='Golos Text', FH='Golos Text', word_w=800, word_ls='0.02em', word_k=0.95,
           bg='#F7F4EE', panel='#FFFFFF', ink='#15171C', text='#15171C', muted='#676A70', line='#E3DED4',
           acc='#0E9F8E', acc_ink='#FFFFFF', acc2='#F6B93B', sand='#E4EFEC', dir=('#0E9F8E', '#0E9F8E', '#0E9F8E'),
           palette=[('Молочный', '#F7F4EE', 40), ('Графит', '#15171C', 24), ('Бирюза', '#0E9F8E', 22), ('Солнце', '#F6B93B', 8), ('Туман', '#E4EFEC', 6)],
           idea='Платформа — конструктор: квартиру, ремонт и дом собирают из одинаковых модулей. «П» сложена из 7 модулей сетки 3×3, пустые клетки — дверной проём. Жёлтый модуль — это вы: тот, который мы ставим на место.',
           why=['Знак — система: из тех же модулей собираются иконки направлений', 'Фото помещаются прямо в модули — мозаика вместо баннеров', 'Бирюза свежая и спокойная, жёлтый — одна яркая точка внимания'],
           type_desc='Golos Text — гротеск российских дизайнеров с кириллицей. Логотип 800, заголовки 700, текст 400.',
           mood='Собрано и понятно. Молочный фон, бирюзовые модули и один жёлтый — как в конструкторе.'),
}


def mosaic(v, W, H, cells, photos, s=None, g=None, r=None, x0=0, y0=0):
    """«Модуль» supergraphic: rounded modules on a grid; some modules hold photos, one is the accent."""
    s = s or 96; g = g or 12; r = r or 18
    defs = ''; body = ''
    uid = abs(hash((W, H, len(cells), s))) % 100000
    for i, (c, rr, kind) in enumerate(cells):
        x, y = x0 + c * (s + g), y0 + rr * (s + g)
        if kind == 'acc':
            body += f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{r}" fill="{v["acc2"]}"/>'
        elif kind == 'mod':
            body += f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{r}" fill="{v["acc"]}"/>'
        elif kind == 'ghost':
            body += f'<rect x="{x + 1}" y="{y + 1}" width="{s - 2}" height="{s - 2}" rx="{r}" fill="none" stroke="{v["muted"]}" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="6 6"/>'
        else:
            src = photos[int(kind[1:]) % len(photos)]
            defs += f'<clipPath id="mz{uid}_{i}"><rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{r}"/></clipPath>'
            body += f'<image href="{src}" x="{x}" y="{y}" width="{s}" height="{s}" preserveAspectRatio="xMidYMid slice" clip-path="url(#mz{uid}_{i})"/>'
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Мозаика из модулей"><defs>{defs}</defs>{body}</svg>'


def mark(v, w, mono=None, on_dark=False):
    k = fam(v)
    if k == 'L':
        return mark_L(w, mono or v['acc'])
    if k == 'D':
        if mono == 'LIGHTBG':
            return mark_D(w, front='#14120E', top='#7A7F87', side='#3A3D43', glow='#FFB547')
        if mono == 'YELLOWBG':
            return mark_D(w, front='#14120E', top='#8A6A2A', side='#4A3712', glow='#FFFFFF')
        if mono:
            return mark_D(w, mono=mono)
        return mark_D(w)
    if mono:
        return mark_Y(w, mono, mono, mono)
    return mark_Y(w, *v['dir'])


def lockup(v, size, ink, sub, mono=None, mw=None, vertical=False, on_dark=False):
    FH = v['FH']; s = round(size * v['word_k'])
    m = mark(v, mw or round(size * 1.45), mono, on_dark)
    sub_letters = ''.join(f'<span>{ch}</span>' for ch in 'НЕДВИЖИМОСТИ')
    ls_fix = f'margin-right: -{v["word_ls"]};' if v['word_ls'] not in ('0', '0em') else ''
    words = (f'<div style="display: inline-flex; flex-direction: column; gap: {max(4, round(size * 0.16))}px">'
             f'<span style="font: {v["word_w"]} {s}px/0.9 \'{FH}\', sans-serif; letter-spacing: {v["word_ls"]}; {ls_fix} color: {ink}; white-space: nowrap">ПЛАТФОРМА</span>'
             f'<span style="display: flex; justify-content: space-between; width: 0; min-width: 100%; font: 500 {max(9, round(size * 0.24))}px/1 \'{v["F"]}\', sans-serif; color: {sub}">{sub_letters}</span></div>')
    d = 'column' if vertical else 'row'
    return f'<div style="display: flex; flex-direction: {d}; align-items: center; gap: {round(size * (0.5 if vertical else 0.42))}px">{m}{words}</div>'


def head(title, v, h):
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?{v['gf']}&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0}}
</style>
</helmet>
'''


def tail(h):
    return f'''</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":{h}}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''


def label(v, t, color=None):
    return f'<span style="font: 400 13px \'{v["F"]}\', sans-serif; color: {color or v["muted"]}">[ {t} ]</span>'


# ---------- construction drawings ----------
def construction(v, H=420):
    k = fam(v); g = v['muted']; ink = v['ink']
    if v['key'] == 'M':
        import marks as _mk
        sc = H / 36; W = 36 * sc
        cells = ''.join(f'<rect x="{c * 12.8 * sc:.1f}" y="{r * 12.8 * sc:.1f}" width="{10.4 * sc:.1f}" height="{10.4 * sc:.1f}" rx="{2.2 * sc:.1f}" fill="none" stroke="{g}" stroke-width="1" stroke-dasharray="4 6"/>' for c in range(3) for r in range(3))
        body = f'<svg x="0" y="0" width="{W}" height="{H}" viewBox="0 0 36 36">{_mk.module_rects()}</svg>'
        notes = (f'<text x="{W + 40}" y="{5.2 * sc}" font-size="13" fill="{v["acc2"]}" font-family="{v["F"]}">← ваш модуль</text>'
                 f'<text x="{W + 40}" y="{24 * sc}" font-size="13" fill="{g}" font-family="{v["F"]}">сетка 3 × 3</text>'
                 f'<text x="{W + 40}" y="{24 * sc + 20}" font-size="13" fill="{g}" font-family="{v["F"]}">модуль 10.4 · шаг 2.4</text>'
                 f'<line x1="0" y1="{-14}" x2="{W}" y2="{-14}" stroke="{g}" stroke-width="1"/><line x1="0" y1="-20" x2="0" y2="-8" stroke="{g}"/><line x1="{W}" y1="-20" x2="{W}" y2="-8" stroke="{g}"/>'
                 f'<text x="{W / 2}" y="-20" font-size="12" fill="{g}" text-anchor="middle" font-family="{v["F"]}">3x</text>'
                 f'<line x1="-14" y1="0" x2="-14" y2="{10.4 * sc}" stroke="{g}" stroke-width="1"/><text x="-20" y="{5.6 * sc}" font-size="12" fill="{g}" text-anchor="end" font-family="{v["F"]}">x</text>'
                 f'<rect x="{-10.4 * sc * 0.5}" y="{-10.4 * sc * 0.5}" width="{W + 10.4 * sc}" height="{H + 10.4 * sc}" fill="none" stroke="{v["acc"]}" stroke-width="1" stroke-dasharray="2 5"/>'
                 f'<text x="{W + 10.4 * sc * 0.5 + 6}" y="{H + 10.4 * sc * 0.5}" font-size="12" fill="{v["acc"]}" font-family="{v["F"]}">охранное поле ½x</text>')
        return f'<svg width="{W + 180}" height="{H}" viewBox="-30 -30 {W + 210} {H + 60}" style="overflow: visible" aria-label="Построение знака">{cells}{body}{notes}</svg>'
    if k == 'L':
        s = H / 40; W = 36 * s
        lines = ''.join(f'<line x1="{x * s}" y1="-30" x2="{x * s}" y2="{H + 30}" stroke="{g}" stroke-width="1" stroke-dasharray="4 6" opacity="0.6"/>' for x in (0, 10, 18, 26, 36))
        lines += ''.join(f'<line x1="-30" y1="{y * s}" x2="{W + 30}" y2="{y * s}" stroke="{g}" stroke-width="1" stroke-dasharray="4 6" opacity="0.6"/>' for y in (0, 12, 20, 40))
        lines += f'<circle cx="{18 * s}" cy="{(19.1 if v.get('shape') == 'masonry' else 20) * s}" r="{8 * s}" fill="none" stroke="{ink}" stroke-width="1.2" opacity="0.55"/>'
        lines += f'<circle cx="{18 * s}" cy="{(19.1 if v.get('shape') == 'masonry' else 20) * s}" r="3" fill="{ink}"/>'
        notes = (f'<text x="{W + 40}" y="{12 * s + 4}" font-size="13" fill="{g}" font-family="{v["F"]}">r = 8 модулей</text>'
                 f'<text x="{W + 40}" y="{40 * s}" font-size="13" fill="{g}" font-family="{v["F"]}">10 · 16 · 10</text>')
        body = f'<g transform="translate(0,0)">{mark_L(W, v["acc"]).split(">", 1)[1].rsplit("</svg>", 1)[0]}</g>'
        body = f'<svg x="0" y="0" width="{W}" height="{H}" viewBox="0 0 36 40">' + body + '</svg>'
        return f'<svg width="{W + 180}" height="{H}" viewBox="-30 -30 {W + 210} {H + 60}" style="overflow: visible" aria-label="Построение знака">{body}{lines}{notes}</svg>'
    if k == 'D':
        s = H / 36; W = 36 * s
        inner = mark_D(W).split('>', 1)[1].rsplit('</svg>', 1)[0]
        body = f'<svg x="0" y="0" width="{W}" height="{H}" viewBox="0 0 36 36">{inner}</svg>'
        lines = ''.join(f'<line x1="{(a - 10) * s}" y1="{(b + 10) * s}" x2="{(a + 12) * s}" y2="{(b - 12) * s}" stroke="{g}" stroke-width="1" stroke-dasharray="4 6" opacity="0.7"/>'
                        for a, b in ((0, 8), (28, 8), (28, 36), (8, 16)))
        lines += ''.join(f'<line x1="{x * s}" y1="-30" x2="{x * s}" y2="{H + 30}" stroke="{g}" stroke-width="1" stroke-dasharray="4 6" opacity="0.5"/>' for x in (0, 8, 20, 28))
        notes = f'<text x="{W + 40}" y="{8 * s}" font-size="13" fill="{g}" font-family="{v["F"]}">глубина 45°</text><text x="{W + 40}" y="{30 * s}" font-size="13" fill="{g}" font-family="{v["F"]}">свет внутри</text>'
        return f'<svg width="{W + 180}" height="{H}" viewBox="-30 -30 {W + 210} {H + 60}" style="overflow: visible" aria-label="Построение знака">{body}{lines}{notes}</svg>'
    s = H / 36; W = 40 * s
    inner = mark_Y(W, *v['dir']).split('>', 1)[1].rsplit('</svg>', 1)[0]
    body = f'<svg x="0" y="0" width="{W}" height="{H}" viewBox="0 0 40 36">{inner}</svg>'
    lines = (f'<line x1="{-4 * s}" y1="{-4 * s}" x2="{16 * s}" y2="{16 * s}" stroke="{g}" stroke-width="1" stroke-dasharray="4 6"/>'
             f'<line x1="{44 * s}" y1="{-4 * s}" x2="{24 * s}" y2="{16 * s}" stroke="{g}" stroke-width="1" stroke-dasharray="4 6"/>')
    lines += ''.join(f'<line x1="{x * s}" y1="-30" x2="{x * s}" y2="{H + 30}" stroke="{g}" stroke-width="1" stroke-dasharray="4 6" opacity="0.5"/>' for x in (0, 10, 30, 40))
    notes = (f'<text x="{W + 40}" y="{5 * s + 4}" font-size="14" fill="{v["dir"][1]}" font-family="{v["F"]}">← ремонт</text>'
             f'<text x="{W + 40}" y="{26 * s}" font-size="14" fill="{v["dir"][2]}" font-family="{v["F"]}">← дома</text>'
             f'<text x="{12 * s}" y="{30 * s}" font-size="14" fill="{v["dir"][0]}" font-family="{v["F"]}">← квартиры</text>')
    return f'<svg width="{W + 180}" height="{H}" viewBox="-30 -30 {W + 210} {H + 60}" style="overflow: visible" aria-label="Построение знака">{body}{lines}{notes}</svg>'


def directions(v):
    names = ('Квартиры', 'Ремонт', 'Дома')
    subs = ('новостройки и вторичка', 'под ключ, со сметой', 'каменные, по проекту')
    cells = ''
    for i, (n, s) in enumerate(zip(names, subs)):
        c = v['dir'][i]
        if v['key'] == 'M':
            import marks as _mk
            m = _mk.glyph(('flat', 'renov', 'house')[i], 44, v['acc'], v['acc2'])
        elif fam(v) == 'Y':
            cols = ['#DADDE6'] * 3; cols[i] = c
            m = mark_Y(44, cols[0], cols[1], cols[2], f'Знак направления {n}')
        else:
            m = mark(v, 40)
        cells += (f'<div style="background: {v["panel"]}; padding: 22px 24px; display: flex; flex-direction: column; justify-content: space-between">'
                  f'<div style="display: flex; align-items: center; gap: 14px">{m}<div style="display: flex; flex-direction: column; gap: 3px">'
                  f'<span style="font: {v["word_w"]} {round(15 * v["word_k"])}px \'{v["FH"]}\', sans-serif; letter-spacing: {v["word_ls"]}; color: {v["ink"]}">ПЛАТФОРМА</span>'
                  f'<span style="font: 600 22px \'{v["F"]}\', sans-serif; color: {c}">{n}</span></div></div>'
                  f'<span style="font: 400 14px \'{v["F"]}\', sans-serif; color: {v["muted"]}">{s}</span></div>')
    return cells


def logo_board(v):
    F, FH, ink, muted, line, panel, acc = v['F'], v['FH'], v['ink'], v['muted'], v['line'], v['panel'], v['acc']
    dark_bg = '#14161F' if fam(v) == 'Y' else ('#1F1D1B' if fam(v) == 'L' else '#F2F1EE')
    dark_ink = '#FFFFFF' if fam(v) != 'D' else '#14120E'
    why = ''.join(f'<li style="margin: 0 0 8px">{w}</li>' for w in v['why'])
    # app icon
    icon_bg = {'L': acc, 'D': '#2A2D32', 'Y': '#14161F'}[fam(v)]
    icon_mark = {'L': lambda w: mark_L(w, '#FBF9F5'), 'D': lambda w: mark_D(w), 'Y': lambda w: mark_Y(w, *v['dir'])}[fam(v)]
    alt_lock = (lockup(v, 30, '#FBF9F5', 'rgba(255,255,255,.72)', mono='#FBF9F5') if fam(v) == 'L' else
                lockup(v, 30, '#14120E', '#5A4A2A', mono='YELLOWBG') if fam(v) == 'D' else
                lockup(v, 30, '#FFFFFF', '#C9D0FF', mono='#FFFFFF'))
    alt_bg = acc
    if fam(v) == 'D':
        inv = lockup(v, 30, '#14120E', '#5C616B', mono='LIGHTBG')
    else:
        inv = lockup(v, 30, '#FFFFFF', '#A9A39A' if fam(v) == 'L' else '#9A9EAB', on_dark=True)
    h = 1540
    return head(f'{v["title"]} · {v["name"]} — логотип', v, h) + f'''<div style="width: 1440px; height: {h}px; box-sizing: border-box; padding: 48px 56px; background: {v['bg']}; color: {v['text']}; font-family: '{F}', system-ui, sans-serif; display: flex; flex-direction: column; gap: 24px; overflow: hidden">
  <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid {line}; padding-bottom: 16px">
    <div style="font: 500 30px '{F}', sans-serif; letter-spacing: -0.02em">{v['title']} · <span style="color: {acc if fam(v) != 'Y' else ink}">«{v['name']}»</span></div>
    <div style="font: 400 14px '{F}', sans-serif; color: {muted}">[ 01 · логотип ]</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 20px; height: 560px">
    <div style="grid-column: span 7; background: {panel}; padding: 56px 48px; display: flex; flex-direction: column; justify-content: space-between">
      {label(v, 'построение знака')}
      <div style="display: flex; justify-content: center">{construction(v, 360)}</div>
    </div>
    <div style="grid-column: span 5; display: flex; flex-direction: column; gap: 20px">
      <div style="flex: 1; background: {panel}; display: flex; align-items: center; justify-content: center; padding: 24px">{lockup(v, 40, ink, muted)}</div>
      <div style="background: {panel}; padding: 28px; display: flex; flex-direction: column; gap: 14px">
        <div style="font: 400 16px/1.55 '{F}', sans-serif"><b style="font-weight: 600">Идея.</b> {v['idea']}</div>
        <ul style="margin: 0; padding-left: 18px; font: 400 14px/1.45 '{F}', sans-serif; color: {muted}">{why}</ul>
      </div>
    </div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; height: 260px">
    <div style="background: {dark_bg}; display: flex; flex-direction: column; justify-content: space-between; padding: 20px">
      {label(v, 'на тёмном' if fam(v) != 'D' else 'на светлом', '#8D929A')}
      <div style="display: flex; justify-content: center">{inv}</div><span></span>
    </div>
    <div style="background: {alt_bg}; display: flex; flex-direction: column; justify-content: space-between; padding: 20px">
      {label(v, 'на фирменном цвете', dark_ink)}
      <div style="display: flex; justify-content: center">{alt_lock}</div><span></span>
    </div>
    <div style="background: {panel}; display: flex; flex-direction: column; justify-content: space-between; padding: 20px">
      {label(v, 'вертикальная версия')}
      <div style="display: flex; justify-content: center">{lockup(v, 26, ink, muted, vertical=True, mw=64)}</div><span></span>
    </div>
  </div>
  <div style="display: flex; flex-direction: column; gap: 10px">
    {label(v, 'направления платформы — отдельные страницы и разделы приложения')}
    <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; height: 150px">{directions(v)}</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 20px; flex: 1; min-height: 0">
    <div style="grid-column: span 4; background: {panel}; padding: 20px; display: flex; flex-direction: column; justify-content: space-between">
      {label(v, 'иконка приложения')}
      <div style="display: flex; align-items: flex-end; gap: 16px; margin: auto 0">
        <div style="width: 116px; height: 116px; border-radius: 27px; background: {icon_bg}; display: flex; align-items: center; justify-content: center">{icon_mark(60)}</div>
        <div style="width: 58px; height: 58px; border-radius: 14px; background: {icon_bg}; display: flex; align-items: center; justify-content: center">{icon_mark(30)}</div>
      </div>
    </div>
    <div style="grid-column: span 4; background: {panel}; padding: 20px; display: flex; flex-direction: column; justify-content: space-between">
      {label(v, 'малые размеры · 48 / 32 / 16 px')}
      <div style="display: flex; align-items: flex-end; gap: 24px; margin: auto 0">{mark(v, 48)}{mark(v, 32)}{mark(v, 16)}</div>
    </div>
    <div style="grid-column: span 4; background: {panel}; padding: 20px; display: flex; flex-direction: column; justify-content: space-between">
      {label(v, 'одноцветный — печать, гравировка, стекло')}
      <div style="display: flex; align-items: flex-end; gap: 24px; margin: auto 0">{mark(v, 56, mono=ink)}{mark(v, 56, mono=muted)}</div>
    </div>
  </div>
</div>
''' + tail(h)


# ---------- style board ----------
def supergraphic(v, W=820, H=500):
    k = fam(v); acc = v['acc']; F = v['F']; FH = v['FH']
    if v['key'] == 'M':
        q = "'"
        cells = [(0, 0, 'p0'), (1, 0, 'acc'), (2, 0, 'p1'), (0, 1, 'mod'), (2, 1, 'p2'), (0, 2, 'p3'), (2, 2, 'mod'), (1, 1, 'ghost'), (1, 2, 'ghost')]
        ph = [IMG['kitchen'], IMG['detail'], IMG['stone'], IMG['bedroom']]
        mz = mosaic(v, 3 * 132 + 2 * 14, 3 * 132 + 2 * 14, cells, ph, s=132, g=14, r=24)
        return (f'<div style="width: 100%; height: 100%; background: {v["sand"]}; position: relative; overflow: hidden; display: flex; align-items: center; gap: 44px; padding: 0 44px; box-sizing: border-box">'
                f'<div style="flex: none">{mz}</div>'
                f'<div style="display: flex; flex-direction: column; gap: 20px">'
                f'<span style="font: 400 13px {q}{F}{q}, sans-serif; color: {v["muted"]}">[ мозаика из модулей — фото внутри знака ]</span>'
                f'<div style="font: 800 40px/1.05 {q}{FH}{q}, sans-serif; letter-spacing: -0.02em; color: {v["ink"]}">Собираем ваш дом<br>по модулям</div>'
                f'<span style="font: 400 16px/1.5 {q}{F}{q}, sans-serif; color: {v["muted"]}">Квартира, ремонт и каменный дом — из одних и тех же надёжных шагов.</span>'
                f'<span style="align-self: flex-start; padding: 14px 22px; background: {acc}; color: #FFFFFF; font: 600 16px {q}{F}{q}, sans-serif; border-radius: 14px">Собрать свой</span></div></div>')
    if v['key'] in ('K', 'S'):
        import marks as _mk
        q = "'"
        hgt = 600; sc = hgt / 40; wd = 36 * sc
        if v['key'] == 'K':
            _mk.SHAPE = 'masonry'
            shape = f'<path d="{_mk.arch_d("masonry")}" fill="#FBF8F3" fill-opacity="0.96"/>'
            hole = 'M10 40 V20 A8 8 0 0 1 26 20 V40 Z'
            photo, head, sub, cta = IMG['kitchen'], 'Строим так,<br>чтобы стояло век.', 'Кладка, ремонт и ключи — в одном договоре. Квартиры, ремонт и каменные дома в Екатеринбурге.', 'Подобрать квартиру'
            field, ink_h, ink_s, btn_bg, btn_ink = acc, '#FFFFFF', 'rgba(255,255,255,.86)', '#FBF8F3', v['ink']
        else:
            shape = ('<path d="M0 0 H36 V40 H26 V20 A8 8 0 0 0 10 20 V40 H0 Z" fill="#24493A"/>'
                     '<path d="M11.6 37 V20 A6.4 6.4 0 0 1 24.4 20 V37 H23.2 V20 A5.2 5.2 0 0 0 12.8 20 V37 Z" fill="#F1EEE6"/>'
                     '<path d="M7 37.6 H29 V40 H7 Z" fill="#F1EEE6"/>')
            hole = 'M12.8 37 V20 A5.2 5.2 0 0 1 23.2 20 V37 Z'
            photo, head, sub, cta = IMG['living2'], 'Ваш дом<br>уже ждёт.', 'Порог переступили — дальше наша забота. Квартира, ремонт и свой дом за городом.', 'Выбрать дом'
            field, ink_h, ink_s, btn_bg, btn_ink = acc, '#FFFFFF', 'rgba(255,255,255,.86)', '#F1EEE6', v['ink']
        cid = 'sg' + v['key']
        svg = (f'<svg width="{wd:.0f}" height="{hgt}" viewBox="0 0 36 40" style="position: absolute; right: -170px; top: -40px" role="img" aria-label="Знак как рамка для фото">'
               f'<defs><clipPath id="{cid}"><path d="{hole}"/></clipPath></defs>'
               f'<image href="{photo}" x="6" y="10" width="24" height="30" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>{shape}</svg>')
        return (f'<div style="width: 100%; height: 100%; background: {field}; position: relative; overflow: hidden">{svg}'
                f'<div style="position: absolute; left: 48px; top: 52px; bottom: 48px; width: 320px; display: flex; flex-direction: column; justify-content: space-between; color: {ink_h}">'
                f'<span style="font: 400 13px {q}{F}{q}, sans-serif; color: {ink_s}">[ знак — рамка для фото ]</span>'
                f'<div style="font: {v["word_w"]} 42px/1.06 {q}{FH}{q}, sans-serif; letter-spacing: -0.02em">{head}</div>'
                f'<div style="display: flex; flex-direction: column; gap: 16px"><span style="font: 400 16px/1.5 {q}{F}{q}, sans-serif; color: {ink_s}">{sub}</span>'
                f'<span style="align-self: flex-start; padding: 14px 22px; background: {btn_bg}; color: {btn_ink}; font: 600 16px {q}{F}{q}, sans-serif">{cta}</span></div></div></div>')
    if k == 'L':
        # arch-window photo on terracotta field
        aw, ah = 330, 420
        r = aw / 2
        path = f'M0 {ah} V{r} A{r} {r} 0 0 1 {aw} {r} V{ah} Z'
        return (f'<div style="width: 100%; height: 100%; background: {acc}; position: relative; overflow: hidden">'
                f'<svg width="{aw}" height="{ah}" viewBox="0 0 {aw} {ah}" style="position: absolute; left: 56px; bottom: 0" role="img" aria-label="Квартира в арке">'
                f'<defs><clipPath id="archL"><path d="{path}"/></clipPath></defs>'
                f'<image href="{IMG["kitchen"]}" x="-120" y="0" width="{aw + 240}" height="{ah}" preserveAspectRatio="xMidYMid slice" clip-path="url(#archL)"/></svg>'
                f'<div style="position: absolute; left: 440px; right: 48px; top: 56px; bottom: 48px; display: flex; flex-direction: column; justify-content: space-between; color: #FBF9F5">'
                f'<span style="font: 400 13px \'{F}\', sans-serif; color: rgba(255,255,255,.72)">[ арка — фирменная рамка для фото ]</span>'
                f'<div style="font: 600 46px/1.05 \'{F}\', sans-serif; letter-spacing: -0.02em">Входите.<br>Дальше мы сами.</div>'
                f'<div style="display: flex; flex-direction: column; gap: 14px"><span style="font: 400 17px/1.5 \'{F}\', sans-serif; color: rgba(255,255,255,.86)">Квартира, ремонт и каменный дом — одна компания, один договор, один менеджер.</span>'
                f'<span style="align-self: flex-start; padding: 14px 22px; background: #FBF9F5; color: #1F1D1B; font: 600 16px \'{F}\', sans-serif">Подобрать квартиру</span></div></div></div>')
    if k == 'D':
        Wm = 470
        return (f'<div style="width: 100%; height: 100%; background: #0B0C0E; position: relative; overflow: hidden">'
                f'<svg width="{Wm}" height="{Wm}" viewBox="0 0 36 36" style="position: absolute; right: -24px; top: 16px" role="img" aria-label="Портал с фото дома">'
                f'<defs><clipPath id="frontD"><path d="M0 8 H28 V36 H20 V16 H8 V36 H0 Z"/></clipPath></defs>'
                f'<polygon points="0,8 8,0 36,0 28,8" fill="#3A3E45"/><polygon points="28,8 36,0 36,28 28,36" fill="#24272C"/>'
                f'<polygon points="8,16 16,16 16,28 8,36" fill="{acc}"/>'
                f'<image href="{IMG["building"]}" x="-4" y="6" width="34" height="32" preserveAspectRatio="xMidYMid slice" clip-path="url(#frontD)"/></svg>'
                f'<div style="position: absolute; left: 48px; top: 56px; bottom: 48px; width: 300px; display: flex; flex-direction: column; justify-content: space-between; color: #F2F1EE">'
                f'<span style="font: 400 13px \'{F}\', sans-serif; color: #8D929A">[ портал — фото внутри знака ]</span>'
                f'<div style="font: 600 40px/1.08 \'{F}\', sans-serif; letter-spacing: -0.02em">Дом, в котором<br>уже горит свет</div>'
                f'<div style="display: flex; flex-direction: column; gap: 14px"><span style="font: 400 17px/1.5 \'{F}\', sans-serif; color: #A7ACB4">Квартиры, ремонт и каменные дома в Екатеринбурге.</span>'
                f'<span style="align-self: flex-start; padding: 14px 22px; background: {acc}; color: #14120E; font: 600 16px \'{F}\', sans-serif">Выбрать квартиру</span></div></div></div>')
    # Y: three parts filled with three photos
    s = (H - 60) / 36; Wm = 40 * s
    parts = (('0,3 10,13 10,36 0,36', IMG['kitchen'], v['dir'][0], 'Квартиры', '0', '3'),
             ('0,0 40,0 30,10 10,10', IMG['detail'], v['dir'][1], 'Ремонт', '0', '0'),
             ('40,3 40,36 30,36 30,13', IMG['gable'], v['dir'][2], 'Дома', '30', '3'))
    defs = ''.join(f'<clipPath id="pY{i}"><polygon points="{p[0]}"/></clipPath>' for i, p in enumerate(parts))
    imgs = ''
    for i, p in enumerate(parts):
        if i == 1:
            imgs += f'<image href="{p[1]}" x="0" y="0" width="40" height="10" preserveAspectRatio="xMidYMid slice" clip-path="url(#pY{i})"/>'
        else:
            imgs += f'<image href="{p[1]}" x="{p[4]}" y="3" width="10" height="33" preserveAspectRatio="xMidYMid slice" clip-path="url(#pY{i})"/>'
        imgs += f'<polygon points="{p[0]}" fill="{p[2]}" opacity="0.28"/>'
    tags = ''.join(f'<span style="padding: 7px 12px; background: {c}; color: #FFFFFF; font: 600 14px \'{F}\', sans-serif">{n}</span>' for c, n in zip(v['dir'], ('Квартиры', 'Ремонт', 'Дома')))
    return (f'<div style="width: 100%; height: 100%; background: #F3F4F8; position: relative; overflow: hidden">'
            f'<svg width="{Wm}" height="{H - 60}" viewBox="0 0 40 36" style="position: absolute; left: 40px; top: 30px" role="img" aria-label="Знак из трёх фото">'
            f'<defs>{defs}</defs>{imgs}</svg>'
            f'<div style="position: absolute; left: {Wm + 80}px; right: 40px; top: 48px; bottom: 40px; display: flex; flex-direction: column; justify-content: space-between">'
            f'<span style="font: 400 13px \'{F}\', sans-serif; color: #6B6F7D">[ три части знака — три направления ]</span>'
            f'<div style="font: 600 34px/1.1 \'{FH}\', sans-serif; letter-spacing: -0.01em; color: #14161F">Всё для дома — на одной платформе</div>'
            f'<div style="display: flex; gap: 8px; flex-wrap: wrap">{tags}</div></div></div>')


def phone(v):
    F, FH, ink, muted, acc = v['F'], v['FH'], v['ink'], v['muted'], v['acc']
    k = fam(v)
    scr = {'L': '#FBF9F5', 'D': '#0E0F11', 'Y': '#FFFFFF'}[k]
    tile = {'L': '#F2EEE7', 'D': '#1B1D21', 'Y': '#F3F4F8'}[k]
    txt = {'L': '#1F1D1B', 'D': '#F2F1EE', 'Y': '#14161F'}[k]
    names = (('Квартиры', '[N] вариантов', IMG['bedroom']), ('Ремонт', 'смета за 2 мин', IMG['bath']), ('Дома', '[N] проектов', IMG['stone']))
    tiles = ''
    for i, (n, s, im) in enumerate(names):
        c = v['dir'][i]
        tiles += (f'<div style="display: flex; gap: 10px; align-items: center; padding: 8px; background: {tile}">'
                  f'<div style="width: 64px; height: 52px; flex: none; overflow: hidden; {"border-radius: 26px 26px 0 0;" if k == "L" else ""}"><img src="{im}" alt="{n}" style="width: 100%; height: 100%; object-fit: cover; display: block"></div>'
                  f'<div style="display: flex; flex-direction: column; gap: 2px; flex: 1"><span style="font: 600 14px \'{F}\', sans-serif; color: {c if k == "Y" else txt}">{n}</span>'
                  f'<span style="font: 400 11px \'{F}\', sans-serif; color: {muted}">{s}</span></div><span style="color: {muted}; font: 400 14px \'{F}\', sans-serif">→</span></div>')
    small = mark_L(18, acc) if k == 'L' else mark_D(20) if k == 'D' else mark_Y(20, *v['dir'])
    return f'''<div style="width: 300px; height: 620px; border-radius: 46px; background: #111111; border: 2px solid #3A3D43; padding: 11px; box-sizing: border-box; box-shadow: 0 30px 60px rgba(0,0,0,0.25)">
  <div style="width: 100%; height: 100%; border-radius: 36px; background: {scr}; overflow: hidden; display: flex; flex-direction: column; color: {txt}">
    <div style="padding: 22px 16px 12px; display: flex; justify-content: space-between; align-items: center">
      <div style="display: flex; align-items: center; gap: 8px">{small}<span style="font: {v['word_w']} {round(13 * v['word_k'])}px '{FH}', sans-serif; letter-spacing: {v['word_ls']}">ПЛАТФОРМА</span></div>
      <span style="font: 400 12px '{F}', sans-serif; color: {muted}">ЕКБ</span>
    </div>
    <div style="padding: 0 16px; font: 600 22px/1.12 '{FH if k == 'Y' else F}', sans-serif; letter-spacing: -0.01em">{'Что делаем<br>для вас?' if k != 'Y' else 'Что делаем<br>для вас?'}</div>
    <div style="padding: 14px 16px 0; display: flex; flex-direction: column; gap: 8px">{tiles}</div>
    <div style="margin: 12px 16px 0; padding: 14px; background: {acc}; color: {v['acc_ink']}; display: flex; flex-direction: column; gap: 4px">
      <span style="font: 400 12px '{F}', sans-serif; opacity: 0.85">Мой объект · каменный дом</span>
      <span style="font: 600 15px '{F}', sans-serif">Этап 3 из 7 · кладка стен</span>
      <div style="display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 3px; margin-top: 6px">{''.join(f'<div style="height: 4px; background: {v["acc_ink"]}; opacity: {1 if j < 3 else 0.3}"></div>' for j in range(7))}</div>
    </div>
    <div style="margin: 8px 16px 0; padding: 12px 14px; border: 1px solid {v['line']}; display: flex; justify-content: space-between; align-items: center"><div style="display: flex; flex-direction: column; gap: 2px"><span style="font: 600 13px '{F}', sans-serif">Ипотечный лимит</span><span style="font: 400 11px '{F}', sans-serif; color: {muted}">узнать за 1 минуту, без визита в банк</span></div><span style="color: {muted}">→</span></div>
    <div style="margin-top: auto; border-top: 1px solid {v['line']}; padding: 12px 16px 18px; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); font: 500 11px '{F}', sans-serif; color: {muted}; text-align: center"><span style="color: {txt}">Главная</span><span>Поиск</span><span>Объект</span><span>Профиль</span></div>
  </div>
</div>'''


def banner(v):
    k, F = fam(v), v['F']
    return (f'<div style="position: relative; width: 100%; height: 100%; overflow: hidden">'
            f'<img src="{IMG["life_" + v["key"] + "_fence"]}" alt="Баннер на ограждении стройки" style="width: 100%; height: 100%; object-fit: cover; display: block">'
            f'<span style="position: absolute; left: 16px; top: 16px; padding: 6px 10px; background: #FFFFFF; color: #1F1D1B; font: 400 12px {F!r}, sans-serif">[ баннер на ограждении стройки ]</span></div>')


def cards(v):
    F, FH, acc = v['F'], v['FH'], v['acc']
    k = fam(v)
    front_bg = {'L': '#FBF9F5', 'D': '#F2F1EE', 'Y': '#FFFFFF'}[k]
    back_bg = {'L': acc, 'D': '#17191C', 'Y': '#14161F'}[k]
    back = (lockup(v, 22, '#FBF9F5', 'rgba(255,255,255,.72)', mono='#FBF9F5', mw=40) if k == 'L' else lockup(v, 22, '#F2F1EE', '#8D929A', mw=40))
    corner = mark_L(26, acc) if k == 'L' else mark_D(28) if k == 'D' else mark_Y(30, *v['dir'])
    return f'''<div style="position: relative; width: 100%; height: 100%">
  <div style="position: absolute; left: 10px; top: 4px; width: 340px; height: 196px; background: {front_bg}; transform: rotate(-5deg); box-shadow: 0 18px 40px rgba(0,0,0,0.22); padding: 24px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; color: #1F1D1B">
    <div style="display: flex; flex-direction: column; gap: 2px"><span style="font: 600 19px '{F}', sans-serif">[ИМЯ ФАМИЛИЯ]</span><span style="font: 400 13px '{F}', sans-serif; color: #7A7368">Менеджер проекта · Дома</span></div>
    <div style="display: flex; flex-direction: column; gap: 2px; font: 400 13px '{F}', sans-serif"><span>+7 [ТЕЛЕФОН]</span><span>[САЙТ] · Екатеринбург</span></div>
    <div style="position: absolute; right: 22px; top: 22px">{corner}</div>
  </div>
  <div style="position: absolute; left: 230px; top: 84px; width: 340px; height: 196px; background: {back_bg}; transform: rotate(4deg); box-shadow: 0 18px 40px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center">{back}</div>
  <span style="position: absolute; left: 10px; bottom: 0; font: 400 12px '{F}', sans-serif; color: {v['muted']}">[ визитки ]</span>
</div>'''


def posts(v):
    F, FH, acc = v['F'], v['FH'], v['acc']
    k = fam(v)
    if k == 'L':
        p1 = (f'<div style="width: 250px; height: 250px; background: {v["bg"]}; position: relative; overflow: hidden">'
              f'<div style="position: absolute; left: 24px; right: 24px; top: 24px; bottom: 70px; border-radius: 101px 101px 0 0; overflow: hidden"><img src="{IMG["after"]}" alt="Комната после ремонта" style="width: 100%; height: 100%; object-fit: cover; display: block"></div>'
              f'<div style="position: absolute; left: 24px; right: 24px; bottom: 18px; display: flex; justify-content: space-between; align-items: center"><span style="font: 600 15px \'{F}\', sans-serif; color: #1F1D1B">Ремонт под ключ</span>{mark_L(18, acc)}</div></div>')
        p2 = f'<div style="width: 250px; height: 250px; background: {acc}; display: flex; align-items: center; justify-content: center">{mark_L(110, "#FBF9F5")}</div>'
    elif k == 'D':
        p1 = (f'<div style="width: 250px; height: 250px; position: relative; overflow: hidden"><img src="{IMG["stone"]}" alt="Каменный фасад" style="width: 100%; height: 100%; object-fit: cover; display: block">'
              f'<div style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(14,15,17,0) 30%, rgba(14,15,17,0.9) 100%)"></div>'
              f'<div style="position: absolute; left: 18px; right: 18px; bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end"><span style="font: 600 17px/1.15 \'{F}\', sans-serif; color: #F2F1EE">Каменный дом<br>за 7 этапов</span><span style="padding: 6px 10px; background: {acc}; color: #14120E; font: 600 12px \'{F}\', sans-serif">Смотреть</span></div></div>')
        p2 = f'<div style="width: 250px; height: 250px; background: #17191C; display: flex; align-items: center; justify-content: center">{mark_D(120)}</div>'
    else:
        p1 = (f'<div style="width: 250px; height: 250px; background: {v["dir"][1]}; position: relative; overflow: hidden; padding: 20px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between">'
              f'<span style="font: 600 22px/1.1 \'{FH}\', sans-serif; color: #FFFFFF">Смета ремонта за 2 минуты</span>'
              f'<div style="height: 120px; overflow: hidden"><img src="{IMG["bath"]}" alt="Ванная после ремонта" style="width: 100%; height: 100%; object-fit: cover; display: block"></div></div>')
        p2 = f'<div style="width: 250px; height: 250px; background: #FFFFFF; border: 1px solid #E3E5EC; box-sizing: border-box; display: flex; align-items: center; justify-content: center">{mark_Y(130, *v["dir"])}</div>'
    return (f'<div style="display: flex; flex-direction: column; gap: 10px"><div style="display: flex; gap: 20px">{p1}{p2}</div>'
            f'<span style="font: 400 12px \'{F}\', sans-serif; color: {v["muted"]}">[ пост в соцсетях · аватар ]</span></div>')


def style_board(v):
    F, FH, ink, muted, line, panel, acc = v['F'], v['FH'], v['ink'], v['muted'], v['line'], v['panel'], v['acc']
    pal = ''
    rgb = lambda h: ' · '.join(str(int(h[i:i + 2], 16)) for i in (1, 3, 5))
    for n, c, f in v['palette']:
        light = c in ('#FFFFFF', '#F7F4EE', '#E4EFEC', '#F6B93B', '#F2EEE7', '#F4EFE8', '#E4D3BF', '#F1EEE6', '#D8CDB4', '#FBF9F5', '#D9CBB5', '#F2F1EE', '#A7ACB4', '#FFB547', '#F3F4F8')
        border = f'border: 1px solid {line};' if c in (v['bg'], '#FFFFFF') else ''
        pal += (f'<div style="flex: {f}; background: {c}; {border} padding: 10px; display: flex; flex-direction: column; justify-content: flex-end; '
                f'font: 400 12px/1.4 \'{F}\', sans-serif; color: {"#1F1D1B" if light else "#FFFFFF"}">{n}<br>{c}{('<br>' + rgb(c)) if v['key'] in ('K', 'S', 'M') else ''}</div>')
    h = 1640
    return head(f'{v["title"]} · {v["name"]} — стиль и носители', v, h) + f'''<div style="width: 1440px; height: {h}px; box-sizing: border-box; padding: 48px 56px; background: {v['bg']}; color: {v['text']}; font-family: '{F}', system-ui, sans-serif; display: flex; flex-direction: column; gap: 24px; overflow: hidden">
  <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid {line}; padding-bottom: 16px">
    <div style="font: 500 30px '{F}', sans-serif; letter-spacing: -0.02em">{v['title']} · <span style="color: {acc if fam(v) != 'Y' else ink}">«{v['name']}»</span></div>
    <div style="font: 400 14px '{F}', sans-serif; color: {muted}">[ 02 · стиль и носители ]</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 20px; height: 500px">
    <div style="grid-column: span 8">{supergraphic(v)}</div>
    <div style="grid-column: span 4; display: flex; flex-direction: column; gap: 20px">
      <div style="background: {panel}; padding: 22px; display: flex; flex-direction: column; gap: 12px; flex: 1">
        {label(v, 'палитра · доли')}
        <div style="display: flex; flex: 1; min-height: 120px">{pal}</div>
      </div>
      <div style="background: {panel}; padding: 22px; display: flex; flex-direction: column; gap: 10px">
        {label(v, 'шрифт')}
        <div style="display: flex; align-items: flex-end; gap: 18px"><span style="font: 600 88px/0.85 '{FH}', sans-serif; letter-spacing: -0.03em">Аа</span>
        <span style="font: 400 13px/1.45 '{F}', sans-serif; color: {muted}">{v['type_desc']}</span></div>
        <span style="font: 400 14px/1.45 '{F}', sans-serif; color: {muted}">{v['mood']}</span>
      </div>
    </div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 28px; height: 640px">
    <div style="grid-column: span 8">{banner(v)}</div>
    <div style="grid-column: span 4; display: flex; align-items: center; justify-content: center">{phone(v)}</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 28px; flex: 1; min-height: 0">
    <div style="grid-column: span 6">{cards(v)}</div>
    <div style="grid-column: span 6; display: flex; justify-content: flex-end; align-items: flex-start">{posts(v)}</div>
  </div>
</div>
''' + tail(h)


if __name__ == '__main__':
    for k, v in V.items():
        fam(v)
        open(OUT + f'Logo{k}.dc.html', 'w', encoding='utf8').write(logo_board(v))
        open(OUT + f'Style{k}.dc.html', 'w', encoding='utf8').write(style_board(v))
    print('ok')
