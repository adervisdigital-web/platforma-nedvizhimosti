"""Документ «Логотип — версии и правила» (PDF A4 альбом, вектор) из готовых SVG в 09_Логотип_файлы/SVG.
Run: py -3 -X utf8 tools/logo_doc.py   (после tools/logo_files.py)"""
import os, glob, re, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, '09_Логотип_файлы')
CHROME = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'
NIGHT, MILK, RED, INK, SUB, GRAY = '#0E0E0F', '#F4F2EE', '#F5553C', '#161617', '#8A867F', '#ECEAE6'
BG = {'на_тёмном': NIGHT, 'на_светлом': MILK, 'на_красном': RED, 'чёрный': '#FFFFFF', 'белый': NIGHT}
CAP = {'на_тёмном': 'Основная · на тёмном', 'на_светлом': 'На светлом · сайт, документы, печать',
       'на_красном': 'На красном · реклама, соцсети', 'чёрный': 'Один цвет · чёрный', 'белый': 'Один цвет · белый'}
CAPC = {'на_тёмном': SUB, 'на_светлом': SUB, 'на_красном': '#FFD9D2', 'чёрный': SUB, 'белый': SUB}


def inline(path):
    s = open(path, encoding='utf8').read()
    s = re.sub(r'<\?xml[^>]*>\s*', '', s)
    return re.sub(r' width="[\d.]+" height="[\d.]+"', '', s, count=1)


def tiles(layout, h):
    out = ''
    for f in sorted(glob.glob(os.path.join(D, 'SVG', f'*_ПН_{layout}_*.svg'))):
        sch = next(k for k in BG if f.endswith(k + '.svg'))
        out += (f'<figure style="background:{BG[sch]}"><div class="lg">{inline(f).replace("<svg ", f"<svg style=\"height:{h}mm\" ", 1)}</div>'
                f'<figcaption style="color:{CAPC[sch]}">{CAP[sch]}<br><span>{os.path.basename(f)[:-4]}</span></figcaption></figure>')
    return out


def page(title, num, body, dark=False):
    return (f'<section class="pg{" dk" if dark else ""}"><header><b>ПЛАТФОРМА НЕДВИЖИМОСТИ</b><span>Логотип · {title}</span><i>{num}</i></header>{body}</section>')


css = f'''@page{{size:297mm 210mm;margin:0}}*{{box-sizing:border-box;margin:0}}
@font-face{{font-family:M;src:url("file:///{ROOT.replace(os.sep, '/')}/tools/fonts/Manrope[wght].ttf")}}
body{{font-family:M,sans-serif;color:{INK};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:297mm;height:210mm;padding:14mm 16mm;background:#FFFFFF;page-break-after:always;display:flex;flex-direction:column;gap:8mm;overflow:hidden}}
.pg.dk{{background:{NIGHT};color:{MILK}}}
header{{display:flex;gap:6mm;align-items:baseline;font-size:8pt;letter-spacing:.18em;text-transform:uppercase;color:{SUB}}}
header b{{font-weight:400;color:inherit}} header i{{margin-left:auto;font-style:normal}}
h1{{font-weight:300;font-size:30pt;letter-spacing:-.01em;line-height:1.1}} h2{{font-weight:500;font-size:12pt;margin-bottom:3mm}}
.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;flex:1}}
figure{{border-radius:3mm;padding:6mm 5mm 4mm;display:flex;flex-direction:column;min-height:0;border:.25mm solid #E4E1DB}}
.lg{{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}} .lg svg{{max-width:100%;width:auto}}
figcaption{{font-size:7pt;line-height:1.45;letter-spacing:.02em}} figcaption span{{opacity:.75;font-size:6pt}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:10mm;flex:1}} p,li{{font-size:9pt;line-height:1.55}} ul{{padding-left:4mm}}
.sw{{display:grid;grid-template-columns:repeat(5,1fr);gap:3mm}} .sw div{{border:.25mm solid #E4E1DB;height:26mm;border-radius:3mm;padding:3mm;font-size:7.5pt;display:flex;flex-direction:column;justify-content:flex-end}}
.cs{{background:#fff;border-radius:3mm;display:flex;align-items:center;justify-content:center;padding:6mm}}
table{{border-collapse:collapse;font-size:8.5pt;width:100%}} td{{padding:1.6mm 0;border-bottom:.2mm solid #d9d5ce;vertical-align:top}} td:first-child{{width:38%;color:{SUB}}}
'''

# охранное поле: рамка вокруг горизонтального логотипа = диаметр точки (18 ед. знака)
hz = inline(os.path.join(D, 'SVG', '1.2_ПН_горизонтальный_на_светлом.svg'))
vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', hz).group(1).split()]
x0, y0, w, h = vb[0] + 6, vb[1] + 6, vb[2] - 12, vb[3] - 12          # без отступа файла (6)
cs = (f'<svg viewBox="{x0 - 26} {y0 - 26} {w + 52} {h + 52}" style="width:100%;max-height:52mm">'
      f'<rect x="{x0 - 18}" y="{y0 - 18}" width="{w + 36}" height="{h + 36}" fill="none" stroke="{RED}" stroke-width=".5" stroke-dasharray="2 1.5"/>'
      f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#bbb" stroke-width=".3"/>'
      + re.sub(r'^<svg[^>]*>|</svg>$', '', hz).replace('<title>Платформа недвижимости</title>', '')
      + f'<circle cx="{x0 - 9}" cy="{y0 - 9}" r="9" fill="none" stroke="{RED}" stroke-width=".4"/></svg>')

