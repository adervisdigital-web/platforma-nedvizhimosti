"""Перевод всех генераторов и сайта на знак D «Высокая дверь».
Геометрия: viewBox 0 0 76 72; арка R24 (центр 24,24), ножки 15, проём r9 (центр 24,26), высота 72; точка Ø18 (67,63) с зазором 10.
Run из корня репо: py -3 tools/patches/mark_D.py"""
OLD_ARCH = 'M0 60 V24 A24 24 0 0 1 48 24 V60 H34 V24 A10 10 0 0 0 14 24 V60 Z'
NEW_ARCH = 'M0 72 V24 A24 24 0 0 1 48 24 V72 H33 V26 A9 9 0 0 0 15 26 V72 Z'
OLD_DOT = '<circle cx="61" cy="54" r="6"'
NEW_DOT = '<circle cx="67" cy="63" r="9"'


def patch(p, extra=()):
    s = open(p, encoding='utf8').read()
    n0 = s.count(OLD_ARCH)
    s = s.replace(OLD_ARCH, NEW_ARCH).replace(OLD_DOT, NEW_DOT)
    s = s.replace('w * 60 / 68', 'w * 72 / 76').replace('viewBox="0 0 68 60"', 'viewBox="0 0 76 72"')
    for a, b in extra:
        assert s.count(a) >= 1, (p, a[:60])
        s = s.replace(a, b)
    open(p, 'w', encoding='utf8').write(s)
    print(p, 'arch:', n0)


CONS_PRESENT_OLD_START = 'def construction(s=7.4):'
CONS_PRESENT_NEW = '''def construction(s=6.6):
    L = '#B9B4AB'
    g = ''
    for x in (0, 15, 24, 33, 48, 58, 76):
        g += f'<line x1="{x}" y1="-8" x2="{x}" y2="80" stroke="{L}" stroke-width=".18" stroke-dasharray=".8 .9"/>'
    for y in (0, 24, 26, 54, 72):
        g += f'<line x1="-8" y1="{y}" x2="84" y2="{y}" stroke="{L}" stroke-width=".18" stroke-dasharray=".8 .9"/>'
    g += (f'<circle cx="24" cy="24" r="24" fill="none" stroke="{RED}" stroke-width=".22"/><circle cx="24" cy="26" r="9" fill="none" stroke="{RED}" stroke-width=".22"/>'
          f'<circle cx="24" cy="24" r=".7" fill="{RED}"/>')
    t = 'font-family="Manrope" font-size="2.3" letter-spacing=".05"'
    notes = (f'<text x="24" y="-10" {t} fill="{SUB}" text-anchor="middle">R 24 · проём r 9</text>'
             f'<text x="7.5" y="77" {t} fill="{SUB}" text-anchor="middle">15</text><text x="40.5" y="77" {t} fill="{SUB}" text-anchor="middle">15</text>'
             f'<text x="24" y="77" {t} fill="{SUB}" text-anchor="middle">18</text>'
             f'<text x="53" y="77" {t} fill="{SUB}" text-anchor="middle">10</text>'
             f'<text x="67" y="77" {t} fill="{RED}" text-anchor="middle">Ø 18 = точка</text>'
             f'<text x="-7" y="49" {t} fill="{SUB}" transform="rotate(-90 -7 49)" text-anchor="middle">высота 72 = 4 точки</text>')
    return (f'<svg width="{92 * s:.0f}" height="{94 * s:.0f}" viewBox="-10 -14 92 94" role="img" aria-label="Построение знака">'
            f'<path d="{ARCH}" fill="{INK}"/><circle cx="67" cy="63" r="9" fill="{RED}"/>{g}{notes}</svg>')


'''

p = 'tools/p_present.py'
s = open(p, encoding='utf8').read()
i = s.index(CONS_PRESENT_OLD_START); j = s.index('def pattern(', i)
s = s[:i] + CONS_PRESENT_NEW + s[j:]
s = s.replace('k = cell * .6 / 68', 'k = cell * .56 / 76')
open(p, 'w', encoding='utf8').write(s)
patch(p, [
    ('Свод построен на двух окружностях с общим центром.', 'Высокий узкий проём — силуэт входной двери.'),
    ('Стоит на базовой линии, Ø 12 — чуть тоньше ножки «П».', 'Стоит на базовой линии, Ø 18 — крупнее ножки «П» и отделена от неё зазором.'),
])

p = 'tools/p_dot.py'
s = open(p, encoding='utf8').read()
i = s.index('def construction():'); j = s.index('def page(', i)
s = s[:i] + '''def construction():
    s = 4.6  # px per unit
    g = ''
    for x in (0, 15, 24, 33, 48, 58, 76):
        g += f'<line x1="{x}" y1="-6" x2="{x}" y2="78" stroke="{SAND}" stroke-width=".25" stroke-dasharray="1 1.2"/>'
    for y in (0, 24, 26, 54, 72):
        g += f'<line x1="-6" y1="{y}" x2="82" y2="{y}" stroke="{SAND}" stroke-width=".25" stroke-dasharray="1 1.2"/>'
    g += f'<circle cx="24" cy="24" r="24" fill="none" stroke="{SAND}" stroke-width=".3"/><circle cx="24" cy="26" r="9" fill="none" stroke="{SAND}" stroke-width=".3"/>'
    notes = (f'<text x="24" y="-9" font-size="3" fill="{SAND}" text-anchor="middle" font-family="Manrope">R 24 · r 9</text>'
             f'<text x="7.5" y="77" font-size="3" fill="{SAND}" text-anchor="middle" font-family="Manrope">15</text>'
             f'<text x="67" y="77" font-size="3" fill="{PEACH}" text-anchor="middle" font-family="Manrope">● 18</text>')
    return (f'<svg width="{88 * s}" height="{92 * s}" viewBox="-6 -12 88 92" role="img" aria-label="Построение знака">'
            f'<path d="{ARCH}" fill="{MILK}" fill-opacity=".92"/><circle cx="67" cy="63" r="9" fill="{PEACH}"/>{g}{notes}</svg>')


''' + s[j:]
open(p, 'w', encoding='utf8').write(s)
patch(p)

for p in ('tools/p_life.py', 'tools/p_hub.py', 'tools/mockups/p_mockups.py'):
    patch(p)

p = '08_Сайт_пример/index.html'
s = open(p, encoding='utf8').read()
s = s.replace('<symbol id="mark" viewBox="0 0 68 60"><path d="' + OLD_ARCH + '"/><circle cx="61" cy="54" r="6"',
              '<symbol id="mark" viewBox="0 0 76 72"><path d="' + NEW_ARCH + '"/><circle cx="67" cy="63" r="9"')
s = s.replace(OLD_ARCH, NEW_ARCH).replace('<circle cx="61" cy="54" r="6"', '<circle cx="67" cy="63" r="9"')
s = s.replace('viewBox="0 0 68 60"', 'viewBox="0 0 76 72"')
open(p, 'w', encoding='utf8').write(s)
print(p, 'ok', s.count(NEW_ARCH))

p = 'DESIGN.md'
s = open(p, encoding='utf8').read()
s = s.replace('скруглённая «П»-арка (R 24, r 10, ножки 14) + красная точка Ø12',
              'знак D «Высокая дверь» (с 2026-11-13): «П»-арка 48×72 (R 24, ножки 15, узкий проём r 9) + красная точка Ø18 с зазором 10 на базовой линии')
open(p, 'w', encoding='utf8').write(s)
print('done')
