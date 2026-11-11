"""Board 05 — brand in real life: logo applied to generated product/facade photos."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marks import mark_L, mark_D, mark_Y
from gen_v3 import V, IMG, OUT, head, tail, label, lockup

HERE = os.path.dirname(os.path.abspath(__file__))
IMG.update({k: '/_blob/' + v for k, v in json.load(open(HERE + '/blobs2.json', encoding='utf8')).items()})
IMG.update({k: '/_blob/' + v for k, v in json.load(open(HERE + '/blobs3.json', encoding='utf8')).items()})

VOICE = {
    'L': ('Спокойно и по-домашнему', ['Входите. Дальше мы сами.', 'Ремонт к переезду — в одном договоре.', 'Свой каменный дом без сюрпризов в смете.']),
    'D': ('Уверенно и коротко', ['Дом, в котором уже горит свет.', 'Стройка онлайн, 24/7.', 'Цена в договоре не меняется.']),
    'Y': ('Бодро и понятно', ['Всё для дома — на одной платформе.', 'Квартира. Ремонт. Дом. В одном приложении.', 'Смета ремонта за 2 минуты.']),
}


def colored_mark(v, w, on='white'):
    k = v['key']
    if k == 'L':
        return mark_L(w, v['acc'])
    if k == 'D':
        return mark_D(w, front='#14120E', top='#7A7F87', side='#3A3D43', glow='#FFB547') if on == 'white' else mark_D(w)
    return mark_Y(w, *v['dir'])


def photo(src, alt, inner=''):
    return (f'<div style="position: relative; width: 100%; aspect-ratio: 1344 / 768; overflow: hidden">'
            f'<img src="{src}" alt="{alt}" style="position: absolute; inset: 0; width: 100%; height: 100%; display: block">{inner}</div>')


def tag(t, F):
    return f'<span style="position: absolute; left: 10px; top: 10px; padding: 5px 9px; background: #FFFFFF; color: #1F1D1B; font: 400 12px \'{F}\', sans-serif">[ {t} ]</span>'


def sign(v):
    k = v['key']; F = v['F']
    bg = {'L': '#FBF9F5', 'D': '#0B0C0E', 'Y': '#FFFFFF'}[k]
    ink = {'L': '#1F1D1B', 'D': '#F2F1EE', 'Y': '#14161F'}[k]
    sub = {'L': '#7A7368', 'D': '#8D929A', 'Y': '#6B6F7D'}[k]
    glow = 'box-shadow: 0 0 34px rgba(255,214,150,0.55), inset 0 0 18px rgba(0,0,0,0.12);' if k != 'D' else 'box-shadow: 0 0 40px rgba(255,181,71,0.45);'
    stripe = ''
    if k == 'Y':
        stripe = '<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 6px; display: flex">' + ''.join(f'<div style="flex: 1; background: {c}"></div>' for c in v['dir']) + '</div>'
    if k == 'L':
        stripe = f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 6px; background: {v["acc"]}"></div>'
    panel = (f'<div style="position: absolute; left: 30%; top: 39%; width: 41.6%; height: 33.5%; background: {bg}; {glow} display: flex; align-items: center; justify-content: center">'
             f'{lockup(v, 26, ink, sub, mw=46)}{stripe}</div>')
    return photo(IMG['mk_facade'], 'Фасад офиса продаж с вывеской', panel + tag('вывеска на фасаде офиса', F))


def billboard(v):
    k = v['key']; F, FH, acc = v['F'], v['FH'], v['acc']
    if k == 'L':
        vis = f'<div style="width: 92px; height: 112px; border-radius: 46px 46px 0 0; overflow: hidden; flex: none"><img src="{IMG["kitchen"]}" alt="" style="width: 100%; height: 100%; object-fit: cover"></div>'
        bg, ink, head_ = '#F2EEE7', '#1F1D1B', 'Входите.<br>Дальше мы сами.'
    elif k == 'D':
        vis = mark_D(96)
        bg, ink, head_ = '#0E0F11', '#F2F1EE', 'Дом, в котором<br>уже горит свет'
    else:
        vis = mark_Y(104, *v['dir'])
        bg, ink, head_ = '#FFFFFF', '#14161F', 'Квартира. Ремонт.<br>Дом.'
    btn_bg = v['dir'][0] if k == 'Y' else acc
    inner = (f'<div style="position: absolute; left: 31.2%; top: 27.9%; width: 55.1%; height: 38%; background: {bg}; display: flex; align-items: center; gap: 16px; padding: 0 18px; box-sizing: border-box; box-shadow: inset 0 0 30px rgba(0,0,0,0.12)">'
             f'{vis}<div style="display: flex; flex-direction: column; gap: 8px; color: {ink}">'
             f'<span style="font: {600 if k != "L" else 700} {16 if k == "Y" else 19}px/1.05 \'{FH}\', sans-serif; letter-spacing: -0.01em">{head_}</span>'
             f'<span style="align-self: flex-start; padding: 5px 9px; background: {btn_bg}; color: {v["acc_ink"]}; font: 600 10px \'{F}\', sans-serif">ПЛАТФОРМА · ЕКБ</span></div></div>')
    return photo(IMG['mk_billboard'], 'Билборд на улице города', inner + tag('билборд 6×3', F))


def keys(v):
    m = colored_mark(v, 40)
    inner = f'<div style="position: absolute; left: 57.3%; top: 61%; transform: translate(-50%, -50%) rotate(-15deg); mix-blend-mode: multiply; opacity: 0.92">{m}</div>'
    return photo(IMG['mk_keys'], 'Ключи с кожаным брелоком', inner + tag('брелок к ключам от новой квартиры', v['F']))


def helmet(v):
    m = colored_mark(v, 40)
    inner = f'<div style="position: absolute; left: 50.5%; top: 48%; transform: translate(-50%, -50%) perspective(300px) rotateY(-18deg) rotate(-4deg); mix-blend-mode: multiply; opacity: 0.9">{m}</div>'
    return photo(IMG['mk_helmet'], 'Строительная каска', inner + tag('каска', v['F']))


def vest(v):
    k = v['key']
    if k == 'D':
        lk = lockup(v, 22, '#14120E', '#14120E', mono='#14120E', mw=40)
    else:
        lk = lockup(v, 22, '#FFFFFF', '#FFFFFF', mono='#FFFFFF', mw=40)
    inner = f'<div style="position: absolute; left: 58.8%; top: 56%; transform: translate(-50%, -50%) rotate(-2deg); opacity: 0.93">{lk}</div>'
    return photo(IMG['mk_vest'], 'Сигнальный жилет прораба', inner + tag('спецодежда', v['F']))


def bag(v):
    k = v['key']
    ink = {'L': '#1F1D1B', 'D': '#14120E', 'Y': '#14161F'}[k]
    m = colored_mark(v, 30)
    w = f'<span style="font: {v["word_w"]} {round(11 * v["word_k"])}px \'{v["FH"]}\', sans-serif; letter-spacing: {v["word_ls"]}; color: {ink}">ПЛАТФОРМА</span>'
    inner = f'<div style="position: absolute; left: 51.3%; top: 76%; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; gap: 6px; mix-blend-mode: multiply">{m}{w}</div>'
    return photo(IMG['mk_bag'], 'Бумажный пакет', inner + tag('пакет для документов', v['F']))


def voice(v):
    F, FH = v['F'], v['FH']
    title, lines = VOICE[v['key']]
    acc = v['dir'] if v['key'] == 'Y' else (v['acc'],) * 3
    items = ''.join(f'<div style="display: flex; gap: 14px; align-items: baseline; padding: 12px 0; border-bottom: 1px solid {v["line"]}"><span style="width: 10px; height: 10px; flex: none; background: {acc[i]}"></span>'
                    f'<span style="font: 600 {24 if v["key"] != "Y" else 20}px/1.2 \'{FH}\', sans-serif; letter-spacing: -0.01em">{t}</span></div>' for i, t in enumerate(lines))
    return (f'<div style="height: 100%; background: {v["panel"]}; padding: 22px 26px; box-sizing: border-box; display: flex; flex-direction: column; gap: 6px">'
            f'{label(v, "как мы говорим")}<span style="font: 500 15px \'{F}\', sans-serif; color: {v["muted"]}">{title}. Без «элитного», без восклицаний и звёздочек; цифры — только реальные.</span>{items}</div>')


def life_board(v):
    k = v['key']; F, acc, line, muted, ink = v['F'], v['acc'], v['line'], v['muted'], v['ink']
    h = 1340
    return head(f'{v["title"]} · {v["name"]} — бренд в жизни', v, h) + f'''<div style="width: 1440px; height: {h}px; box-sizing: border-box; padding: 48px 56px; background: {v['bg']}; color: {v['text']}; font-family: '{F}', system-ui, sans-serif; display: flex; flex-direction: column; gap: 24px; overflow: hidden">
  <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid {line}; padding-bottom: 16px">
    <div style="font: 500 30px '{F}', sans-serif; letter-spacing: -0.02em">{v['title']} · <span style="color: {acc if k != 'Y' else ink}">«{v['name']}»</span></div>
    <div style="font: 400 14px '{F}', sans-serif; color: {muted}">[ 05 · бренд в жизни ]</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 20px; align-items: start">
    <div style="grid-column: span 8">{sign(v)}</div>
    <div style="grid-column: span 4; display: flex; flex-direction: column; gap: 12px">{keys(v)}{helmet(v)}</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 20px">
    <div style="grid-column: span 6">{billboard(v)}</div>
    <div style="grid-column: span 6">{vest(v)}</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 20px; flex: 1; min-height: 0">
    <div style="grid-column: span 4">{bag(v)}</div>
    <div style="grid-column: span 8">{voice(v)}</div>
  </div>
</div>
''' + tail(h)


if __name__ == '__main__':
    for k, v in V.items():
        open(OUT + f'Life{k}.dc.html', 'w', encoding='utf8').write(life_board(v))
    print('ok')
