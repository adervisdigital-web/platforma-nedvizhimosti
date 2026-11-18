"""Демо-подробности квартир: схемы планировок (SVG), площади комнат, описание, фото.
Пишет site/public/assets/img/plans/apt-<id>.svg и site/data/seed/apartment_details.json.
Run из корня репо: py -3 -X utf8 site/tools/gen_apartment_details.py
Схемы — демонстрационные (как и сами демо-квартиры); у настоящих объектов менеджер загружает планировку застройщика."""
import json, os, math

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(S, 'public', 'assets', 'img', 'plans')
os.makedirs(OUT, exist_ok=True)

LIVING = {'Комната', 'Гостиная', 'Спальня', 'Детская', 'Кабинет', 'Комната-студия'}
HALL = {'Прихожая', 'Коридор'}
WET = {'Санузел', 'Ванная', 'Туалет'}

# Раскладки в условных единицах: (название, x, y, w, h). Верхний ряд — окна наверх, лоджия над комнатой `balc`.
L = {
    0: dict(W=6.4, H=5.5, balc='Комната-студия', rooms=[('Комната-студия', 0, 0, 6.4, 3.8), ('Прихожая', 0, 3.8, 3.9, 1.7), ('Санузел', 3.9, 3.8, 2.5, 1.7)]),
    1: dict(W=8.0, H=5.9, balc='Комната', rooms=[('Комната', 0, 0, 4.4, 4.0), ('Кухня', 4.4, 0, 3.6, 4.0), ('Прихожая', 0, 4.0, 5.2, 1.9), ('Санузел', 5.2, 4.0, 2.8, 1.9)]),
    2: dict(W=10.4, H=6.1, balc='Гостиная', rooms=[('Спальня', 0, 0, 3.8, 4.3), ('Гостиная', 3.8, 0, 3.8, 4.3), ('Кухня', 7.6, 0, 2.8, 4.3),
                                                   ('Санузел', 0, 4.3, 2.6, 1.8), ('Прихожая', 2.6, 4.3, 5.2, 1.8), ('Гардероб', 7.8, 4.3, 2.6, 1.8)]),
    '2s': dict(W=10.4, H=6.1, balc='Гостиная', rooms=[('Спальня', 0, 0, 3.8, 4.3), ('Гостиная', 3.8, 0, 3.8, 4.3), ('Кухня', 7.6, 0, 2.8, 4.3),
                                                     ('Ванная', 0, 4.3, 2.6, 1.8), ('Прихожая', 2.6, 4.3, 6.4, 1.8), ('Туалет', 9.0, 4.3, 1.4, 1.8)]),
    3: dict(W=12.0, H=8.1, balc='Гостиная', rooms=[('Спальня', 0, 0, 4.0, 4.2), ('Гостиная', 4.0, 0, 4.4, 4.2), ('Кухня', 8.4, 0, 3.6, 4.2), ('Коридор', 0, 4.2, 12.0, 1.0),
                                                   ('Детская', 0, 5.2, 4.2, 2.9), ('Прихожая', 4.2, 5.2, 3.0, 2.9), ('Ванная', 7.2, 5.2, 3.2, 2.9), ('Туалет', 10.4, 5.2, 1.6, 2.9)]),
    4: dict(W=14.0, H=8.4, balc='Гостиная', rooms=[('Спальня', 0, 0, 4.4, 4.4), ('Гостиная', 4.4, 0, 5.0, 4.4), ('Кухня', 9.4, 0, 4.6, 4.4), ('Коридор', 0, 4.4, 14.0, 1.0),
                                                   ('Детская', 0, 5.4, 4.0, 3.0), ('Кабинет', 4.0, 5.4, 3.4, 3.0), ('Прихожая', 7.4, 5.4, 2.8, 3.0), ('Ванная', 10.2, 5.4, 2.4, 3.0), ('Туалет', 12.6, 5.4, 1.4, 3.0)]),
}

