"""Boards 03 (identity system) and 04 (site on laptop + app on iPhone) for the three variants."""
import sys
sys.path.insert(0, 'C:/Users/MSI/AppData/Local/Temp/claude/10d39200edc2b63f/973356bb-8c70-4e3b-b6ae-d636a7404011/scratchpad/v3')
from marks import mark_L, mark_D, mark_Y
from gen_v3 import V, IMG, OUT, head, tail, label, lockup, mark
import json, os

EXTRA = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/blobs2.json', encoding='utf8'))
IMG.update({k: '/_blob/' + v for k, v in EXTRA.items()})

UI = {
 'L': dict(bg='#FBF9F5', surf='#FFFFFF', soft='#F2EEE7', txt='#1F1D1B', mut='#7A7368', line='#E6DFD3', r=0, ir='0', hw=700, cap='none'),
 'D': dict(bg='#0E0F11', surf='#17191C', soft='#1F2226', txt='#F2F1EE', mut='#8D929A', line='#2A2D32', r=2, ir='0', hw=600, cap='none'),
 'Y': dict(bg='#FFFFFF', surf='#FFFFFF', soft='#F3F4F8', txt='#14161F', mut='#6B6F7D', line='#E3E5EC', r=14, ir='14px', hw=600, cap='none'),
}


def small_mark(v, w):
    k = v['key']
    return mark_L(w, v['acc']) if k == 'L' else mark_D(w) if k == 'D' else mark_Y(w, *v['dir'])


def word(v, size, color):
    return f'<span style="font: {v["word_w"]} {round(size * v["word_k"])}px \'{v["FH"]}\', sans-serif; letter-spacing: {v["word_ls"]}; color: {color}; white-space: nowrap">ПЛАТФОРМА</span>'


def img(src, alt, r='0', extra=''):
    return f'<img src="{src}" alt="{alt}" style="width: 100%; height: 100%; object-fit: cover; display: block; border-radius: {r}; {extra}">'


# ---------------- icons ----------------
ICONS = [
    ('Квартиры', '<rect x="6" y="3" width="12" height="18"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>'),
    ('Ремонт', '<rect x="4" y="4" width="13" height="5"/><path d="M17 6.5h3v5h-8v3"/><rect x="11" y="14.5" width="2" height="6"/>'),
    ('Дома', '<path d="M4 21V10l8-6 8 6v11z"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/>'),
    ('Ипотека', '<path d="M6 18L18 6"/><circle cx="7.5" cy="7.5" r="2.5"/><circle cx="16.5" cy="16.5" r="2.5"/>'),
    ('Смета', '<rect x="5" y="3" width="14" height="18"/><path d="M8 7h8M8 12h2M14 12h2M8 16h2M14 16h2"/>'),
    ('Камера 24/7', '<path d="M3 8h4l2-3h6l2 3h4v12H3z"/><circle cx="12" cy="14" r="3.5"/>'),
    ('Договор', '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h7"/>'),
    ('Ключи', '<circle cx="8" cy="15" r="4"/><path d="M11 12l8-8M16 7l2 2"/>'),
    ('На карте', '<path d="M12 21s-6-5.6-6-11a6 6 0 0 1 12 0c0 5.4-6 11-6 11z"/><circle cx="12" cy="10" r="2"/>'),
    ('Чат', '<path d="M4 5h16v11H9l-5 4z"/>'),
    ('Избранное', '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>'),
    ('Поиск', '<circle cx="11" cy="11" r="6"/><path d="M16 16l4 4"/>'),
]


def icon(v, i, size=28, color=None):
    cap = 'square' if v['key'] == 'D' else 'round'
    c = color or UI[v['key']]['txt']
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" '
            f'stroke-linecap="{cap}" stroke-linejoin="{"miter" if cap == "square" else "round"}" aria-hidden="true">{ICONS[i][1]}</svg>')


