"""Photo-real brand mockups: render artwork per surface (transparent PNG via Edge), warp onto measured quads,
blend with the photo's own light. Output: _source/gen/life_{L,D,Y}_{surface}.jpg"""
import os, sys, subprocess
import numpy as np, cv2

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'v3'))
from marks import mark_L, mark_D, mark_Y          # noqa: E402
from gen_v3 import V, lockup                      # noqa: E402

PROJ = 'C:/Users/MSI/Desktop/ПЛАТФОРМА -приложение'
GEN = PROJ + '/_source/gen/'
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
ART = os.path.join(HERE, 'art')
os.makedirs(ART, exist_ok=True)
imread = lambda p, f=cv2.IMREAD_COLOR: cv2.imdecode(np.fromfile(p, np.uint8), f)
imwrite = lambda p, im, q: cv2.imencode('.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, q])[1].tofile(p)
FILE = lambda p: 'file:///' + p.replace('\\', '/').replace(' ', '%20')


def tag_quad():
    # keychain: inside-stitching body of the tag (measured on full-res crop)
    BL = np.array([725.0, 617.5]); BR = np.array([917.5, 520.0]); LT = np.array([617.5, 400.0])
    RT = LT + (BR - BL)
    return [LT, RT, BR, BL]


SURF = {
    #   name       base photo           canvas (w,h)   quad TL,TR,BR,BL (photo px)                                        mode
    'facade':   ('mk_facade.jpg',    (563, 255), [(401, 302.5), (962.5, 303.5), (962.5, 555.5), (401, 555.5)], 'emissive'),
    'billboard': ('mk_billboard.jpg', (733, 292), [(430, 216.5), (1148.5, 220.5), (1158, 508.5), (421, 499.5)], 'board'),
    'keys':     ('mk_keys.jpg',      (216, 243), [tuple(p) for p in tag_quad()], 'print'),
    'helmet':   ('mk_helmet_front.jpg', (300, 70), dict(cx=676, R=262, x0=528, x1=824, y0=452, hh=64, arc=5), 'curve'),
    'bag':      ('mk_bag.jpg',       (383, 430), [(503, 285), (886, 286), (874, 725), (482, 697)], 'print'),
    'fence':    ('mk_fence.jpg',     (1176, 285), [(88, 369), (1263, 347.5), (1263, 657), (88, 626)], 'banner'),
    'store':    ('mk_store.jpg',     (1220, 104), [(82, 298), (1302, 298), (1302, 401), (82, 401)], 'letters'),
    'plate':    ('mk_plate.jpg',     (307, 353), [(194, 167), (808, 167), (808, 873), (194, 873)], 'print'),
    'vest':     ('mk_vest.jpg',      (300, 150), [(622.4, 418.7), (986.3, 424.5), (976.0, 589.1), (636.3, 582.8)], 'fabric'),
}


def page(v, w, h, body, bg='transparent'):
    return (f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?{v["gf"]}&amp;display=swap" rel="stylesheet">'
            f'<style>html,body{{margin:0;background:{bg}}}</style></head><body><div style="width:{w}px;height:{h}px;position:relative;overflow:hidden;'
            f'font-family:\'{v["F"]}\',sans-serif">{body}</div></body></html>')


def colored_mark(v, w, light_surface=True):
    k = v['key']
    if k == 'L':
        return mark_L(w, v['acc'])
    if k == 'D':
        return mark_D(w, front='#14120E', top='#7A7F87', side='#3A3D43', glow='#FFB547') if light_surface else mark_D(w)
    return mark_Y(w, *v['dir'])


def art_html(v, surf):
    k, F, FH = v['key'], v['F'], v['FH']
    w, h = SURF[surf][1]
    center = lambda inner, extra='': f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;{extra}">{inner}</div>'
    if surf == 'facade':
        bg = {'L': '#FBF9F5', 'D': '#0B0C0E', 'Y': '#FFFFFF'}[k]
        ink = {'L': '#1F1D1B', 'D': '#F2F1EE', 'Y': '#14161F'}[k]
        sub = {'L': '#7A7368', 'D': '#8D929A', 'Y': '#6B6F7D'}[k]
        stripe = ''
        if k == 'L':
            stripe = f'<div style="position:absolute;left:0;right:0;bottom:0;height:9px;background:{v["acc"]}"></div>'
        if k == 'Y':
            stripe = '<div style="position:absolute;left:0;right:0;bottom:0;height:9px;display:flex">' + ''.join(f'<div style="flex:1;background:{c}"></div>' for c in v['dir']) + '</div>'
        if k == 'D':
            stripe = f'<div style="position:absolute;left:0;right:0;bottom:0;height:3px;background:{v["acc"]};opacity:.9"></div>'
        return page(v, w, h, center(lockup(v, 40, ink, sub, mw=70)) + stripe, bg)
    if surf == 'billboard':
        kitchen = FILE(GEN + 'kv_kitchen.jpg')
        if k == 'L':
            vis = f'<div style="width:150px;height:232px;border-radius:75px 75px 0 0;overflow:hidden;flex:none;align-self:flex-end"><img src="{kitchen}" style="width:100%;height:100%;object-fit:cover"></div>'
            bg, ink, sub, head = '#F2EEE7', '#1F1D1B', '#7A7368', 'Входите.<br>Дальше мы сами.'
            hs, hw = 44, 700
        elif k == 'D':
            vis = f'<div style="flex:none">{mark_D(190)}</div>'
            bg, ink, sub, head = '#0E0F11', '#F2F1EE', '#8D929A', 'Дом, в котором<br>уже горит свет'
            hs, hw = 40, 600
        else:
            vis = f'<div style="flex:none">{mark_Y(206, *v["dir"])}</div>'
            bg, ink, sub, head = '#FFFFFF', '#14161F', '#6B6F7D', 'Квартира.<br>Ремонт. Дом.'
            hs, hw = 36, 600
        small = lockup(v, 16, ink, sub, mw=26)
        body = (f'<div style="position:absolute;inset:0;background:{bg};display:flex;align-items:center;gap:34px;padding:30px 40px 0 44px;box-sizing:border-box">'
                f'{vis}<div style="display:flex;flex-direction:column;gap:22px;color:{ink}"><div style="font:{hw} {hs}px/1.04 \'{FH}\',sans-serif;letter-spacing:-0.02em">{head}</div>{small}</div></div>')
        if k == 'Y':
            body += '<div style="position:absolute;left:0;right:0;bottom:0;height:10px;display:flex">' + ''.join(f'<div style="flex:1;background:{c}"></div>' for c in v['dir']) + '</div>'
        if k == 'L':
            body += f'<div style="position:absolute;left:0;right:0;bottom:0;height:10px;background:{v["acc"]}"></div>'
        return page(v, w, h, body, bg)
    if surf == 'fence':
        bg = {'L': '#FBF9F5', 'D': '#0E0F11', 'Y': '#FFFFFF'}[k]
        ink = {'L': '#1F1D1B', 'D': '#F2F1EE', 'Y': '#14161F'}[k]
        sub = {'L': '#7A7368', 'D': '#8D929A', 'Y': '#6B6F7D'}[k]
        btn = v['dir'][0] if k == 'Y' else v['acc']
        stripe = ''
        if k == 'Y':
            stripe = '<div style="position:absolute;left:0;right:0;top:0;height:14px;display:flex">' + ''.join(f'<div style="flex:1;background:{c}"></div>' for c in v['dir']) + '</div>'
        elif k == 'L':
            stripe = f'<div style="position:absolute;left:0;top:0;bottom:0;width:18px;background:{v["acc"]}"></div>'
        q = "'"
        body = (f'<div style="position:absolute;inset:0;background:{bg};display:flex;align-items:center;justify-content:space-between;padding:0 56px 0 70px;box-sizing:border-box">'
                f'{lockup(v, 36 if k == "Y" else 44, ink, sub, mw=64 if k == "Y" else 78)}'
                f'<div style="display:flex;align-items:center;gap:34px"><div style="display:flex;flex-direction:column;gap:6px;text-align:right;color:{ink}">'
                f'<span style="font:600 {26 if k == 'Y' else 30}px/1.1 {q}{FH}{q},sans-serif;white-space:nowrap">Строим каменный дом</span><span style="font:400 22px {q}{F}{q},sans-serif;color:{sub};white-space:nowrap">этап 3 из 7</span></div>'
                f'<span style="padding:22px 30px;background:{btn};color:{v["acc_ink"]};font:600 26px {q}{F}{q},sans-serif;white-space:nowrap">Хочу такой дом</span></div></div>')
        return page(v, w, h, body + stripe, bg)
    if surf == 'store':
        ink = {'L': '#1F1D1B', 'D': '#14120E', 'Y': '#14161F'}[k]
        sub = {'L': '#7A7368', 'D': '#4A4E55', 'Y': '#6B6F7D'}[k]
        return page(v, w, h, center(lockup(v, 40, ink, sub, mono=('LIGHTBG' if k == 'D' else None), mw=66)))
    if surf == 'plate':
        ink = '#1F1D1B'; mut = '#6E6A63'; line = '#D9D5CE'
        bar = (''.join(f'<div style="flex:1;background:{c}"></div>' for c in v['dir'])) if k == 'Y' else f'<div style="flex:1;background:{"#14120E" if k == "D" else v["acc"]}"></div>'
        rows = (('Объект', 'Индивидуальный жилой дом'), ('Материал', 'кирпич, 2 этажа'), ('Заказчик', '[ФИО]'), ('Подрядчик', 'ПЛАТФОРМА НЕДВИЖИМОСТИ'),
                ('Начало работ', '[ДАТА]'), ('Окончание', '[ДАТА]'), ('Прораб', '[ФИО]'), ('Телефон', '+7 [ТЕЛЕФОН]'))
        q = "'"
        rr = ''.join(f'<div style="display:flex;justify-content:space-between;gap:8px;padding:5px 0;border-bottom:1px solid {line};font:400 10.5px {q}{F}{q},sans-serif"><span style="color:{mut}">{a}</span><span style="text-align:right;color:{ink}">{b}</span></div>' for a, b in rows)
        mk = mark_L(24, v['acc']) if k == 'L' else (mark_D(26, front='#14120E', top='#7A7F87', side='#3A3D43', glow='#FFB547') if k == 'D' else mark_Y(28, *v['dir']))
        word = f'<span style="font:{v["word_w"]} {round(15 * v["word_k"])}px {q}{FH}{q},sans-serif;letter-spacing:{v["word_ls"]};color:{ink}">ПЛАТФОРМА</span>'
        body = (f'<div style="position:absolute;left:30px;right:30px;top:34px;bottom:34px;display:flex;flex-direction:column;gap:10px">'
                f'<div style="display:flex;height:6px">{bar}</div>'
                f'<div style="display:flex">{lockup(v, 17, ink, mut, mono=("LIGHTBG" if k == "D" else None), mw=28)}</div>'
                f'<div style="font:700 19px {q}{F}{q},sans-serif;color:{ink}">Паспорт объекта</div><div>{rr}</div></div>')
        return page(v, w, h, body)
    ink_l = {'L': '#1F1D1B', 'D': '#14120E', 'Y': '#14161F'}[k]
    sub_l = {'L': '#7A7368', 'D': '#4A4E55', 'Y': '#6B6F7D'}[k]
    mono_l = 'LIGHTBG' if k == 'D' else None
    if surf == 'keys':
        return page(v, w, h, f'<div style="position:absolute;left:0;right:0;top:{round(h * 0.30)}px;display:flex;justify-content:center">{lockup(v, 22, ink_l, sub_l, mono=mono_l, mw=64, vertical=True)}</div>')
    if surf == 'helmet':
        return page(v, w, h, center(lockup(v, 30, ink_l, sub_l, mono=mono_l, mw=50)))
    if surf == 'bag':
        ink = {'L': '#1F1D1B', 'D': '#14120E', 'Y': '#14161F'}[k]
        return page(v, w, h, f'<div style="position:absolute;left:0;right:0;top:{round(h * 0.46)}px;display:flex;justify-content:center">{lockup(v, 30, ink, sub_l, mono=mono_l, mw=84, vertical=True)}</div>')
    if surf == 'vest':
        return page(v, w, h, center(lockup(v, 26, '#FFFFFF', '#FFFFFF', mono='#FFFFFF', mw=56, vertical=True)))


def render(v, surf):
    w, h = SURF[surf][1]
    hp = os.path.join(ART, f'{v["key"]}_{surf}.html')
    open(hp, 'w', encoding='utf8').write(art_html(v, surf))
    png = os.path.join(ART, f'{v["key"]}_{surf}.png')
    if os.path.exists(png):
        os.remove(png)
    import time
    for attempt in range(4):
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--default-background-color=00000000',
                        '--force-device-scale-factor=2', f'--window-size={w},{max(h, 120)}', '--virtual-time-budget=8000', f'--screenshot={png}', FILE(hp)],
                       capture_output=True, timeout=120)
        if os.path.exists(png):
            break
        time.sleep(2)
    if h < 120:  # window was padded; crop back to the canvas
        im = cv2.imread(png, cv2.IMREAD_UNCHANGED); cv2.imwrite(png, im[:h * 2])
    return png