# Демо-подробности по id квартиры (из seed/apartments.json): раскладка, отзеркалить, потолки, балкон, вид, фото, особенности для описания.
D = {
    1: dict(lay='2s', mir=0, ceil=2.8, balc='лоджия', view='во двор и на парк', ph=['kv_living2', 'kv_kitchen2', 'kv_bedroom2', 'rem_bathroom'], note='окна гостиной выходят на парк, двор без машин'),
    2: dict(lay=1, mir=1, ceil=2.7, balc='балкон', view='во двор', ph=['kv_empty', 'kv_building', 'zhk'], note='светлая комната с большими окнами, удобная квадратная кухня'),
    3: dict(lay=3, mir=0, ceil=2.8, balc='лоджия', view='на город', ph=['kv_kids', 'kv_living3', 'kv_kitchen', 'kv_bedroom'], note='отдельная детская, школа и детский сад во дворе'),
    4: dict(lay=2, mir=1, ceil=3.0, balc='балкон', view='на тихую улицу', ph=['kv_bedroom2', 'kv_living2', 'kv_kitchen2'], note='высокие потолки, центр города в шаговой доступности'),
    5: dict(lay='2s', mir=0, ceil=2.7, balc='лоджия', view='во двор', ph=['rem_bathroom', 'kv_living3', 'kv_bedroom', 'kv_kitchen'], note='свежий ремонт от нашей бригады с гарантией 5 лет'),
    6: dict(lay=0, mir=1, ceil=2.75, balc='лоджия', view='на город, высокий этаж', ph=['kv_building', 'kv_empty', 'zhk'], note='высокий этаж и вид на город, удобно под сдачу'),
    7: dict(lay=2, mir=0, ceil=2.8, balc='лоджия', view='на Исеть', ph=['kv_complex2', 'kv_empty', 'zhk'], note='вид на Исеть, рядом набережная и Ботанический сад'),
    8: dict(lay=1, mir=0, ceil=2.6, balc='балкон', view='во двор', ph=['kv_bedroom', 'kv_kitchen2', 'kv_living2'], note='ухоженный дом, рядом остановки и магазины'),
    9: dict(lay=0, mir=0, ceil=2.8, balc='нет', view='во двор', ph=['kv_studio', 'kv_kitchen2', 'rem_bathroom'], note='готовая студия с отделкой: можно заезжать или сдавать'),
    10: dict(lay=1, mir=1, ceil=2.8, balc='лоджия', view='на реку и лес', ph=['kv_kitchen2', 'kv_bedroom2', 'kv_living2'], note='рядом лесопарк и река, тихий район'),
    11: dict(lay=4, mir=0, ceil=3.0, balc='два балкона', view='на две стороны', ph=['kv_living3', 'kv_kitchen', 'kv_bedroom2', 'kv_kids'], note='окна на две стороны, отдельный кабинет'),
    12: dict(lay=3, mir=1, ceil=2.8, balc='лоджия', view='на парк', ph=['kv_kitchen', 'kv_living2', 'kv_kids', 'kv_bedroom'], note='большая кухня 12+ м², рядом парк'),
}
ROOMS_RU = {0: 'Студия', 1: 'Однокомнатная квартира', 2: 'Двухкомнатная квартира', 3: 'Трёхкомнатная квартира', 4: 'Четырёхкомнатная квартира'}


def fmt(v, d=1):
    return f'{v:.{d}f}'.replace('.', ',')


