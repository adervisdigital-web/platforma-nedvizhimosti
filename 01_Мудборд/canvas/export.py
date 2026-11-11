import re, os, subprocess, time
from PIL import Image

S = os.path.dirname(os.path.abspath(__file__)).replace(chr(92), '/')
OUT = 'C:/Users/MSI/Desktop/ПЛАТФОРМА -приложение/01_Мудборд'
H = OUT + '/_html'
SRC = 'C:/Users/MSI/Desktop/ПЛАТФОРМА -приложение/_source/houses/'
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
imgs = {'b471f2a087272c564fa40cb48156b5a1': 'house-gable.jpg', '241aa9c6494b7c64ac1bea49f925807d': 'house-flat.jpg', '2ef3674ef6e253cb347aaef38d116872': 'house-wood.jpg'}
names = {'Main.dc.html': '1_Надёжная_опора', 'Blueprint.dc.html': '2_Чертёж', 'Ural.dc.html': '3_Уральский_дом'}
os.makedirs(H, exist_ok=True)
pngs = []
for f, n in names.items():
    t = open(f'{S}/{f}', encoding='utf8').read()
    head = re.search(r'<helmet>(.*?)</helmet>', t, re.S).group(1)
    body = re.search(r'</helmet>(.*?)</x-dc>', t, re.S).group(1)
    for k, v in imgs.items():
        body = body.replace(f'/_blob/{k}', '../../_source/houses/' + v)
    html = f'<!doctype html><html lang="ru"><head><meta charset="utf-8">{head}</head><body>{body}</body></html>'
    hp = f'{H}/{n}.html'
    open(hp, 'w', encoding='utf8').write(html)
    png = f'{OUT}/{n}.png'
    if os.path.exists(png): os.remove(png)
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--virtual-time-budget=10000', '--window-size=1440,1900', '--force-device-scale-factor=1',
                    f'--screenshot={png.replace("/", chr(92))}', 'file:///' + hp], capture_output=True, timeout=120)
    print(n, os.path.exists(png) and os.path.getsize(png))
    pngs.append(png)
ims = [Image.open(p).convert('RGB') for p in pngs if os.path.exists(p)]
if ims:
    ims[0].save(f'{OUT}/Мудборд_Платформа_3_направления.pdf', save_all=True, append_images=ims[1:], resolution=144)
    print('pdf ok')
