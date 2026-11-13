"""Сводная картинка: наш знак и варианты + самые похожие знаки из изобразительного поиска Роспатента (МКТУ 36).
Вход: %TEMP%/pn_be/s_<key>_<i>.png (масштаб 67 %, вид «список с изображением», 50 на странице).
Номер плитки и номер заявки распознаются по шаблонам цифр (шаблоны — из верхнего снимка, где номера известны по порядку).
Выход: _проверка_ТЗ/Похожие_знаки.png/.jpg (чужие знаки — в репозиторий не публикуется)."""
import os, sys, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont

T = os.path.join(os.environ['TEMP'], 'pn_be')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '_проверка_ТЗ')
os.makedirs(OUT, exist_ok=True)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
KEYS = [('now', 'Сейчас: «П.»'), ('leg', '1 · Ножка-точка'), ('base', '2 · Платформа'), ('line', '3 · Монолиния'), ('frame', '4 · Прямой свод')]
ALLN = dict(KEYS + [('roof', '5 · Козырёк'), ('podium', '6 · Подиум'), ('steps', '7 · Ступени'), ('dots', '8 · Отбор')])
if len(sys.argv) > 2:
    KEYS = [(k, ALLN[k]) for k in sys.argv[2].split(',')]
OUTNAME = sys.argv[3] if len(sys.argv) > 3 else 'Похожие_знаки'
FLAGS = {}
fp = os.path.join(T, 'flags.txt')
if os.path.exists(fp):
    for line in open(fp, encoding='utf8'):
        if line.strip():
            k, r, txt = line.rstrip('\n').split('|', 2)
            FLAGS.setdefault(k, {})[int(r)] = txt


def runs(arr, minlen):
    out, s = [], None
    for i, v in enumerate(list(arr) + [False]):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= minlen:
                out.append((s, i))
            s = None
    return out


def tile_boxes(a):
    H, W = a.shape[:2]
    bg = np.abs(a - 248).sum(2) <= 3
    xs = None
    for y in range(150, H - 20, 3):
        r = runs(bg[y, 90:W - 60], 300)
        if len(r) == 4:
            xs = [(s + 90, e + 90) for s, e in r]
            break
    if not xs:
        return []
    rows = [(s, e) for s, e in runs(bg[:, xs[0][0] + 110], 80) if s > 2 and e < H - 3]
    return [(ys, ye, x0, x1) for ys, ye in rows for x0, x1 in xs]


def glyphs(img_rgb):
    """Тёмные (не синие) символы → список бинарных массивов по столбцам."""
    g = img_rgb.astype(int)
    dark = (g.mean(2) < 150) & ((g[..., 2] - g[..., 0]) < 40)
    cols = dark.any(0)
    out = []
    for s, e in runs(cols, 1):
        part = dark[:, s:e]
        ys = np.where(part.any(1))[0]
        if len(ys) == 0:
            continue
        out.append(part[ys[0]:ys[-1] + 1])
    return out


def norm(gl, size=(16, 20)):
    c = np.zeros((size[1], size[0]), float)
    h, w = min(gl.shape[0], size[1]), min(gl.shape[1], size[0])
    c[:h, :w] = gl[:h, :w]
    return c


TPL = {}


def learn(a, boxes):
    for i, (ys, ye, x0, x1) in enumerate(boxes):
        num = str(i + 1)
        gl = glyphs(a[ys + 2:ys + 24, x0 + 2:x0 + 60])
        if len(gl) != len(num):
            continue
        for ch, g in zip(num, gl):
            TPL.setdefault(ch, []).append(norm(g))


def read(gls):
    s = ''
    for g in gls:
        n = norm(g)
        best = min(TPL, key=lambda ch: min(np.abs(n - t).sum() for t in TPL[ch]))
        s += best
    return s


