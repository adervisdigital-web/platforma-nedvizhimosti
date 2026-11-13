"""Презентация бренда «П.» в подаче Behance (по образцу Northlight Properties): обложка, о бренде, знак, построение,
версии, идея «Ставим точку», цвета, шрифт, паттерн, иконка, слоганы, носители, соцсети, сайт, финал.
Run: py -3 tools/p_present.py → 07_Презентация/index.html (+ фото копируются в 07_Презентация/photo)"""
import os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '07_Презентация')
PH = os.path.join(OUT, 'photo')
os.makedirs(PH, exist_ok=True)

NIGHT, GRAPH, MILK, RED, GRAY, INK, SUB, WHITE = '#0E0E0F', '#1C1C1E', '#F4F2EE', '#F5553C', '#ECEAE6', '#161617', '#8A867F', '#FFFFFF'
ARCH = 'M0 60 V24 A24 24 0 0 1 48 24 V60 H34 V24 A10 10 0 0 0 14 24 V60 Z'

for s in ('facade', 'fence', 'billboard', 'store', 'helmet', 'keys', 'bag', 'vest', 'plate'):
    shutil.copy(os.path.join(ROOT, '_source', 'gen', f'life_P_{s}.jpg'), os.path.join(PH, f'P_{s}.jpg'))
for s in ('kv_living2', 'kv_kitchen', 'kv_bedroom', 'kv_building', 'house_stone2', 'rem_bathroom'):
    shutil.copy(os.path.join(ROOT, '_source', 'gen', f'{s}.jpg'), os.path.join(PH, f'{s}.jpg'))
for s in ('desktop', 'mobile'):
    shutil.copy(os.path.join(ROOT, '08_Сайт_пример', f'{s}.png'), os.path.join(PH, f'site_{s}.png'))


def mark(w, c=MILK, dot=RED, label='Знак «П.»'):
    return (f'<svg width="{w}" height="{w * 60 / 68:.1f}" viewBox="0 0 68 60" role="img" aria-label="{label}" style="overflow:visible;display:block">'
            f'<path d="{ARCH}" fill="{c}"/><circle cx="61" cy="54" r="6" fill="{dot}"/></svg>')


def word(c, size, sub, align='flex-start', gap=None):
    gap = round(size * .55) if gap is None else gap
    return (f'<div style="display:flex;flex-direction:column;align-items:{align}">'
            f'<div style="font:300 {size}px/1 Manrope,sans-serif;letter-spacing:.42em;margin-right:-.42em;color:{c};white-space:nowrap">ПЛАТФОРМА</div>'
            f'<div style="font:400 {size * .55:.1f}px/1 Manrope,sans-serif;letter-spacing:.5em;margin-right:-.5em;color:{sub};white-space:nowrap;margin-top:{gap}px">НЕДВИЖИМОСТИ</div></div>')


def hlock(w, size, c=MILK, dot=RED, sub=SUB):
    return f'<div style="display:flex;align-items:center;gap:{round(w * .42)}px">{mark(w, c, dot)}{word(c, size, sub)}</div>'


def vlock(w, size, c=MILK, dot=RED, sub=SUB):
    return f'<div style="display:flex;flex-direction:column;align-items:center;gap:{round(w * .32)}px">{mark(w, c, dot)}{word(c, size, sub, "center")}</div>'


D = '<i class="o"></i>'  # красная точка в тексте — круг (точка Manrope квадратная)


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(h, t):  # t = доля цвета, остальное белый
    r, g, b = rgb(h)
    return '#%02X%02X%02X' % tuple(round(v * t + 255 * (1 - t)) for v in (r, g, b))


def construction(s=7.4):
    L = '#B9B4AB'
    g = ''
    for x in (0, 14, 24, 34, 48, 55, 67):
        g += f'<line x1="{x}" y1="-8" x2="{x}" y2="68" stroke="{L}" stroke-width=".18" stroke-dasharray=".8 .9"/>'
    for y in (0, 24, 48, 60):
        g += f'<line x1="-8" y1="{y}" x2="76" y2="{y}" stroke="{L}" stroke-width=".18" stroke-dasharray=".8 .9"/>'
    g += (f'<circle cx="24" cy="24" r="24" fill="none" stroke="{RED}" stroke-width=".22"/><circle cx="24" cy="24" r="10" fill="none" stroke="{RED}" stroke-width=".22"/>'
          f'<circle cx="24" cy="24" r=".7" fill="{RED}"/><circle cx="61" cy="54" r="9" fill="none" stroke="{L}" stroke-width=".18" stroke-dasharray=".8 .9"/>')
    t = 'font-family="Manrope" font-size="2.3" letter-spacing=".05"'
    notes = (f'<text x="24" y="-10" {t} fill="{SUB}" text-anchor="middle">R 24 · r 10 — общий центр</text>'
             f'<text x="7" y="64.6" {t} fill="{SUB}" text-anchor="middle">14</text><text x="41" y="64.6" {t} fill="{SUB}" text-anchor="middle">14</text>'
             f'<text x="24" y="64.6" {t} fill="{SUB}" text-anchor="middle">20</text>'
             f'<text x="61" y="67" {t} fill="{RED}" text-anchor="middle">Ø 12 = точка</text>'
             f'<text x="74" y="23.4" {t} fill="{SUB}">ось</text><text x="74" y="59.4" {t} fill="{SUB}">база</text>')
    return (f'<svg width="{88 * s:.0f}" height="{82 * s:.0f}" viewBox="-8 -14 88 82" role="img" aria-label="Построение знака">'
            f'<path d="{ARCH}" fill="{INK}"/><circle cx="61" cy="54" r="6" fill="{RED}"/>{g}{notes}</svg>')


