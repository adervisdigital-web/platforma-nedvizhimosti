"""Иконки сайта-приложения и картинка превью ссылки. Запуск из папки site: py -3 tools/make_icons.py
- public/favicon.ico (16, 32, 48) — для Яндекса и старых браузеров;
- public/assets/icons/: apple-touch-icon.png (180), icon-192.png, icon-512.png, site.webmanifest;
- public/assets/img/og-main.jpg (1200×630) — превью главной в мессенджерах: фото Екатеринбурга, знак «П.», слоган.
Исходник иконки — 09_Логотип_файлы/PNG/4_ПН_иконка_на_тёмном_1024px.png (знак уже в безопасной зоне круглых иконок)."""
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SITE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO = os.path.dirname(SITE)
ICON = os.path.join(REPO, '09_Логотип_файлы', 'PNG', '4_ПН_иконка_на_тёмном_1024px.png')
FONT = os.path.join(REPO, 'tools', 'fonts', 'Manrope[wght].ttf')
OUT = os.path.join(SITE, 'public', 'assets', 'icons')
os.makedirs(OUT, exist_ok=True)

src = Image.open(ICON).convert('RGB')
for name, size in (('apple-touch-icon.png', 180), ('icon-192.png', 192), ('icon-512.png', 512)):
    src.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, name), optimize=True)
src.resize((48, 48), Image.LANCZOS).save(os.path.join(SITE, 'public', 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])

manifest = {
    'name': 'Платформа недвижимости', 'short_name': 'Платформа', 'lang': 'ru',
    'description': 'Квартиры, дома и ремонт в Екатеринбурге — проверенные предложения, ипотека и рассрочка.',
    'start_url': '../../', 'scope': '../../', 'display': 'standalone',
    'background_color': '#0E0E0F', 'theme_color': '#0E0E0F',
    'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any maskable'},
              {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'}],
}
open(os.path.join(OUT, 'site.webmanifest'), 'w', encoding='utf8').write(json.dumps(manifest, ensure_ascii=False, indent=1))

# превью ссылки 1200×630
W, H = 1200, 630
ph = Image.open(os.path.join(SITE, 'public', 'assets', 'img', 'ekb_dusk.jpg')).convert('RGB')
s = max(W / ph.width, H / ph.height); ph = ph.resize((round(ph.width * s), round(ph.height * s)), Image.LANCZOS)
x = round((ph.width - W) * .72); y = round((ph.height - H) * .45)
og = ph.crop((x, y, x + W, y + H))
grad = Image.new('L', (W, 1))
for i in range(W): grad.putpixel((i, 0), int(235 * max(0, 1 - i / (W * .78)) ** 1.1))
shade = Image.new('RGB', (W, H), (13, 10, 8)); og = Image.composite(shade, og, grad.resize((W, H)))
d = ImageDraw.Draw(og)


def font(px, wght):
    f = ImageFont.truetype(FONT, px)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f


# знак «П.» (как <symbol id="mark">: viewBox 76×72)
k = 0.62
def P(xx, yy): return (64 + xx * k, 64 + yy * k)
d.rounded_rectangle([P(0, 24), P(48, 72)], radius=0, fill=None)
mark = Image.new('L', (int(76 * k * 4), int(72 * k * 4)), 0); md = ImageDraw.Draw(mark); q = k * 4
md.pieslice([0, 0, 48 * q, 48 * q], 180, 360, fill=255); md.rectangle([0, 24 * q, 48 * q, 72 * q], fill=255)
md.pieslice([15 * q, 17 * q, 33 * q, 35 * q], 180, 360, fill=0); md.rectangle([15 * q, 26 * q, 33 * q, 72 * q], fill=0)
mark = mark.resize((int(76 * k), int(72 * k)), Image.LANCZOS)
og.paste((244, 242, 238), (64, 64), mark)
d.ellipse([64 + 58 * k, 64 + 54 * k, 64 + 76 * k, 64 + 72 * k], fill=(245, 85, 60))
d.text((64 + 76 * k + 16, 64 + 4), 'П Л А Т Ф О Р М А', font=font(22, 300), fill=(244, 242, 238))
d.text((64 + 76 * k + 16, 64 + 31), 'Н Е Д В И Ж И М О С Т И', font=font(11, 400), fill=(200, 196, 190))
big = font(76, 400)
yy = 250
for line, red in (('Квартиры,', False), ('за которые', False), ('мы ', 'ручаемся')):
    if red:
        d.text((60, yy), line, font=big, fill=(255, 255, 255)); w = d.textlength(line, font=big)
        d.text((60 + w, yy), red, font=big, fill=(245, 85, 60)); w2 = d.textlength(red, font=big)
        d.ellipse([60 + w + w2 + 6, yy + 62, 60 + w + w2 + 20, yy + 76], fill=(255, 255, 255))
    else:
        d.text((60, yy), line, font=big, fill=(255, 255, 255))
    yy += 82
d.text((64, H - 60), 'Екатеринбург · новостройки, вторичка, дома и ремонт · 0 ₽ комиссии', font=font(20, 500), fill=(230, 226, 220))
og.save(os.path.join(SITE, 'public', 'assets', 'img', 'og-main.jpg'), quality=86, optimize=True, progressive=True)
print('ok')
