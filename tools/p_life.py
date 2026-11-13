"""«П.» в жизни: фото-носители + визитки + соцсети. Run: py -3 tools/p_life.py → 06_П_точка/life.html (+ photos copied)"""
import os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '06_П_точка')
PH = os.path.join(OUT, 'photo')
os.makedirs(PH, exist_ok=True)
NIGHT, GRAPH, MILK, RED, GRAY, INK, SUB = '#0E0E0F', '#1C1C1E', '#F4F2EE', '#F5553C', '#ECEAE6', '#161617', '#8A867F'
ARCH = 'M0 60 V24 A24 24 0 0 1 48 24 V60 H34 V24 A10 10 0 0 0 14 24 V60 Z'

for s in ('facade', 'fence', 'billboard', 'store', 'helmet', 'keys', 'bag', 'vest', 'plate'):
    shutil.copy(os.path.join(ROOT, '_source', 'gen', f'life_P_{s}.jpg'), os.path.join(PH, f'{s}.jpg'))
for s in ('kv_living2', 'kv_kitchen', 'house_stone2', 'rem_bathroom'):
    shutil.copy(os.path.join(ROOT, '_source', 'gen', f'{s}.jpg'), os.path.join(PH, f'{s}.jpg'))


def mark(w, c=INK, dot=RED):
    return (f'<svg width="{w}" height="{w * 60 / 68:.1f}" viewBox="0 0 68 60" style="overflow:visible;display:block" aria-hidden="true">'
            f'<path d="{ARCH}" fill="{c}"/><circle cx="61" cy="54" r="6" fill="{dot}"/></svg>')


def word(c, size, sub=SUB, align='flex-start'):
    return (f'<div style="display:flex;flex-direction:column;align-items:{align}">'
            f'<div style="font:300 {size}px/1 Manrope,sans-serif;letter-spacing:.42em;margin-right:-.42em;color:{c};white-space:nowrap">ПЛАТФОРМА</div>'
            f'<div style="font:400 {size * .55:.1f}px/1 Manrope,sans-serif;letter-spacing:.5em;margin-right:-.5em;color:{sub};white-space:nowrap;margin-top:{size * .55:.0f}px">НЕДВИЖИМОСТЬ</div></div>')


def ph(name, cap, cls='', h=360, pos='center'):
    return f'<figure class="ph {cls}" style="height:{h}px"><img src="photo/{name}.jpg" alt="{cap}" style="object-position:{pos}"><figcaption>{cap}</figcaption></figure>'


