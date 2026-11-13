"""«П.» — логотип и система. Run: py -3 tools/p_dot.py → 06_П_точка/index.html"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '06_П_точка')
os.makedirs(OUT, exist_ok=True)

NIGHT, GRAPH, MILK, PEACH, SAND, INK = '#0E0E0F', '#1C1C1E', '#F4F2EE', '#F5553C', '#9A968F', '#161617'
LIGHT = '#ECEAE6'
ARCH = 'M0 60 V24 A24 24 0 0 1 48 24 V60 H34 V24 A10 10 0 0 0 14 24 V60 Z'


def mark(w, c=MILK, dot=PEACH, label='Знак «П.»'):
    return (f'<svg width="{w}" height="{w * 60 / 68:.1f}" viewBox="0 0 68 60" role="img" aria-label="{label}" style="overflow:visible">'
            f'<path d="{ARCH}" fill="{c}"/><circle cx="61" cy="54" r="6" fill="{dot}"/></svg>')


def word(c, size=16, sub=SAND, gap=10):
    return (f'<div style="display:flex;flex-direction:column;align-items:center">'
            f'<div style="font:300 {size}px/1 Manrope,sans-serif;letter-spacing:.42em;margin-right:-.42em;color:{c};white-space:nowrap">ПЛАТФОРМА</div>'
            f'<div style="font:400 {size * .55:.1f}px/1 Manrope,sans-serif;letter-spacing:.5em;margin-right:-.5em;color:{sub};white-space:nowrap;margin-top:{gap}px">НЕДВИЖИМОСТИ</div></div>')


def vlock(w, size, c=MILK, dot=PEACH, sub=SAND):
    return f'<div style="display:flex;flex-direction:column;align-items:center;gap:{round(w * .3)}px">{mark(w, c, dot)}{word(c, size, sub)}</div>'


def hlock(w, size, c=MILK, dot=PEACH, sub=SAND):
    wd = (f'<div style="display:flex;flex-direction:column;align-items:flex-start">'
          f'<div style="font:300 {size}px/1 Manrope,sans-serif;letter-spacing:.42em;color:{c};white-space:nowrap">ПЛАТФОРМА</div>'
          f'<div style="font:400 {size * .55:.1f}px/1 Manrope,sans-serif;letter-spacing:.5em;color:{sub};white-space:nowrap;margin-top:9px">НЕДВИЖИМОСТИ</div></div>')
    return f'<div style="display:flex;align-items:center;gap:{round(w * .45)}px">{mark(w, c, dot)}{wd}</div>'


def construction():
    s = 5.2  # px per unit
    g = ''
    for x in (0, 14, 24, 34, 48, 55, 67):
        g += f'<line x1="{x}" y1="-6" x2="{x}" y2="66" stroke="{SAND}" stroke-width=".25" stroke-dasharray="1 1.2"/>'
    for y in (0, 24, 48, 60):
        g += f'<line x1="-6" y1="{y}" x2="74" y2="{y}" stroke="{SAND}" stroke-width=".25" stroke-dasharray="1 1.2"/>'
    g += f'<circle cx="24" cy="24" r="24" fill="none" stroke="{SAND}" stroke-width=".3"/><circle cx="24" cy="24" r="10" fill="none" stroke="{SAND}" stroke-width=".3"/>'
    notes = (f'<text x="24" y="-9" font-size="3" fill="{SAND}" text-anchor="middle" font-family="Manrope">R 24 · r 10</text>'
             f'<text x="7" y="64.5" font-size="3" fill="{SAND}" text-anchor="middle" font-family="Manrope">14</text>'
             f'<text x="61" y="64.5" font-size="3" fill="{PEACH}" text-anchor="middle" font-family="Manrope">● 12</text>')
    return (f'<svg width="{78 * s}" height="{76 * s}" viewBox="-6 -12 80 80" role="img" aria-label="Построение знака">'
            f'<path d="{ARCH}" fill="{MILK}" fill-opacity=".92"/><circle cx="61" cy="54" r="6" fill="{PEACH}"/>{g}{notes}</svg>')


def page():
    dot = f'<span style="color:{PEACH}">.</span>'
    pin = (f'<svg width="120" height="120" viewBox="0 0 120 120" aria-hidden="true"><rect width="120" height="120" rx="14" fill="#26272A"/>'
           f'<path d="M0 40 H120 M0 82 H120 M38 0 V120 M84 0 V120" stroke="#34363A" stroke-width="6"/>'
           f'<circle cx="62" cy="58" r="16" fill="{PEACH}" fill-opacity=".22"/><circle cx="62" cy="58" r="7" fill="{PEACH}"/></svg>')
    prog = ''.join(f'<i style="background:{PEACH if i < 3 else "#3A3B3F"}"></i>' for i in range(7))
    tiles_ver = ''.join(f'<div class="t s3" style="background:{bg}">{vlock(58, 11, c, d, s_)}<span class="cap" style="color:{s_}">{cap}</span></div>'
                        for bg, c, d, s_, cap in ((MILK, INK, PEACH, '#8A847B', 'на светлом'), (PEACH, MILK, INK, '#FFE3DC', 'на красном'),
                                                  ('#24252A', MILK, MILK, SAND, 'одноцветный'), ('#FFFFFF', INK, INK, '#8A847B', 'чёрно-белый')))
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Логотип «П.»</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}}body{{margin:0;background:{NIGHT};color:{MILK};font:400 16px/1.5 Manrope,system-ui,sans-serif}}
.wrap{{max-width:1440px;margin:0 auto;padding:56px}}
.top{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid #2A2B2F;padding-bottom:16px;margin-bottom:22px}}
.top b{{font:500 26px Manrope,sans-serif;letter-spacing:-.01em}}.top span{{color:{SAND};font-size:13px;letter-spacing:.12em;text-transform:uppercase}}
.g{{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:18px}}
.t{{border-radius:16px;position:relative;display:flex;align-items:center;justify-content:center;min-height:240px;padding:28px}}
.cap{{position:absolute;left:18px;top:14px;font-size:11px;letter-spacing:.14em;text-transform:uppercase}}
.s3{{grid-column:span 3}}.s4{{grid-column:span 4}}.s5{{grid-column:span 5}}.s6{{grid-column:span 6}}.s7{{grid-column:span 7}}.s8{{grid-column:span 8}}.s12{{grid-column:span 12}}
.idea{{font:300 64px/1.05 Manrope,sans-serif;letter-spacing:-.02em}}
.txt{{color:#BDB7AD;font-size:15px;line-height:1.6;max-width:440px}}
.prog{{display:flex;gap:6px}}.prog i{{display:block;width:30px;height:6px;border-radius:3px}}
.sw{{display:flex;flex-direction:column;justify-content:flex-end;padding:14px;border-radius:12px;min-height:150px;font-size:12px}}
@media(max-width:900px){{.wrap{{padding:24px 16px}}.g>*{{grid-column:span 12!important}}.idea{{font-size:40px}}}}
</style></head><body><div class="wrap">
<div class="top"><b>ПЛАТФОРМА · «П.»</b><span>логотип и система · v2 · красная точка</span></div>
<div class="g">
  <div class="t s8" style="background:{GRAPH};min-height:420px"><span class="cap" style="color:{SAND}">основной логотип</span>{vlock(118, 21)}</div>
  <div class="t s4" style="background:{GRAPH};min-height:420px"><span class="cap" style="color:{SAND}">построение</span>{construction()}</div>

  <div class="t s6" style="background:#FFFFFF"><span class="cap" style="color:#8A867F">светлая версия — для сайта</span>{hlock(62, 15, INK, PEACH, '#8A867F')}</div>
  <div class="t s3" style="background:{GRAPH}"><span class="cap" style="color:{SAND}">иконка приложения</span>
    <div style="display:flex;align-items:flex-end;gap:16px"><div style="width:104px;height:104px;border-radius:24px;background:{NIGHT};display:flex;align-items:center;justify-content:center;border:1px solid #2E2F33">{mark(58)}</div>
    <div style="width:52px;height:52px;border-radius:12px;background:{PEACH};display:flex;align-items:center;justify-content:center">{mark(28, MILK, INK)}</div></div></div>
  <div class="t s3" style="background:{GRAPH}"><span class="cap" style="color:{SAND}">малые размеры</span>
    <div style="display:flex;align-items:flex-end;gap:18px">{mark(48)}{mark(32)}{mark(16)}</div></div>

  {tiles_ver}

  <div class="t s7" style="background:{NIGHT};border:1px solid #2A2B2F;justify-content:flex-start;align-items:flex-start;flex-direction:column;gap:22px;min-height:360px">
    <span class="cap" style="color:{SAND}">идея: точка</span>
    <div class="idea" style="margin-top:28px">Квартира{dot}<br>Ремонт{dot}<br>Дом{dot}</div>
    <div class="txt">Точка в знаке — это вы. Мы ставим точку в поиске квартиры, в ремонте и в стройке: доводим до результата. Точка становится фирменным приёмом — в слогане, на карте, в прогрессе стройки.</div>
  </div>
  <div class="s5" style="display:grid;grid-template-rows:1fr 1fr;gap:18px">
    <div class="t" style="background:{GRAPH};justify-content:space-between;min-height:170px"><span class="cap" style="color:{SAND}">точка на карте</span>
      <div style="margin-top:14px">{pin}</div><div class="txt" style="max-width:220px">Ваш дом — красная точка. Все объекты компании на карте — точки.</div></div>
    <div class="t" style="background:{GRAPH};flex-direction:column;align-items:flex-start;justify-content:center;gap:14px;min-height:170px"><span class="cap" style="color:{SAND}">точки прогресса</span>
      <div style="font:500 20px Manrope,sans-serif;margin-top:14px">Ваш дом: этап 3 из 7</div><div class="prog">{prog}</div></div>
  </div>

  <div class="s8" style="display:flex;gap:10px">
    <div class="sw" style="flex:30;background:{NIGHT};border:1px solid #2A2B2F">Ночь<br>{NIGHT}</div>
    <div class="sw" style="flex:26;background:{GRAPH}">Графит<br>{GRAPH}</div>
    <div class="sw" style="flex:22;background:{MILK};color:{INK}">Молоко<br>{MILK}</div>
    <div class="sw" style="flex:12;background:{LIGHT};color:{INK}">Светло-серый<br>{LIGHT}</div>
    <div class="sw" style="flex:14;background:{PEACH};color:#FFFFFF">Красный<br>{PEACH}</div>
  </div>
  <div class="t s4" style="background:{GRAPH};flex-direction:column;align-items:flex-start;justify-content:flex-end;gap:8px"><span class="cap" style="color:{SAND}">шрифт</span>
    <div style="font:300 64px/1 Manrope,sans-serif">Аа</div><div class="txt">Manrope: Light 300 с разрядкой — логотип и заголовки, Regular/Medium — текст.</div></div>
</div></div></body></html>'''


if __name__ == '__main__':
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(page())
    print('ok')
