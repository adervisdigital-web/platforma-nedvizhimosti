"""Главная страница сайта проекта (GitHub Pages): текущий бренд «П.» — презентация, пример сайта, логотип, носители.
Старая галерея «Арки» сохранена как arka.html (без ссылок с главной). Run: py -3 tools/p_hub.py → index.html + _hub/*.jpg"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUB = os.path.join(ROOT, '_hub')
os.makedirs(HUB, exist_ok=True)
NIGHT, GRAPH, MILK, RED, SUB = '#0E0E0F', '#1C1C1E', '#F4F2EE', '#F5553C', '#8A867F'
ARCH = 'M0 60 V24 A24 24 0 0 1 48 24 V60 H34 V24 A10 10 0 0 0 14 24 V60 Z'

ITEMS = [  # (папка/страница, превью-источник, кадр, заголовок, описание, png для скачивания)
    ('07_Презентация/', '07_Презентация/Презентация_бренда.png', (0, 0, 1440, 900), 'Презентация бренда',
     'Идея, знак и построение, цвета, шрифт, графика, иконка, слоганы, носители и сайт.', '07_Презентация/Презентация_бренда.jpg'),
    ('08_Сайт_пример/', '08_Сайт_пример/desktop.png', (0, 0, 1440, 900), 'Пример сайта',
     'Поиск по квартирам, ремонту и домам на первом экране, карточки и карта. Работает на телефоне.', None),
    ('06_П_точка/index.html', '06_П_точка/П_логотип.png', (0, 0, 1440, 900), 'Логотип и система',
     'Знак «П.», версии логотипа, малые размеры, иконка, точка как система.', '06_П_точка/П_логотип.png'),
    ('06_П_точка/life.html', '06_П_точка/П_в_жизни.png', (0, 0, 1440, 900), 'Бренд в жизни',
     'Вывеска, ограждение стройки, билборд, каска, спецодежда, визитки и соцсети.', '06_П_точка/П_в_жизни.png'),
]


def mark(w, c=MILK, dot=RED):
    return (f'<svg width="{w}" height="{w * 60 / 68:.1f}" viewBox="0 0 68 60" aria-hidden="true" style="display:block;overflow:visible">'
            f'<path d="{ARCH}" fill="{c}"/><circle cx="61" cy="54" r="6" fill="{dot}"/></svg>')


def thumbs():
    for i, (_, src, box, *_r) in enumerate(ITEMS):
        im = Image.open(os.path.join(ROOT, src)).convert('RGB').crop(box)
        im.thumbnail((960, 600))
        im.save(os.path.join(HUB, f'{i + 1}.jpg'), quality=84)


def page():
    cards = ''
    for i, (href, _, _, title, desc, dl) in enumerate(ITEMS):
        dl_link = f'<a class="dl" href="{dl}" download>Скачать картинкой</a>' if dl else ''
        cards += (f'<article class="card"><a class="pv" href="{href}"><img src="_hub/{i + 1}.jpg" alt="{title}" loading="lazy"></a>'
                  f'<div class="tx"><span class="n">0{i + 1}</span><h2><a href="{href}">{title}<i class="o"></i></a></h2><p>{desc}</p>'
                  f'<div class="act"><a class="open" href="{href}">Открыть</a>{dl_link}</div></div></article>')
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Платформа недвижимости — фирменный стиль</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}}body{{margin:0;background:{NIGHT};color:{MILK};font:400 16px/1.5 Manrope,system-ui,sans-serif}}
a{{color:inherit;text-decoration:none}}
.w{{max-width:1280px;margin:0 auto;padding:0 40px}}
header{{padding:64px 0 56px;display:flex;justify-content:space-between;align-items:flex-end;gap:30px;flex-wrap:wrap;border-bottom:1px solid #ffffff1a}}
.lg{{display:flex;align-items:center;gap:26px}}
.wm b{{display:block;font:300 22px/1 Manrope;letter-spacing:.42em}}.wm small{{display:block;font:400 12px/1 Manrope;letter-spacing:.5em;color:{SUB};margin-top:12px}}
.meta{{color:{SUB};font-size:13px;letter-spacing:.2em;text-transform:uppercase;text-align:right}}
h1{{font:300 56px/1.05 Manrope;letter-spacing:-.04em;margin:64px 0 0;max-width:900px}}
.lead{{color:#B5B0A8;font-size:18px;max-width:640px;margin:20px 0 56px}}
i.o{{display:inline-block;width:.15em;height:.15em;border-radius:50%;background:{RED};margin-left:.06em}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px;padding-bottom:90px}}
.card{{background:{GRAPH};border-radius:18px;overflow:hidden;display:flex;flex-direction:column}}
.pv{{display:block;aspect-ratio:16/10;overflow:hidden;background:#000}}
.pv img{{width:100%;height:100%;object-fit:cover;object-position:top;display:block;transition:transform .5s}}
.card:hover .pv img{{transform:scale(1.03)}}
.tx{{padding:24px 26px 26px;display:flex;flex-direction:column;gap:8px;flex:1}}
.n{{color:{RED};font-size:12px;letter-spacing:.3em}}
h2{{margin:0;font:400 28px/1.15 Manrope;letter-spacing:-.02em}}
.tx p{{margin:0;color:#A9A49B;font-size:15px}}
.act{{display:flex;gap:10px;flex-wrap:wrap;margin-top:auto;padding-top:14px}}
.act a{{min-height:44px;display:inline-flex;align-items:center;padding:0 20px;border-radius:999px;font-weight:600;font-size:14px}}
.open{{background:{RED};color:#fff}}.open:hover{{background:#E0442C}}
.dl{{border:1px solid #ffffff2e}}.dl:hover{{border-color:#ffffff66}}
:focus-visible{{outline:2px solid {RED};outline-offset:3px}}
footer{{border-top:1px solid #ffffff1a;padding:28px 0 40px;color:{SUB};font-size:13px}}
@media(max-width:800px){{.w{{padding:0 16px}}header{{padding:36px 0 30px}}.meta{{text-align:left}}h1{{font-size:34px;margin-top:40px}}.lead{{font-size:16px;margin-bottom:32px}}.grid{{grid-template-columns:minmax(0,1fr);gap:18px}}.wm b{{font-size:17px}}}}
</style></head><body><div class="w">
<header><div class="lg">{mark(64)}<div class="wm"><b>ПЛАТФОРМА</b><small>НЕДВИЖИМОСТИ</small></div></div>
<div class="meta">Фирменный стиль<br>Екатеринбург · 2026</div></header>
<h1>Квартира<i class="o"></i> Ремонт<i class="o"></i> Дом<i class="o"></i><br>Ставим точку<i class="o"></i></h1>
<p class="lead">Материалы по бренду: презентация, пример сайта, логотип и носители.</p>
<main class="grid">{cards}</main>
<footer>Цены, площади, имена и контакты на макетах — заглушки до данных заказчика.</footer>
</div></body></html>'''


if __name__ == '__main__':
    thumbs()
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf8').write(page())
    print('ok')