# ---------------- patterns ----------------
def pattern(v, W=760, H=400):
    k = v['key']
    if k == 'L':
        cols = ['#B4532A', '#D9CBB5', '#1F1D1B', '#E7DCCB']
        out = ''
        cw, ch = 76, 96
        for r in range(H // ch + 1):
            for c in range(W // cw + 1):
                col = cols[(r * 3 + c * 2 + (r * c) % 3) % 4]
                x, y = c * cw + 8, r * ch + 12
                w, h = cw - 16, ch - 12
                out += f'<path d="M{x} {y + h} V{y + w / 2} A{w / 2} {w / 2} 0 0 1 {x + w} {y + w / 2} V{y + h} Z" fill="{col}"/>'
        return f'<svg width="100%" height="100%" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Паттерн из арок"><rect width="{W}" height="{H}" fill="#F2EEE7"/>{out}</svg>'
    if k == 'D':
        out = ''
        lit = {(1, 2), (2, 5), (0, 7), (3, 1), (2, 9), (1, 11), (3, 6), (0, 3)}
        for r in range(5):
            for c in range(13):
                x, y = c * 60, r * 84 + 6
                glow = '#FFB547' if (r, c) in lit else '#1B1D21'
                out += (f'<g transform="translate({x},{y}) scale(1.55)"><polygon points="0,8 8,0 36,0 28,8" fill="#2A2D32"/>'
                        f'<polygon points="28,8 36,0 36,28 28,36" fill="#1F2226"/><polygon points="8,16 16,16 16,28 8,36" fill="{glow}"/>'
                        f'<path d="M0 8 H28 V36 H20 V16 H8 V36 H0 Z" fill="#3A3E45"/></g>')
        return f'<svg width="100%" height="100%" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Паттерн: ночной фасад из порталов"><rect width="{W}" height="{H}" fill="#0E0F11"/>{out}</svg>'
    out = ''
    cols = v['dir']
    for r in range(6):
        for c in range(10):
            x, y = c * 80, r * 72
            pick = (r * 7 + c * 3) % 5
            a = cols[0] if pick == 0 else '#E3E5EC'
            b = cols[1] if pick == 1 else '#E3E5EC'
            d = cols[2] if pick == 2 else '#E3E5EC'
            if pick == 3:
                a, b, d = cols
            out += (f'<g transform="translate({x + 10},{y + 8}) scale(1.5)"><polygon points="0,0 40,0 30,10 10,10" fill="{b}"/>'
                    f'<polygon points="0,3 10,13 10,36 0,36" fill="{a}"/><polygon points="40,3 40,36 30,36 30,13" fill="{d}"/></g>')
    return f'<svg width="100%" height="100%" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Паттерн из знаков"><rect width="{W}" height="{H}" fill="#FFFFFF"/>{out}</svg>'


# ---------------- identity system board ----------------
def system_board(v):
    k = v['key']; u = UI[k]; F, FH, acc = v['F'], v['FH'], v['acc']
    ink, muted, line, panel = v['ink'], v['muted'], v['line'], v['panel']
    icons = ''.join(f'<div style="display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 12px 4px; background: {u["surf"] if k != "D" else "#1F2226"}">'
                    f'{icon(v, i, 30, (v["dir"][i] if (k == "Y" and i < 3) else (acc if (k != "Y" and i < 3) else u["txt"])))}'
                    f'<span style="font: 400 12px \'{F}\', sans-serif; color: {muted}">{ICONS[i][0]}</span></div>' for i in range(12))
    scale = [('H1 · заголовок экрана', 56, u['hw'], FH, 'Свой дом' if k == 'Y' else 'Каменный дом'), ('H2 · раздел', 36, u['hw'], FH, 'Квартиры у парка'),
             ('H3 · карточка', 24, 600, F, 'от [ЦЕНА] ₽'), ('Текст', 16, 400, F, 'Подберём квартиру и сделаем ремонт к переезду.'),
             ('Подпись', 13, 500, F, '2-комн. · [ПЛОЩАДЬ] м² · Академический')]
    sc = ''.join(f'<div style="display: flex; align-items: baseline; gap: 16px; border-bottom: 1px solid {line}; padding: 8px 0">'
                 f'<span style="width: 140px; flex: none; font: 400 12px \'{F}\', sans-serif; color: {muted}">{n} · {s}</span>'
                 f'<span style="font: {w} {round(s * (v["word_k"] if f == FH else 1))}px/1.1 \'{f}\', sans-serif; letter-spacing: {"-0.02em" if s > 30 else "0"}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{t}</span></div>'
                 for n, s, w, f, t in scale)
    ph_r = '999px 999px 0 0' if k == 'L' else u['ir']
    photos = ''.join(f'<div style="display: flex; flex-direction: column; gap: 8px; flex: 1"><div style="height: 170px; overflow: hidden; border-radius: {ph_r}">{img(IMG[src], alt)}</div>'
                     f'<span style="font: 500 13px \'{F}\', sans-serif">{t}</span><span style="font: 400 12px/1.4 \'{F}\', sans-serif; color: {muted}">{d}</span></div>'
                     for src, alt, t, d in (('living2', 'Гостиная в новой квартире', 'Дневной свет', 'светлые интерьеры без людей-моделей'),
                                            ('process', 'Квартира в процессе ремонта', 'Честный процесс', 'стройку и ремонт показываем как есть'),
                                            ('stone2', 'Каменный дом', 'Готовый результат', 'дом, двор, ключи — то, ради чего всё')))
    btn_r = f'{u["r"]}px'
    comp = f'''
      <div style="display: flex; gap: 10px; flex-wrap: wrap">
        <span style="padding: 14px 22px; background: {acc}; color: {v['acc_ink']}; font: 600 15px '{F}', sans-serif; border-radius: {btn_r}">Подобрать квартиру</span>
        <span style="padding: 13px 21px; border: 1px solid {u['txt']}; color: {u['txt']}; font: 600 15px '{F}', sans-serif; border-radius: {btn_r}">Рассчитать ремонт</span>
      </div>
      <div style="display: flex; gap: 8px; flex-wrap: wrap">
        {''.join(f'<span style="padding: 8px 12px; background: {(v["dir"][i] if k == "Y" else u["txt"]) if i == 0 else (u["surf"] if k == "Y" else u["soft"])}; color: {("#FFFFFF" if k != "D" else "#14120E") if i == 0 else u["txt"]}; font: 500 13px \'{F}\', sans-serif; border-radius: {btn_r}">{t}</span>' for i, t in enumerate(("2-комн.", "до [ЦЕНА] ₽", "Академический", "С отделкой")))}
      </div>
      <div style="display: flex; align-items: center; justify-content: space-between; padding: 14px 16px; border: 1px solid {line}; background: {u['surf']}; border-radius: {btn_r}">
        <span style="font: 400 14px '{F}', sans-serif; color: {muted}">Район или ЖК</span>{icon(v, 11, 20, muted)}
      </div>
      <div style="padding: 14px 16px; background: {u['surf'] if k == 'Y' else u['soft']}; border-radius: {btn_r}; display: flex; flex-direction: column; gap: 8px">
        <div style="display: flex; justify-content: space-between; font: 500 13px '{F}', sans-serif"><span>Этап 3 из 7 · стены</span><span style="color: {muted}">43%</span></div>
        <div style="display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 3px">{''.join(f'<div style="height: 5px; background: {acc if j < 3 else line}"></div>' for j in range(7))}</div>
      </div>'''
    sign = (f'<div style="position: relative; height: 100%; overflow: hidden">{img(IMG["life_" + k + "_store"], "Вывеска над входом в офис продаж")}'
            f'<span style="position: absolute; left: 12px; top: 12px; padding: 5px 9px; background: #FFFFFF; color: #1F1D1B; font: 400 12px {F!r}, sans-serif">[ вывеска офиса продаж ]</span></div>')
    passport = (f'<div style="position: relative; height: 100%; overflow: hidden">{img(IMG["life_" + k + "_plate"], "Паспорт объекта на заборе стройки")}'
                f'<span style="position: absolute; left: 12px; top: 12px; padding: 5px 9px; background: #FFFFFF; color: #1F1D1B; font: 400 12px {F!r}, sans-serif">[ паспорт объекта на стройке ]</span></div>')
    h = 1540
    return head(f'{v["title"]} · {v["name"]} — айдентика', v, h) + f'''<div style="width: 1440px; height: {h}px; box-sizing: border-box; padding: 48px 56px; background: {v['bg']}; color: {v['text']}; font-family: '{F}', system-ui, sans-serif; display: flex; flex-direction: column; gap: 24px; overflow: hidden">
  <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid {line}; padding-bottom: 16px">
    <div style="font: 500 30px '{F}', sans-serif; letter-spacing: -0.02em">{v['title']} · <span style="color: {acc if k != 'Y' else ink}">«{v['name']}»</span></div>
    <div style="font: 400 14px '{F}', sans-serif; color: {muted}">[ 03 · айдентика: система ]</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 20px; height: 400px">
    <div style="grid-column: span 7; position: relative; overflow: hidden">{pattern(v)}
      <span style="position: absolute; left: 14px; top: 14px; padding: 5px 9px; background: #FFFFFF; color: #1F1D1B; font: 400 12px '{F}', sans-serif">[ паттерн — {('фасад из арок' if k == 'L' else 'ночной фасад: в части окон горит свет' if k == 'D' else 'знаки-направления')} ]</span></div>
    <div style="grid-column: span 5; background: {panel}; padding: 20px; display: flex; flex-direction: column; gap: 14px">
      {label(v, 'иконки — линия 1.8 px, сетка 24 px')}
      <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; flex: 1">{icons}</div>
    </div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 20px; height: 380px">
    <div style="grid-column: span 6; background: {panel}; padding: 20px 24px; display: flex; flex-direction: column; gap: 6px; overflow: hidden">
      {label(v, 'шрифтовая шкала')}
      {sc}
    </div>
    <div style="grid-column: span 6; background: {panel}; padding: 20px 24px; display: flex; flex-direction: column; gap: 14px">
      {label(v, 'фотостиль')}
      <div style="display: flex; gap: 16px">{photos}</div>
      <span style="font: 400 13px/1.5 '{F}', sans-serif; color: {muted}">Не используем: стоковые улыбки, небоскрёбы, золото, «домики с ключом».</span>
    </div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 20px; flex: 1; min-height: 0">
    <div style="grid-column: span 4; background: {panel}; padding: 20px; display: flex; flex-direction: column; gap: 14px">
      {label(v, 'компоненты интерфейса')}
      {comp}
    </div>
    <div style="grid-column: span 4">{sign}</div>
    <div style="grid-column: span 4">{passport}</div>
  </div>
</div>
''' + tail(h)


# ---------------- site on laptop ----------------
def hero_visual(v, H=300):
    k = v['key']
    if k == 'L':
        return (f'<div style="position: relative; width: 100%; height: {H}px">'
                f'<div style="position: absolute; right: 120px; top: 0; width: 230px; height: {H}px; border-radius: 115px 115px 0 0; overflow: hidden">{img(IMG["kitchen"], "Кухня-гостиная")}</div>'
                f'<div style="position: absolute; right: 0; bottom: 0; width: 150px; height: 190px; border-radius: 75px 75px 0 0; overflow: hidden; border: 6px solid #FBF9F5">{img(IMG["stone2"], "Каменный дом")}</div></div>')
    if k == 'D':
        return (f'<div style="position: relative; width: 100%; height: {H}px; display: flex; justify-content: flex-end">'
                f'<svg width="{H}" height="{H}" viewBox="0 0 36 36" role="img" aria-label="Портал с фото жилого комплекса">'
                f'<defs><clipPath id="hD"><path d="M0 8 H28 V36 H20 V16 H8 V36 H0 Z"/></clipPath></defs>'
                f'<polygon points="0,8 8,0 36,0 28,8" fill="#3A3E45"/><polygon points="28,8 36,0 36,28 28,36" fill="#24272C"/>'
                f'<polygon points="8,16 16,16 16,28 8,36" fill="#FFB547"/>'
                f'<image href="{IMG["complex2"]}" x="-6" y="6" width="38" height="32" preserveAspectRatio="xMidYMid slice" clip-path="url(#hD)"/></svg></div>')
    W = round(H * 40 / 36)
    parts = (('0,3 10,13 10,36 0,36', IMG['living2'], 0, 3, 10, 33), ('0,0 40,0 30,10 10,10', IMG['detail'], 0, 0, 40, 10), ('40,3 40,36 30,36 30,13', IMG['stone2'], 30, 3, 10, 33))
    defs = ''.join(f'<clipPath id="hY{i}"><polygon points="{p[0]}"/></clipPath>' for i, p in enumerate(parts))
    ims = ''.join(f'<image href="{p[1]}" x="{p[2]}" y="{p[3]}" width="{p[4]}" height="{p[5]}" preserveAspectRatio="xMidYMid slice" clip-path="url(#hY{i})"/><polygon points="{p[0]}" fill="{v["dir"][i]}" opacity="0.22"/>' for i, p in enumerate(parts))
    return f'<div style="display: flex; justify-content: flex-end"><svg width="{W}" height="{H}" viewBox="0 0 40 36" role="img" aria-label="Знак из трёх фото">{"<defs>" + defs + "</defs>" + ims}</svg></div>'


def site(v):
    k = v['key']; u = UI[k]; F, FH, acc = v['F'], v['FH'], v['acc']
    r = f'{u["r"]}px'
    tabs = ''
    for i, n in enumerate(('Квартиры', 'Ремонт', 'Дома')):
        c = v['dir'][i]
        on = i == 0
        tabs += (f'<span style="padding: 10px 16px; font: 600 14px \'{F}\', sans-serif; border-radius: {r} {r} 0 0; '
                 f'background: {u["surf"] if on else "transparent"}; color: {(c if k == "Y" else u["txt"]) if on else u["mut"]}; '
                 f'{("box-shadow: inset 0 3px 0 " + c + ";") if on else ""}">{n}</span>')
    field = lambda t, val: (f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 10px 14px; background: {u["soft"]}; border-radius: {r}">'
                            f'<span style="font: 400 11px \'{F}\', sans-serif; color: {u["mut"]}">{t}</span><span style="font: 500 14px \'{F}\', sans-serif">{val}</span></div>')
    rooms = ''.join(f'<span style="padding: 2px 7px; {"background: " + (v["dir"][0] if k == "Y" else u["txt"]) + "; color: " + ("#FFFFFF" if k != "D" else "#14120E") + ";" if n == "2" else ""} border-radius: {max(0, u["r"] - 8)}px">{n}</span>' for n in ('1', '2', '3', '4+'))
    h1 = 'Квартира, ремонт и дом —<br>на одной платформе'
    h1size = 40 if k != 'Y' else 32
    dirs = ''
    subs = (('Квартиры', '[N] предложений в Екатеринбурге', IMG['bedroom']), ('Ремонт', 'смета за 2 минуты, фиксированная цена', IMG['bath']), ('Дома', '[N] проектов каменных домов', IMG['gable']))
    for i, (n, s, im) in enumerate(subs):
        c = v['dir'][i]
        ir = '60px 60px 0 0' if k == 'L' else f'{max(0, u["r"] - 4)}px'
        dirs += (f'<div style="display: flex; gap: 14px; align-items: center; padding: 10px; background: {u["surf"]}; border: 1px solid {u["line"]}; border-radius: {r}">'
                 f'<div style="width: 120px; height: 96px; flex: none; overflow: hidden; border-radius: {ir}">{img(im, n)}</div>'
                 f'<div style="display: flex; flex-direction: column; gap: 4px"><span style="font: {u["hw"]} 18px \'{FH if k != "Y" else FH}\', sans-serif; color: {c if k == "Y" else u["txt"]}">{n}</span>'
                 f'<span style="font: 400 13px/1.35 \'{F}\', sans-serif; color: {u["mut"]}">{s}</span>'
                 f'<span style="font: 500 13px \'{F}\', sans-serif; color: {c if k == "Y" else acc}">Перейти →</span></div></div>')
    cards = ''
    items = (('living2', 'от [ЦЕНА] ₽', '2-комн. · [ПЛОЩАДЬ] м² · Академический', 0, 'Ипотека'), ('after', 'от [ЦЕНА] ₽/м²', 'Ремонт под ключ · 3 тарифа', 1, 'Смета онлайн'),
             ('stone2', 'от [ЦЕНА] ₽', 'Каменный дом · [ПЛОЩАДЬ] м² · 2 этажа', 2, 'Камера 24/7'), ('kids', 'от [ЦЕНА] ₽', '3-комн. · [ПЛОЩАДЬ] м² · ЖК [НАЗВАНИЕ]', 0, 'С отделкой'))
    for src, p, d, di, tag in items:
        c = v['dir'][di]
        ir = '110px 110px 0 0' if k == 'L' else f'{u["r"]}px'
        tag_bg = c if k == 'Y' else acc
        tag_c = '#FFFFFF' if k != 'D' else '#14120E'
        cards += (f'<div style="display: flex; flex-direction: column; gap: 8px"><div style="height: 150px; overflow: hidden; position: relative; border-radius: {ir}">{img(IMG[src], d)}'
                  f'<span style="position: absolute; left: 8px; bottom: 8px; padding: 4px 8px; background: {tag_bg}; color: {tag_c}; font: 600 11px \'{F}\', sans-serif; border-radius: {max(0, u["r"] - 8)}px">{tag}</span></div>'
                  f'<span style="font: 600 17px \'{F}\', sans-serif">{p}</span><span style="font: 400 12px \'{F}\', sans-serif; color: {u["mut"]}">{d}</span></div>')
    nav = ''.join(f'<span>{n}</span>' for n in ('Квартиры', 'Ремонт', 'Дома', 'Ипотека', 'О компании'))
    sub_c = u['mut']
    return f'''<div style="width: 1280px; height: 800px; background: {u['bg']}; color: {u['txt']}; font-family: '{F}', sans-serif; overflow: hidden">
  <div style="height: 68px; padding: 0 40px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid {u['line']}">
    <div style="display: flex; align-items: center; gap: 40px">{lockup(v, 18, u['txt'], sub_c, mw=30)}
      <div style="display: flex; gap: 26px; font: 500 14px '{F}', sans-serif">{nav}</div></div>
    <div style="display: flex; align-items: center; gap: 18px"><span style="font: 500 14px '{F}', sans-serif">+7 [ТЕЛЕФОН]</span>
      <span style="padding: 10px 16px; background: {acc}; color: {v['acc_ink']}; font: 600 14px '{F}', sans-serif; border-radius: {r}">Личный кабинет</span></div>
  </div>
  <div style="padding: 28px 40px 0; display: grid; grid-template-columns: 7fr 5fr; gap: 32px; height: 330px; box-sizing: border-box">
    <div style="display: flex; flex-direction: column; gap: 18px">
      <span style="font: 500 13px '{F}', sans-serif; color: {u['mut']}">Екатеринбург · квартиры, ремонт, каменные дома</span>
      <div style="font: {u['hw']} {h1size}px/1.08 '{FH}', sans-serif; letter-spacing: -0.02em">{h1}</div>
      <div>
        <div style="display: flex; gap: 2px">{tabs}</div>
        <div style="padding: 14px; background: {u['surf']}; border: 1px solid {u['line']}; border-radius: 0 {r} {r} {r}; display: grid; grid-template-columns: 1.1fr 1.3fr 1.2fr auto; gap: 10px; align-items: stretch">
          <div style="display: flex; flex-direction: column; gap: 4px; padding: 10px 14px; background: {u['soft']}; border-radius: {r}"><span style="font: 400 11px '{F}', sans-serif; color: {u['mut']}">Комнат</span><div style="display: flex; gap: 6px; font: 500 14px '{F}', sans-serif">{rooms}</div></div>
          {field('Цена, ₽', 'от — до [ЦЕНА]')}{field('Район', 'Академический ▾')}
          <span style="display: flex; align-items: center; padding: 0 20px; background: {v['dir'][0] if k == 'Y' else acc}; color: {v['acc_ink']}; font: 600 14px '{F}', sans-serif; border-radius: {r}; white-space: nowrap">Показать [N]</span>
        </div>
      </div>
    </div>
    <div>{hero_visual(v, 290)}</div>
  </div>
  <div style="padding: 22px 40px 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px">{dirs}</div>
  <div style="padding: 26px 40px 0; display: flex; justify-content: space-between; align-items: baseline"><span style="font: {u['hw']} 22px '{FH}', sans-serif">Новые предложения</span><span style="font: 500 14px '{F}', sans-serif; color: {u['mut']}">Смотреть все →</span></div>
  <div style="padding: 14px 40px 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px">{cards}</div>
</div>'''


def laptop(v):
    return f'''<div style="display: flex; flex-direction: column; align-items: center">
  <div style="width: 1100px; background: #1B1B1B; border-radius: 22px 22px 0 0; padding: 18px 18px 22px; box-sizing: border-box">
    <div style="width: 1064px; height: 665px; overflow: hidden; position: relative; background: #FFFFFF">
      <div style="position: absolute; left: 0; top: 0; transform: scale(0.83125); transform-origin: 0 0">{site(v)}</div>
    </div>
  </div>
  <div style="width: 1240px; height: 24px; background: linear-gradient(180deg, #D3D3CF 0%, #A6A6A1 100%); border-radius: 0 0 28px 28px; position: relative">
    <div style="position: absolute; left: 50%; top: 0; width: 150px; height: 9px; margin-left: -75px; background: #96968F; border-radius: 0 0 9px 9px"></div>
  </div>
</div>'''


# ---------------- app on iPhone ----------------
def status(u):
    return (f'<div style="height: 50px; padding: 0 28px; display: flex; justify-content: space-between; align-items: center; font: 600 15px -apple-system, \'Inter\', sans-serif; color: {u["txt"]}">'
            f'<span>9:41</span><span style="display: flex; gap: 5px; align-items: center"><span style="width: 17px; height: 10px; border: 1.5px solid {u["txt"]}; border-radius: 3px; display: inline-block"></span></span></div>')


def tabbar(v, active=0):
    k = v['key']; u = UI[k]
    items = ((11, 'Поиск'), (10, 'Избранное'), (5, 'Мой объект'), (9, 'Чат'))
    out = ''
    for j, (ic, n) in enumerate(items):
        col = (v['dir'][0] if k == 'Y' else v['acc']) if j == active else u['mut']
        out += f'<div style="display: flex; flex-direction: column; align-items: center; gap: 4px">{icon(v, ic, 24, col)}<span style="font: 500 11px \'{v["F"]}\', sans-serif; color: {col}">{n}</span></div>'
    return f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 84px; padding: 10px 24px 0; box-sizing: border-box; background: {u["surf"]}; border-top: 1px solid {u["line"]}; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr))">{out}</div>'