def svg_plan(lay, mirror, total):
    W, H = lay['W'], lay['H']
    rooms = [(n, (W - x - w) if mirror else x, y, w, h) for n, x, y, w, h in lay['rooms']]
    s2 = total / (W * H); s = math.sqrt(s2)                                   # м² на кв. единицу, м на единицу
    areas = [round(w * h * s2, 1) for _, _, _, w, h in rooms]
    areas[-1] = round(total - sum(areas[:-1]), 1)                             # сумма ровно = общей площади
    P = 0.9; balc_h = 1.15 if lay.get('balc_on', True) else 0
    vx, vy, vw, vh = -P, -P - balc_h, W + 2 * P, H + 2 * P + balc_h + 0.3
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx} {vy:.2f} {vw} {vh:.2f}" font-family="Manrope, Segoe UI, Arial, sans-serif">',
         '<defs><pattern id="h" width=".28" height=".28" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2=".28" stroke="#C9C4BC" stroke-width=".05"/></pattern></defs>',
         f'<rect x="{vx}" y="{vy:.2f}" width="{vw}" height="{vh:.2f}" fill="#fff"/>']
    # лоджия / балкон над комнатой
    bal = None
    for n, x, y, w, h in rooms:
        if n == lay.get('balc') and balc_h:
            bw = w * .78; bx = x + (w - bw) / 2; bal = (bx, -balc_h, bw, balc_h)
            o.append(f'<rect x="{bx:.2f}" y="{-balc_h:.2f}" width="{bw:.2f}" height="{balc_h:.2f}" fill="url(#h)" stroke="#161617" stroke-width=".06"/>')
    fill = lambda n: '#EEF1F2' if n in WET else ('#F6F4F0' if n in HALL or n == 'Гардероб' else '#fff')
    for n, x, y, w, h in rooms:
        o.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill(n)}" stroke="#161617" stroke-width=".1"/>')
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#161617" stroke-width=".26"/>')
    d = 0.82 / s                                                              # дверь 82 см
    def gap_h(x0, y0, w0, t):   # разрыв горизонтальной стены
        o.append(f'<rect x="{x0:.2f}" y="{y0 - t / 2:.2f}" width="{w0:.2f}" height="{t:.2f}" fill="#fff"/>')
    def gap_v(x0, y0, h0, t):
        o.append(f'<rect x="{x0 - t / 2:.2f}" y="{y0:.2f}" width="{t:.2f}" height="{h0:.2f}" fill="#fff"/>')
    def door(room, other):
        n, x, y, w, h = room; m, X, Y, Wd, Hd = other
        out = -1 if n in WET or n == 'Гардероб' else 1          # санузлы и гардероб открываются наружу
        # горизонтальная граница
        for yy, inside in ((y + h, -1), (y, 1)):
            if abs(yy - (Y if inside == -1 else Y + Hd)) < 1e-6:
                a, b = max(x, X), min(x + w, X + Wd)
                if b - a >= d + .3:
                    x0 = a + .2 if (a + b) / 2 > W / 2 or True else b - .2 - d
                    gap_h(x0, yy, d, .14)
                    sg = inside * out; sy = sg * d
                    o.append(f'<path d="M{x0:.2f} {yy:.2f} v{sy:.2f} A{d:.2f} {d:.2f} 0 0 {1 if sg == -1 else 0} {x0 + d:.2f} {yy:.2f}" fill="none" stroke="#8A857C" stroke-width=".04"/>')
                    return True
        for xx, inside in ((x + w, -1), (x, 1)):
            if abs(xx - (X if inside == -1 else X + Wd)) < 1e-6:
                a, b = max(y, Y), min(y + h, Y + Hd)
                if b - a >= d + .3:
                    y0 = a + .2
                    gap_v(xx, y0, d, .14)
                    sg = inside * out; sx = sg * d
                    o.append(f'<path d="M{xx:.2f} {y0:.2f} h{sx:.2f} A{d:.2f} {d:.2f} 0 0 {0 if sg == -1 else 1} {xx:.2f} {y0 + d:.2f}" fill="none" stroke="#8A857C" stroke-width=".04"/>')
                    return True
        return False
    for r in rooms:
        if r[0] in HALL: continue
        order = [q for q in rooms if q[0] in HALL] + [q for q in rooms if q[0] in ('Гостиная', 'Комната-студия')]
        for q in order:
            if q is not r and door(r, q): break
    # окна: верхний ряд — наверх, нижние жилые — вниз
    def win_h(x0, w0, yy):
        ww = min(w0 * .5, 1.9 / s); xw = x0 + (w0 - ww) / 2
        gap_h(xw, yy, ww, .3)
        o.append(f'<rect x="{xw:.2f}" y="{yy - .13:.2f}" width="{ww:.2f}" height=".26" fill="#fff" stroke="#161617" stroke-width=".04"/>'
                 f'<line x1="{xw:.2f}" y1="{yy:.2f}" x2="{xw + ww:.2f}" y2="{yy:.2f}" stroke="#161617" stroke-width=".03"/>')
    for n, x, y, w, h in rooms:
        if y == 0 and n not in HALL and n not in WET: win_h(x, w, 0)
        if abs(y + h - H) < 1e-6 and (n in LIVING or n == 'Кухня'): win_h(x, w, H)
    if bal:   # выход на лоджию
        bx, by, bw, bh = bal; gap_h(bx + bw - .3 - d, 0, d, .3)
    # вход: из прихожей вниз (или вбок), красная точка
    hall = [r for r in rooms if r[0] == 'Прихожая'][0]
    n, x, y, w, h = hall
    ex = x + w / 2 - d / 2
    gap_h(ex, H, d + .1, .3)
    o.append(f'<circle cx="{ex + d / 2:.2f}" cy="{H + .55:.2f}" r=".2" fill="#F5553C"/><text x="{ex + d / 2 + .38:.2f}" y="{H + .66:.2f}" font-size=".32" fill="#6B675F">вход</text>')
    # подписи
    for (n, x, y, w, h), ar in zip(rooms, areas):
        cx, cy = x + w / 2, y + h / 2
        k = max(.75, W / 9)
        small = w < 2.2 or h < 1.6
        fs = (.27 if small else .36) * k
        label = n if not (small and len(n) > 7) else n[:6] + '.'
        o.append(f'<text x="{cx:.2f}" y="{cy - .06:.2f}" text-anchor="middle" font-size="{fs}" fill="#6B675F">{label}</text>'
                 f'<text x="{cx:.2f}" y="{cy + fs + .08:.2f}" text-anchor="middle" font-size="{fs * 1.2:.2f}" font-weight="700" fill="#161617">{fmt(ar)}</text>')
    if bal:
        bx, by, bw, bh = bal
        o.append(f'<text x="{bx + bw / 2:.2f}" y="{by + bh / 2 + .1:.2f}" text-anchor="middle" font-size=".28" fill="#6B675F">лоджия</text>')
    o.append('</svg>')
    return '\n'.join(o), dict(zip([r[0] for r in rooms], areas))


