"""Logo marks for the three variants (light / dark / bright). All built on the letter П."""


def mark_L_old(w, ink="#1D1D1B", acc="#B4532A", label="x"):
    # slab resting on two supports, thin shadow gap between slab and legs
    h = round(w * 34 / 40, 2)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 40 34" role="img" aria-label="{label}">'
            f'<rect x="0" y="0" width="40" height="8" fill="{acc}"/>'
            f'<rect x="5" y="10" width="9" height="24" fill="{ink}"/>'
            f'<rect x="26" y="10" width="9" height="24" fill="{ink}"/></svg>')


def mark_D(w, front='#F2F1EE', top='#A7ACB4', side='#5C616B', glow='#FFB547', label='Знак «Портал»', mono=None):
    # П extruded in axonometry; warm light on the inner wall of the doorway
    if mono:
        front = top = side = glow = mono
    h = round(w * 36 / 36, 2)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 36 36" role="img" aria-label="{label}">'
            f'<polygon points="0,8 8,0 36,0 28,8" fill="{top}"/>'
            f'<polygon points="28,8 36,0 36,28 28,36" fill="{side}"/>'
            f'<polygon points="8,16 16,16 16,28 8,36" fill="{glow}"/>'
            f'<path d="M0 8 H28 V36 H20 V16 H8 V36 H0 Z" fill="{front}"/></svg>')


def _mark_Y_assembly(w, c1='#2E4BFF', c2='#FF6B2C', c3='#18B26B', label='Знак «Сборка»'):
    # П assembled from three mitred parts: квартиры (left), ремонт (top), дома (right)
    h = round(w * 36 / 40, 2)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 40 36" role="img" aria-label="{label}">'
            f'<polygon points="0,0 40,0 30,10 10,10" fill="{c2}"/>'
            f'<polygon points="0,3 10,13 10,36 0,36" fill="{c1}"/>'
            f'<polygon points="40,3 40,36 30,36 30,13" fill="{c3}"/></svg>')
def mark_L(w, ink='#B4532A', acc=None, label='Знак «Арка»'):
    # square block with an arched doorway: the letter П and an entrance to a stone house
    h = round(w * 40 / 36, 2)
    d = 'M0 0 H36 V40 H26 V20 A8 8 0 0 0 10 20 V40 H0 Z'
    extra = f'<rect x="10" y="34" width="16" height="6" fill="{acc}"/>' if acc else ''
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 36 40" role="img" aria-label="{label}">'
            f'<path d="{d}" fill="{ink}"/>{extra}</svg>')


# ---------- arch family: shape switch (set marks.SHAPE before generating a variant) ----------
import math as _m
SHAPE = 'arch'
_ARCH_D = 'M0 0 H36 V40 H26 V20 A8 8 0 0 0 10 20 V40 H0 Z'


def _poly(pts):
    return 'M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + ' Z'


def _masonry_d_old():
    """Arch block built from stone: radial voussoirs with a raised keystone, staggered brick courses around it."""
    g = 0.9                      # joint width
    cx, cy, r0, r1 = 18, 20, 8, 13.2
    R = r1 + g                   # clearance around the voussoir ring
    out = []
    # voussoirs: 7 wedges over 180°, middle one is the keystone (taller)
    n = 7
    for i in range(n):
        a0 = _m.pi - i * _m.pi / n - (g / 2) / ((r0 + r1) / 2)
        a1 = _m.pi - (i + 1) * _m.pi / n + (g / 2) / ((r0 + r1) / 2)
        if i == 0: a0 = _m.pi
        if i == n - 1: a1 = 0
        ro = r1 + (1.6 if i == n // 2 else 0)
        pts = [(cx + r0 * _m.cos(a0), cy - r0 * _m.sin(a0))]
        for t in [a0 + (a1 - a0) * k / 6 for k in range(7)]:
            pts.append((cx + ro * _m.cos(t), cy - ro * _m.sin(t)))
        for t in [a1 + (a0 - a1) * k / 6 for k in range(7)]:
            pts.append((cx + r0 * _m.cos(t), cy - r0 * _m.sin(t)))
        out.append(_poly(pts))
    # courses: 7 rows, staggered joints; bricks keep a joint's distance from the ring and the keystone
    nr = 7; hgt = 40 / nr
    rows = [(i * hgt, (i + 1) * hgt - g if i < nr - 1 else 40) for i in range(nr)]
    kt = _m.pi * 3 / 7
    k_half = (r1 + 1.6) * _m.cos(kt) + g / 2 + g     # keystone half-width + joint
    k_top = cy - (r1 + 1.6) * _m.sin(kt) - g          # keystone top + joint
    def edge(y, left):
        dy = y - cy
        xs = []
        if dy < 0 and abs(dy) < R:
            h = _m.sqrt(R * R - dy * dy); xs.append(cx - h if left else cx + h)
        if k_top <= y < cy:
            xs.append(cx - k_half if left else cx + k_half)
        if not xs:
            return None
        return min(xs) if left else max(xs)
    for ri, (y0, y1) in enumerate(rows):
        joints = [9, 18, 27] if ri % 2 == 0 else [4.5, 13.5, 22.5, 31.5]
        edges = [0] + joints + [36]
        ys = [y0 + (y1 - y0) * k / 10 for k in range(11)]
        for a_, b_ in zip(edges[:-1], edges[1:]):
            x0, x1 = a_ + (g / 2 if a_ > 0 else 0), b_ - (g / 2 if b_ < 36 else 0)
            if y0 >= cy:
                for lo, hi in ((0, 10), (26, 36)):
                    xa, xb = max(x0, lo), min(x1, hi)
                    if xb - xa > 1.5:
                        out.append(_poly([(xa, y0), (xb, y0), (xb, y1), (xa, y1)]))
                continue
            L = [edge(y, True) for y in ys]; Rr = [edge(y, False) for y in ys]
            if all(e is None for e in L):
                out.append(_poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])); continue
            # piece left of the obstacle
            lim = [min(x1, e) if e is not None else x1 for e in L]
            if min(lim) - x0 > 1.5:
                out.append(_poly([(x0, y0)] + [(xx, y) for xx, y in zip(lim, ys)] + [(x0, y1)]))
            lim = [max(x0, e) if e is not None else x0 for e in Rr]
            if x1 - max(lim) > 1.5:
                out.append(_poly([(x1, y0)] + [(xx, y) for xx, y in zip(lim, ys)] + [(x1, y1)]))
    return ' '.join(out)


