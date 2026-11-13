"""Сайт v4: широкоэкранная (резиновая) версия + улучшения после разбора v3. Run из корня репо: py -3 tools/patches/site_v4_wide.py"""
import shutil

p = '08_Сайт_пример/index.html'
shutil.copy(p, '08_Сайт_пример/v3.html')
s = open(p, encoding='utf8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)


# 1. резиновая сетка и типографика
rep('.w{max-width:1400px;margin:0 auto;padding:0 40px}', '.w{max-width:2240px;margin:0 auto;padding:0 clamp(16px,3.6vw,96px)}')
rep('h2.t{font:400 60px/1.02 Manrope;', 'h2.t{font:400 clamp(36px,3.9vw,104px)/1.02 Manrope;')
rep('.hero h1{font:400 104px/.95 Manrope;', '.hero h1{font:400 clamp(46px,6.6vw,176px)/.95 Manrope;')
rep('.hero .sub{font-size:19px;', '.hero .sub{font-size:clamp(16px,1.15vw,24px);max-width:min(640px,90%)!important;')
rep('gap:24px;min-height:720px}', 'gap:24px;min-height:clamp(720px,calc(100vh - 110px),1180px)}')
rep('z-index:3;width:min(880px,100%);', 'z-index:3;width:min(1180px,66%);')
rep('.mtext{font:400 54px/1.12 Manrope;letter-spacing:-.04em;margin:26px 0 0;max-width:1180px;',
    '.mtext{font:400 clamp(28px,3.5vw,92px)/1.1 Manrope;letter-spacing:-.04em;margin:26px 0 0;max-width:min(1800px,92%);')
rep('.stats b{display:block;font:300 76px/1 Manrope;', '.stats b{display:block;font:300 clamp(56px,5.4vw,140px)/1 Manrope;')
rep('align-content:center;min-height:420px}', 'align-content:center;min-height:clamp(420px,30vw,720px)}')
rep('.cout .pay{font:300 76px/1 Manrope;', '.cout .pay{font:300 clamp(52px,5vw,128px)/1 Manrope;')
rep('.lead h2.t{color:#fff;font-size:66px}', '.lead h2.t{color:#fff;font-size:clamp(38px,4.4vw,116px)}')
rep('grid-template-columns:minmax(0,1fr) 460px;gap:60px;align-items:center}', 'grid-template-columns:minmax(0,1fr) clamp(380px,28vw,600px);gap:60px;align-items:center}')

# 2. красный — только для главного: кнопка телефона в карточке тёмная, раскрытый номер — красный
rep('<button class="btn red tel-btn">Показать телефон</button>', '<button class="btn dark tel-btn">Показать телефон</button>')
rep('''b.outerHTML = '<a class="btn dark" href="tel:+79655002918">''', '''b.outerHTML = '<a class="btn red" href="tel:+79655002918">''')

# 3. переключатель вида «Список / Плитка» и «Показать ещё»
rep('<div class="seg" role="group" aria-label="Сортировка"><button aria-pressed="true">Самые выгодные</button><button aria-pressed="false">Дешевле</button><button aria-pressed="false">Срок сдачи</button></div>',
    '<div style="display:flex;gap:10px;flex-wrap:wrap"><div class="seg" role="group" aria-label="Сортировка"><button aria-pressed="true">Самые выгодные</button><button aria-pressed="false">Дешевле</button><button aria-pressed="false">Срок сдачи</button></div>'
    '<div class="seg view" role="group" aria-label="Вид"><button aria-pressed="false" data-v="list">Список</button><button aria-pressed="false" data-v="grid">Плитка</button></div></div>')
rep('    <div id="cards"></div>', '    <div><div id="cards"></div><div class="more"><button class="btn white">Показать ещё [N] проверенных</button></div></div>')
rep('.map{position:sticky;top:96px;border-radius:26px;overflow:hidden;height:680px;',
    '.more{display:flex;justify-content:center;margin-top:16px}\n'
    '#cards.grid{display:grid;grid-template-columns:repeat(var(--cols,2),minmax(0,1fr));gap:14px}\n'
    '#cards.grid .card{grid-template-columns:minmax(0,1fr);margin:0;gap:12px;align-content:start}\n'
    '#cards.grid .rcol{border-left:0;border-top:1px solid var(--line);padding:12px 4px 4px}\n#cards.grid .mid{padding:2px 4px}\n'
    '.map{position:sticky;top:96px;border-radius:26px;overflow:hidden;height:min(calc(100vh - 120px),900px);')

# 4. широкие экраны
rep('.tabbar{display:none}', '''.tabbar{display:none}
@media(min-width:1700px){body{font-size:16px}.res{grid-template-columns:minmax(0,1fr) minmax(460px,34%)}.hd{height:84px}
 .cat b{font-size:20px}.pt{min-height:300px;padding:32px}.pt h3{font-size:clamp(30px,1.9vw,48px);max-width:520px}.pt p{font-size:16px;max-width:440px}
 .pc h3{font-size:clamp(28px,1.8vw,44px)}.pc p{font-size:16px}.prom b{font-size:clamp(54px,3.6vw,96px)}.prom span{font-size:17px}.clist li{font-size:18px;padding:18px 0}.checks h3{font-size:34px}
 .chipv{width:340px;padding:18px 20px}.chipv ul{font-size:14px}.f{min-height:76px}.f input,.chip{font-size:16px}.go{min-height:76px;font-size:17px}.tabs button{font-size:15px;padding:12px 20px}}
@media(min-width:2200px){#cards.grid{--cols:3}}''')

# 5. больше объявлений (6), чтобы плитка заполнялась 2×3 / 3×2
rep("tags: ['Вторичка', 'С ремонтом'], tag: '', x: 330, y: 540},",
    "tags: ['Вторичка', 'С ремонтом'], tag: '', x: 330, y: 540, sec: 1},\n"
    "  {img: 'family_home', t: '3-комн. квартира, [ПЛОЩАДЬ] м², 6/10 этаж', a: 'ЖК [НАЗВАНИЕ] · Ботанический', line: 'Дом сдан · ремонт от партнёра — смета до начала работ', tags: ['С ремонтом', 'Семейная ипотека'], tag: 'Квартира + ремонт', x: 70, y: 600},\n"
    "  {img: 'kv_building', t: 'Студия, [ПЛОЩАДЬ] м², 12/24 этаж', a: 'ЖК [НАЗВАНИЕ] · Юго-Западный', line: 'Сдача — [КВАРТАЛ] · старт продаж', tags: ['Новостройка', 'Ипотека'], tag: '', x: 60, y: 160},")
rep("${i === 3 ? 'Сделка проверена юристом' : 'Застройщик проверен'}", "${it.sec ? 'Сделка проверена юристом' : 'Застройщик проверен'}")
rep("CHECKS[i === 3 ? 'sec' : 'dev']", "CHECKS[it.sec ? 'sec' : 'dev']")

# логика вида: на широких экранах по умолчанию плитка
rep("$('#leadForm').addEventListener('submit', e => e.currentTarget.classList.add('sent'));",
    """$('#leadForm').addEventListener('submit', e => e.currentTarget.classList.add('sent'));
const vbtns = $$('.view button');
function setView(v) { $('#cards').classList.toggle('grid', v === 'grid'); vbtns.forEach(b => b.setAttribute('aria-pressed', b.dataset.v === v)); }
vbtns.forEach(b => b.addEventListener('click', () => setView(b.dataset.v)));
setView(innerWidth >= 1700 ? 'grid' : 'list');""")

open(p, 'w', encoding='utf8').write(s)
print('ok')