files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(D, 'SVG', '*.svg')))
rules = f'''<div class="two"><div>
<h2>Охранное поле</h2><div class="cs">{cs}</div>
<p style="margin-top:3mm">Вокруг логотипа — свободное поле не меньше диаметра точки. Внутрь поля не заходят текст, края макета и другие знаки.</p>
<h2 style="margin-top:6mm">Минимальный размер</h2>
<table><tr><td>Горизонтальный</td><td>ширина от 120 px на экране, от 35 мм в печати</td></tr>
<tr><td>Вертикальный</td><td>ширина от 80 px, от 25 мм</td></tr>
<tr><td>Знак «П.»</td><td>от 16 px (фавикон), от 6 мм; меньше — только знак без надписи</td></tr></table>
</div><div>
<h2>Правила</h2><ul>
<li>Точка красная <b>#F5553C</b>. На красном фоне точка чёрная.</li>
<li>Пропорции, разрядку и шрифт не менять, логотип не наклонять, не обводить, без теней и градиентов.</li>
<li>На фото — только на спокойном участке: тёмном (версия «на тёмном») или светлом («на светлом»).</li>
<li>Надписи в файлах переведены в кривые: шрифт для открытия не нужен. Шрифт бренда — Manrope (ПЛАТФОРМА — 300 с разрядкой 0,42 em, НЕДВИЖИМОСТИ — 400 с разрядкой 0,5 em).</li></ul>
<h2 style="margin-top:6mm">Какой файл брать</h2>
<table><tr><td>SVG</td><td>сайт, приложение, передача дизайнеру</td></tr>
<tr><td>PDF</td><td>типография, наружная реклама, документы (вектор)</td></tr>
<tr><td>PNG</td><td>презентации, соцсети, офисные документы (прозрачный фон)</td></tr>
<tr><td>Иконка</td><td>аватар соцсетей, значок приложения, 1024×1024</td></tr></table>
</div></div>'''

sw = ''.join(f'<div style="background:{c};color:{t}"><b style="font-weight:500">{n}</b>{c.upper()} · RGB {", ".join(str(int(c[i:i + 2], 16)) for i in (1, 3, 5))}</div>'
             for n, c, t in (('Красная точка', RED, '#fff'), ('Ночь', NIGHT, MILK), ('Графит', '#1C1C1E', MILK), ('Молоко', MILK, INK), ('Светло-серый', GRAY, INK)))
icons = ''.join(f'<figure style="background:transparent;padding:0;gap:2mm;border:0"><div class="lg">{inline(p).replace("<svg ", "<svg style=\"height:32mm\" ", 1)}</div>'
                f'<figcaption style="color:{SUB}">{os.path.basename(p)[:-4]}</figcaption></figure>'
                for p in sorted(glob.glob(os.path.join(D, 'SVG', '4_*.svg'))))

html = (f'<!doctype html><meta charset="utf-8"><style>{css}</style>'
        + page('версии', '01', f'<h1>Горизонтальный логотип</h1><div class="grid" style="grid-template-columns:repeat(3,1fr)">{tiles("горизонтальный", 16)}</div>')
        + page('версии', '02', f'<h1>Вертикальный логотип</h1><div class="grid">{tiles("вертикальный", 40)}</div>')
        + page('версии', '03', f'<h1>Знак «П.» и иконка</h1><div class="grid" style="flex:0 0 74mm">{tiles("знак", 30)}</div>'
               f'<div class="grid" style="grid-template-columns:repeat(5,1fr);flex:0">{icons}</div>')
        + page('правила', '04', f'<h1>Как использовать</h1>{rules}')
        + page('цвета и файлы', '05', f'<h1>Цвета</h1><div class="sw">{sw}</div><h2 style="margin-top:4mm">Файлы в папке</h2>'
               f'<p style="columns:3;font-size:7.5pt;line-height:1.7">{"<br>".join(files)}<br><br>Каждый — в трёх форматах: SVG/, PDF/, PNG/.</p>'))
tmp = os.path.join(tempfile.gettempdir(), 'pn_logo_doc.html')
open(tmp, 'w', encoding='utf8').write(html)
out = os.path.join(D, 'Логотип_ПЛАТФОРМА_НЕДВИЖИМОСТИ.pdf')
subprocess.run([CHROME, '--headless=new', '--disable-gpu', f'--user-data-dir={os.path.join(tempfile.gettempdir(), "pn_chrome_logo")}',
                '--allow-file-access-from-files', '--virtual-time-budget=4000', '--no-pdf-header-footer', f'--print-to-pdf={out}',
                'file:///' + tmp.replace(os.sep, '/')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
print(out, os.path.getsize(out))
