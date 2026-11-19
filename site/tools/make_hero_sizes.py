"""Уменьшенные копии больших фоновых фото для srcset: <имя>-1280.jpg и <имя>-1920.jpg рядом с оригиналом.
Оригинал (2880 px) остаётся для широких экранов. Запуск из папки site: py -3 tools/make_hero_sizes.py
После замены фото в списке — запустить снова (копии перезаписываются)."""
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..', 'public', 'assets', 'img')
HEROES = ['ekb_dusk.jpg', 'ekb_aerial.jpg', 'ekb_city.jpg', 'ba_after.jpg', 'houses/y195_1.jpg']

for name in HEROES:
    src = os.path.join(ROOT, name)
    im = Image.open(src).convert('RGB')
    for w in (1280, 1920):
        if im.width <= w:
            continue
        out = src[:-4] + f'-{w}.jpg'
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out, 'JPEG', quality=82, optimize=True, progressive=True)
        print(os.path.relpath(out, ROOT), os.path.getsize(out) // 1024, 'KB')
