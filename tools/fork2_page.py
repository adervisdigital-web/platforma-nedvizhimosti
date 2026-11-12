"""Развилка 2: знаки в эстетике, которую прислал клиент (тонкая линия, тёмный фон, разрядка, одна находка).
Run: py -3 tools/fork2_page.py → 05_Под_вкус_клиента/index.html"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '05_Под_вкус_клиента')
os.makedirs(OUT, exist_ok=True)

WORD = lambda c, size=15, ls='.42em', w=300: (f'<div style="font:{w} {size}px/1 Manrope,sans-serif;letter-spacing:{ls};margin-right:-{ls};color:{c};white-space:nowrap">ПЛАТФОРМА</div>')
SUB = lambda c, size=8.5: (f'<div style="font:400 {size}px/1 Manrope,sans-serif;letter-spacing:.5em;margin-right:-.5em;color:{c};white-space:nowrap;margin-top:9px">НЕДВИЖИМОСТЬ</div>')


def svg(w, vb, inner, label):
    W, H = [float(x) for x in vb.split()[2:]]
    return f'<svg width="{w}" height="{w * H / W:.1f}" viewBox="{vb}" role="img" aria-label="{label}" style="overflow:visible">{inner}</svg>'


def stack(mark, word, sub, gap=26):
    return f'<div style="display:flex;flex-direction:column;align-items:center;gap:{gap}px">{mark}<div style="display:flex;flex-direction:column;align-items:center">{word}{sub}</div></div>'


TILES = []

# 1 · «П.» — плотная скруглённая арка + точка-акцент («вы здесь»)
TILES.append(dict(
    n='1', name='«П.»', bg='#0E0E0F',
    idea='Скруглённая «П» — арка входа. Точка — это вы: дом, в котором поставили точку в поиске.',
    html=stack(svg(86, '0 0 68 60', '<path d="M0 60 V24 A24 24 0 0 1 48 24 V60 H34 V24 A10 10 0 0 0 14 24 V60 Z" fill="#F4F1EC"/>'
                                     '<circle cx="61" cy="54" r="6" fill="#E3A57A"/>', 'Знак П с точкой'),
               WORD('#F4F1EC'), SUB('#8D8A85'))))

# 2 · «Порог-линия» — тонкая арка и окно, как в любимом знаке с домиком
TILES.append(dict(
    n='2', name='Линия-дом', bg='#141416',
    idea='Одна тонкая линия рисует арку и землю, в проёме — светящееся окно. Тепло дома в минимуме средств.',
    html=stack(svg(96, '0 0 60 46', '<path d="M2 45 H58" stroke="#E8B48A" stroke-width="1.4" fill="none"/>'
                                    '<path d="M14 45 V20 A16 16 0 0 1 46 20 V45" stroke="#E8B48A" stroke-width="1.4" fill="none"/>'
                                    '<g fill="#E8B48A"><rect x="26.4" y="27" width="3" height="3"/><rect x="30.6" y="27" width="3" height="3"/>'
                                    '<rect x="26.4" y="31.2" width="3" height="3"/><rect x="30.6" y="31.2" width="3" height="3"/></g>', 'Арка и окно линией'),
               WORD('#EDE6DC'), SUB('#8A847B'))))

# 3 · «П-арка в слове» — как TOWER: находка внутри самого слова
arch_letter = ('<svg width="17" height="21" viewBox="0 0 30 37" style="display:inline-block;margin-right:.42em;margin-bottom:2px" aria-label="П">'
               '<path d="M2.5 37 V14.5 A12.5 12.5 0 0 1 27.5 14.5 V37" stroke="#C9A66B" stroke-width="3.2" fill="none"/></svg>')
TILES.append(dict(
    n='3', name='Буква-арка', bg='#3A3936',
    idea='Отдельного знака нет: первая «П» в слове — тонкая латунная арка. Узнаётся, как TOWER из ваших примеров.',
    html=(f'<div style="display:flex;flex-direction:column;align-items:center"><div style="font:300 22px/1 Manrope,sans-serif;letter-spacing:.42em;margin-right:-.42em;color:#EDEAE4;white-space:nowrap;display:flex;align-items:flex-end">'
          f'{arch_letter}ЛАТФОРМА</div>{SUB("#A49E92", 9)}</div>')))

# 4 · «Платформа» — линия-основа, которая поднимается в арку (как ZERO LIMITS)
TILES.append(dict(
    n='4', name='Линия платформы', bg='#1B2333',
    idea='Ровная линия — платформа, основа. В одном месте она поднимается аркой: вход в ваш дом. Красная точка — ваш адрес.',
    html=stack(svg(150, '0 0 120 40', '<path d="M0 38 H42 V20 A18 18 0 0 1 78 20 V38 H120" stroke="#E9EDF3" stroke-width="1.6" fill="none"/>'
                                      '<circle cx="60" cy="31" r="2.6" fill="#E25B4C"/>', 'Линия с аркой'),
               WORD('#E9EDF3'), SUB('#8C97A8'))))

# 5 · «Три арки» — квартиры, ремонт, дома (как DOMINOS: тонкие пересечения)
TILES.append(dict(
    n='5', name='Три арки', bg='#FFFFFF',
    idea='Три тонкие арки — квартиры, ремонт, дома. Пересекаются, потому что это одна компания и один путь.',
    html=stack(svg(96, '0 0 74 46', '<path d="M2 45 V22 A16 16 0 0 1 34 22 V45" stroke="#1F3A5F" stroke-width="1.5" fill="none"/>'
                                    '<path d="M21 45 V22 A16 16 0 0 1 53 22 V45" stroke="#C4553B" stroke-width="1.5" fill="none"/>'
                                    '<path d="M40 45 V22 A16 16 0 0 1 72 22 V45" stroke="#2F6B57" stroke-width="1.5" fill="none"/>', 'Три арки'),
               WORD('#2A2B2E'), SUB('#8A8C90'))))

# 6 · «Рамка с проёмом» — как CITY CASA: тонкая рамка, в которой вырезан вход
frame = ('<svg width="250" height="92" viewBox="0 0 250 92" role="img" aria-label="Рамка с арочным проёмом">'
         '<path d="M30 91 H1 V1 H249 V91 H62 V72 A16 16 0 0 0 30 72 Z" stroke="#E6DED2" stroke-width="1.3" fill="none"/>'
         '<text x="84" y="44" font-family="Manrope" font-weight="300" font-size="15" letter-spacing="4.6" fill="#E6DED2">ПЛАТФОРМА</text>'
         '<text x="84" y="62" font-family="Manrope" font-weight="400" font-size="7" letter-spacing="3.9" fill="#B8AE9F">НЕДВИЖИМОСТЬ</text></svg>')
TILES.append(dict(
    n='6', name='Рамка с проёмом', bg='#5A564C',
    idea='Тонкая рамка — участок, план, витрина. В углу вырезан арочный вход: всё, что внутри, — ваше.',
    html=frame))


def page():
    tiles = ''.join(f'<figure><div class="tile" style="background:{t["bg"]}">{t["html"]}</div>'
                    f'<figcaption><b>{t["n"]} · {t["name"]}</b><span>{t["idea"]}</span></figcaption></figure>' for t in TILES)
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Знаки под вкус клиента</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#F3F1ED;color:#1F1D1B;font:400 16px/1.5 Manrope,system-ui,sans-serif}}
.wrap{{max-width:1440px;margin:0 auto;padding:56px 56px 64px}}
h1{{font:800 42px/1.05 Manrope,sans-serif;letter-spacing:-.02em;margin:0 0 10px}}
p.lead{{margin:0 0 30px;color:#6F6A62;max-width:900px;font-size:17px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}
figure{{margin:0}}
.tile{{aspect-ratio:4/3;border-radius:14px;display:flex;align-items:center;justify-content:center;border:1px solid #0000000f}}
figcaption{{padding:12px 4px 0}}figcaption b{{display:block;font:700 16px Manrope,sans-serif}}figcaption span{{display:block;color:#6F6A62;font-size:14px;line-height:1.45}}
.ask{{margin-top:30px;background:#1F1D1B;color:#F2EEE7;border-radius:16px;padding:20px 24px;font:600 19px/1.4 Manrope,sans-serif}}.ask span{{color:#E8B48A}}
@media(max-width:900px){{.wrap{{padding:28px 16px}}.grid{{grid-template-columns:1fr 1fr}}h1{{font-size:30px}}}}
@media(max-width:560px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<h1>Знаки в вашем вкусе</h1>
<p class="lead">По логотипам, которые вам нравятся: тонкая линия, тёмный фон, слово с большой разрядкой и одна находка. Все шесть — про арку-вход и платформу-основу.</p>
<div class="grid">{tiles}</div>
<div class="ask">Какой ближе? Ответьте номером — <span>например, «4», или «2, но на синем»</span>.</div>
</div></body></html>'''


if __name__ == '__main__':
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(page())
    print('ok')