def screen_home(v):
    k = v['key']; u = UI[k]; F, FH, acc = v['F'], v['FH'], v['acc']
    r = f'{u["r"]}px'
    tiles = ''
    for i, (n, im) in enumerate((('Квартиры', 'bedroom'), ('Ремонт', 'bath'), ('Дома', 'gable'))):
        c = v['dir'][i]
        ir = '50px 50px 0 0' if k == 'L' else r
        tiles += (f'<div style="display: flex; flex-direction: column; gap: 6px"><div style="height: 96px; overflow: hidden; border-radius: {ir}; {"box-shadow: inset 0 -4px 0 " + c if k == "Y" else ""}">{img(IMG[im], n)}</div>'
                  f'<span style="font: 600 14px \'{F}\', sans-serif; color: {c if k == "Y" else u["txt"]}">{n}</span></div>')
    return f'''<div style="width: 375px; height: 812px; background: {u['bg']}; color: {u['txt']}; position: relative; overflow: hidden">
  {status(u)}
  <div style="padding: 4px 20px 0; display: flex; justify-content: space-between; align-items: center">
    <div style="display: flex; align-items: center; gap: 8px">{small_mark(v, 26)}{word(v, 15, u['txt'])}</div>{icon(v, 9, 24)}</div>
  <div style="padding: 18px 20px 0; font: {u['hw']} {28 if k != 'Y' else 24}px/1.1 '{FH}', sans-serif; letter-spacing: -0.01em">Добрый день,<br>[Имя]</div>
  <div style="margin: 16px 20px 0; padding: 14px 16px; background: {u['soft']}; border-radius: {r}; display: flex; gap: 10px; align-items: center">{icon(v, 11, 20, u['mut'])}<span style="font: 400 15px '{F}', sans-serif; color: {u['mut']}">Квартира, ремонт или дом</span></div>
  <div style="padding: 18px 20px 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px">{tiles}</div>
  <div style="margin: 18px 20px 0; border-radius: {r}; overflow: hidden; background: {u['surf']}; border: 1px solid {u['line']}">
    <div style="height: 120px; position: relative">{img(IMG['process'], 'Камера на объекте')}<span style="position: absolute; left: 10px; top: 10px; padding: 4px 8px; background: rgba(0,0,0,0.65); color: #FFFFFF; font: 600 11px '{F}', sans-serif">● Камера 24/7</span></div>
    <div style="padding: 12px 14px; display: flex; flex-direction: column; gap: 8px">
      <div style="display: flex; justify-content: space-between; font: 600 15px '{F}', sans-serif"><span>Мой дом · этап 3 из 7</span><span style="color: {u['mut']}; font-weight: 400">43%</span></div>
      <div style="display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 3px">{''.join(f'<div style="height: 5px; background: {(v["dir"][2] if k == "Y" else acc) if j < 3 else u["line"]}"></div>' for j in range(7))}</div>
    </div>
  </div>
  <div style="margin: 12px 20px 0; padding: 14px 16px; background: {v['dir'][0] if k == 'Y' else acc}; color: {v['acc_ink']}; border-radius: {r}; display: flex; justify-content: space-between; align-items: center"><div style="display: flex; flex-direction: column; gap: 2px"><span style="font: 600 15px '{F}', sans-serif">Ипотечный лимит</span><span style="font: 400 12px '{F}', sans-serif; opacity: 0.85">за 1 минуту, без визита в банк</span></div><span style="font: 600 18px '{F}', sans-serif">→</span></div>
  {tabbar(v, 0)}
</div>'''