apts = json.load(open(os.path.join(S, 'data', 'seed', 'apartments.json'), encoding='utf8'))
out = {}
for a in apts:
    dd = D[a['id']]
    lay = dict(L[dd['lay']]); lay['balc_on'] = dd['balc'] != 'нет'
    svg, ar = svg_plan(lay, dd['mir'], float(a['area']))
    name = f"apt-{a['id']}.svg"
    open(os.path.join(OUT, name), 'w', encoding='utf8', newline='\n').write(svg)
    living = round(sum(v for k, v in ar.items() if k in LIVING), 1)
    kitchen = ar.get('Кухня')
    bath = 'раздельный' if 'Туалет' in ar else 'совмещённый'
    where = a['complex'] and f"в {a['complex'].replace('ЖК ', 'ЖК «')}»" or f"на {a['address']}"
    kind = ROOMS_RU[a['rooms']]
    p1 = (f"{kind} {fmt(a['area'])} м² на {a['floor']} этаже {a['floors']}-этажного дома {where}, район {a['district']}. "
          + (f"Кухня {fmt(kitchen)} м², жилая площадь {fmt(living)} м². " if kitchen else f"Жилая зона {fmt(living)} м² с кухонным уголком. ")
          + f"Потолки {fmt(dd['ceil'], 2).rstrip('0').rstrip(',')} м, санузел {bath}" + (f", {dd['balc']}" if dd['balc'] != 'нет' else '') + f", окна {dd['view']}.")
    p2 = dd['note'][0].upper() + dd['note'][1:] + '. ' + (
        'Отделка от застройщика: можно заезжать сразу после сделки.' if a['finish'] == 'with' and a['market'] == 'new' else
        'Квартира с ремонтом, юрист проверил историю и документы.' if a['market'] == 'secondary' else
        'Без отделки: посчитаем ремонт под ключ по нашей смете — цена фиксируется в договоре.')
    p3 = 'Покажем квартиру в удобное время, поможем с ипотекой и проверим документы до сделки. Описание демонстрационное.'
    out[a['id']] = dict(living_area=living, kitchen_area=kitchen, ceiling=dd['ceil'], bathroom=bath, balcony=dd['balc'], view=dd['view'],
                        photos=dd['ph'], plans=[f'plans/{name}'], description=p1 + '\n\n' + p2 + '\n\n' + p3)
    print(a['id'], name, ar)
json.dump(out, open(os.path.join(S, 'data', 'seed', 'apartment_details.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('ok:', len(out))