def pattern(cols, rows, cell, bg, fg, reds):
    w, h = cols * cell, rows * cell
    out = ''
    for r in range(rows):
        for c in range(cols):
            x, y = c * cell + cell * .2, r * cell + cell * .24
            k = cell * .6 / 68
            dot = RED if (r, c) in reds else fg
            out += (f'<g transform="translate({x:.1f},{y:.1f}) scale({k:.4f})"><path d="{ARCH}" fill="{fg}"/>'
                    f'<circle cx="61" cy="54" r="6" fill="{dot}"/></g>')
    return f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" style="display:block;width:100%;height:100%;background:{bg}" aria-hidden="true">{out}</svg>'


def dots_pattern(cols, rows, cell, bg, fg, red):
    out = ''.join(f'<circle cx="{c * cell + cell / 2}" cy="{r * cell + cell / 2}" r="{cell * (.16 if (r, c) == red else .09):.1f}" fill="{NIGHT if (r, c) == red else fg}"/>'
                  for r in range(rows) for c in range(cols))
    return f'<svg viewBox="0 0 {cols * cell} {rows * cell}" preserveAspectRatio="xMidYMid slice" style="display:block;width:100%;height:100%;background:{bg}" aria-hidden="true">{out}</svg>'


def phone(inner, w=300, dark=True):
    return (f'<div class="phone" style="width:{w}px"><div class="scr">{inner}</div><i class="isl"></i></div>')


def icon(size, r=None):
    r = r or size * .225
    return (f'<div style="width:{size}px;height:{size}px;border-radius:{r:.0f}px;background:{NIGHT};display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 1px #ffffff14">'
            f'{mark(size * .56, MILK, RED, "Иконка приложения")}</div>')


def home_screen():
    tiles = ''
    shades = ['#ffffff2e', '#ffffff24', '#ffffff33', '#ffffff1f']
    for i in range(16):
        if i == 5:
            tiles += f'<div class="app">{icon(54)}<span>Платформа</span></div>'
        else:
            tiles += f'<div class="app"><div style="width:54px;height:54px;border-radius:12px;background:{shades[i % 4]};backdrop-filter:blur(6px)"></div><span style="width:34px;height:6px;background:#ffffff40;border-radius:3px;margin-top:4px"></span></div>'
    dock = ''.join(f'<div style="width:54px;height:54px;border-radius:12px;background:#ffffff2a"></div>' for _ in range(4))
    return (f'<div style="position:absolute;inset:0;background:url(photo/kv_living2.jpg) center/cover;filter:blur(14px) brightness(.62);transform:scale(1.2)"></div>'
            f'<div style="position:relative;padding:58px 18px 0;color:#fff"><div style="text-align:center;font:300 58px/1 Manrope">9:41</div>'
            f'<div style="text-align:center;font-size:13px;opacity:.8;margin:6px 0 30px">Пятница, 13 ноября</div>'
            f'<div class="apps">{tiles}</div></div>'
            f'<div style="position:absolute;left:12px;right:12px;bottom:14px;height:78px;border-radius:26px;background:#ffffff26;backdrop-filter:blur(10px);display:flex;justify-content:space-around;align-items:center">{dock}</div>')