def page():
    d = f'<span style="color:{RED}">.</span>'
    cards = (f'<div class="cards">'
             f'<div class="card" style="background:{NIGHT};color:{MILK};transform:rotate(-4deg)">{mark(46, MILK)}<div style="margin-top:auto">{word(MILK, 13, "#9A968F")}</div></div>'
             f'<div class="card" style="background:#FFFFFF;color:{INK};transform:rotate(3deg) translate(260px,-40px)">'
             f'<div style="display:flex;justify-content:space-between"><div><b style="font:600 15px Manrope">[Имя Фамилия]</b><div style="font-size:11px;color:{SUB}">Менеджер · Квартиры</div></div>{mark(24)}</div>'
             f'<div style="margin-top:auto;font-size:11px;line-height:1.6">+7 965 500-29-18<br>[сайт] · Екатеринбург</div></div></div>')
    posts = (f'<div class="posts">'
             f'<div class="post" style="background:{RED};color:#FFFFFF"><div style="font:500 30px/1.02 Manrope;letter-spacing:-.02em">Ставим<br>точку<span style="color:{INK}">.</span></div><div style="margin-top:auto">{mark(34, "#FFFFFF", INK)}</div></div>'
             f'<div class="post" style="background:#000 url(photo/kv_living2.jpg) center/cover;color:#FFFFFF;justify-content:flex-end"><div style="background:linear-gradient(0deg,#000a,#0000);margin:-18px;padding:18px"><div style="font:500 20px/1.1 Manrope">Квартира с ремонтом{d}</div><div style="font-size:11px;opacity:.8">2-комн. · [ПЛОЩАДЬ] м² · от [ЦЕНА] ₽</div></div></div>'
             f'<div class="post" style="background:{GRAY};color:{INK}"><div style="font-size:11px;color:{SUB};letter-spacing:.12em">ВАШ ДОМ</div><div style="font:500 22px/1.1 Manrope;margin-top:8px">Этап 3 из 7{d}</div>'
             f'<div style="display:flex;gap:5px;margin-top:14px">{"".join(f"<i style=\'display:block;width:22px;height:5px;border-radius:3px;background:{RED if i < 3 else "#C9C5BE"}\'></i>" for i in range(7))}</div>'
             f'<div style="margin-top:auto;font-size:11px;color:{SUB}">Кладка стен · камера 24/7</div></div></div>')
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>«П.» в жизни</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}}body{{margin:0;background:{MILK};color:{INK};font:400 15px/1.5 Manrope,system-ui,sans-serif}}
.wrap{{max-width:1440px;margin:0 auto;padding:56px}}
.top{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1px solid #DDD9D2;padding-bottom:18px;margin-bottom:22px}}
.top h1{{margin:0;font:500 58px/1 Manrope,sans-serif;letter-spacing:-.03em}}.top span{{color:{SUB};font-size:12px;letter-spacing:.14em;text-transform:uppercase}}
.g{{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:16px}}
.ph{{margin:0;position:relative;border-radius:14px;overflow:hidden;background:#ddd}}
.ph img{{display:block;width:100%;height:100%;object-fit:cover}}
.ph figcaption{{position:absolute;left:12px;top:12px;background:#ffffffe6;color:{INK};font-size:11px;letter-spacing:.06em;padding:4px 9px;border-radius:999px}}
.s4{{grid-column:span 4}}.s5{{grid-column:span 5}}.s6{{grid-column:span 6}}.s7{{grid-column:span 7}}.s8{{grid-column:span 8}}.s12{{grid-column:span 12}}
.h1{{aspect-ratio:1344/768}}.sq{{aspect-ratio:1/1}}
.panel{{border-radius:14px;padding:22px;position:relative;overflow:hidden}}
.cap{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:{SUB}}}
.cards{{position:relative;height:300px;margin-top:10px}}
.card{{position:absolute;left:40px;top:70px;width:300px;height:176px;border-radius:10px;padding:20px;display:flex;flex-direction:column;box-shadow:0 18px 40px #0003}}
.posts{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:18px}}
.post{{aspect-ratio:1/1;border-radius:10px;padding:18px;display:flex;flex-direction:column;overflow:hidden}}
@media(max-width:900px){{.wrap{{padding:24px 16px}}.g>*{{grid-column:span 12!important}}.top h1{{font-size:36px}}.card{{position:relative;left:0;top:0;transform:none!important;margin-bottom:12px}}.cards{{height:auto}}}}
</style></head><body><div class="wrap">
<div class="top"><h1>Ставим точку{d}</h1><span>«П.» — бренд в жизни</span></div>
<div class="g">
  {ph('facade', 'световая вывеска офиса', 's8', 520)}
  <div class="s4" style="display:grid;gap:16px">{ph('keys', 'брелок к ключам', '', 252, '60% 50%')}{ph('helmet', 'каска', '', 252, '50% 62%')}</div>
  {ph('fence', 'баннер на ограждении стройки', 's7', 400, '50% 60%')}
  {ph('billboard', 'билборд', 's5', 400, '68% 45%')}
  {ph('store', 'вывеска над входом', 's6', 380, '50% 40%')}
  {ph('vest', 'спецодежда', 's6', 380, '62% 60%')}
  {ph('bag', 'пакет для документов', 's4', 340, '50% 65%')}
  {ph('plate', 'паспорт объекта', 's4', 340, '50% 35%')}
  <div class="panel s4" style="background:{NIGHT};color:{MILK};height:340px"><div class="cap">три обещания</div>
    <div style="font:500 24px/1.25 Manrope;margin-top:14px">Проверено{d}<br>Выгодно{d}<br>Ясно{d}</div></div>
  <div class="panel s6" style="background:#E7E4DE"><div class="cap">визитки</div>{cards}</div>
  <div class="panel s6" style="background:#FFFFFF"><div class="cap">соцсети</div>{posts}</div>
</div></div></body></html>'''


if __name__ == '__main__':
    open(os.path.join(OUT, 'life.html'), 'w', encoding='utf8').write(page())
    print('ok')
