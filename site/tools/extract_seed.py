"""Стартовые данные из прототипа v40 → site/data/seed/*.json (через headless Chrome, tools/cdp.py).
Run из корня репо: py -3 -X utf8 site/tools/extract_seed.py"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from cdp import Browser

OUT = os.path.join(ROOT, 'site', 'data', 'seed')
os.makedirs(OUT, exist_ok=True)
TR = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
              ['a', 'b', 'v', 'g', 'd', 'e', 'yo', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']))


def slug(s):
    s = ''.join(TR.get(c, c) for c in s.lower())
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


b = Browser()
b.open('file:///' + os.path.join(ROOT, '08_Сайт_пример', 'index.html').replace('\\', '/') + '?shot', wait=3)
raw = json.loads(b.ev('''JSON.stringify({ITEMS, HOUSES, QUICK, PROGS, GEO, ZCHK,
  FAQ: FAQ.map(([r, a]) => [r.source, r.flags, a]),
  REV: [...document.querySelectorAll('#rev .rc')].map(a => ({img: a.querySelector('img')?.getAttribute('src'), tag: a.querySelector('.ph span')?.textContent,
       text: a.querySelector('q')?.textContent, name: a.querySelector('.who b')?.textContent, about: a.querySelector('.who span')?.textContent}))})'''))
b.close()
json.dump(raw, open(os.path.join(OUT, '_proto_raw.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)

complexes, apts = {}, []
for i, it in enumerate(raw['ITEMS'], 1):
    is_zk = it['zk'].startswith('ЖК')
    if is_zk and it['zk'] not in complexes:
        complexes[it['zk']] = dict(name=it['zk'], slug=slug(it['zk']), district=it['d'], developer=None,
                                   checks=raw['ZCHK'], lat=raw['GEO'].get(it['d'], [None, None])[0], lng=raw['GEO'].get(it['d'], [None, None])[1])
    apts.append(dict(
        id=i, rooms=it['r'], area=it['s'], floor=it['fl'], floors=it['fls'],
        complex=it['zk'] if is_zk else None, address=None if is_zk else it['zk'], district=it['d'],
        market='new' if it['t'] == 'new' else 'secondary', price=it['p'], discount_pct=it.get('disc', 0) or 0,
        finish='with' if it['fin'] != 'Без отделки' else 'without', finish_label=it['fin'],
        house_status=it['st'], due=it.get('due', 0) or 0, special=1 if it.get('special') else 0,
        photos=[it['img']], map_x=it.get('x'), map_y=it.get('y'), published=1, source='manual', external_id=None,
        slug=f"{i}-{slug(it['zk'])}"))
houses = []
for k, h in enumerate(raw['HOUSES']):
    d = dict(h); d['slug'] = slug(f"{h['line']} {h['n']}"); d['sort'] = k
    houses.append(d)
reviews = [dict(name=r['name'], text=r['text'], about=r['about'], tag=r['tag'], photo=r['img'], rating=5, is_demo=1, published=1) for r in raw['REV']]
settings = dict(phone='+7 965 500-29-18', phone_tel='+79655002918', hours_from='9:00', hours_to='21:00',
                renovation_prices=[20000, 45000, 80000], warm_contour_from=75000,
                mortgage_programs=[dict(name=n, rate=r) for n, r in raw['PROGS']], district_geo=raw['GEO'],
                legal='ИП Сафоев Ш. Р.', domain='p.forma196.ru', demo_data=1, show_demo_reviews=1)
for name, data in (('apartments', apts), ('complexes', list(complexes.values())), ('houses', houses), ('reviews', reviews),
                   ('settings', settings), ('faq', raw['FAQ']), ('quick', raw['QUICK'])):
    json.dump(data, open(os.path.join(OUT, name + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('квартир', len(apts), 'ЖК', len(complexes), 'домов', len(houses), 'отзывов', len(reviews))
