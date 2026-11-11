"""Three identity variants (light / dark / bright) for ПЛАТФОРМА НЕДВИЖИМОСТИ.
Each variant: logo board (1440x1540) + style & mockups board (1440x1640)."""
import sys
sys.path.insert(0, 'C:/Users/MSI/AppData/Local/Temp/claude/10d39200edc2b63f/973356bb-8c70-4e3b-b6ae-d636a7404011/scratchpad/v3')
from marks import mark_L, mark_D, mark_Y

OUT = 'C:/Users/MSI/AppData/Local/Temp/claude/10d39200edc2b63f/973356bb-8c70-4e3b-b6ae-d636a7404011/scratchpad/mood/project/'
B = '/_blob/'
IMG = dict(
    build=B + '0344505071bafebecba4899d1050d932', brick=B + 'ca00be2acd9690fb9dea9110aaaec783',
    stone=B + '597b77d5921d32365d4391f69448844f', gable=B + 'b471f2a087272c564fa40cb48156b5a1',
    hflat=B + '241aa9c6494b7c64ac1bea49f925807d', kitchen=B + '6eb6b66044bc72cd1c691f54afa97fd2',
    bedroom=B + 'a51f99a2ebaa3290cc815a60538e1744', building=B + '1947ff52209ccab806cd2be3be49c501',
    bath=B + 'e05ef6fc38a92410bfb373f11b4be3cd', after=B + 'ab22bbc0ab515db845d3dee45c8b5d04',
    detail=B + '3472f23568c92d74ff24b6057454790b', process=B + 'de9f3f7fe15a4720d9b574a1e479b7c1')

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
}


def mark(v, w, mono=None, on_dark=False):
    k = v['key']
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
             f'<span style="display: flex; justify-content: space-between; font: 500 {max(9, round(size * 0.24))}px/1 \'{v["F"]}\', sans-serif; color: {sub}">{sub_letters}</span></div>')
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
    k = v['key']; g = v['muted']; ink = v['ink']
    if k == 'L':
        s = H / 40; W = 36 * s
        lines = ''.join(f'<line x1="{x * s}" y1="-30" x2="{x * s}" y2="{H + 30}" stroke="{g}" stroke-width="1" stroke-dasharray="4 6" opacity="0.6"/>' for x in (0, 10, 18, 26, 36))
        lines += ''.join(f'<line x1="-30" y1="{y * s}" x2="{W + 30}" y2="{y * s}" stroke="{g}" stroke-width="1" stroke-dasharray="4 6" opacity="0.6"/>' for y in (0, 12, 20, 40))
        lines += f'<circle cx="{18 * s}" cy="{20 * s}" r="{8 * s}" fill="none" stroke="{ink}" stroke-width="1.2" opacity="0.55"/>'
        lines += f'<circle cx="{18 * s}" cy="{20 * s}" r="3" fill="{ink}"/>'
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
        if v['key'] == 'Y':
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
    dark_bg = '#14161F' if v['key'] == 'Y' else ('#1F1D1B' if v['key'] == 'L' else '#F2F1EE')
    dark_ink = '#FFFFFF' if v['key'] != 'D' else '#14120E'
    why = ''.join(f'<li style="margin: 0 0 8px">{w}</li>' for w in v['why'])
    # app icon
    icon_bg = {'L': acc, 'D': '#2A2D32', 'Y': '#14161F'}[v['key']]
    icon_mark = {'L': lambda w: mark_L(w, '#FBF9F5'), 'D': lambda w: mark_D(w), 'Y': lambda w: mark_Y(w, *v['dir'])}[v['key']]
    alt_lock = (lockup(v, 30, '#FBF9F5', '#E9C9B8', mono='#FBF9F5') if v['key'] == 'L' else
                lockup(v, 30, '#14120E', '#5A4A2A', mono='YELLOWBG') if v['key'] == 'D' else
                lockup(v, 30, '#FFFFFF', '#C9D0FF', mono='#FFFFFF'))
    alt_bg = acc
    if v['key'] == 'D':
        inv = lockup(v, 30, '#14120E', '#5C616B', mono='LIGHTBG')
    else:
        inv = lockup(v, 30, '#FFFFFF', '#A9A39A' if v['key'] == 'L' else '#9A9EAB', on_dark=True)
    h = 1540
    return head(f'{v["title"]} · {v["name"]} — логотип', v, h) + f'''<div style="width: 1440px; height: {h}px; box-sizing: border-box; padding: 48px 56px; background: {v['bg']}; color: {v['text']}; font-family: '{F}', system-ui, sans-serif; display: flex; flex-direction: column; gap: 24px; overflow: hidden">
  <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid {line}; padding-bottom: 16px">
    <div style="font: 500 30px '{F}', sans-serif; letter-spacing: -0.02em">{v['title']} · <span style="color: {acc if v['key'] != 'Y' else ink}">«{v['name']}»</span></div>
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
      {label(v, 'на тёмном' if v['key'] != 'D' else 'на светлом', '#8D929A')}
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
      <div style="display: flex; align-items: flex-end; gap: 16px">
        <div style="width: 116px; height: 116px; border-radius: 27px; background: {icon_bg}; display: flex; align-items: center; justify-content: center">{icon_mark(60)}</div>
        <div style="width: 58px; height: 58px; border-radius: 14px; background: {icon_bg}; display: flex; align-items: center; justify-content: center">{icon_mark(30)}</div>
      </div>
    </div>
    <div style="grid-column: span 4; background: {panel}; padding: 20px; display: flex; flex-direction: column; justify-content: space-between">
      {label(v, 'малые размеры · 48 / 32 / 16 px')}
      <div style="display: flex; align-items: flex-end; gap: 24px">{mark(v, 48)}{mark(v, 32)}{mark(v, 16)}</div>
    </div>
    <div style="grid-column: span 4; background: {panel}; padding: 20px; display: flex; flex-direction: column; justify-content: space-between">
      {label(v, 'одноцветный — печать, гравировка, стекло')}
      <div style="display: flex; align-items: flex-end; gap: 24px">{mark(v, 56, mono=ink)}{mark(v, 56, mono=muted)}</div>
    </div>
  </div>
</div>
''' + tail(h)


