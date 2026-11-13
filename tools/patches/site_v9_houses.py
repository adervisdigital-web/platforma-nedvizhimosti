"""Сайт v9 — раздел «Дома» на реальных проектах заказчика (каталог: линейки Северный, Южный, Средний Урал).
Имена архитекторов и название подрядчика из каталога НЕ упоминаем; цитаты переписаны от лица бренда.
Фото и планы — 08_Сайт_пример/photo/houses/ (нарезка: tools/crop_houses.py).
Run из корня репо: py -3 tools/patches/site_v9_houses.py  (исходник — 08_Сайт_пример/v8.html)"""
P = '08_Сайт_пример/'
s = open(P + 'v8.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


def cut(a, b, new, keep_b=True):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + (s[j:] if keep_b else s[j + len(b):])


CSS = r'''
/* v9 — проекты домов */
.hfl{display:flex;gap:6px;flex-wrap:wrap;margin-top:30px}
.hx{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px;margin-top:22px}
.hc{grid-column:span 2;background:#fff;border-radius:26px;overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .25s}
.hc:nth-child(-n+2){grid-column:span 3}.hc:hover{box-shadow:0 20px 44px #00000014}
.hc[hidden]{display:none}
.hc .ph{position:relative;aspect-ratio:16/10;overflow:hidden;border:0;padding:0;background:var(--soft);cursor:pointer;display:block;width:100%}
.hc .ph img{width:100%;height:100%;object-fit:cover;transition:transform .7s}.hc:hover .ph img{transform:scale(1.04)}
.hc .ln,.hdl .ln{display:inline-flex;align-items:center;gap:7px;background:#fff;border-radius:999px;padding:5px 12px;font-size:12px;font-weight:700}
.hc .ph .ln{position:absolute;left:14px;top:14px}.hc .ln i,.hdl .ln i{width:9px;height:9px;border-radius:50%;background:var(--c)}
.hc .b{padding:20px 22px 22px;display:flex;flex-direction:column;gap:8px;flex:1}
.hc h3{margin:0;font:500 clamp(26px,1.9vw,40px)/1 Manrope;letter-spacing:-.03em;display:flex;align-items:baseline;gap:10px}.hc h3 span{font-weight:300;color:var(--mut)}
.hc .mt{font-size:14px;color:var(--mut);font-style:italic}
.hc .sp{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}.hc .sp span{background:var(--soft);border-radius:8px;padding:5px 10px;font-size:13px;font-weight:600}
.hc .ac{display:flex;gap:8px;margin-top:auto;padding-top:12px}.hc .ac .btn{min-height:44px;font-size:14px;padding:0 18px}
.hc .pr{font-size:13px;color:var(--mut)}.hc .pr b{color:var(--ink);font-size:16px}
.dlg.wide{width:min(1320px,calc(100vw - 32px))}
.hdl{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,.9fr);gap:28px}
.hmain{border-radius:20px;overflow:hidden;aspect-ratio:16/10;background:var(--soft)}.hmain img{width:100%;height:100%;object-fit:cover}
.hth{display:flex;gap:8px;margin-top:10px;overflow-x:auto;padding-bottom:4px}
.hth button{flex:none;width:96px;aspect-ratio:4/3;border-radius:12px;overflow:hidden;border:2px solid transparent;padding:0;background:none;opacity:.7}
.hth button[aria-pressed=true]{border-color:var(--ink);opacity:1}.hth img{width:100%;height:100%;object-fit:cover}
.hdl .mt2{font:400 15px Manrope;color:var(--mut);margin:10px 0 0;font-style:italic}
.feats{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:2px}.feats li{display:flex;gap:10px;align-items:center;font-size:15px;padding:7px 0;border-top:1px solid #0000000d}.feats svg{width:16px;height:16px;color:var(--red-ui);flex:none}
.hnote{font-size:13px;color:var(--mut);margin:12px 0 0}
.hidea{font:400 clamp(20px,1.6vw,28px)/1.35 Manrope;letter-spacing:-.015em;margin:34px 0 0;max-width:1000px}
.htext{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:20px;color:#4A4741;font-size:15px}.htext p{margin:0}
.hpl{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:34px 0 12px}.hpl h4{margin:0;font:500 24px Manrope;letter-spacing:-.02em}
.plan{display:block;background:#EBEBEB;border-radius:20px;overflow:hidden}.plan img{width:100%;height:auto}
@media(max-width:1200px){.hx{grid-template-columns:repeat(2,minmax(0,1fr))}.hc,.hc:nth-child(-n+2){grid-column:span 1}.hc:first-child{grid-column:span 2}}
@media(max-width:800px){.hx{grid-template-columns:minmax(0,1fr)}.hc:first-child{grid-column:span 1}.hdl,.htext{grid-template-columns:minmax(0,1fr)}.hth button{width:72px}}
'''
rep('@media(prefers-reduced-motion:reduce)', CSS + '@media(prefers-reduced-motion:reduce)')

rep('data-k="our">Наш ремонт и дома</button>', 'data-k="our">Ремонт и дома</button>')
# --- раздел «Дома»: заголовок, фильтр линеек, карточки
cut('<section class="sec" id="houses" style="padding-top:0"><div class="w">', '  <div class="calc inst">', '''<section class="sec" id="houses" style="padding-top:0"><div class="w">
  <div class="lhead"><div><div class="br">[ <b>05</b> Дома ]</div><h2 class="t">Свой дом — в рассрочку до&nbsp;5&nbsp;лет<i class="o"></i></h2></div>
    <p style="max-width:480px;color:#4A4741;margin:0">Пять проектов в трёх линейках — Северный, Южный и Средний Урал. Планировку и фасад настроим под вашу семью; строим из газоблока, кирпича, керамоблока или дерева.</p></div>
  <div class="hfl seg2" id="hfl" role="group" aria-label="Линейка"><button aria-pressed="true" data-l="">Все проекты</button><button aria-pressed="false" data-l="Северный Урал">Северный Урал</button><button aria-pressed="false" data-l="Южный Урал">Южный Урал</button><button aria-pressed="false" data-l="Средний Урал">Средний Урал</button><button aria-pressed="false" data-fl="1">Одноэтажные</button><button aria-pressed="false" data-fl="2">Двухэтажные</button></div>
  <div class="hx" id="hx"></div>
''')
rep('<div class="rng"><label for="ha">Площадь дома <b id="hav"></b></label><input type="range" id="ha" min="60" max="300" step="5" value="160"></div>',
    '<div><div style="font-size:14px;color:var(--mut);margin-bottom:10px">Проект</div><div class="seg2" id="hproj"></div></div>\n'
    '      <div class="rng"><label for="ha">Площадь дома <b id="hav"></b></label><input type="range" id="ha" min="100" max="400" step="5" value="235"></div>')
rep('<div class="note" id="hname">Проект «Шарташ» · тёплый контур</div>', '<div class="note" id="hname"></div>')

# --- упоминания старых проектов
rep('<a class="cat" role="listitem" href="#houses" style="background-image:url(photo/house.jpg)">', '<a class="cat" role="listitem" href="#houses" style="background-image:url(photo/houses/y140_1.jpg)">')
rep('<div class="pc"><div class="ph"><img src="photo/house.jpg" alt="Двухэтажный дом с гаражом" loading="lazy"><span>Строим</span></div><div class="b"><h3>Дома<i class="o"></i></h3><p>Готовые проекты из газоблока, кирпича, керамоблока и дерева. Первый взнос 30 %, остальное — по этапам или в рассрочку до 5 лет.</p><div class="br2">[ газоблок ] [ кирпич ] [ керамоблок ] [ дерево ] [ гарантия 5 лет ]</div>',
    '<div class="pc"><div class="ph"><img src="photo/houses/n235_1.jpg" alt="Дом «Северный Урал 235» среди сосен" loading="lazy"><span>Строим</span></div><div class="b"><h3>Дома<i class="o"></i></h3><p>Пять проектов в линейках Северный, Южный и Средний Урал — от 140 до 350 м². Первый взнос 30 %, остальное — по этапам или в рассрочку до 5 лет.</p><div class="br2">[ газоблок ] [ кирпич ] [ керамоблок ] [ дерево ] [ гарантия 5 лет ]</div>')
rep('<b>Дом «Шарташ»</b><small>газоблок · Берёзовский</small>', '<b>Южный Урал 140</b><small>газоблок · Берёзовский</small>')
rep('<article class="rc"><div class="ph"><img src="photo/house.jpg" alt="" loading="lazy"><span>Дом</span></div><div class="b"><q>Строим «Шарташ» в рассрочку:',
    '<article class="rc"><div class="ph"><img src="photo/houses/y140_1.jpg" alt="" loading="lazy"><span>Дом</span></div><div class="b"><q>Строим «Южный Урал 140» в рассрочку:')
rep("'Строим по готовым проектам: газоблок, кирпич, керамоблок, дерево. Тёплый контур",
    "'Строим по пяти проектам в линейках Северный, Южный и Средний Урал — от 140 до 350 м²; материал на выбор: газоблок, кирпич, керамоблок, дерево. Тёплый контур")

# --- данные и логика
cut("let hName = 'Шарташ';", "function hcalc()", r'''const HOUSES = [
  {id: 'n235', line: 'Северный Урал', n: 235, motto: 'Единение с природой', c: '#5F7380', fl: 2, rooms: '4 + кабинет', ceil: '3,3 м',
    feats: ['Двухэтажная гостиная — 8,5 м', 'Панорамные окна', 'Навес для двух автомобилей', 'Терраса с навесом для гостиной'],
    idea: 'Дом-резиденция для живописного участка у леса или реки. Силуэт — как у заснеженных гор Северного Урала, отделка — натуральные фактуры в строгой палитре.',
    text: ['Компактный двухэтажный объём занимает меньше места на участке и вмещает все нужные помещения.', 'Детские спальни — на втором этаже, родительская спальня и кабинет — на первом.', 'Двухэтажная гостиная раскрывается во двор панорамными окнами и выходит на террасу. Вход в дом — из-под навеса для машин.'],
    ph: ['n235_1', 'n235_2', 'n235_3', 'n235_i1'], plans: [['1 этаж · 154,73 м²', 'n235_p1'], ['2 этаж · 69,12 м²', 'n235_p2']]},
  {id: 'y195', line: 'Южный Урал', n: 195, motto: 'Красота в моменте', c: '#6E8A62', fl: 1, rooms: '3', ceil: '3,3 м',
    feats: ['Высокие гостиная и спальня — 7 м', 'Светлый коридор с окнами', 'Навес для двух автомобилей', 'Терраса с навесом для гостиной'],
    idea: 'Уральская эко-стилистика: уютные скандинавские планировки и смелые приёмы уральского конструктивизма. Два поднятых односкатных объёма напоминают горы.',
    text: ['Дом из двух блоков — приватного и гостевого — вокруг внутреннего двора с террасой.', 'Металл и натуральное дерево в отделке: природа и современный город в одном фасаде.', 'Панорамные окна наполняют высокие гостиную и спальню дневным светом и зрительно увеличивают комнаты.'],
    ph: ['y195_1', 'y195_2', 'y195_3', 'y195_i3', 'y195_i1', 'y195_i2'], plans: [['1 этаж · 196,56 м²', 'y195_p1']]},
  {id: 'y140', line: 'Южный Урал', n: 140, motto: 'Красота в моменте', c: '#6E8A62', fl: 1, rooms: '3', ceil: '3,3 м',
    feats: ['Высокие гостиная и спальня', 'Двусторонняя гостиная', 'Панорамные окна', 'Мастер-спальня с гардеробом и санузлом'],
    idea: 'Самый компактный дом линейки: те же высокие потолки и панорамные окна — на 140 м².',
    text: ['Приватный и общественный блоки разделены; кухня-гостиная с окнами на три стороны всегда полна солнца.', 'У родителей — спальня с гардеробом и санузлом, у детей — свои спальни, санузел и общий гардероб у прихожей.', 'Выход на террасу во двор — через котельную, которая служит и хозяйственной комнатой для двора.'],
    ph: ['y140_1', 'y140_3', 'y140_i3', 'y140_i1', 'y140_i2', 'y140_2'], plans: [['1 этаж · 148,13 м²', 'y140_p1']]},
  {id: 's250', line: 'Средний Урал', n: 250, motto: 'Спокойствие и уверенность', c: '#A85A3C', fl: 1, rooms: '3 + кабинет', ceil: '3,3 м',
    feats: ['Высокая гостиная — 5,3 м', 'Светлый коридор с окнами', 'Терраса с навесом для гостиной', 'Навес для двух автомобилей'],
    idea: 'Стильная простота и спокойствие. Объём вдохновлён каменными палатками — скалами Урала, фасад — уральским камнерезным ремеслом.',
    text: ['Дом собран вокруг внутреннего двора с террасой — летом здесь встречается вся семья. Во дворе можно поставить баню или гостевой дом.', 'Гостиная с высоким потолком освещена с трёх сторон; окна спален выходят от двора — у каждого своя тишина.', 'У прихожей — рабочий кабинет: для встреч и работы из дома.'],
    ph: ['s250_1', 's250_3', 's250_2', 's250_i3', 's250_i1', 's250_i2'], plans: [['1 этаж · 251,45 м²', 's250_p1']]},
  {id: 's350', line: 'Средний Урал', n: 350, motto: 'Спокойствие и уверенность', c: '#A85A3C', fl: 2, rooms: '4 + кабинет', ceil: '3,3 м',
    feats: ['Высокая гостиная — 4 м', 'Гараж на два автомобиля', 'Терраса с навесом для гостиной', 'Мастер-блок с кабинетом'],
    idea: 'Старший брат Среднего Урала 250: орнаменты и яркие вставки на фасаде, первый этаж — для гостей, второй — для семьи.',
    text: ['На втором этаже — родительский мастер-блок с балконом и кабинетом и детские спальни; у каждого родителя свой гардероб.', 'Кухня-гостиная освещена с трёх сторон. Из гаража — вход прямо в прихожую.', 'На первом этаже — гостевая спальня: гостям удобно, семье спокойно.'],
    ph: ['s350_1', 's350_3', 's350_2', 's350_i1', 's350_i2', 's350_i3'], plans: [['1 этаж · 228,8 м²', 's350_p1'], ['2 этаж · 162,2 м²', 's350_p2']]},
];
let hSel = HOUSES[0], hName = 'Северный Урал 235';
const hFrom = h => h.n * 100000, hMonth = (h, y = 5) => Math.round(hFrom(h) * .7 / (y * 12));
const flTxt = n => n === 1 ? '1 этаж' : n + ' этажа';
$('#hx').innerHTML = HOUSES.map(h => `<article class="hc" data-h="${h.id}">
  <button class="ph" type="button" data-open="${h.id}" aria-label="Подробнее: ${h.line} ${h.n}"><img src="photo/houses/${h.ph[0]}.jpg" alt="Дом «${h.line} ${h.n}»" loading="lazy"><span class="ln" style="--c:${h.c}"><i></i>${h.line}</span></button>
  <div class="b"><h3>${h.line}<span>${h.n}</span></h3><div class="mt">«${h.motto}»</div>
    <div class="sp"><span>${h.n} м²</span><span>${flTxt(h.fl)}</span><span>${h.rooms.replace(" + кабинет", "")} комн.${h.rooms.includes("кабинет") ? " + кабинет" : ""}</span><span>потолки ${h.ceil}</span></div>
    <div class="pr">Тёплый контур — от <b>${fmtM(hFrom(h))}</b> · в рассрочку от ${hMonth(h).toLocaleString('ru-RU')} ₽/мес</div>
    <div class="ac"><button class="btn dark" type="button" data-open="${h.id}">Планировки и фото</button><button class="btn ghost" type="button" data-calc="${h.id}">Рассчитать</button></div></div>
</article>`).join('');
$('#hproj').innerHTML = HOUSES.map(h => `<button type="button" aria-pressed="${h === hSel}" data-p="${h.id}">${h.line.split(' ')[0]} ${h.n}</button>`).join('');
const byId = id => HOUSES.find(h => h.id === id);
function pickHouse(h, scroll) {
  hSel = h; hName = `${h.line} ${h.n}`; $('#ha').value = h.n;
  $$('#hproj button').forEach(b => b.setAttribute('aria-pressed', b.dataset.p === h.id)); hcalc(); fillAll();
  if (scroll) $('#hproj').closest('.calc').scrollIntoView({behavior: 'smooth', block: 'center'});
}
$$('#hproj button').forEach(b => b.addEventListener('click', () => pickHouse(byId(b.dataset.p))));
$$('[data-calc]').forEach(b => b.addEventListener('click', () => pickHouse(byId(b.dataset.calc), true)));
$$('[data-open]').forEach(b => b.addEventListener('click', () => houseView(byId(b.dataset.open))));
$$('#hfl button').forEach(b => b.addEventListener('click', () => {
  $$('#hfl button').forEach(x => x.setAttribute('aria-pressed', x === b));
  HOUSES.forEach(h => { $(`.hc[data-h="${h.id}"]`).hidden = !(b.dataset.l === undefined ? h.fl === +b.dataset.fl : !b.dataset.l || h.line === b.dataset.l); });
}));
function houseView(h) {
  dlg.classList.add('wide');
  openDlg(`${h.line} ${h.n}`, `<div class="hdl"><div><div class="hmain"><img id="hvMain" src="photo/houses/${h.ph[0]}.jpg" alt="${h.line} ${h.n}"></div>
      <div class="hth">${h.ph.map((p, i) => `<button type="button" data-p="${p}" aria-pressed="${i === 0}" aria-label="Фото ${i + 1}"><img src="photo/houses/${p}.jpg" alt=""></button>`).join('')}</div></div>
    <div><span class="ln" style="--c:${h.c}"><i></i>Линейка «${h.line}»</span><p class="mt2">«${h.motto}»</p>
      <dl class="qvp"><div><dt>Площадь</dt><dd>${h.n} м²</dd></div><div><dt>Этажность</dt><dd>${flTxt(h.fl)}</dd></div><div><dt>Жилых комнат</dt><dd>${h.rooms}</dd></div><div><dt>Потолки</dt><dd>${h.ceil}</dd></div></dl>
      <ul class="feats">${h.feats.map(f => `<li><svg><use href="#check"/></svg>${f}</li>`).join('')}</ul>
      <div class="qvm" style="margin-top:16px"><div><small>Тёплый контур от ${fmtM(hFrom(h))} · взнос 30 %</small><b>от ${hMonth(h).toLocaleString('ru-RU')} ₽/мес</b><small>внутренняя рассрочка на 5 лет</small></div><button type="button" id="hvCalc">Рассчитать</button></div>
      <div class="qva"><a class="btn red" href="tel:+79655002918">Позвонить</a><a class="btn white" href="#lead" id="hvLead">Обсудить проект</a></div>
      <p class="hnote">Планировку и фасад настроим под вашу семью. Материал стен — на выбор.</p></div></div>
    <p class="hidea">${h.idea}</p><div class="htext">${h.text.map(t => `<p>${t}</p>`).join('')}</div>
    <div class="hpl"><h4>Планировка</h4>${h.plans.length > 1 ? `<div class="seg2" id="plTabs">${h.plans.map((p, i) => `<button type="button" aria-pressed="${i === 0}" data-i="${i}">${p[0]}</button>`).join('')}</div>` : `<span style="color:var(--mut)">${h.plans[0][0]}</span>`}</div>
    <a class="plan" id="plLink" href="photo/houses/${h.plans[0][1]}.jpg" target="_blank" rel="noopener" title="Открыть в полном размере"><img id="plImg" src="photo/houses/${h.plans[0][1]}.jpg" alt="Планировка: ${h.plans[0][0]}"></a>`);
  $$('#dlgB .hth button').forEach(b => b.addEventListener('click', () => { $('#hvMain').src = `photo/houses/${b.dataset.p}.jpg`; $$('#dlgB .hth button').forEach(x => x.setAttribute('aria-pressed', x === b)); }));
  $$('#plTabs button').forEach(b => b.addEventListener('click', () => { const p = h.plans[b.dataset.i]; $('#plImg').src = $('#plLink').href = `photo/houses/${p[1]}.jpg`; $('#plImg').alt = 'Планировка: ' + p[0]; $$('#plTabs button').forEach(x => x.setAttribute('aria-pressed', x === b)); }));
  $('#hvCalc').addEventListener('click', () => { dlg.close(); pickHouse(h, true); });
  $('#hvLead').addEventListener('click', () => dlg.close());
}
dlg.addEventListener('close', () => dlg.classList.remove('wide'));
''')
cut("$$('#hgrid .hp').forEach(b => b.addEventListener('click', () => {", "}));\n", '', keep_b=False)
rep("hcalc();\n\n// ремонт", "pickHouse(hSel);\n\n// ремонт")

open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok', len(s))
