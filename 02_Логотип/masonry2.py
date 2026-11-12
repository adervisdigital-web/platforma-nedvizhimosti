import math as _m


def _poly(pts):
    return 'M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + ' Z'


def masonry_d():
    """Symmetric masonry arch-«П»: 8 courses, 9 voussoirs with a raised keystone, clean jambs, no slivers."""
    g = 0.9
    cx, cy = 18.0, 19.1          # springing line just above course 4
    r0, r1, kx = 8.0, 12.2, 2.0  # inner / outer radius, keystone extra
    n = 9
    out = []
    da = _m.pi / n
    # --- voussoirs
    key_poly = None
    for i in range(n):
        a0 = _m.pi - i * da - (0 if i == 0 else g / 2 / ((r0 + r1) / 2))
        a1 = _m.pi - (i + 1) * da + (0 if i == n - 1 else g / 2 / ((r0 + r1) / 2))
        ro = r1 + (kx if i == n // 2 else 0)
        pts = [(cx + ro * _m.cos(a0 + (a1 - a0) * k / 8), cy - ro * _m.sin(a0 + (a1 - a0) * k / 8)) for k in range(9)]
        pts += [(cx + r0 * _m.cos(a1 + (a0 - a1) * k / 8), cy - r0 * _m.sin(a1 + (a0 - a1) * k / 8)) for k in range(9)]
        if i == n // 2:
            key_poly = pts
        out.append(pts)
    # clearance boundary for wall bricks (left half): ring + joint, keystone + joint
    R = r1 + g
    ka = _m.pi / 2 + da / 2           # keystone left edge angle
    kx_out = cx + (r1 + kx) * _m.cos(ka)   # keystone outer-left x
    k_top = cy - (r1 + kx) * _m.sin(ka) - g

    def edge(y):
        """x of the free wall boundary on the left at height y (None = no obstacle)."""
        xs = []
        dy = y - cy
        if dy <= 0 and abs(dy) < R:
            xs.append(cx - _m.sqrt(R * R - dy * dy))
        if k_top <= y <= cy - r1:
            xs.append(kx_out - g)
        return min(xs) if xs else None

    rows = [(5 * k, 5 * k + 5 - g if k < 7 else 40.0) for k in range(8)]
    left = []
    for ri, (y0, y1) in enumerate(rows):
        ys = [y0 + (y1 - y0) * k / 12 for k in range(13)]
        if y0 >= cy:                                       # jambs: alternate stretcher / two headers
            if ri % 2 == 0:
                left.append(([(0, y0), (10, y0), (10, y1), (0, y1)], False))
            else:
                left.append(([(0, y0), (4.55, y0), (4.55, y1), (0, y1)], False))
                left.append(([(5.45, y0), (10, y0), (10, y1), (5.45, y1)], False))
            continue
        joints = [9.0, 18.0] if ri % 2 == 0 else [4.5, 13.5]
        bounds = [0.0] + joints
        es = [edge(y) for y in ys]
        free = all(e is None for e in es)
        lim = [e if e is not None else 18.0 for e in es]
        mn = min(lim)
        for j, a in enumerate(bounds):
            b = bounds[j + 1] if j + 1 < len(bounds) else 18.0
            x0 = a + (g / 2 if a > 0 else 0)
            x1 = b - g / 2
            if free:
                if b == 18.0 and ri % 2 == 0:
                    x1 = 18.0 - g / 2
                elif b == 18.0:
                    x1 = 18.0          # brick crosses the centre: mirrored half closes it
                left.append(([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], b == 18.0 and ri % 2 == 1))
                continue
            nxt = bounds[j + 2] if j + 2 < len(bounds) else 18.0
            if x0 >= mn - 2.4:
                break                                     # no room for a decent brick
            # if the next brick would be a sliver, extend this one to the curve
            if b >= mn - 2.4 or (b + g / 2) >= mn - 2.4:
                pts = [(x0, y0)] + [(max(x0 + 1.2, l), y) for l, y in zip(lim, ys)] + [(x0, y1)]
                left.append((pts, False))
                break
            left.append(([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], False))
    # mirror the wall to the right; bricks touching x=18 merge with their mirror
    walls = []
    for p, cross in left:
        if cross:
            xs0 = min(x for x, _ in p); y0 = min(y for _, y in p); y1 = max(y for _, y in p)
            walls.append([(xs0, y0), (36 - xs0, y0), (36 - xs0, y1), (xs0, y1)])
        else:
            walls.append(p)
            walls.append([(36 - x, y) for x, y in reversed(p)])
    return ' '.join(_poly(p) for p in out + walls)
