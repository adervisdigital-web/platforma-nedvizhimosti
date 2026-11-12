"""Build index.html — interactive gallery of the three identity variants.
Run: py -3 tools/build_gallery.py   (from the repo root). Also makes JPG thumbnails in 01_Мудборд/_thumbs/."""
import glob, hashlib, json, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '02_Логотип'))
from marks import mark_L, mark_D, mark_Y, arch_d  # noqa: E402

MB = os.path.join(ROOT, '01_Мудборд')
TH = os.path.join(MB, '_thumbs')
os.makedirs(TH, exist_ok=True)

SHEETS = {'1': 'Логотип', '2': 'Стиль и носители', '3': 'Айдентика', '4': 'Сайт-приложение', '5': 'Бренд в жизни'}
VARS = [
    dict(n='1', key='L', title='Светлый', name='Арка', font='Manrope', fw=800, ls='0.04em', k=1.0, sub='#8A847A',
         bg='#F2EEE7', ink='#1F1D1B', acc='#B4532A', acc_ink='#FFFFFF', dark='#1F1D1B',
         palette=[('Камень', '#F2EEE7'), ('Графит', '#1F1D1B'), ('Терракота', '#B4532A'), ('Песок', '#D9CBB5')],
         idea='«П» с арочным проёмом — буква и вход в каменный дом. Тёплая терракота, много воздуха. Арка — рамка для всех фото.',
         svgs=['1_Светлый_Арка_терракота.svg', '1_Светлый_Арка_графит.svg', '1_Светлый_Арка_белый.svg'], photo='_source/gen/kv_kitchen.jpg'),
    dict(n='2', key='D', title='Тёмный', name='Портал', font='Inter Tight', fw=600, ls='0.02em', k=1.0, sub='#8D929A',
         bg='#0E0F11', ink='#F2F1EE', acc='#FFB547', acc_ink='#14120E', dark='#0E0F11',
         palette=[('Ночь', '#0E0F11'), ('Бетон', '#2A2D32'), ('Сталь', '#A7ACB4'), ('Белый', '#F2F1EE'), ('Свет', '#FFB547')],
         idea='Объёмная «П» — дом-портал, в проёме горит тёплый свет. Технологично и уверенно: тёмный бетон, сталь и один источник света.',
         svgs=['2_Тёмный_Портал_для-тёмного-фона.svg', '2_Тёмный_Портал_для-светлого-фона.svg', '2_Тёмный_Портал_одноцветный.svg'], photo='_source/gen/kv_complex2.jpg'),
    dict(n='3', key='Y', title='Яркий', name='Сборка', font='Unbounded', fw=600, ls='0', k=0.86, sub='#6B6F7D',
         bg='#FFFFFF', ink='#14161F', acc='#2E4BFF', acc_ink='#FFFFFF', dark='#14161F',
         palette=[('Белый', '#FFFFFF'), ('Чернила', '#14161F'), ('Квартиры', '#2E4BFF'), ('Ремонт', '#FF6B2C'), ('Дома', '#18B26B')],
         idea='«П» из трёх частей: квартиры, ремонт, дома. Вместе — платформа. Цвет направления ведёт человека по сайту и приложению.',
         svgs=['3_Яркий_Сборка_цвет.svg', '3_Яркий_Сборка_чёрный.svg', '3_Яркий_Сборка_белый.svg'], photo='_source/gen/house_stone2.jpg'),
    dict(n='4', key='L', shape='masonry', title='Красный', name='Кладка', font='Manrope', fw=800, ls='0.04em', k=1.0, sub='#76706A',
         bg='#F4EFE8', ink='#1E1B19', acc='#C8102E', acc_ink='#FFFFFF', dark='#1E1B19',
         palette=[('Известь', '#F4EFE8'), ('Графит', '#1E1B19'), ('Красный', '#C8102E'), ('Глина', '#E4D3BF')],
         idea='Арка-«П», сложенная из камня: ряды кладки, клинчатая перемычка и замковый камень. Красный акцент — кирпич и энергия. В малых размерах знак упрощается до чистой арки.',
         svgs=[], photo='_source/gen/house_stone2.jpg'),
    dict(n='5', key='L', shape='vault', title='Зелёный', name='Свод', font='Geologica', fw=700, ls='0.03em', k=0.96, sub='#6B7069',
         bg='#F1EEE6', ink='#1D2620', acc='#2F5D46', acc_ink='#FFFFFF', dark='#1D2620',
         palette=[('Песок', '#F1EEE6'), ('Хвоя', '#1D2620'), ('Зелень', '#2F5D46'), ('Лён', '#D8CDB4')],
         idea='Арка-«П» с дверной рамой и порогом внутри: вход в дом, который уже готов. Тёплый песок и глубокая зелень, мягкий шрифт Geologica.',
         svgs=[], photo='_source/gen/kv_living2.jpg'),
]


