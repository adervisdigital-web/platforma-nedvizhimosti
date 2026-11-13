"""Обрезка рендеров сайта: убирает пустой низ, сохраняет desktop.png (первый экран 1440×1700), mobile.png (390×2400) и полные версии."""
import sys
import numpy as np
from PIL import Image
T, R = sys.argv[1], sys.argv[2]
S = R + '/08_Сайт_пример/'


def trim(im):
    a = np.asarray(im.convert('RGB'))
    dark = np.where((a.mean(2) < 30).mean(1) > .9)[0]   # футер тёмный — режем по его низу
    rest = a[dark[-1] + 1:] if len(dark) else a[:0]
    if len(dark) and (not len(rest) or np.ptp(rest.reshape(len(rest), -1), axis=1).max() < 12):
        return im.crop((0, 0, im.width, dark[-1] + 1))
    used = np.where(a.reshape(len(a), -1).min(1) < 245)[0]  # иначе — по последней непустой строке
    return im.crop((0, 0, im.width, used[-1] + 1 if len(used) else im.height))


d = trim(Image.open(T + '/site_full.png'))
m = trim(Image.open(T + '/site_m.png').crop((0, 0, 390, 30000)))
d.convert('RGB').save(S + 'full_desktop.jpg', quality=86); m.convert('RGB').save(S + 'full_mobile.jpg', quality=86)
Image.open(T + '/site_first.png').save(S + 'desktop.png'); m.crop((0, 0, 390, 2400)).save(S + 'mobile.png')
print('desktop', d.size, 'mobile', m.size)