def profile():
    posts = [
        f'<div style="background:{RED};color:#fff;padding:8px;font:600 11px/1.05 Manrope">Ставим<br>точку<i class="o n"></i></div>',
        '<div style="background:url(photo/kv_living2.jpg) center/cover"></div>',
        f'<div style="background:{NIGHT};display:flex;align-items:center;justify-content:center">{mark(34)}</div>',
        '<div style="background:url(photo/P_helmet.jpg) 50% 60%/cover"></div>',
        f'<div style="background:{GRAY};color:{INK};padding:8px;font:600 10px/1.1 Manrope">Этап 3 из 7<i class="o"></i></div>',
        '<div style="background:url(photo/house_stone2.jpg) center/cover"></div>',
        '<div style="background:url(photo/rem_bathroom.jpg) center/cover"></div>',
        f'<div style="background:{RED};color:#fff;padding:8px;font:600 10px/1.1 Manrope">Ремонт без<br>многоточий<i class="o n"></i></div>',
        '<div style="background:url(photo/kv_kitchen.jpg) center/cover"></div>',
    ]
    grid = ''.join(f'<div class="pp">{p}</div>' for p in posts)
    hl = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;font-size:9px;color:{SUB}">'
                 f'<div style="width:46px;height:46px;border-radius:50%;border:1.5px solid #DDD9D2;display:flex;align-items:center;justify-content:center;background:{bg}">{inner}</div>{t}</div>'
                 for t, bg, inner in (('Квартиры', GRAY, f'<b style="color:{RED};font-size:20px;line-height:0">.</b>'),
                                      ('Ремонт', GRAY, f'<b style="color:{RED};font-size:20px;line-height:0">.</b>'),
                                      ('Дома', GRAY, f'<b style="color:{RED};font-size:20px;line-height:0">.</b>'),
                                      ('Ипотека', GRAY, f'<b style="color:{RED};font-size:20px;line-height:0">.</b>')))
    return (f'<div style="background:#fff;position:absolute;inset:0;color:{INK};font-size:11px">'
            f'<div style="padding:52px 14px 10px;display:flex;justify-content:space-between;font-weight:700;font-size:13px">[ник] <span style="letter-spacing:2px">···</span></div>'
            f'<div style="display:flex;align-items:center;gap:16px;padding:0 14px">{icon(70, 35)}'
            f'<div style="display:flex;gap:14px;text-align:center;font-size:10px;color:{SUB}">'
            f'<div><b style="display:block;font-size:13px;color:{INK}">[N]</b>публикаций</div><div><b style="display:block;font-size:13px;color:{INK}">[N]</b>подписчиков</div></div></div>'
            f'<div style="padding:10px 14px 0;line-height:1.4"><b>Платформа недвижимости</b><br>Квартиры<i class="o"></i> Ремонт<i class="o"></i> Дома<i class="o"></i><br>Только проверенные предложения<br><span style="color:{SUB}">Екатеринбург · +7 965 500-29-18</span></div>'
            f'<div style="display:flex;gap:6px;padding:10px 14px"><div style="flex:1;background:{RED};color:#fff;border-radius:8px;text-align:center;padding:7px;font-weight:700">Подписаться</div>'
            f'<div style="flex:1;background:{GRAY};border-radius:8px;text-align:center;padding:7px;font-weight:700">Написать</div></div>'
            f'<div style="display:flex;gap:12px;padding:4px 14px 12px">{hl}</div>'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px">{grid}</div></div>')


def swatch(name, h, role, txt, tints=True, wide=False):
    r, g, b = rgb(h)
    tl = ''
    if tints:
        tl = '<div class="tints">' + ''.join(f'<div style="background:{mix(h, t)};color:{txt if t > .5 else INK}">{int(t * 100)}</div>' for t in (.8, .6, .4, .2)) + '</div>'
    return (f'<div class="sw{" wide" if wide else ""}"><div class="chip" style="background:{h};color:{txt}">'
            f'<div><b>{name}</b><span>{role}</span></div><div class="codes">HEX {h}<br>RGB {r} {g} {b}</div></div>{tl}</div>')


def page():
    palette = (swatch('Красная точка', RED, 'отметка «проверено», главная кнопка', WHITE, wide=True)
               + swatch('Ночь', NIGHT, 'фон бренда и основной текст', MILK)
               + swatch('Графит', GRAPH, 'карточки и панели на тёмном', MILK)
               + swatch('Молоко', MILK, 'фон сайта и полиграфии', INK, tints=False)
               + swatch('Светло-серый', GRAY, 'поля ввода, плашки, фильтры', INK, tints=False))
    weights = ''.join(f'<div class="wt"><div style="font-weight:{w}">Аа</div><span>{n} · {w}</span></div>'
                      for w, n in ((300, 'Light'), (400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (800, 'ExtraBold')))
    scale = ''.join(f'<div class="sc"><span>{lab}</span><div style="font:{wgt} {sz}px/1.1 Manrope;letter-spacing:{ls}">{txt}</div></div>'
                    for lab, wgt, sz, ls, txt in (('Заголовок · 56 / 500', 500, 56, '-.035em', f'Квартира с ремонтом{D}'),
                                                  ('Подзаголовок · 28 / 500', 500, 28, '-.02em', 'Только проверенные застройщики и бригады'),
                                                  ('Цена · 22 / 700', 700, 22, '-.01em', '[ЦЕНА] ₽ · [N] ₽/м²'),
                                                  ('Текст · 15 / 400', 400, 15, '0', 'Этот ЖК прошёл нашу проверку: надёжный застройщик, понятные сроки сдачи, выгодная ипотека.'),
                                                  ('Подпись · 11 / 400 · разрядка', 400, 11, '.5em', 'ПЛАТФОРМА НЕДВИЖИМОСТИ · ЕКАТЕРИНБУРГ')))
    versions = ''.join(f'<div class="ver" style="background:{bg}">{hlock(64, 19, c, d, s)}<span style="color:{s}">{t}</span></div>'
                       for bg, c, d, s, t in ((NIGHT, MILK, RED, '#8A867F', 'основная · на тёмном'),
                                              (MILK, INK, RED, SUB, 'на светлом · сайт и печать'),
                                              (RED, WHITE, NIGHT, '#FFD9D2', 'на красном · реклама и соцсети'),
                                              (WHITE, INK, INK, SUB, 'монохром · штамп, гравировка')))
    sizes = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px">{mark(w, INK)}<span>{w} px</span></div>' for w in (96, 64, 40, 24, 16))
    slogans = ''.join(f'<div class="slg" style="background-image:url(photo/{img});background-position:{pos}"><div class="sh"></div>'
                      f'<div class="st">{t}</div><div class="sm">{hlock(30, 9, WHITE, RED, "#ffffffb0")}</div></div>'
                      for img, pos, t in (('slg_zhk.jpg', 'center', f'Только проверенные<br>застройщики{D} Точка{D}'),
                                          ('rem_bathroom.jpg', 'center', f'Ремонт<br>без многоточий{D}'),
                                          ('slg_house.jpg', 'center 60%', f'Свой дом{D}<br>Точка{D}')))
    car = lambda n, cap, cls, pos='center': f'<figure class="ph {cls}"><img src="photo/P_{n}.jpg" alt="{cap}" style="object-position:{pos}"><figcaption>{cap}</figcaption></figure>'
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Платформа недвижимости — бренд</title>
<script>function fit(){{var w=innerWidth;document.documentElement.style.zoom=w>1440?w/1440:1}}fit();addEventListener("resize",fit)</script>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}}html{{background:#00FF00}}body{{margin:0;background:{MILK};color:{INK};font:400 16px/1.5 Manrope,system-ui,sans-serif}}
i.d{{font-style:normal;color:{RED}}}
i.o{{display:inline-block;width:.15em;height:.15em;border-radius:50%;background:{RED};margin-left:.06em}}
i.o.n{{background:{NIGHT}}}em.nw{{white-space:nowrap;font-style:inherit}}i.o.w{{background:#fff}}
section{{position:relative;overflow:hidden}}
.in{{max-width:1440px;margin:0 auto;padding:110px 96px}}
.lab{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:{SUB};display:flex;gap:18px;align-items:center}}
.lab b{{font-weight:500;color:{RED}}}
h2{{font:400 64px/1.02 Manrope;letter-spacing:-.04em;margin:26px 0 0}}
p.lead{{font-size:20px;line-height:1.55;max-width:620px;color:inherit;opacity:.85;margin:26px 0 0}}
.dark{{background:{NIGHT};color:{MILK}}}.red{{background:{RED};color:#fff}}.gray{{background:{GRAY}}}.white{{background:#fff}}
.dark .lab,.red .lab{{color:#ffffff8c}}.red .lab b{{color:{NIGHT}}}
/* cover */
.cover{{height:780px;background:{RED};display:grid;grid-template-columns:1fr 1fr}}
.cover .l svg{{width:150px;height:auto}}
.cover .l{{padding:80px 96px;display:flex;flex-direction:column;justify-content:space-between;color:#fff}}
.cover .r{{background:url(photo/ekb_aerial.jpg) 46% 50%/cover;position:relative}}
.cover .r::after{{display:none}}
.cover .meta{{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.3em;text-transform:uppercase;opacity:.8}}
/* about */
.about{{display:grid;grid-template-columns:1.1fr .9fr;gap:80px;align-items:end}}
.about .big{{font:300 44px/1.18 Manrope;letter-spacing:-.025em;margin:30px 0 0}}
.trio{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:70px}}
.trio div{{border-top:1px solid #ffffff24;padding-top:18px}}.trio b{{font:500 24px Manrope;display:block;margin-bottom:6px}}.trio span{{color:#A9A49B;font-size:15px}}
.photos2{{display:grid;grid-template-columns:1fr 1fr;gap:16px;height:520px}}
.photos2 div{{border-radius:4px;background-size:cover;background-position:center}}
/* logo */
.hero-logo{{height:860px;display:flex;align-items:center;justify-content:center}}
.cons{{display:grid;grid-template-columns:auto 1fr;gap:90px;align-items:center}}
.facts{{display:grid;gap:22px;margin-top:40px}}.facts div{{border-top:1px solid #DDD9D2;padding-top:14px;font-size:15px;color:#4A4741}}.facts b{{display:block;color:{INK};font:500 20px Manrope;margin-bottom:4px}}
.vers{{display:grid;grid-template-columns:1fr 1fr;gap:0}}
.ver{{height:420px;display:flex;align-items:center;justify-content:center;position:relative}}
.ver>span{{position:absolute;left:28px;bottom:22px;font-size:12px;letter-spacing:.14em;text-transform:uppercase}}
.sizes{{display:flex;align-items:flex-end;gap:70px;margin-top:60px;color:{SUB};font-size:12px}}
/* idea */
.idea{{min-height:900px;display:flex;flex-direction:column;justify-content:space-between}}
.idea .mega{{font:400 150px/.95 Manrope;letter-spacing:-.055em;margin:40px 0}}
.idea .mega i{{font-style:normal;color:{NIGHT}}}
.ib{{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:end}}
.mf{{margin-top:60px;border-top:1px solid #ffffff4d}}
.mrow{{display:grid;grid-template-columns:200px 1fr;gap:40px;align-items:center;border-bottom:1px solid #ffffff4d;padding:22px 0}}
.mrow .gl{{font:300 120px/1 Manrope;height:120px;display:flex;align-items:center;color:{NIGHT}}}
.mrow b{{display:block;font:500 30px/1.1 Manrope;letter-spacing:-.02em}}.mrow span{{font-size:19px;opacity:.85}}
.mfin{{font:400 64px/1.04 Manrope;letter-spacing:-.04em;margin-top:70px}}
.prin{{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;margin-top:60px}}
.prin b{{display:block;font:400 54px/1 Manrope;letter-spacing:-.04em;margin-bottom:18px}}.prin span{{color:#B5B0A8;font-size:17px}}
.slist{{display:grid;grid-template-columns:1fr 1fr;gap:0 40px;margin-top:60px}}
.slist div{{border-top:1px solid #ffffff24;padding:18px 0;font:400 24px/1.25 Manrope;letter-spacing:-.01em}}
.voice{{margin-top:70px;display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.voice>div{{border-radius:18px;padding:26px}}.voice .yes{{background:{GRAPH}}}.voice .no{{border:1px solid #ffffff24}}
.voice h3{{margin:0 0 14px;font:600 13px Manrope;letter-spacing:.2em;text-transform:uppercase}}.voice .yes h3{{color:{RED}}}.voice .no h3{{color:#8A867F}}
.voice p{{margin:0;padding:12px 0;border-top:1px solid #ffffff14;font-size:18px}}.voice .no p{{color:#8A867F;text-decoration:line-through;text-decoration-color:#8A867F80}}
.uses{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.use{{background:#ffffff12;border-radius:18px;padding:24px;min-height:210px;display:flex;flex-direction:column;justify-content:space-between}}
.use b{{font:500 20px Manrope}}.use span{{font-size:14px;opacity:.8}}
/* colors */
.pal{{display:grid;grid-template-columns:1.3fr 1fr 1fr;grid-template-rows:auto auto;gap:16px;margin-top:60px}}
.sw{{display:flex;flex-direction:column;gap:8px}}.sw.wide{{grid-row:span 2}}
.sw .chip{{border-radius:20px;padding:26px;min-height:240px;display:flex;flex-direction:column;justify-content:space-between;flex:1}}
.sw b{{font:500 26px Manrope;display:block;letter-spacing:-.01em}}.sw span{{font-size:14px;opacity:.75}}
.codes{{font:500 13px/1.6 Manrope;letter-spacing:.06em}}
.tints{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}}.tints div{{border-radius:10px;height:46px;font-size:11px;padding:6px 9px;font-weight:600}}
.prop{{display:flex;height:22px;border-radius:999px;overflow:hidden;margin-top:30px}}
/* type */
.type{{display:grid;grid-template-columns:.9fr 1.1fr;gap:80px}}
.aa{{font:300 330px/.85 Manrope;letter-spacing:-.06em}}.aa i{{font-style:normal;color:{RED}}}
.wts{{display:flex;gap:30px;margin-top:40px}}.wt div{{font-size:54px;line-height:1}}.wt span{{font-size:12px;color:{SUB}}}
.abc{{font:400 22px/1.5 Manrope;letter-spacing:.04em;color:#4A4741;margin-top:30px}}
.sc{{border-top:1px solid #DDD9D2;padding:18px 0}}.sc span{{display:block;font-size:12px;color:{SUB};margin-bottom:10px;letter-spacing:.06em}}
/* pattern */
.pat{{display:grid;grid-template-columns:1.4fr 1fr;height:760px}}
/* icon */
.icons{{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}}
.phone{{position:relative;aspect-ratio:9/19.5;border-radius:48px;background:#0B0B0C;padding:11px;box-shadow:0 40px 80px #0000003d,inset 0 0 0 2px #2C2C2F}}
.phone .scr{{position:relative;width:100%;height:100%;border-radius:38px;overflow:hidden;background:#000}}
.phone .isl{{position:absolute;top:22px;left:50%;transform:translateX(-50%);width:92px;height:26px;border-radius:14px;background:#000}}
.pp{{aspect-ratio:1/1;overflow:hidden;display:flex;flex-direction:column}}.pp>div{{flex:1}}
.apps{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px 10px}}.app{{display:flex;flex-direction:column;align-items:center;gap:5px;font-size:11px}}
.isz{{display:flex;align-items:flex-end;gap:36px;margin-top:50px;color:{SUB};font-size:12px}}.isz>div{{display:flex;flex-direction:column;align-items:center;gap:12px}}
/* slogans */
.slgs{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:60px}}
.slg{{position:relative;height:560px;border-radius:6px;overflow:hidden;background-size:cover;color:#fff}}
.slg .sh{{position:absolute;inset:0;background:linear-gradient(180deg,#0000009e 0%,#00000014 45%,#0000008c 100%)}}
.slg .st{{position:absolute;left:30px;top:30px;right:30px;font:500 40px/1.04 Manrope;letter-spacing:-.03em}}
.slg .sm{{position:absolute;left:30px;bottom:28px}}
/* carriers */
.g{{display:grid;grid-template-columns:repeat(12,1fr);gap:16px;margin-top:60px}}
.ph{{margin:0;position:relative;border-radius:6px;overflow:hidden;background:#ddd}}
.ph img{{display:block;width:100%;height:100%;object-fit:cover}}
.ph figcaption{{position:absolute;left:14px;bottom:14px;background:#ffffffe6;color:{INK};font-size:11px;letter-spacing:.08em;padding:5px 11px;border-radius:999px}}
.c8{{grid-column:span 8;height:560px}}.c4{{grid-column:span 4;height:272px}}.c6{{grid-column:span 6;height:440px}}.c4b{{grid-column:span 4;height:380px}}
/* social */
.soc{{display:grid;grid-template-columns:330px 1fr;gap:80px;align-items:center}}
.posts{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.post{{aspect-ratio:4/5;border-radius:6px;overflow:hidden;position:relative;padding:24px;display:flex;flex-direction:column;justify-content:space-between}}
/* site */
.site{{background:{GRAY}}}
.stage{{position:relative;height:820px;margin-top:50px}}
.laptop{{position:absolute;left:0;top:20px;width:1060px}}
.lid{{background:#0B0B0C;border-radius:22px 22px 0 0;padding:18px 18px 22px;box-shadow:inset 0 0 0 2px #2C2C2F}}
.lid .sc2{{height:620px;overflow:hidden;border-radius:4px;background:#fff}}.lid img{{width:100%;display:block}}
.base{{height:22px;margin:0 -70px;background:linear-gradient(#D9D7D2,#A9A69F);border-radius:0 0 18px 18px;position:relative}}
.base::before{{content:'';position:absolute;left:50%;top:0;transform:translateX(-50%);width:160px;height:9px;background:#BAB7B0;border-radius:0 0 10px 10px}}
.stage .phone{{position:absolute;right:20px;top:90px}}
.stage .phone img{{width:100%;display:block}}
.notes{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:40px}}
.notes div{{border-top:2px solid {INK};padding-top:16px;font-size:15px;color:#4A4741}}.notes b{{display:block;font:600 17px Manrope;color:{INK};margin-bottom:6px}}
.end{{height:860px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:70px}}
@media(max-width:900px){{
.in{{padding:64px 20px}}h2{{font-size:38px}}.cover{{grid-template-columns:1fr;height:auto}}.cover .l{{padding:40px 20px;min-height:520px}}.cover .r{{height:420px}}
.about,.cons,.type,.icons,.soc,.pat,.ib{{grid-template-columns:minmax(0,1fr)}}.about .big{{font-size:30px}}.abc{{font-size:15px;word-break:break-all}}.idea{{min-height:0}}.uses .use{{min-height:150px}}.slg{{height:420px}}.ib{{gap:30px}}.pat{{height:auto}}.pat>*{{height:360px}}.trio,.uses,.slgs,.notes,.posts,.prin,.slist,.voice{{grid-template-columns:minmax(0,1fr)}}.mrow{{grid-template-columns:70px 1fr;gap:16px}}.mrow .gl{{font-size:56px;height:60px}}.mrow b{{font-size:22px}}.mrow span{{font-size:15px}}.mfin{{font-size:36px}}.prin b{{font-size:40px}}.slist div{{font-size:19px}}
.vers{{grid-template-columns:1fr}}.ver{{height:280px;transform:none}}.ver>div{{transform:scale(.7)}}.pal{{grid-template-columns:1fr}}
.idea .mega{{font-size:64px}}.aa{{font-size:160px}}.g>*{{grid-column:span 12!important;height:300px!important}}
.stage{{height:auto}}.laptop{{position:relative;width:100%}}.lid .sc2{{height:260px}}.base{{margin:0}}.stage .phone{{position:relative;right:auto;top:auto;margin:40px auto 0}}
.photos2{{height:320px}}.sizes,.isz,.wts{{flex-wrap:wrap;gap:24px}}.hero-logo,.end{{height:auto;padding:120px 20px}}.hero-logo>div{{transform:scale(.6)}}.cons svg{{width:100%;height:auto}}
}}
</style></head><body>

<section class="cover" aria-label="Обложка">
  <div class="l">
    <div class="meta"><span>Фирменный стиль</span><span>Екатеринбург · 2026</span></div>
    <div>{mark(150, WHITE, NIGHT)}<div style="margin-top:56px">{word(WHITE, 30, "#FFE1DB")}</div></div>
    <div style="font:400 26px/1.2 Manrope;letter-spacing:-.01em">Квартира<i class="o n"></i> Ремонт<i class="o n"></i> Дом<i class="o n"></i></div>
  </div>
  <div class="r" role="img" aria-label="Екатеринбург на закате: новые кварталы у пруда"></div>
</section>

<section class="dark"><div class="in">
  <div class="about">
    <div><div class="lab"><b>01</b> О бренде</div>
      <div class="big">Рынок недвижимости полон многоточий. Мы ставим точку: проверяем застройщиков и строительные бригады, отбираем самые выгодные предложения и ведём вас от квартиры до своего дома{D}</div></div>
    <div class="photos2"><div style="background-image:url(photo/crane.jpg)"></div><div style="background-image:url(photo/redfacade.jpg)"></div></div>
  </div>
  <div class="trio">
    <div><b>Квартиры{D}</b><span>Новостройки и вторичное жильё Екатеринбурга только от проверенных застройщиков. Подбор, самая выгодная ипотека, сопровождение сделки.</span></div>
    <div><b>Ремонт{D}</b><span>Ремонт у партнёров, за которых мы ручаемся. Смета и сроки — до начала работ, приёмка каждого этапа.</span></div>
    <div><b>Дома{D}</b><span>Каменные дома от проверенных строителей-партнёров — по готовым и индивидуальным проектам.</span></div>
  </div>
</div></section>

<section class="dark hero-logo" aria-label="Логотип">{vlock(230, 40, MILK, RED, "#8A867F")}</section>

<section><div class="in">
  <div class="cons">
    {construction()}
    <div><div class="lab"><b>02</b> Знак</div><h2>Буква «П» и точка{D}</h2>
      <p class="lead">«П» — первая буква названия и арка входа в новый дом. Рядом — точка, наша отметка «проверено»: за этим входом нет сюрпризов.</p>
      <div class="facts"><div><b>Арка = вход</b>Скруглённая «П» читается и как буква, и как дверной проём. Свод построен на двух окружностях с общим центром.</div>
      <div><b>Точка = проверено</b>Единственный цветной элемент знака — наша подпись. Стоит на базовой линии, Ø 12 — чуть тоньше ножки «П». На красном фоне точка становится чёрной.</div>
      <div><b>Охранное поле</b>Свободное место вокруг знака — не меньше диаметра точки.</div></div></div>
  </div>
  <div class="sizes">{sizes}<span style="max-width:260px;line-height:1.5">Знак читается даже в 16 px — во вкладке браузера и в уведомлении на телефоне.</span></div>
</div></section>

<section class="vers" aria-label="Версии логотипа">{versions}</section>

<section class="red"><div class="in">
  <div class="lab"><b>03</b> Идея</div>
  <h2>У каждой покупки —<br>свой знак препинания<i class="o n"></i></h2>
  <div class="mf"><div class="mrow"><div class="gl">?</div><div><b>Покупка квартиры</b><span>Какой застройщик надёжен? Где ипотека выгоднее? Сдадут ли дом вовремя?</span></div></div><div class="mrow"><div class="gl">!</div><div><b>Ремонт</b><span>Смета выросла вдвое! Бригада пропала! Сроки сорваны!</span></div></div><div class="mrow"><div class="gl" style="padding-bottom:.35em">…</div><div><b>Стройка дома</b><span>Сроки, которые тянутся, и вопросы, на которые никто не отвечает…</span></div></div><div class="mrow"><div class="gl"><i class="o n" style="width:.5em;height:.5em;margin:0"></i></div><div><b>Платформа</b><span>Проверили. Выбрали самое выгодное. Передали ключи. Точка.</span></div></div></div>
  <div class="mfin">Мы ставим точку там,<br>где у других многоточие<i class="o n"></i></div>
</div></section>

<section class="dark"><div class="in">
  <div class="lab"><b>04</b> Принципы</div><h2>Три обещания{D}<br>Три точки{D}</h2>
  <div class="prin">
    <div><b>Проверено{D}</b><span>Работаем только с застройщиками и строительными бригадами, которых проверили сами. Красная точка рядом с объектом — наша подпись под ним.</span></div>
    <div><b>Выгодно{D}</b><span>Не выкладываем всё подряд. Сравниваем цены, ипотечные программы и условия — и показываем только самые выгодные предложения.</span></div>
    <div><b>Ясно{D}</b><span>Цена, срок и следующий шаг известны до начала работ. Без звёздочек, мелкого шрифта и многоточий.</span></div>
  </div>
  <div class="lab" style="margin-top:80px">Где живёт точка</div>
  <div class="uses">
    <div class="use"><svg width="52" height="52" viewBox="0 0 52 52" aria-hidden="true"><circle cx="26" cy="22" r="14" fill="none" stroke="{MILK}" stroke-width="2"/><circle cx="26" cy="22" r="5" fill="{RED}"/><path d="M26 36v12" stroke="{MILK}" stroke-width="2"/></svg><div><b>На карте</b><br><span>красная точка — объект проверен</span></div></div>
    <div class="use"><div style="display:flex;gap:5px">{"".join(f'<i style="display:block;width:16px;height:6px;border-radius:3px;background:{RED if i < 3 else "#3A3A3D"}"></i>' for i in range(7))}</div><div><b>В стройке</b><br><span>каждый принятый этап — точка</span></div></div>
    <div class="use"><div style="font:500 30px/1 Manrope">Принято{D}</div><div><b>В тексте</b><br><span>фраза без многоточий</span></div></div>
  </div>
</div></section>

<section class="white"><div class="in">
  <div class="lab"><b>05</b> Цвет</div><h2>Ночь, молоко<br>и одна красная точка{D}</h2>
  <p class="lead" style="color:#4A4741">Красный — цвет отметки «проверено». В интерфейсе его мало: точка, главная кнопка, метка на карте — поэтому он всегда означает главное. В рекламе красный может занять весь фон, тогда точка становится чёрной.</p>
  <div class="pal">{palette}</div>
  <div class="prop" aria-label="Пропорции цвета"><div style="flex:40;background:{MILK};box-shadow:inset 0 0 0 1px #E2DED7"></div><div style="flex:28;background:{NIGHT}"></div><div style="flex:16;background:{GRAY}"></div><div style="flex:10;background:{GRAPH}"></div><div style="flex:6;background:{RED}"></div></div>
  <div style="display:flex;justify-content:space-between;font-size:12px;color:{SUB};margin-top:10px"><span>баланс цвета в интерфейсе: молоко 40 · ночь 28 · серый 16 · графит 10</span><span style="color:{RED}">красный 6</span></div>
</div></section>

<section><div class="in type">
  <div><div class="lab"><b>06</b> Шрифт</div><div class="aa" style="margin-top:40px">Аа<i class="o"></i></div>
    <div style="font:500 34px Manrope;letter-spacing:-.02em;margin-top:30px">Manrope</div>
    <div style="color:{SUB};font-size:15px;margin-top:6px">Современный гротеск с полной кириллицей и свободной лицензией. Light — в логотипе, Medium — в заголовках, Regular — в тексте.</div>
    <div class="wts">{weights}</div>
    <div class="abc">АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ<br>абвгдеёжзийклмнопрстуфхцчшщъыьэюя<br>0123456789 ₽ м² № — «» .</div></div>
  <div style="padding-top:60px">{scale}</div>
</div></section>

<section class="pat" aria-label="Паттерн">
  <div>{pattern(9, 6, 100, NIGHT, GRAPH, {(1, 2), (3, 6), (4, 1)})}</div>
  <div style="position:relative">{dots_pattern(7, 9, 60, RED, "#FF7A64", (2, 4))}
    <div style="position:absolute;left:0;bottom:0;right:0;padding:34px 44px 40px;color:#fff;background:{RED}"><div class="lab" style="color:#ffffffa6"><b style="color:{NIGHT}">07</b> Графика</div>
    <div style="font:400 30px/1.2 Manrope;letter-spacing:-.02em;margin-top:14px">Сотни точек — и одна выделенная. Так выглядит наш отбор: из всего рынка — предложение, за которое мы ручаемся<i class="o n"></i></div></div></div>
</section>

<section class="gray"><div class="in icons">
  <div><div class="lab"><b>08</b> Приложение</div><h2>Иконка — тёмная,<br>точка — красная{D}</h2>
    <p class="lead" style="color:#4A4741">Тёмная иконка с одной красной точкой выделяется среди пёстрых соседей именно сдержанностью. Силуэт арки узнаётся даже в 40 px.</p>
    <div class="isz">{"".join(f'<div>{icon(s)}<span>{s} px</span></div>' for s in (120, 80, 58, 40))}</div></div>
  <div style="display:flex;justify-content:center">{phone(home_screen(), 340)}</div>
</div></section>

<section class="dark"><div class="in">
  <div class="lab"><b>09</b> Голос</div><h2>Говорим коротко{D}<br>Заканчиваем точкой{D}</h2>
  <div class="slgs">{slogans}</div>
  <div class="slist"><div>Сначала проверяем{D} Потом предлагаем{D}</div><div>Отбор — наша работа{D} Выбор — ваш{D}</div><div>Мы говорим «нет» многим, чтобы вы сказали «да» одному{D}</div><div>Ипотека, после которой не остаётся вопросов{D}</div><div>Квартира, ремонт и дом — от тех, за кого мы ручаемся{D}</div><div>Где у других многоточие — у нас точка{D}</div></div>
  <div class="voice"><div class="yes"><h3>Так говорим</h3><p>Сдача — III квартал 2027{D}</p><p>Смета — [N] ₽, срок — [N] недель{D}</p><p>Застройщик проверен: документы и сданные дома{D}</p><p>Платёж — [N] ₽ в месяц, на [N] ₽ ниже среднего{D}</p></div>
    <div class="no"><h3>Так не говорим</h3><p>Сдача в ближайшее время…</p><p>Цена от [N] ₽*</p><p>Надёжный застройщик!!!</p><p>Элитный. Премиальный. Уникальный.</p></div></div>
</div></section>

<section><div class="in">
  <div class="lab"><b>10</b> Носители</div><h2>В городе и на стройке{D}</h2>
  <div class="g">
    {car('facade', 'световая вывеска офиса', 'c8')}
    <div style="grid-column:span 4;display:grid;gap:16px">{car('helmet', 'каска инспектора', 'c4', '50% 62%')}{car('keys', 'брелок', 'c4', '60% 50%')}</div>
    {car('fence', 'ограждение объекта партнёра', 'c6', '50% 60%')}{car('billboard', 'билборд', 'c6', '68% 45%')}
    {car('vest', 'жилет инспектора', 'c4b', '62% 60%')}{car('bag', 'пакет для документов', 'c4b', '50% 65%')}{car('plate', 'паспорт объекта с отметкой о проверке', 'c4b', '50% 35%')}
  </div>
</div></section>

<section class="white"><div class="in soc">
  {phone(profile(), 330)}
  <div><div class="lab"><b>11</b> Соцсети</div><h2>Лента как витрина{D}</h2>
    <p class="lead" style="color:#4A4741">В ленте — только отобранные предложения: фото реальных объектов чередуются с красными карточками-фразами. Аватар — иконка приложения.</p>
    <div class="posts" style="margin-top:44px">
      <div class="post" style="background:{RED};color:#fff"><div style="font:500 34px/1.05 Manrope;letter-spacing:-.03em">Проверено<i class="o n"></i><br>Выгодно<i class="o n"></i><br>Ясно<i class="o n"></i></div>{mark(40, WHITE, NIGHT)}</div>
      <div class="post" style="background:url(photo/kv_living2.jpg) center/cover;color:#fff;justify-content:flex-end"><div style="position:absolute;inset:0;background:linear-gradient(0deg,#000a,#0000 60%)"></div><div style="position:relative"><div style="font:500 20px/1.15 Manrope">Квартира с ремонтом{D}</div><div style="font-size:12px;opacity:.85">2-комн. · [ПЛОЩАДЬ] м² · от [ЦЕНА] ₽</div></div></div>
      <div class="post" style="background:{NIGHT};color:{MILK}"><div style="font-size:11px;letter-spacing:.2em;color:#8A867F">ВАШ ДОМ</div><div><div style="font:500 26px/1.1 Manrope">Этап 3 из 7 принят{D}</div>
        <div style="display:flex;gap:5px;margin-top:14px">{"".join(f'<i style="display:block;width:22px;height:5px;border-radius:3px;background:{RED if i < 3 else "#3A3A3D"}"></i>' for i in range(7))}</div><div style="font-size:12px;color:#8A867F;margin-top:10px">Кладка стен · проверено Платформой</div></div></div>
    </div></div>
</div></section>

<section class="site"><div class="in">
  <div class="lab"><b>12</b> Сайт-приложение</div><h2>Поиск — первым экраном{D}</h2>
  <p class="lead" style="color:#4A4741">Светлый интерфейс в логике привычных сервисов недвижимости: поиск — сразу, на первом экране. Красный — только кнопка действия и отметка «проверено».</p>
  <div class="stage">
    <div class="laptop"><div class="lid"><div class="sc2"><img src="photo/site_desktop.png" alt="Главная страница на ноутбуке"></div></div><div class="base"></div></div>
    {phone('<img src="photo/site_mobile.png" alt="Главная страница на телефоне">', 300)}
  </div>
  <div class="notes">
    <div><b>Вкладки</b>Квартиры, Ремонт, Дома — три направления в одном поиске.</div>
    <div><b>Фильтры сразу</b>Тип, комнаты, цена и район — на первом экране, на кнопке — число найденных вариантов.</div>
    <div><b>Отметка «проверено»</b>Красная точка в карточке и на карте — застройщик или бригада прошли нашу проверку.</div>
    <div><b>Карточки и карта</b>Фото, цена и цена за м²; при наведении объект подсвечивается на карте.</div>
  </div>
</div></section>

<section class="dark end" aria-label="Финал">{mark(120, MILK, RED)}<div style="font:300 64px/1.05 Manrope;letter-spacing:-.04em;text-align:center">Ставим точку{D}</div>{word(MILK, 18, "#8A867F", "center")}<a href="tel:+79655002918" style="color:{MILK};text-decoration:none;font:400 20px Manrope;letter-spacing:.06em;margin-top:-30px">+7 965 500-29-18</a></section>

</body></html>'''


if __name__ == '__main__':
    import re
    html = re.sub(r'([A-Za-zА-Яа-яЁё0-9»]+)(<i class="o[^"]*"></i>)', lambda m: '<em class="nw">' + m.group(1) + m.group(2) + '</em>', page())  # точка не уходит на новую строку
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(html)
    print('ok')
