"""Варианты доработки знака «П.» под регистрацию (уход от сходства с № 800341 и прекращённым № 563712).
Run: py -3 tools/p_mark_variants.py → 09_Доработка_знака/index.html"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '09_Доработка_знака')
os.makedirs(OUT, exist_ok=True)
NIGHT, GRAPH, MILK, RED, GRAY, INK, SUB = '#0E0E0F', '#1C1C1E', '#F4F2EE', '#F5553C', '#ECEAE6', '#161617', '#8A867F'

# Каждый знак: viewBox, тело (fill = {c}), точка (fill = {d})
MARKS = {
    'now': ('0 0 68 60',
            '<path d="M0 60 V24 A24 24 0 0 1 48 24 V60 H34 V24 A10 10 0 0 0 14 24 V60 Z" fill="{c}"/>',
            '<circle cx="61" cy="54" r="6" fill="{d}"/>'),
    # 1. Ножка-точка: правая ножка обрывается, её продолжает точка того же диаметра
    'leg': ('0 0 48 60',
            '<path d="M0 60 V24 A24 24 0 0 1 48 24 V39 H34 V24 A10 10 0 0 0 14 24 V60 Z" fill="{c}"/>',
            '<circle cx="41" cy="53" r="7" fill="{d}"/>'),
    # 2. Платформа: «П» стоит на линии-платформе, линия заканчивается точкой
    'base': ('0 0 76 60',
             '<path d="M0 52 V24 A24 24 0 0 1 48 24 V52 H34 V24 A10 10 0 0 0 14 24 V52 Z" fill="{c}"/><rect x="0" y="55.5" width="62" height="4.5" fill="{c}"/>',
             '<circle cx="70.5" cy="57.75" r="5.5" fill="{d}"/>'),
    # 3. Монолиния: тонкий контур «П», точка — единственная заливка
    'line': ('0 0 66 60',
             '<path d="M3 60 V24 A21 21 0 0 1 45 24 V60" fill="none" stroke="{c}" stroke-width="5"/>',
             '<circle cx="59" cy="55" r="5" fill="{d}"/>'),
    # 4. Прямой свод: «П»-рамка двери с прямым проёмом, точка с большим зазором
    'frame': ('0 0 72 60',
              '<path d="M0 60 V9 Q0 0 9 0 H39 Q48 0 48 9 V60 H35 V13 H13 V60 Z" fill="{c}"/>',
              '<circle cx="65" cy="53" r="7" fill="{d}"/>'),
}

VARIANTS = [
    ('leg', '1 · Ножка-точка',
     'Правая ножка «П» обрывается, и её продолжает точка того же диаметра. Точка — не отдельный элемент рядом, а окончание самой буквы.',
     'Нет круга в проёме и нет точки сбоку у основания: силуэт другой — это «П», дописанная точкой.',
     'Самый сильный по отличию и по смыслу «ставим точку». Рекомендую.'),
    ('base', '2 · Платформа',
     '«П» стоит на тонкой линии-платформе, линия уходит вправо и заканчивается точкой. Буквально: дом на платформе, в конце — результат.',
     'Добавлен горизонтальный элемент, который меняет общий силуэт; точка — конец линии, а не круг рядом с аркой.',
     'Название читается в самом знаке. Чуть сложнее в маленьком размере.'),
    ('line', '3 · Монолиния',
     'Тонкий контур арки вместо заливки, единственное заполненное — красная точка. Ближе всего к тонким знакам, которые нравились клиенту.',
     'Контурный знак против залитых арок; акцент целиком на точке.',
     'Самый лёгкий и «дорогой» на вид. Тонкую линию нужно проверить на вывеске и в 16 px.'),
    ('frame', '4 · Прямой свод',
     'Скруглены только наружные углы, проём прямой — «П» становится дверным проёмом, а не аркой. Точка отодвинута дальше.',
     'Уходим от полукруглой арки — главной общей черты с найденными знаками.',
     'Самый спокойный. Меньше связи с прошлым знаком.'),
]


def svg(key, w, c, d, label='Знак'):
    vb, body, dot = MARKS[key]
    _, _, vw, vh = map(float, vb.split())
    return (f'<svg width="{w}" height="{w * vh / vw:.1f}" viewBox="{vb}" role="img" aria-label="{label}" style="display:block;overflow:visible">'
            f'{body.format(c=c)}{dot.format(d=d)}</svg>')


def word(c, size, sub):
    return (f'<div style="display:flex;flex-direction:column;align-items:flex-start">'
            f'<div style="font:300 {size}px/1 Manrope,sans-serif;letter-spacing:.42em;color:{c};white-space:nowrap">ПЛАТФОРМА</div>'
            f'<div style="font:400 {size * .55:.1f}px/1 Manrope,sans-serif;letter-spacing:.5em;color:{sub};white-space:nowrap;margin-top:{size * .5:.0f}px">НЕДВИЖИМОСТИ</div></div>')


def lock(key, mw, size, c, d, sub):
    return f'<div style="display:flex;align-items:center;gap:{round(mw * .42)}px">{svg(key, mw, c, d)}{word(c, size, sub)}</div>'


def row(key, title, idea, diff, note):
    sizes = ''.join(f'<div class="sz">{svg(key, s, MILK, RED)}<span>{s}</span></div>' for s in (64, 32, 20, 16))
    icon = f'<div class="ic">{svg(key, 46, MILK, RED)}</div>'
    return f'''<section class="v">
  <div class="vh"><h2>{title}<i class="o"></i></h2><p>{idea}</p></div>
  <div class="vg">
    <div class="t big">{svg(key, 230, MILK, RED)}</div>
    <div class="t light">{lock(key, 70, 22, INK, RED, SUB)}</div>
    <div class="t red">{svg(key, 120, '#FFFFFF', NIGHT)}</div>
    <div class="t dark2"><div class="cap">малые размеры и иконка</div><div class="szs">{sizes}{icon}</div></div>
    <div class="t txt"><div class="cap">чем отличается</div><p>{diff}</p><div class="cap" style="margin-top:18px">оценка</div><p>{note}</p></div>
  </div>
</section>'''


def page():
    rows = ''.join(row(*v) for v in VARIANTS)
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Доработка знака «П.»</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}}body{{margin:0;background:{NIGHT};color:{MILK};font:400 16px/1.5 Manrope,system-ui,sans-serif}}
.w{{max-width:1600px;margin:0 auto;padding:64px clamp(16px,4vw,72px) 90px}}
i.o{{display:inline-block;width:.15em;height:.15em;border-radius:50%;background:{RED};margin-left:.05em}}
header{{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:48px;align-items:end;border-bottom:1px solid #ffffff1f;padding-bottom:40px}}
h1{{font:300 clamp(40px,4.4vw,72px)/1.02 Manrope;letter-spacing:-.04em;margin:18px 0 0}}
.br{{font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:{SUB}}}.br b{{color:{RED};font-weight:600}}
.lead{{color:#B5B0A8;font-size:17px;margin:0}}
.ref{{display:flex;gap:16px;margin-top:28px}}.ref>div{{flex:1;background:{GRAPH};border-radius:18px;padding:18px}}
.ref .cap{{margin-bottom:12px}}.ref p{{margin:0;font-size:14px;color:#B5B0A8}}
.cap{{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:{SUB}}}
.v{{padding-top:64px}}
.vh{{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:48px;align-items:end;margin-bottom:22px}}
.vh h2{{margin:0;font:400 clamp(30px,2.6vw,44px)/1.05 Manrope;letter-spacing:-.03em}}.vh p{{margin:0;color:#B5B0A8;font-size:17px;max-width:720px}}
.vg{{display:grid;grid-template-columns:1.25fr 1.15fr .8fr;grid-template-rows:auto auto;gap:14px}}
.t{{border-radius:22px;min-height:230px;display:flex;align-items:center;justify-content:center;padding:28px;position:relative}}
.big{{grid-row:span 2;background:{GRAPH};min-height:480px}}.light{{background:{MILK}}}.red{{background:{RED}}}
.dark2{{background:#151517;flex-direction:column;align-items:flex-start;justify-content:space-between}}
.szs{{display:flex;align-items:flex-end;gap:22px;margin-top:20px}}.sz{{display:flex;flex-direction:column;align-items:center;gap:8px}}.sz span{{font-size:11px;color:{SUB}}}
.ic{{width:76px;height:76px;border-radius:18px;background:{NIGHT};box-shadow:inset 0 0 0 1px #ffffff1a;display:flex;align-items:center;justify-content:center}}
.txt{{background:transparent;border:1px solid #ffffff1f;flex-direction:column;align-items:flex-start;justify-content:flex-start}}
.txt p{{margin:6px 0 0;font-size:15px;color:{MILK}}}
footer{{margin-top:80px;border-top:1px solid #ffffff1f;padding-top:24px;color:{SUB};font-size:13px}}
@media(max-width:900px){{header,.vh{{grid-template-columns:minmax(0,1fr);gap:18px}}.ref{{flex-direction:column}}
.vg{{grid-template-columns:minmax(0,1fr)}}.big{{grid-row:auto;min-height:320px}}.txt{{grid-column:auto}}.light>div{{transform:scale(.8)}}}}
</style></head><body><div class="w">
<header>
  <div><div class="br">[ <b>●</b> знак «П.» · варианты под регистрацию ]</div><h1>Тот же характер<i class="o"></i><br>Другой силуэт<i class="o"></i></h1></div>
  <div><p class="lead">По поиску в реестре Роспатента у нынешнего знака есть похожие: действующий знак банка в 36 классе — арка с кругом внутри проёма, и прекращённый знак — арка с точкой снаружи у ножки. Ниже четыре доработки, которые сохраняют «П», красную точку и тонкий шрифт, но меняют общий силуэт.</p>
    <div class="ref"><div><div class="cap">сейчас</div>{svg('now', 70, MILK, RED)}<p style="margin-top:12px">арка + точка у ножки</p></div>
    <div><div class="cap">чего избегаем</div><p>круг внутри проёма арки;<br>точка вплотную к основанию правой ножки;<br>полукруглая арка как единственная форма</p></div></div></div>
</header>
{rows}
<footer>Предварительная проработка. Окончательный выбор формы для подачи — после заключения патентного поверенного.</footer>
</div></body></html>'''


if __name__ == '__main__':
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(page())
    print('ok')