def composite(v, surf):
    base_name, (w, h), quad, mode = SURF[surf]
    base = imread(GEN + base_name).astype(np.float32) / 255.0
    H, W = base.shape[:2]
    art = imread(render(v, surf), cv2.IMREAD_UNCHANGED).astype(np.float32) / 255.0
    if art.shape[2] == 3:
        art = np.dstack([art, np.ones(art.shape[:2], np.float32)])
    ah, aw = art.shape[:2]
    src = np.float32([[0, 0], [aw, 0], [aw, ah], [0, ah]])
    if mode == 'curve':
        c = quad
        xs, ys = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
        th0, th1 = np.arcsin((c['x0'] - c['cx']) / c['R']), np.arcsin((c['x1'] - c['cx']) / c['R'])
        th = np.arcsin(np.clip((xs - c['cx']) / c['R'], -1, 1))
        u = (th - th0) / (th1 - th0)
        sn = (xs - (c['x0'] + c['x1']) / 2) / ((c['x1'] - c['x0']) / 2)
        top = c['y0'] - c['arc'] * sn ** 2
        vv = (ys - top) / (c['hh'] * np.cos(th).clip(0.35, 1) ** 0.15)
        warped = cv2.remap(art, (u * aw).astype(np.float32), (vv * ah).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        dst = np.float32([[c['x0'], c['y0'] - c['arc']], [c['x1'], c['y0'] - c['arc']], [c['x1'], c['y0'] + c['hh']], [c['x0'], c['y0'] + c['hh']]])
        mode = 'print'
    else:
        dst = np.float32(quad)
        M = cv2.getPerspectiveTransform(src, dst)
        warped = cv2.warpPerspective(art, M, (W, H), flags=cv2.INTER_AREA if aw > 400 else cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    rgb, a = warped[..., :3], warped[..., 3:4]
    gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
    mask = np.zeros((H, W), np.uint8)
    cv2.fillConvexPoly(mask, dst.astype(np.int32), 1)
    region = gray[mask > 0]
    if mode == 'print':
        shade = np.clip(gray / np.percentile(region, 96), 0, 1.03)[..., None]
        a = cv2.GaussianBlur(a, (0, 0), 0.6)[..., None] * 0.96 if a.ndim == 2 else cv2.GaussianBlur(a[..., 0], (0, 0), 0.6)[..., None] * 0.96
        out = base * (1 - a) + (rgb * shade) * a
    elif mode == 'fabric':
        # folds: push the print along the fabric's luminance gradient, then shade by the fabric light
        g = cv2.GaussianBlur(gray, (0, 0), 7)
        dx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=5); dy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=5)
        xs, ys = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
        k_ = 9.0 / (np.abs(dx).max() + 1e-6)
        warped = cv2.remap(warped, xs - dx * k_, ys - dy * k_, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        rgb, a = warped[..., :3], warped[..., 3:4]
        shade = np.clip(gray / np.median(region), 0.5, 1.15)[..., None]
        detail = (gray - cv2.GaussianBlur(gray, (0, 0), 2.0))[..., None]
        ink = np.clip(rgb * shade * 0.94 + detail * 0.9, 0, 1)
        a2 = cv2.GaussianBlur(a[..., 0], (0, 0), 0.7)[..., None] * 0.9
        out = base * (1 - a2) + ink * a2
    elif mode == 'board':
        shade = np.clip(gray / np.percentile(region, 98), 0, 1.0)[..., None]
        shade = cv2.GaussianBlur(shade[..., 0], (0, 0), 3)[..., None]
        out = base * (1 - a) + (rgb * (0.12 + 0.9 * shade)) * a
    elif mode == 'banner':
        # exact fabric silhouette (with its sag), slightly grown so no white fringe is left
        hsv = cv2.cvtColor((base * 255).astype(np.uint8), cv2.COLOR_BGR2HSV)
        grow = cv2.dilate(mask, np.ones((25, 25), np.uint8))
        fabric = ((hsv[..., 2] > 115) & (hsv[..., 1] < 60) & (grow > 0)).astype(np.uint8)
        fabric = cv2.morphologyEx(fabric, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
        n, lab, stats, _ = cv2.connectedComponentsWithStats(fabric)
        fabric = (lab == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
        cnt = max(cv2.findContours(fabric, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0], key=cv2.contourArea)
        cnt = cv2.approxPolyDP(cnt, 0.0012 * cv2.arcLength(cnt, True), True)
        fill = np.zeros_like(fabric); cv2.fillPoly(fill, [cnt], 1)
        fill = cv2.dilate(fill, np.ones((5, 5), np.uint8))
        fa = cv2.GaussianBlur(fill.astype(np.float32), (0, 0), 0.9)[..., None]
        x, y, bw, bh = cv2.boundingRect(fill)
        q = np.float32(quad); ctr = q.mean(0)
        sx = (bw + 8) / (q[:, 0].max() - q[:, 0].min()); sy = (bh + 8) / (q[:, 1].max() - q[:, 1].min())
        q2 = (q - ctr) * np.float32([sx, sy]) + np.float32([x + bw / 2, y + bh / 2])
        M2 = cv2.getPerspectiveTransform(src, q2)
        rgb2 = cv2.warpPerspective(art, M2, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)[..., :3]
        fr = gray[fabric > 0]
        shade = cv2.GaussianBlur(np.clip(gray / np.percentile(fr, 97), 0, 1.05), (0, 0), 1.2)[..., None]
        sheen = cv2.GaussianBlur(np.clip(gray / np.percentile(fr, 50) - 1, -0.3, 0.3), (0, 0), 2)[..., None]
        ink = np.clip(rgb2 * (0.08 + 0.94 * shade) + 0.10 * sheen + 0.025, 0, 1)
        out = base * (1 - fa) + ink * fa
        a = fa
    elif mode == 'letters':
        a1 = a[..., 0]
        sh = cv2.GaussianBlur(np.roll(np.roll(a1, 4, axis=0), 3, axis=1), (0, 0), 3.0)[..., None] * 0.38
        out = base * (1 - sh)
        shade = np.clip(gray / np.percentile(region, 90), 0.45, 1.05)[..., None]
        out = out * (1 - a) + np.clip(rgb * (0.25 + 0.8 * shade), 0, 1) * a
    else:  # emissive lightbox: own light, slightly brighter centre, faint vertical falloff
        ys = np.linspace(0.95, 1.02, H, dtype=np.float32)[:, None, None]
        glow = np.clip(rgb * ys, 0, 1)
        out = base * (1 - a) + glow * a
        halo = cv2.GaussianBlur((a * glow).astype(np.float32), (0, 0), 14) * 0.18
        out = np.clip(out + halo * (1 - a), 0, 1)
    grain = np.random.default_rng(7).normal(0, 0.006, out.shape).astype(np.float32)
    out = np.clip(out + grain * a, 0, 1)
    dst_path = GEN + f'life_{v["key"]}_{surf}.jpg'
    imwrite(dst_path, (out * 255).astype(np.uint8), 90)
    return dst_path


if __name__ == '__main__':
    keys = sys.argv[1:] or ['L', 'D', 'Y']
    for k in keys:
        for s in SURF:
            print(composite(V[k], s))
