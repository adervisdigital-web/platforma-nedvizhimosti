"""Прогулка по сайту в реальном времени: листает экран за экраном с паузой (анимации доигрывают), снимает кадры.
Run из корня репо: py -3 -X utf8 tools/walk.py <папка> [ширина=1440] [высота=900] [mobile=0] [пауза=1.6]
→ <папка>/w<ширина>_NN.png и склейки <папка>/w<ширина>_sheetN.jpg (по 6 кадров)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import Browser
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 1440; H = int(sys.argv[3]) if len(sys.argv) > 3 else 900
MOB = len(sys.argv) > 4 and sys.argv[4] == '1'; PAUSE = float(sys.argv[5]) if len(sys.argv) > 5 else 1.6
URL = 'file:///' + os.path.join(ROOT, '08_Сайт_пример', 'index.html').replace('\\', '/') + '?shot'
b = Browser(); b.viewport(W, H, MOB); b.open(URL, 2.5)
b.ev("document.documentElement.style.scrollBehavior='auto'")
total = b.ev('document.documentElement.scrollHeight'); step = int(H * .9); frames = []
y = 0; k = 0
while y < total:
    b.ev(f'scrollTo(0,{y})'); time.sleep(PAUSE)
    p = os.path.join(OUT, f'w{W}_{k:02d}.png'); b.shot(p); frames.append(p)
    k += 1; y += step; total = b.ev('document.documentElement.scrollHeight')
b.close()
per = 6; tw = 640 if not MOB else 300
for s in range(0, len(frames), per):
    ims = [Image.open(f).convert('RGB') for f in frames[s:s + per]]
    ims = [i.resize((tw, int(i.height * tw / i.width))) for i in ims]
    cols = 3 if not MOB else 6
    rows = (len(ims) + cols - 1) // cols
    o = Image.new('RGB', (cols * (tw + 6), rows * (ims[0].height + 6)), 'white')
    for i, im in enumerate(ims): o.paste(im, ((i % cols) * (tw + 6), (i // cols) * (ims[0].height + 6)))
    o.save(os.path.join(OUT, f'w{W}_sheet{s // per}.jpg'), quality=80)
print('frames', len(frames))