from masonry2 import masonry_d as _masonry_d  # redesigned symmetric masonry


def _vault_d():
    """Arch block with an inner door frame and a threshold step."""
    frame = ('M11.6 37 V20 A6.4 6.4 0 0 1 24.4 20 V37 H23.2 V20 A5.2 5.2 0 0 0 12.8 20 V37 Z')
    step = 'M7 37.6 H29 V40 H7 Z'
    return _ARCH_D + ' ' + frame + ' ' + step


def arch_d(shape=None):
    s = shape or SHAPE
    return _masonry_d() if s == 'masonry' else _vault_d() if s == 'vault' else _ARCH_D


def mark_L(w, ink='#B4532A', acc=None, label='Знак'):
    h = round(w * 40 / 36, 2)
    d = _ARCH_D if (SHAPE == 'masonry' and float(w) < 44) else arch_d()   # small sizes: simplified mark
    extra = f'<rect x="10" y="34" width="16" height="6" fill="{acc}"/>' if acc else ''
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 36 40" role="img" aria-label="{label}">'
            f'<path d="{d}" fill="{ink}"/>{extra}</svg>')


# ---------- «Модуль»: П из 7 модулей сетки 3×3, один модуль-акцент ----------
SHAPE_Y = 'assembly'
MOD = ('#0E9F8E', '#F6B93B')          # modules, accent module
MOD_CELLS = [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]
MOD_S, MOD_G, MOD_R = 10.4, 2.4, 2.2


def module_rects(cells=None, accent=(1, 0), main=None, acc=None, cls=False):
    main = main or MOD[0]; acc = acc or MOD[1]
    out = ''
    for (c, r) in (cells or MOD_CELLS):
        x, y = c * (MOD_S + MOD_G), r * (MOD_S + MOD_G)
        a = (c, r) == accent
        k = f' class="{"p2" if a else "p1"}"' if cls else f' fill="{acc if a else main}"'
        out += f'<rect{k} x="{x:.1f}" y="{y:.1f}" width="{MOD_S}" height="{MOD_S}" rx="{MOD_R}"/>'
    return out


def mark_Y(w, c1='#2E4BFF', c2='#FF6B2C', c3='#18B26B', label='Знак'):
    if SHAPE_Y != 'module':
        return _mark_Y_assembly(w, c1, c2, c3, label)
    if c1 == c2 == c3 and c1 != MOD[0]:          # one-colour version (white, black, grey)
        inner = module_rects(main=c1, acc=c1)
    else:
        inner = module_rects()
    return f'<svg width="{w}" height="{w}" viewBox="0 0 36 36" role="img" aria-label="{label}">{inner}</svg>'


def glyph(kind, w, main=None, acc=None):
    """Direction glyphs built from the same modules: квартиры (tower), ремонт (wall + module being placed), дома (house)."""
    main = main or MOD[0]; acc = acc or MOD[1]
    if kind == 'flat':
        cells, a, vb = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)], (1, 0), '0 0 23.2 36'
        inner = module_rects(cells, a, main, acc)
    elif kind == 'renov':
        cells = [(0, 1), (1, 1), (2, 1), (0, 2), (2, 2)]
        inner = module_rects(cells, None, main, acc)
        inner += f'<rect x="{(MOD_S + MOD_G):.1f}" y="2" width="{MOD_S}" height="{MOD_S}" rx="{MOD_R}" fill="{acc}" transform="rotate(-12 18 7)"/>'
        vb = '0 0 36 36'
    else:
        cells = [(0, 1), (1, 1), (2, 1), (0, 2), (2, 2)]
        inner = module_rects(cells, None, main, acc)
        inner += f'<path d="M0 10.4 L18 0 L36 10.4 Z" fill="{acc}"/>'
        vb = '0 0 36 36'
    W, H = [float(x) for x in vb.split()[2:]]
    return f'<svg width="{w * W / 36:.1f}" height="{w * H / 36:.1f}" viewBox="{vb}" aria-hidden="true">{inner}</svg>'