def anim_mark(key, cls='mk', shape='arch'):
    """Mark SVG with classed parts so CSS can animate it. Colours come from CSS variables."""
    if key == 'L':
        return ('<svg class="%s mL" viewBox="0 0 36 40" role="img" aria-label="Знак">'
                '<path class="p1" d="%s"/></svg>') % (cls, arch_d(shape))
    if key == 'D':
        return ('<svg class="%s mD" viewBox="0 0 36 36" role="img" aria-label="Знак «Портал»">'
                '<polygon class="p2" points="0,8 8,0 36,0 28,8"/><polygon class="p3" points="28,8 36,0 36,28 28,36"/>'
                '<polygon class="p4" points="8,16 16,16 16,28 8,36"/><path class="p1" d="M0 8 H28 V36 H20 V16 H8 V36 H0 Z"/></svg>') % cls
    return ('<svg class="%s mY" viewBox="0 0 40 36" role="img" aria-label="Знак «Сборка»">'
            '<polygon class="p2" points="0,0 40,0 30,10 10,10"/><polygon class="p1" points="0,3 10,13 10,36 0,36"/>'
            '<polygon class="p3" points="40,3 40,36 30,36 30,13"/></svg>') % cls


def grid_overlay(key):
    if key == 'L':
        lines = ''.join(f'<line x1="{x}" y1="-4" x2="{x}" y2="44"/>' for x in (0, 10, 18, 26, 36))
        lines += ''.join(f'<line x1="-4" y1="{y}" x2="40" y2="{y}"/>' for y in (0, 12, 20, 40))
        lines += '<circle cx="18" cy="20" r="8"/>'
        vb = '-4 -4 44 48'
    elif key == 'D':
        lines = ''.join(f'<line x1="{a - 8}" y1="{b + 8}" x2="{a + 10}" y2="{b - 10}"/>' for a, b in ((0, 8), (28, 8), (28, 36), (8, 16)))
        lines += ''.join(f'<line x1="{x}" y1="-4" x2="{x}" y2="40"/>' for x in (0, 8, 20, 28, 36))
        vb = '-4 -4 44 44'
    else:
        lines = '<line x1="-4" y1="-4" x2="14" y2="14"/><line x1="44" y1="-4" x2="26" y2="14"/>'
        lines += ''.join(f'<line x1="{x}" y1="-4" x2="{x}" y2="40"/>' for x in (0, 10, 30, 40))
        vb = '-4 -4 48 44'
    pos = {'L': (-11.11, -10, 122.22, 120), 'D': (-11.11, -11.11, 122.22, 122.22), 'Y': (-10, -11.11, 120, 122.22)}[key]
    st = f'left:{pos[0]}%;top:{pos[1]}%;width:{pos[2]}%;height:{pos[3]}%'
    return f'<svg class="grid" style="{st}" viewBox="{vb}" aria-hidden="true">{lines}</svg>'


def thumbs():
    data = {}
    for v in VARS:
        lst = []
        for s, label in SHEETS.items():
            f = glob.glob(os.path.join(MB, f'{v["n"]}-{s}_*.png'))
            if not f:
                continue
            f = f[0]
            base = os.path.basename(f)
            th = os.path.join(TH, base.replace('.png', '.jpg'))
            if not os.path.exists(th) or os.path.getmtime(th) < os.path.getmtime(f):
                im = Image.open(f).convert('RGB')
                im.thumbnail((900, 1100))
                im.save(th, quality=82)
            ver = lambda path: hashlib.md5(open(path, 'rb').read()).hexdigest()[:8]
            lst.append(dict(s=s, label=label, full=f'01_Мудборд/{base}?v={ver(f)}', th=f'01_Мудборд/_thumbs/{os.path.basename(th)}?v={ver(th)}'))
        data[v['n']] = lst
    return data




def build():
    data = thumbs()
    vjs = [dict(n=v['n'], key=v['key'], title=v['title'], name=v['name'], font=v['font'], fw=v['fw'], ls=v['ls'], k=v['k'], sub=v['sub'],
                bg=v['bg'], ink=v['ink'], acc=v['acc'], acc_ink=v['acc_ink'], dark=v['dark'], palette=v['palette'], idea=v['idea'],
                photo=v['photo'], sheets=data[v['n']], mark=anim_mark(v['key'], shape=v.get('shape', 'arch')), grid=grid_overlay(v['key'])) for v in VARS]
    html = open(os.path.join(ROOT, 'tools', 'gallery_template.html'), encoding='utf8').read()
    html = html.replace('/*DATA*/', 'const VARS = ' + json.dumps(vjs, ensure_ascii=False) + ';\nconst SHEETS = ' + json.dumps(SHEETS, ensure_ascii=False) + ';')
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf8').write(html)
    print('index.html ok,', sum(len(x) for x in data.values()), 'sheets')


if __name__ == '__main__':
    build()
