"""Полный снимок мобильной версии (390 px) кусками — обход лимита Chrome 16384 px. Run из корня репо:
py -3 tools/shot_mobile.py <папка_вывода> [page=index.html] → m_0.png, m_1.png … (по 6000 px) и m_all.jpg (склейка)"""
import os, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, '08_Сайт_пример')
OUT = sys.argv[1]
PAGE = sys.argv[2] if len(sys.argv) > 2 else 'index.html'
C = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'
STEP, H = 6000, 32000
parts = []
for k in range(H // STEP):
    w = (f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:#fff}}div{{width:390px;height:{STEP}px;overflow:hidden}}'
         f'iframe{{border:0;width:390px;height:{H}px;margin-top:-{k * STEP}px;display:block}}</style></head><body><div><iframe src="{PAGE}?shot"></iframe></div></body></html>')
    fn = os.path.join(SITE, '_mw.html'); open(fn, 'w', encoding='utf8').write(w)
    png = os.path.join(OUT, f'm_{k}.png')
    subprocess.run([C, '--headless=new', '--disable-gpu', '--user-data-dir=' + os.environ['TEMP'] + r'\pn_chrome_test', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--virtual-time-budget=7000', f'--window-size=600,{STEP}', '--screenshot=' + png, 'file:///' + fn.replace('\\', '/')], capture_output=True)
    os.remove(fn)
    im = Image.open(png).convert('RGB').crop((0, 0, 390, STEP))
    if im.getextrema() == ((255, 255), (255, 255), (255, 255)): break
    parts.append(im)
allim = Image.new('RGB', (390, STEP * len(parts)), 'white')
for i, p in enumerate(parts): allim.paste(p, (0, i * STEP))
allim.save(os.path.join(OUT, 'm_all.jpg'), quality=82)
print('ok', len(parts))