def screen_catalog(v):
    k = v['key']; u = UI[k]; F, FH, acc = v['F'], v['FH'], v['acc']
    r = f'{u["r"]}px'
    c0 = v['dir'][0] if k == 'Y' else (u['txt'])
    chips = ''.join(f'<span style="padding: 8px 12px; white-space: nowrap; font: 500 13px \'{F}\', sans-serif; border-radius: {r}; background: {c0 if i == 0 else u["soft"]}; color: {("#FFFFFF" if k != "D" else "#14120E") if i == 0 else u["txt"]}">{t}</span>' for i, t in enumerate(('2-комн.', 'до [ЦЕНА]', 'Академический', 'Фильтры')))
    card = lambda im, p, d, tags: (f'<div style="margin: 14px 20px 0; background: {u["surf"]}; border: 1px solid {u["line"]}; border-radius: {r}; overflow: hidden">'
                                   f'<div style="height: 170px; position: relative; {"border-radius: 160px 160px 0 0; overflow: hidden; margin: 10px 10px 0" if k == "L" else ""}">{img(IMG[im], d)}'
                                   f'<span style="position: absolute; right: 10px; top: 10px; width: 34px; height: 34px; background: rgba(255,255,255,0.92); border-radius: 17px; display: flex; align-items: center; justify-content: center">{icon(v, 10, 18, "#1F1D1B")}</span></div>'
                                   f'<div style="padding: 12px 14px; display: flex; flex-direction: column; gap: 6px"><span style="font: 700 19px \'{F}\', sans-serif">{p}</span>'
                                   f'<span style="font: 400 13px \'{F}\', sans-serif; color: {u["mut"]}">{d}</span>'
                                   f'<div style="display: flex; gap: 6px">{"".join(f"<span style=\"padding: 4px 8px; background: {u["soft"]}; font: 500 11px {chr(39)}{F}{chr(39)}, sans-serif; border-radius: {max(0, u["r"] - 8)}px\">{t}</span>" for t in tags)}</div></div></div>')
    return f'''<div style="width: 375px; height: 812px; background: {u['bg']}; color: {u['txt']}; position: relative; overflow: hidden">
  {status(u)}
  <div style="padding: 4px 20px 0; display: flex; justify-content: space-between; align-items: center"><span style="font: {u['hw']} {24 if k != 'Y' else 20}px '{FH}', sans-serif; color: {v['dir'][0] if k == 'Y' else u['txt']}">Квартиры</span>
    <span style="display: flex; align-items: center; gap: 6px; font: 500 14px '{F}', sans-serif">{icon(v, 8, 20)}Карта</span></div>
  <div style="padding: 14px 20px 0; display: flex; gap: 8px; overflow: hidden">{chips}</div>
  <div style="padding: 12px 20px 0; font: 400 13px '{F}', sans-serif; color: {u['mut']}">[N] предложений</div>
  {card('living2', 'от [ЦЕНА] ₽', '2-комн. · [ПЛОЩАДЬ] м² · 7/12 эт. · Академический', ('Ипотека', 'С отделкой', 'Сдан'))}
  {card('kitchen', 'от [ЦЕНА] ₽', '2-комн. · [ПЛОЩАДЬ] м² · 4/9 эт. · Академический', ('Ремонт к переезду', 'Ипотека'))}
  {tabbar(v, 0)}
</div>'''