# ---------- style board ----------
def supergraphic(v, W=820, H=500):
    k = v['key']; acc = v['acc']; F = v['F']; FH = v['FH']
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
                f'<span style="font: 400 13px \'{F}\', sans-serif; color: #F1D3C3">[ арка — фирменная рамка для фото ]</span>'
                f'<div style="font: 600 46px/1.05 \'{F}\', sans-serif; letter-spacing: -0.02em">Входите.<br>Дальше мы сами.</div>'
                f'<div style="display: flex; flex-direction: column; gap: 14px"><span style="font: 400 17px/1.5 \'{F}\', sans-serif; color: #F6E2D7">Квартира, ремонт и каменный дом — одна компания, один договор, один менеджер.</span>'
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
    k = v['key']
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
    F, FH, acc = v['F'], v['FH'], v['acc']
    k = v['key']
    if k == 'L':
        pbg, pink, psub = '#FBF9F5', '#1F1D1B', '#7A7368'
    elif k == 'D':
        pbg, pink, psub = '#0E0F11', '#F2F1EE', '#8D929A'
    else:
        pbg, pink, psub = '#FFFFFF', '#14161F', '#6B6F7D'
    lk = lockup(v, 24, pink, psub, mw=44)
    stripe = ''
    if k == 'Y':
        stripe = '<div style="display: flex; height: 8px">' + ''.join(f'<div style="flex: 1; background: {c}"></div>' for c in v['dir']) + '</div>'
    return (f'<div style="position: relative; width: 100%; height: 100%; overflow: hidden">'
            f'<img src="{IMG["build"]}" alt="Стройплощадка кирпичного дома" style="width: 100%; height: 100%; object-fit: cover; display: block">'
            f'<div style="position: absolute; left: 5%; right: 5%; bottom: 8%; background: {pbg}; box-shadow: 0 12px 30px rgba(0,0,0,0.35)">{stripe}'
            f'<div style="height: 128px; display: flex; align-items: center; justify-content: space-between; padding: 0 30px">{lk}'
            f'<div style="display: flex; align-items: center; gap: 20px"><span style="font: 400 15px/1.35 \'{F}\', sans-serif; color: {psub}; text-align: right">Строим каменный дом<br>этап 3 из 7</span>'
            f'<span style="padding: 14px 20px; background: {acc}; color: {v["acc_ink"]}; font: 600 16px \'{F}\', sans-serif; white-space: nowrap">Хочу такой дом</span></div></div></div>'
            f'<span style="position: absolute; left: 16px; top: 16px; padding: 6px 10px; background: #FFFFFF; color: #1F1D1B; font: 400 12px \'{F}\', sans-serif">[ баннер на ограждении стройки ]</span></div>')


def cards(v):
    F, FH, acc = v['F'], v['FH'], v['acc']
    k = v['key']
    front_bg = {'L': '#FBF9F5', 'D': '#F2F1EE', 'Y': '#FFFFFF'}[k]
    back_bg = {'L': acc, 'D': '#17191C', 'Y': '#14161F'}[k]
    back = (lockup(v, 22, '#FBF9F5', '#F1D3C3', mono='#FBF9F5', mw=40) if k == 'L' else lockup(v, 22, '#F2F1EE', '#8D929A', mw=40))
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
    k = v['key']
    if k == 'L':
        p1 = (f'<div style="width: 250px; height: 250px; background: #F2EEE7; position: relative; overflow: hidden">'
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
    for n, c, f in v['palette']:
        light = c in ('#FFFFFF', '#F2EEE7', '#FBF9F5', '#D9CBB5', '#F2F1EE', '#A7ACB4', '#FFB547', '#F3F4F8')
        border = f'border: 1px solid {line};' if c in (v['bg'], '#FFFFFF') else ''
        pal += (f'<div style="flex: {f}; background: {c}; {border} padding: 10px; display: flex; flex-direction: column; justify-content: flex-end; '
                f'font: 400 12px/1.4 \'{F}\', sans-serif; color: {"#1F1D1B" if light else "#FFFFFF"}">{n}<br>{c}</div>')
    h = 1640
    return head(f'{v["title"]} · {v["name"]} — стиль и носители', v, h) + f'''<div style="width: 1440px; height: {h}px; box-sizing: border-box; padding: 48px 56px; background: {v['bg']}; color: {v['text']}; font-family: '{F}', system-ui, sans-serif; display: flex; flex-direction: column; gap: 24px; overflow: hidden">
  <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid {line}; padding-bottom: 16px">
    <div style="font: 500 30px '{F}', sans-serif; letter-spacing: -0.02em">{v['title']} · <span style="color: {acc if v['key'] != 'Y' else ink}">«{v['name']}»</span></div>
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
        open(OUT + f'Logo{k}.dc.html', 'w', encoding='utf8').write(logo_board(v))
        open(OUT + f'Style{k}.dc.html', 'w', encoding='utf8').write(style_board(v))
    print('ok')
