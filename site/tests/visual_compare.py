"""Скриншоты прототипа v40 и сборки (?shot — без заставки и анимаций) на 1440/1920/390 и доля отличающихся пикселей.
Run из корня репо: py -3 -X utf8 site/tests/visual_compare.py [сборка=10_Сайт/index.html] [папка=site/tests/_tmp/visual]
Порог: ≤ 0.5 % пикселей. Иначе — смотреть diff_<w>.jpg глазами."""
import os, sys, time
from PIL import Image, ImageChops
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from cdp import Browser
BUILD = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '10_Сайт', 'index.html'))
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'site', 'tests', '_tmp', 'visual'); os.makedirs(OUT, exist_ok=True)
PROTO = os.path.join(ROOT, '08_Сайт_пример', 'index.html')
MAXH = 14000
url = lambda p: 'file:///' + p.replace('\\', '/') + '?shot'


def grab(b, page, w, mobile, path):
    b.viewport(w, 900, mobile); b.open(url(page), wait=4)
    b.ev('document.querySelectorAll("#lmap,.leaflet-container").forEach(e=>e.style.visibility="hidden")')   # тайлы карты грузятся из сети по-разному
    h = min(int(b.ev('document.documentElement.scrollHeight')), MAXH)
    b.call('Emulation.setDeviceMetricsOverride', width=w, height=h, deviceScaleFactor=1, mobile=mobile); time.sleep(1.5)
    b.shot(path); return Image.open(path).convert('RGB')


b = Browser(); worst = 0; rep = []
for w, mob in ((1440, False), (1920, False), (390, True)):
    a = grab(b, PROTO, w, mob, os.path.join(OUT, f'proto_{w}.png')); c = grab(b, BUILD, w, mob, os.path.join(OUT, f'build_{w}.png'))
    H = min(a.height, c.height); a, c = a.crop((0, 0, w, H)), c.crop((0, 0, w, H))
    d = ImageChops.difference(a, c).convert('L').point(lambda v: 255 if v > 24 else 0)
    frac = sum(d.histogram()[255:]) / (w * H) * 100; worst = max(worst, frac)
    if frac > .05: d.convert('RGB').save(os.path.join(OUT, f'diff_{w}.jpg'), quality=70)
    rep.append(f'{w}px: высота прототип {a.height}/сборка {c.height}, отличается {frac:.3f} % пикселей')
b.close()
print('\n'.join(rep)); print('ИТОГ:', 'ok' if worst <= .5 else f'РАСХОЖДЕНИЕ {worst:.2f} % — смотреть {OUT}')