def screen_house(v):
    k = v['key']; u = UI[k]; F, FH, acc = v['F'], v['FH'], v['acc']
    r = f'{u["r"]}px'
    c = v['dir'][2] if k == 'Y' else acc
    stages = ('Фундамент', 'Цоколь и гидроизоляция', 'Стены 1 этажа', 'Стены 2 этажа', 'Кровля', 'Окна и двери', 'Инженерия и отделка')
    st = ''
    for i, n in enumerate(stages):
        done, cur = i < 3, i == 3
        dot_bg = c if done else (u['surf'] if not cur else c)
        mark_ = '✓' if done else ''
        st += (f'<div style="display: flex; gap: 12px; align-items: center; padding: 7px 0">'
               f'<span style="width: 22px; height: 22px; flex: none; border-radius: 11px; border: 2px solid {c if (done or cur) else u["line"]}; background: {dot_bg if done else "transparent"}; color: {"#FFFFFF" if k != "D" else "#14120E"}; font: 700 12px \'{F}\', sans-serif; display: flex; align-items: center; justify-content: center; box-sizing: border-box">{mark_}</span>'
               f'<span style="flex: 1; font: {600 if cur else 400} 14px \'{F}\', sans-serif; color: {u["txt"] if (done or cur) else u["mut"]}">{n}</span>'
               f'<span style="font: 400 12px \'{F}\', sans-serif; color: {u["mut"]}">{"готово" if done else ("идёт · 60%" if cur else "[ДАТА]")}</span></div>')
    return f'''<div style="width: 375px; height: 812px; background: {u['bg']}; color: {u['txt']}; position: relative; overflow: hidden">
  {status(u)}
  <div style="padding: 4px 20px 0; display: flex; justify-content: space-between; align-items: center"><span style="font: {u['hw']} {24 if k != 'Y' else 20}px '{FH}', sans-serif; color: {v['dir'][2] if k == 'Y' else u['txt']}">Мой дом</span><span style="font: 400 13px '{F}', sans-serif; color: {u['mut']}">договор № [N]</span></div>
  <div style="margin: 14px 20px 0; height: 190px; position: relative; overflow: hidden; border-radius: {'95px 95px 0 0' if k == 'L' else r}">{img(IMG['build'], 'Стройка дома, камера')}
    <span style="position: absolute; left: 10px; bottom: 10px; padding: 5px 9px; background: rgba(0,0,0,0.65); color: #FFFFFF; font: 600 12px '{F}', sans-serif">● LIVE · камера 24/7</span></div>
  <div style="padding: 10px 20px 0">{st}</div>
  <div style="margin: 8px 20px 0; padding: 12px 14px; background: {u['soft']}; border-radius: {r}; display: flex; justify-content: space-between; font: 400 13px '{F}', sans-serif"><span style="color: {u['mut']}">Следующий платёж</span><span style="font-weight: 600">[ДАТА] · [СУММА] ₽</span></div>
  {tabbar(v, 2)}
</div>'''


