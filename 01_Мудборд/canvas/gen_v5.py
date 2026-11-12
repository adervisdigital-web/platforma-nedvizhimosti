"""Board 05 — brand in real life: logo applied to generated product/facade photos."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marks import mark_L, mark_D, mark_Y
from gen_v3 import V, IMG, OUT, head, tail, label, lockup, fam

HERE = os.path.dirname(os.path.abspath(__file__))
IMG.update({k: '/_blob/' + v for k, v in json.load(open(HERE + '/blobs2.json', encoding='utf8')).items()})
IMG.update({k: '/_blob/' + v for k, v in json.load(open(HERE + '/blobs3.json', encoding='utf8')).items()})

VOICE = {
    'K': ('Твёрдо и по делу', ['Строим так, чтобы стояло век.', 'Кладка, ремонт, ключи — в одном договоре.', 'Каменный дом без сюрпризов в смете.']),
    'S': ('Тепло и спокойно', ['Ваш дом уже ждёт.', 'Порог переступили — дальше наша забота.', 'Квартира, ремонт и свой дом за городом.']),
    'L': ('Спокойно и по-домашнему', ['Входите. Дальше мы сами.', 'Ремонт к переезду — в одном договоре.', 'Свой каменный дом без сюрпризов в смете.']),
    'D': ('Уверенно и коротко', ['Дом, в котором уже горит свет.', 'Стройка онлайн, 24/7.', 'Цена в договоре не меняется.']),
    'Y': ('Бодро и понятно', ['Всё для дома — на одной платформе.', 'Квартира. Ремонт. Дом. В одном приложении.', 'Смета ремонта за 2 минуты.']),
}


def colored_mark(v, w, on='white'):
    k = fam(v)
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


def shot(v, surf, alt, label):
    return photo(IMG['life_' + v['key'] + '_' + surf], alt, tag(label, v['F']))


def sign(v):
    return shot(v, 'facade', 'Световая вывеска на фасаде офиса', 'вывеска на фасаде офиса')


def billboard(v):
    return shot(v, 'billboard', 'Билборд на улице города', 'билборд 6×3')


def keys(v):
    return shot(v, 'keys', 'Брелок к ключам от новой квартиры', 'брелок к ключам от новой квартиры')


def helmet(v):
    return shot(v, 'helmet', 'Строительная каска', 'каска')


def vest(v):
    return shot(v, 'vest', 'Сигнальный жилет прораба', 'спецодежда')


def bag(v):
    return shot(v, 'bag', 'Бумажный пакет для документов', 'пакет для документов')


def voice(v):
    F, FH = v['F'], v['FH']
    title, lines = VOICE[v['key']]
    acc = v['dir'] if fam(v) == 'Y' else (v['acc'],) * 3
    items = ''.join(f'<div style="display: flex; gap: 14px; align-items: baseline; padding: 12px 0; border-bottom: 1px solid {v["line"]}"><span style="width: 10px; height: 10px; flex: none; background: {acc[i]}"></span>'
                    f'<span style="font: 600 {24 if v["key"] != "Y" else 20}px/1.2 \'{FH}\', sans-serif; letter-spacing: -0.01em">{t}</span></div>' for i, t in enumerate(lines))
    return (f'<div style="height: 100%; background: {v["panel"]}; padding: 22px 26px; box-sizing: border-box; display: flex; flex-direction: column; gap: 6px">'
            f'{label(v, "как мы говорим")}<span style="font: 500 15px \'{F}\', sans-serif; color: {v["muted"]}">{title}. Без «элитного», без восклицаний и звёздочек; цифры — только реальные.</span>{items}</div>')


def life_board(v):
    k = fam(v); F, acc, line, muted, ink = v['F'], v['acc'], v['line'], v['muted'], v['ink']
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
