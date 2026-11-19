"""Точечная правка кадра через FLUX: вырезать кусок, увеличить, перерисовать по маске, вернуть и вклеить только маску.
Usage: py -3 tools/flux_fix_region.py <src> <out> <crop x0,y0,x1,y1> <маска> "<prompt>" <denoise> [seed] [длинная сторона, по умолч. 1024]
маска: многоугольники «x,y x,y …;x,y …», «rect:x0,y0,x1,y1», «ell:cx,cy,rx,ry» или «img:mask.png» (во весь кадр); несколько через «|». Координаты — в пикселях src.
Кадр вне маски не меняется (пиксель в пиксель). Нужен запущенный ComfyUI (порт 8188) и tools/flux_masked_i2i.py."""
import glob, os, subprocess, sys, time
from PIL import Image, ImageDraw, ImageFilter

COMFY = r'C:\AI\ComfyUI_windows_portable\ComfyUI'
a = sys.argv
src, out, box, mspec, prompt, den = a[1], a[2], [int(v) for v in a[3].split(',')], a[4], a[5], a[6]
seed = a[7] if len(a) > 7 else ''
longside = int(a[8]) if len(a) > 8 else 1024

im = Image.open(src).convert('RGB')
x0, y0, x1, y1 = box
cw, ch = x1 - x0, y1 - y0
s = longside / max(cw, ch)
W, H = max(16, round(cw * s / 16) * 16), max(16, round(ch * s / 16) * 16)

mask = Image.new('L', im.size, 0)
d = ImageDraw.Draw(mask)
for part in mspec.split('|'):
    part = part.strip()
    if part.startswith('img:'):   # готовая маска во весь кадр (белое — перерисовать)
        mask.paste(255, (0, 0), Image.open(part[4:]).convert('L'))
    elif part.startswith('rect:'):
        d.rectangle([int(v) for v in part[5:].split(',')], fill=255)
    elif part.startswith('ell:'):
        cx, cy, rx, ry = [int(v) for v in part[4:].split(',')]
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    else:
        for poly in part.split(';'):
            d.polygon([tuple(int(v) for v in p.split(',')) for p in poly.split()], fill=255)

crop = im.crop(box).resize((W, H), Image.LANCZOS)
mgrow = mask.filter(ImageFilter.MaxFilter(13)).crop(box).resize((W, H), Image.LANCZOS)   # для FLUX маска шире на ~6 px
tag = f'fx{int(time.time())}'
crop.save(os.path.join(COMFY, 'input', tag + '.png'))
mgrow.convert('RGB').save(os.path.join(COMFY, 'input', tag + '_m.png'))
r = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'flux_masked_i2i.py'), tag + '.png', tag + '_m.png', tag, prompt, den, seed],
                   capture_output=True, text=True, encoding='utf8')
print(r.stdout.strip(), r.stderr.strip()[-500:])
res = sorted(glob.glob(os.path.join(COMFY, 'output', tag + '_*.png')))
if not res:
    sys.exit('нет результата')
gen = Image.open(res[-1]).convert('RGB').resize((cw, ch), Image.LANCZOS)
soft = mask.filter(ImageFilter.GaussianBlur(2.5)).crop(box)
patch = im.crop(box)
patch.paste(gen, (0, 0), soft)
im.paste(patch, (x0, y0))
im.save(out)
print('saved', out)
