"""Порядок направлений: «Квартира. Дом. Ремонт.» (продаём квартиры и дома, ремонт — у партнёров). Run из корня репо."""
import re


def patch(p, pairs, regex=()):
    s = open(p, encoding='utf8').read()
    for a, b in pairs:
        assert s.count(a) >= 1, (p, a[:80])
        s = s.replace(a, b)
    for a, b in regex:
        s, n = re.subn(a, b, s)
        assert n >= 1, (p, a)
    open(p, 'w', encoding='utf8').write(s)


patch('tools/p_present.py', [
    ('Квартира<i class="o n"></i> Ремонт<i class="o n"></i> Дом<i class="o n"></i>', 'Квартира<i class="o n"></i> Дом<i class="o n"></i> Ремонт<i class="o n"></i>'),
    ('Квартиры<i class="o"></i> Ремонт<i class="o"></i> Дома<i class="o"></i>', 'Квартиры<i class="o"></i> Дома<i class="o"></i> Ремонт<i class="o"></i>'),
    ("(('Квартиры', GRAY,", "(('Квартиры', GRAY,"),
    ('Квартиры, Ремонт, Дома — три направления в одном поиске.', 'Новостройки, вторичка, дома и квартиры с ремонтом — в одном поиске.'),
], regex=[
    # блок «О бренде»: Квартиры → Дома → Ремонт
    (r'(    <div><b>Ремонт\{D\}</b><span>[^\n]*\n)(    <div><b>Дома\{D\}</b><span>[^\n]*\n)', r'\2\1'),
    # кружки-разделы в профиле соцсети
    (r"\('Ремонт', GRAY, ([^\n]*?)\),\n(\s*)\('Дома', GRAY, ([^\n]*?)\),", r"('Дома', GRAY, \3),\n\2('Ремонт', GRAY, \1),"),
])
patch('tools/p_dot.py', [('Квартира{dot}<br>Ремонт{dot}<br>Дом', 'Квартира{dot}<br>Дом{dot}<br>Ремонт')])
patch('tools/mockups/p_mockups.py', [('Квартира{dot}<br>Ремонт{dot}<br>Дом', 'Квартира{dot}<br>Дом{dot}<br>Ремонт')])
patch('tools/p_hub.py', [('Квартира<i class="o"></i> Ремонт<i class="o"></i> Дом<i class="o"></i>', 'Квартира<i class="o"></i> Дом<i class="o"></i> Ремонт<i class="o"></i>')])
patch('08_Сайт_пример/index.html', [
    ('<button role="tab" aria-selected="false">С ремонтом</button><button role="tab" aria-selected="false">Дома</button>',
     '<button role="tab" aria-selected="false">Дома</button><button role="tab" aria-selected="false">С ремонтом</button>'),
    ('<button type="button" aria-pressed="false">С ремонтом</button><button type="button" aria-pressed="false">Дом</button>',
     '<button type="button" aria-pressed="false">Дом</button><button type="button" aria-pressed="false">С ремонтом</button>'),
], regex=[
    # партнёры: Новостройки → Дома → Ремонт
    (r'(    <div class="pc"><div class="ph"><img src="photo/crew\.jpg"[^\n]*\n)(    <div class="pc"><div class="ph"><img src="photo/house\.jpg"[^\n]*\n)', r'\2\1'),
])
print('ok')