def iphone(screen_html, caption, v):
    u = UI[v['key']]
    return f'''<div style="display: flex; flex-direction: column; align-items: center; gap: 14px">
  <div style="width: 300px; height: 620px; border-radius: 50px; background: #111111; padding: 11px; box-sizing: border-box; box-shadow: 0 30px 60px rgba(0,0,0,0.28); border: 2px solid #3A3D43; position: relative">
    <div style="width: 278px; height: 598px; border-radius: 40px; overflow: hidden; position: relative; background: {u['bg']}">
      <div style="position: absolute; left: 0; top: 0; transform: scale(0.7413); transform-origin: 0 0">{screen_html}</div>
      <div style="position: absolute; left: 50%; top: 9px; width: 90px; height: 26px; margin-left: -45px; background: #000000; border-radius: 13px"></div>
    </div>
  </div>
  <span style="font: 400 14px '{v['F']}', sans-serif; color: {v['muted']}">{caption}</span>
</div>'''


def site_board(v):
    k = v['key']; F, acc, line, muted, ink = v['F'], v['acc'], v['line'], v['muted'], v['ink']
    h = 1580
    return head(f'{v["title"]} · {v["name"]} — сайт-приложение', v, h) + f'''<div style="width: 1440px; height: {h}px; box-sizing: border-box; padding: 48px 56px; background: {v['bg']}; color: {v['text']}; font-family: '{F}', system-ui, sans-serif; display: flex; flex-direction: column; gap: 28px; overflow: hidden">
  <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid {line}; padding-bottom: 16px">
    <div style="font: 500 30px '{F}', sans-serif; letter-spacing: -0.02em">{v['title']} · <span style="color: {acc if k != 'Y' else ink}">«{v['name']}»</span></div>
    <div style="font: 400 14px '{F}', sans-serif; color: {muted}">[ 04 · сайт на ноутбуке и приложение на iPhone ]</div>
  </div>
  {laptop(v)}
  <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1.05fr; gap: 24px; align-items: start">
    {iphone(screen_home(v), 'Главная: три направления и мой объект', v)}
    {iphone(screen_catalog(v), 'Каталог квартир с фильтрами', v)}
    {iphone(screen_house(v), 'Стройка дома: камера и этапы', v)}
    <div style="display: flex; flex-direction: column; gap: 14px; padding-top: 20px">
      <span style="font: 400 13px '{F}', sans-serif; color: {muted}">[ как устроено ]</span>
      <div style="font: 400 15px/1.55 '{F}', sans-serif">Сайт как у Домклика: поиск с фильтрами на первом экране, вкладки направлений, карточки с ценой и параметрами.</div>
      <div style="font: 400 15px/1.55 '{F}', sans-serif">Приложение — для тех, кто уже с нами: стройка в реальном времени, этапы, платежи и чат с прорабом.</div>
      <div style="font: 400 15px/1.55 '{F}', sans-serif; color: {muted}">Цены, площади и названия — заглушки до данных от заказчика.</div>
    </div>
  </div>
</div>
''' + tail(h)


if __name__ == '__main__':
    for k, v in V.items():
        open(OUT + f'System{k}.dc.html', 'w', encoding='utf8').write(system_board(v))
        open(OUT + f'Site{k}.dc.html', 'w', encoding='utf8').write(site_board(v))
    print('ok')