def tiles_of(key):
    """Плитки знака по месту в выдаче. Номер = порядковый индекс в снимке + сдвиг (сдвиг — по большинству распознанных номеров)."""
    from collections import Counter
    res = {}
    for p in sorted(glob.glob(os.path.join(T, f's_{key}_*.png'))):
        a = np.asarray(Image.open(p).convert('RGB')).astype(int)
        boxes = tile_boxes(a)
        reads = []
        for i, (ys, ye, x0, x1) in enumerate(boxes):
            gl = glyphs(a[ys + 2:ys + 24, x0 + 2:x0 + 60])
            r = read(gl) if gl and len(gl) <= 2 else ''
            if r.isdigit():
                reads.append(int(r) - i)
        if not reads:
            continue
        off = Counter(reads).most_common(1)[0][0]
        for i, (ys, ye, x0, x1) in enumerate(boxes):
            n = i + off
            cell = a[ys:ye, x0:x1]
            h, cx = ye - ys, (x1 - x0) // 2
            nonbg = np.abs(cell - 248).sum(2) > 12
            img_ok = nonbg[26:h - 26, 80:-20].sum() > 400
            crop = Image.fromarray(cell[2:h - 1, max(0, cx - int(h * .8)):cx + int(h * .8)].astype('uint8'))
            if n not in res or (img_ok and not res[n][2]):
                res[n] = (crop, '', img_ok)
    return res


# шаблоны цифр: верхний снимок «now», номера идут по порядку с 1
a0 = np.asarray(Image.open(os.path.join(T, 's_now_0.png')).convert('RGB')).astype(int)
learn(a0, tile_boxes(a0))
missing = [d for d in '0123456789' if d not in TPL]
a1 = np.asarray(Image.open(os.path.join(T, 's_leg_0.png')).convert('RGB')).astype(int)
learn(a1, tile_boxes(a1))
print('digits learned:', sorted(TPL), 'missing before 2nd:', missing)

try:
    F = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 26)
    Fs = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 15)
    Fb = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 30)
except OSError:
    F = Fs = Fb = ImageFont.load_default()
COLS, CW, CH, LEFT, GAP = 8, 210, 150, 300, 10
rows_per = (N + COLS - 1) // COLS
SEC = 70 + rows_per * (CH + 34) + 30
canvas = Image.new('RGB', (LEFT + COLS * (CW + GAP) + 40, 150 + SEC * len(KEYS)), '#FFFFFF')
d = ImageDraw.Draw(canvas)
d.text((40, 30), 'Похожие знаки в реестре Роспатента · изобразительный поиск · МКТУ 36 · 13.11.2026', font=Fb, fill='#161617')
d.text((40, 80), f'Порядок — по сходству (алгоритм Роспатента), первые {N}. Под плиткой — место в выдаче. Красная рамка — знаки, на которые стоит обратить внимание.', font=Fs, fill='#77736C')
y0 = 150
report = []
for key, name in KEYS:
    res = tiles_of(key)
    d.line((40, y0 - 14, canvas.width - 40, y0 - 14), fill='#E2DED7', width=2)
    d.text((40, y0), name, font=F, fill='#161617')
    mk = Image.open(os.path.join(T, f'mk_{key}.png')).convert('RGB')
    mk.thumbnail((210, 210))
    canvas.paste(mk, (40, y0 + 50))
    for i in range(N):
        r, c = divmod(i, COLS)
        x, y = LEFT + c * (CW + GAP), y0 + 50 + r * (CH + 34)
        d.rectangle((x, y, x + CW, y + CH), fill='#F8F8F8')
        crop, app, ok = res.get(i + 1, (None, '', False))
        if crop is not None and ok:
            im = crop.copy()
            im.thumbnail((CW - 8, CH - 8))
            canvas.paste(im, (x + (CW - im.width) // 2, y + (CH - im.height) // 2))
        else:
            d.text((x + 30, y + CH // 2 - 9), 'нет изображения в базе', font=Fs, fill='#B5B0A8')
        label = f'№ {i + 1} · {app}' if app else f'№ {i + 1}'
        flag = FLAGS.get(key, {}).get(i + 1)
        if flag:
            d.rectangle((x - 3, y - 3, x + CW + 3, y + CH + 3), outline='#F5553C', width=4)
            label += ' · ' + flag
        d.text((x + 4, y + CH + 5), label, font=Fs, fill='#C2321E' if flag else '#77736C')
        report.append(f'{key}\t{i + 1}\t{app}\t{"ok" if ok else "нет картинки"}')
    y0 += SEC
canvas.save(os.path.join(OUT, OUTNAME + '.png'))
canvas.convert('RGB').save(os.path.join(OUT, OUTNAME + '.jpg'), quality=88)
open(os.path.join(OUT, OUTNAME + '_список.tsv'), 'w', encoding='utf8').write('знак\tместо\tзаявка\tкартинка\n' + '\n'.join(report))
print('ok', canvas.size)
