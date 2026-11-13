"""Фото-мокапы для знака «П.» (красная точка). Reuses the compositor in mockups.py with new artwork.
Run: py -3 tools/mockups/p_mockups.py [surface ...]  → _source/gen/life_P_<surface>.jpg"""
import os, sys, types, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
# stub the old generator imports so mockups.py loads without them
sys.modules['marks'] = types.SimpleNamespace(mark_L=None, mark_D=None, mark_Y=None)
sys.modules['gen_v3'] = types.SimpleNamespace(V={}, lockup=None, fam=lambda v: v.get('fam', v['key']))
sys.path.insert(0, HERE)
import mockups as M  # noqa: E402

CHROME = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'
UD = os.path.join(os.environ.get('TEMP', 'C:/Temp'), 'p_mock_chrome')
M.EDGE = CHROME
M.ART = os.path.join(os.environ.get('TEMP', 'C:/Temp'), 'p_mock_art')   # ASCII path (cv2.imread)
os.makedirs(M.ART, exist_ok=True)
_run = subprocess.run
M.subprocess.run = lambda args, **kw: _run([args[0], f'--user-data-dir={UD}'] + list(args[1:]), **kw) if args and args[0] == CHROME else _run(args, **kw)

NIGHT, INK, MILK, RED, GRAY, SUB = '#0E0E0F', '#161617', '#F4F2EE', '#F5553C', '#ECEAE6', '#8A867F'
ARCH = 'M0 60 V24 A24 24 0 0 1 48 24 V60 H34 V24 A10 10 0 0 0 14 24 V60 Z'
V = dict(key='P', fam='P', F='Manrope', FH='Manrope', gf='family=Manrope:wght@300;400;500;600;800')


def mark(w, c=INK, dot=RED):
    return (f'<svg width="{w}" height="{w * 60 / 68:.1f}" viewBox="0 0 68 60" style="overflow:visible;display:block">'
            f'<path d="{ARCH}" fill="{c}"/><circle cx="61" cy="54" r="6" fill="{dot}"/></svg>')


def word(c, size, sub=SUB, align='center'):
    return (f'<div style="display:flex;flex-direction:column;align-items:{align}">'
            f'<div style="font:300 {size}px/1 Manrope,sans-serif;letter-spacing:.42em;margin-right:-.42em;color:{c};white-space:nowrap">ПЛАТФОРМА</div>'
            f'<div style="font:400 {size * .55:.1f}px/1 Manrope,sans-serif;letter-spacing:.5em;margin-right:-.5em;color:{sub};white-space:nowrap;margin-top:{size * .55:.0f}px">НЕДВИЖИМОСТИ</div></div>')


def v_lock(w, size, c=INK, dot=RED, sub=SUB):
    return f'<div style="display:flex;flex-direction:column;align-items:center;gap:{w * .3:.0f}px">{mark(w, c, dot)}{word(c, size, sub)}</div>'


def h_lock(w, size, c=INK, dot=RED, sub=SUB):
    return f'<div style="display:flex;align-items:center;gap:{w * .42:.0f}px">{mark(w, c, dot)}{word(c, size, sub, "flex-start")}</div>'


def art_html(v, surf):
    w, h = M.SURF[surf][1]
    C = lambda inner, extra='': f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;{extra}">{inner}</div>'
    dot = f'<span style="color:{RED}">.</span>'
    if surf == 'facade':
        body = C(v_lock(78, 26, MILK, RED, '#9A968F')) + f'<div style="position:absolute;left:0;right:0;bottom:0;height:7px;background:{RED}"></div>'
        return M.page(V, w, h, body, NIGHT)
    if surf == 'billboard':
        body = (f'<div style="position:absolute;inset:0;background:{MILK};padding:34px 40px;box-sizing:border-box;display:flex;justify-content:space-between;align-items:stretch">'
                f'<div style="font:500 64px/1.0 Manrope,sans-serif;letter-spacing:-.03em;color:{INK}">Квартира{dot}<br>Дом{dot}<br>Ремонт{dot}</div>'
                f'<div style="display:flex;flex-direction:column;justify-content:space-between;align-items:flex-end">'
                f'<div style="width:150px;height:150px;border-radius:14px;background:{RED};display:flex;align-items:center;justify-content:center">{mark(86, MILK, INK)}</div>'
                f'{word(INK, 15, SUB, "flex-end")}</div></div>')
        return M.page(V, w, h, body, MILK)
    if surf == 'keys':
        return M.page(V, w, h, f'<div style="position:absolute;left:0;right:0;top:{round(h * .32)}px;display:flex;justify-content:center">{v_lock(62, 12)}</div>')
    if surf == 'helmet':
        return M.page(V, w, h, C(h_lock(46, 15)))
    if surf == 'bag':
        return M.page(V, w, h, f'<div style="position:absolute;left:0;right:0;top:{round(h * .44)}px;display:flex;justify-content:center">{v_lock(86, 16)}</div>')
    if surf == 'fence':
        body = (f'<div style="position:absolute;inset:0;background:{RED};display:flex;align-items:center;justify-content:space-between;padding:0 64px 0 70px;box-sizing:border-box">'
                f'{h_lock(80, 30, MILK, INK, "#FFE1DA")}'
                f'<div style="display:flex;align-items:center;gap:34px"><div style="font:500 40px/1.05 Manrope,sans-serif;letter-spacing:-.02em;color:{MILK};text-align:right">Этот дом<br>проверен<span style="color:{INK}">.</span></div>'
                f'<span style="padding:22px 34px;border-radius:999px;background:{MILK};color:{INK};font:600 24px Manrope,sans-serif;white-space:nowrap">+7 965 500-29-18</span></div></div>')
        return M.page(V, w, h, body, RED)
    if surf == 'store':
        return M.page(V, w, h, C(h_lock(70, 26)))
    if surf == 'plate':
        rows = (('Объект', 'Индивидуальный жилой дом'), ('Материал', 'кирпич, 2 этажа'), ('Заказчик', '[ФИО]'), ('Подрядчик', '[НАЗВАНИЕ]'), ('Проверено', 'ПЛАТФОРМА НЕДВИЖИМОСТИ'),
                ('Начало работ', '[ДАТА]'), ('Окончание', '[ДАТА]'), ('Прораб', '[ФИО]'), ('Телефон', '+7 965 500-29-18'))
        rr = ''.join(f'<div style="display:flex;justify-content:space-between;gap:8px;padding:5px 0;border-bottom:1px solid #D9D5CE;font:400 10.5px Manrope,sans-serif"><span style="color:#6E6A63">{a}</span><span style="color:{INK};text-align:right">{b}</span></div>' for a, b in rows)
        body = (f'<div style="position:absolute;left:30px;right:30px;top:34px;bottom:34px;display:flex;flex-direction:column;gap:12px">'
                f'<div style="height:6px;flex:none;background:{RED}"></div>{h_lock(30, 11)}'
                f'<div style="font:600 19px Manrope,sans-serif;color:{INK}">Паспорт объекта<span style="color:{RED}">.</span></div><div>{rr}</div></div>')
        return M.page(V, w, h, body)
    if surf == 'vest':
        return M.page(V, w, h, C(v_lock(66, 16, '#FFFFFF', '#FFFFFF', '#FFFFFF')))
    raise KeyError(surf)


M.art_html = art_html

if __name__ == '__main__':
    for s in (sys.argv[1:] or list(M.SURF)):
        print(M.composite(V, s), flush=True)
