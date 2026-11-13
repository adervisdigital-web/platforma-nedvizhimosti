"""Сайт v7 — «всё работает»: демо-объекты с ценами (заказчик разрешил придуманные данные до запуска), рабочий поиск
и счётчик, сортировка, фильтры из подборок, сравнение и избранное (окно + localStorage), «Показать ещё», ипотека из карточки,
ремонт к квартире без отделки, маска и проверка телефона, подсветка раздела в меню, стрелки отзывов, meta/OG/favicon/JSON-LD.
Run из корня репо: py -3 tools/patches/site_v7_working.py  (исходник — 08_Сайт_пример/v6.html)"""
P = '08_Сайт_пример/'
s = open(P + 'v6.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


def cut(a, b, new, keep_b=True):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + (s[j:] if keep_b else s[j + len(b):])


FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-6 -6 88 84'%3E%3Crect x='-6' y='-6' width='88' height='84' rx='18' fill='%230E0E0F'/%3E"
       "%3Cpath d='M0 72 V24 A24 24 0 0 1 48 24 V72 H33 V26 A9 9 0 0 0 15 26 V72 Z' fill='%23F4F2EE'/%3E%3Ccircle cx='67' cy='63' r='9' fill='%23F5553C'/%3E%3C/svg%3E")
URL = 'https://adervisdigital-web.github.io/platforma-nedvizhimosti/08_%D0%A1%D0%B0%D0%B9%D1%82_%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80/'
DESC = 'Квартиры от проверенных застройщиков Екатеринбурга без комиссии, свой ремонт с гарантией 5 лет и дома в рассрочку до 5 лет.'
rep('<link href="https://fonts.googleapis.com', f'''<meta name="description" content="{DESC}">
<meta name="theme-color" content="#F4F2EE">
<meta property="og:type" content="website"><meta property="og:title" content="Платформа недвижимости — квартиры, дома и ремонт">
<meta property="og:description" content="{DESC}"><meta property="og:image" content="{URL}photo/ekb_dusk.jpg">
<link rel="icon" href="{FAV}">
<link rel="preload" as="image" href="photo/ekb_dusk.jpg">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"RealEstateAgent","name":"Платформа недвижимости","telephone":"+7 965 500-29-18","areaServed":"Екатеринбург","url":"https://p.forma196.ru"}}</script>
<link href="https://fonts.googleapis.com''')

CSS = r'''
/* v7 */
.pt>div,.pt .gl{z-index:1}.pt p{max-width:min(330px,62%)}.pt .dotgrid{width:150px;height:92px}
.go{gap:6px}
.flt{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:22px;font-size:14px}.flt[hidden]{display:none}
.flt span{background:#fff;border-radius:999px;padding:8px 14px;font-weight:700}.flt button{border:0;background:transparent;font-weight:700;color:var(--red);padding:8px 4px}
.cnt2{font:500 15px Manrope;color:var(--mut);letter-spacing:0;margin-left:10px;white-space:nowrap}
button.mort{border:0;text-align:left;width:100%;transition:background .2s}button.mort:hover{background:#FEECE8}
.mort small{display:block;color:var(--mut);font-size:11px}
.rx{align-self:flex-start;font-size:13px;font-weight:700;color:#B8321D;border-bottom:1px dashed #B8321D80}
.empty{background:#fff;border-radius:26px;padding:40px;display:flex;flex-direction:column;align-items:flex-start;gap:10px;color:var(--mut)}.empty b{font:500 28px Manrope;color:var(--ink);letter-spacing:-.02em}
.more[hidden]{display:none}
.dlg{border:0;border-radius:26px;padding:0;width:min(1100px,calc(100vw - 32px));max-height:calc(100vh - 60px);background:var(--milk);color:var(--ink);box-shadow:0 40px 100px #0000004d}
.dlg::backdrop{background:#0e0e0f99;backdrop-filter:blur(4px)}
.dh{display:flex;align-items:center;gap:12px;padding:20px 24px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--milk);z-index:1}
.dh h3{margin:0;font:500 26px Manrope;letter-spacing:-.02em}.dh button{margin-left:auto;width:44px;height:44px;border-radius:50%;border:1px solid var(--line);background:#fff;font-size:20px}
.db{padding:20px 24px 26px;overflow:auto}
.ctab{border-collapse:separate;border-spacing:10px 0;min-width:100%;table-layout:fixed}.ctab th{position:sticky;left:0;background:var(--milk);z-index:1;width:130px}
.ctab th,.ctab td{text-align:left;vertical-align:top;padding:9px 0;font-size:14px;border-bottom:1px solid var(--line);min-width:200px}
.ctab th{color:var(--mut);font-weight:500;min-width:120px}.ctab td b{font-size:17px}
.ctab img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:14px}
.ctab .best{color:#B8321D;font-weight:700}
.ctab .rm{border:0;background:transparent;color:var(--mut);font-size:12px;font-weight:700;padding:4px 0}
.flist{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
.fi{background:#fff;border-radius:18px;overflow:hidden}.fi img{width:100%;aspect-ratio:4/3;object-fit:cover}.fi div{padding:12px 14px;font-size:13px}.fi b{display:block;font-size:17px}
.toast{position:fixed;left:50%;bottom:28px;transform:translate(-50%,20px);z-index:60;background:var(--ink);color:#fff;border-radius:999px;padding:12px 20px;font-size:14px;font-weight:600;opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;max-width:calc(100vw - 32px);text-align:center}
.toast.on{opacity:1;transform:translate(-50%,0)}
.f .err{display:none;color:#B8321D;font-size:12px;font-weight:600}.f.bad{border-color:#E0442C;background:#FFF5F3}.f.bad .err{display:block}
.arr{display:flex;gap:8px}.arr button{width:50px;height:50px;border-radius:50%;border:1px solid var(--line);background:#fff;font-size:18px}.arr button:hover{background:var(--ink);color:#fff}
.rvh{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
@media(max-width:800px){.toast{bottom:84px}.dlg{width:100vw;max-width:100vw;max-height:100svh;height:100svh;border-radius:0;margin:0}.arr{display:none}.cnt2{display:block;margin:8px 0 0}}
'''
rep('@media(prefers-reduced-motion:reduce)', CSS + '@media(prefers-reduced-motion:reduce)')

# --- шапка, первый экран
rep('<button class="hicon hide-m" aria-label="Сравнение">', '<button class="hicon hide-m" id="cmpBtn" aria-label="Сравнение">')
rep('<button class="hicon" aria-label="Избранное">', '<button class="hicon" id="favBtn" aria-label="Избранное">')
rep('<h3><i></i>ЖК [НАЗВАНИЕ] — проверен</h3>', '<h3><i></i>ЖК Липовый сквер — проверен</h3>')
rep('<form class="sf" onsubmit="return false" aria-label="Поиск">', '<form class="sf" id="sf" aria-label="Поиск">')
rep('<div class="f"><label for="pr">Цена, ₽</label><input id="pr" placeholder="от — до" inputmode="numeric"></div>',
    '<div class="f"><label for="pr">Цена до, млн ₽</label><input id="pr" placeholder="например, 8" inputmode="decimal"></div>')
rep('<a class="btn red go" href="#list">Показать [N]</a>', '<button class="btn red go" type="submit">Показать <span id="goN"></span></button>')

# --- подборки
rep('<a class="cat red" role="listitem" href="#list">', '<a class="cat red" role="listitem" href="#list" data-f="best">')
rep('<b>Сданные дома</b><span>[N] квартир</span>', '<b>Сданные дома</b><span data-c="done"></span>')
rep('href="#list" style="background-image:url(photo/kv_complex2.jpg)"', 'href="#list" data-f="done" style="background-image:url(photo/kv_complex2.jpg)"')
rep('<b>С отделкой</b><span>[N] квартир</span>', '<b>С отделкой</b><span data-c="fin"></span>')
rep('href="#list" style="background-image:url(photo/kv_living2.jpg)"', 'href="#list" data-f="fin" style="background-image:url(photo/kv_living2.jpg)"')
rep('<b>Семейная ипотека</b><span>[N] квартир</span>', '<b>Семейная ипотека</b><span data-c="fam"></span>')
rep('href="#list" style="background-image:url(photo/kv_kids.jpg)"', 'href="#list" data-f="fam" style="background-image:url(photo/kv_kids.jpg)"')
rep('<b>Вторичка, проверенная юристом</b><span>[N] квартир</span>', '<b>Вторичка, проверенная юристом</b><span data-c="sec"></span>')
rep('href="#list" style="background-image:url(photo/kv_bedroom.jpg)"', 'href="#list" data-f="sec" style="background-image:url(photo/kv_bedroom.jpg)"')

# --- объявления
rep('<h2 class="t">[N] квартир прошли проверку<i class="o"></i></h2>', '<h2 class="t">Отобрали на этой <span class="nw">неделе<i class="o"></i></span><span class="cnt2" id="cnt"></span></h2>')
rep('<div class="seg" role="group" aria-label="Сортировка"><button aria-pressed="true">Самые выгодные</button><button aria-pressed="false">Дешевле</button><button aria-pressed="false">Срок сдачи</button></div>',
    '<div class="seg sort" role="group" aria-label="Сортировка"><button aria-pressed="true" data-s="best">Самые выгодные</button><button aria-pressed="false" data-s="cheap">Дешевле</button><button aria-pressed="false" data-s="due">Срок сдачи</button></div>')
rep('</div>\n  <div class="res">', '</div>\n  <div class="flt" id="flt" hidden><span id="fltT"></span><button type="button" id="fltX">Сбросить ×</button></div>\n  <div class="res">')
rep('<div class="more"><button class="btn white">Показать ещё [N] проверенных</button></div>', '<div class="more" id="more"><button class="btn white" id="moreBtn"></button></div>')

# --- дома, кабинет, отзывы
for n, a in (('Шарташ', '2 этажа · гараж'), ('Таватуй', '2 этажа · балкон'), ('Балтым', '1 этаж · плоская кровля'), ('Аять', '1 этаж · терраса')):
    area = {'Шарташ': 160, 'Таватуй': 190, 'Балтым': 130, 'Аять': 100}[n]
    rep(f'{a} · [ПЛОЩАДЬ] м²', f'{a} · {area} м²')
rep('газоблок · [АДРЕС УЧАСТКА]', 'газоблок · Берёзовский')
rep('<b>[СУММА] ₽ · [ДАТА]</b>', '<b>311 100 ₽ · 15 декабря</b>')
rep('<span>2-комн. квартира, ЖК [НАЗВАНИЕ]</span>', '<span>2-комн. квартира, ЖК Кварц</span>')
rep('<span class="demo">Демо-отзывы для макета — заменим настоящими</span></div>',
    '<div class="rvh"><span class="demo">Демо-отзывы для макета — заменим настоящими</span><div class="arr"><button type="button" data-d="-1" aria-label="Предыдущие отзывы">←</button><button type="button" data-d="1" aria-label="Следующие отзывы">→</button></div></div></div>')

# --- заявка, подвал
rep('<div class="f"><label for="lp">Телефон</label><input id="lp" type="tel" autocomplete="tel" placeholder="+7"></div>',
    '<div class="f"><label for="lp">Телефон</label><input id="lp" type="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" aria-describedby="lpErr"><span class="err" id="lpErr">Введите номер полностью — 10 цифр после +7</span></div>')
rep('<form class="form" id="leadForm" onsubmit="return false">', '<form class="form" id="leadForm" novalidate>')
rep('Пример сайта. Цены объектов, площади и названия ЖК — заглушки, отзывы — демо.', 'Пример сайта. Объекты, цены и названия ЖК — демо-данные, отзывы — демо.')
rep('</nav>\n\n<button class="chatfab"', '</nav>\n\n<dialog class="dlg" id="dlg" aria-labelledby="dlgT"><div class="dh"><h3 id="dlgT"></h3><button type="button" id="dlgX" aria-label="Закрыть">×</button></div><div class="db" id="dlgB"></div></dialog>\n<div class="toast" id="toast" role="status" aria-live="polite"></div>\n\n<button class="chatfab"')

# --- данные и логика объявлений
DATA = r'''const fmtM = n => (n / 1e6).toLocaleString('ru-RU', {maximumFractionDigits: 2}) + ' млн ₽';
const ann = (P, r) => { const L = P * .8, m = r / 1200; return L * m / (1 - Math.pow(1 + m, -360)); };
const plural = (n, a, b, c) => { const m = n % 10, h = n % 100; return m === 1 && h !== 11 ? a : m >= 2 && m <= 4 && (h < 12 || h > 14) ? b : c; };
// демо-объекты: заказчик разрешил придуманные данные до запуска
const ITEMS = [
  {img: 'kv_living2', r: 2, s: 58.4, fl: 7, fls: 12, zk: 'ЖК Липовый сквер', d: 'Академический', t: 'new', due: 0, st: 'Дом сдан', fin: 'С отделкой', p: 9450000, disc: 6, x: 120, y: 250},
  {img: 'kv_empty', r: 1, s: 38.2, fl: 4, fls: 9, zk: 'ЖК Северный бульвар', d: 'Уралмаш', t: 'new', due: 202704, st: 'Сдача — II кв. 2027', fin: 'Без отделки', p: 5890000, special: 1, x: 300, y: 110},
  {img: 'kv_kids', r: 3, s: 79.6, fl: 10, fls: 16, zk: 'ЖК Кварц', d: 'ВИЗ', t: 'new', due: 0, st: 'Дом сдан · школа и сад во дворе', fin: 'С отделкой', p: 12300000, disc: 4, x: 190, y: 430},
  {img: 'kv_bedroom2', r: 2, s: 54.1, fl: 3, fls: 5, zk: 'ул. Малышева', d: 'Центр', t: 'sec', due: 0, st: 'Вторичка · юрист проверил', fin: 'С ремонтом', p: 8700000, x: 330, y: 540},
  {img: 'rem_bathroom', r: 2, s: 63.7, fl: 5, fls: 17, zk: 'ЖК Кварц', d: 'ВИЗ', t: 'new', due: 0, st: 'Дом сдан · наш ремонт, гарантия 5 лет', fin: 'С ремонтом', p: 11200000, bundle: 1, x: 70, y: 600},
  {img: 'kv_building', r: 0, s: 26.8, fl: 12, fls: 24, zk: 'ЖК Высота', d: 'Юго-Западный', t: 'new', due: 202612, st: 'Сдача — IV кв. 2026', fin: 'Без отделки', p: 4650000, x: 60, y: 160},
  {img: 'kv_complex2', r: 2, s: 61.0, fl: 8, fls: 14, zk: 'ЖК Новая Исеть', d: 'Ботанический', t: 'new', due: 202709, st: 'Сдача — III кв. 2027', fin: 'Без отделки', p: 8540000, special: 1, x: 250, y: 360},
  {img: 'kv_bedroom', r: 1, s: 41.5, fl: 2, fls: 9, zk: 'ул. Билимбаевская', d: 'Старая Сортировка', t: 'sec', due: 0, st: 'Вторичка · юрист проверил', fin: 'С ремонтом', p: 5300000, x: 40, y: 80},
  {img: 'kv_studio', r: 0, s: 24.9, fl: 6, fls: 18, zk: 'ЖК Липовый сквер', d: 'Академический', t: 'new', due: 0, st: 'Дом сдан', fin: 'С отделкой', p: 4390000, disc: 3, x: 150, y: 300},
  {img: 'kv_kitchen2', r: 1, s: 36.4, fl: 9, fls: 20, zk: 'ЖК Берег', d: 'Широкая речка', t: 'new', due: 202803, st: 'Сдача — I кв. 2028', fin: 'С отделкой', p: 5100000, x: 380, y: 230},
  {img: 'kv_living3', r: 4, s: 98.2, fl: 4, fls: 10, zk: 'ул. Блюхера', d: 'Пионерский', t: 'sec', due: 0, st: 'Вторичка · юрист проверил', fin: 'С ремонтом', p: 13900000, x: 345, y: 190},
  {img: 'kv_kitchen', r: 3, s: 74.0, fl: 11, fls: 17, zk: 'ЖК Северный бульвар', d: 'Уралмаш', t: 'new', due: 202704, st: 'Сдача — II кв. 2027', fin: 'С отделкой', p: 10350000, x: 280, y: 60},
].map((it, i) => ({...it, id: i, disc: it.disc || 0, ppm: Math.round(it.p / it.s)}));
const title = it => `${it.r ? it.r + '-комн. квартира' : 'Студия'}, ${it.s.toLocaleString('ru-RU')} м², ${it.fl}/${it.fls} этаж`;
const FILTERS = {
  best: ['Самые выгодные', it => it.disc || it.special],
  done: ['Сданные дома', it => it.t === 'new' && !it.due],
  fin: ['С отделкой или ремонтом', it => it.fin !== 'Без отделки'],
  fam: ['Под семейную ипотеку', it => it.t === 'new'],
  sec: ['Вторичка', it => it.t === 'sec'],
};
'''
cut('const ITEMS = [', 'const CHECKS = {', DATA)

LOGIC = r'''const store = {get(k) { try { return JSON.parse(localStorage.getItem(k) || '[]'); } catch (e) { return []; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify([...v])); } catch (e) {} }};
const fav = new Set(store.get('pn_fav')), cmp = new Set(store.get('pn_cmp'));
let shown = ITEMS, filtered = false, expanded = false;
const SORT = {best: (a, b) => (b.disc + (b.special ? 5 : 0)) - (a.disc + (a.special ? 5 : 0)) || a.ppm - b.ppm, cheap: (a, b) => a.p - b.p, due: (a, b) => a.due - b.due || a.p - b.p};
const tagOf = it => it.special ? 'Спецпредложение застройщика' : it.disc ? `Ниже рынка на ${it.disc} %` : it.bundle ? 'Квартира + ремонт' : '';
const rateOf = it => it.t === 'new' ? 6 : 20;
function toast(t) { const el = $('#toast'); el.textContent = t; el.classList.add('on'); clearTimeout(toast.h); toast.h = setTimeout(() => el.classList.remove('on'), 3200); }
function cardHTML(it) {
  const tg = tagOf(it), r = rateOf(it);
  return `<article class="card" data-i="${it.id}">
  <div class="gal"><img src="photo/${it.img}.jpg" alt="${title(it)}" loading="lazy">${tg ? `<span class="tag">${tg}</span>` : ''}
    <div class="acts"><button class="ib cmp" aria-pressed="${cmp.has(it.id)}" aria-label="Сравнить"><svg class="ico"><use href="#cmp"/></svg></button><button class="ib fav" aria-pressed="${fav.has(it.id)}" aria-label="В избранное"><svg class="ico"><use href="#heart"/></svg></button></div></div>
  <div class="mid"><div class="t">${title(it)}</div><div class="a">${it.zk} · ${it.d}</div>
    <button class="vbtn" aria-expanded="false"><i></i>${it.t === 'sec' ? 'Сделка проверена юристом' : 'Застройщик проверен'}<span class="vpop" role="tooltip"><b>Что мы проверили</b>${CHECKS[it.t === 'sec' ? 'sec' : 'dev'].slice(0, 4).map(c => `<span>${c[0]}</span>`).join('')}</span></button>
    <div class="line">${it.st} · ${it.fin.toLowerCase()}</div>
    ${it.fin === 'Без отделки' ? `<a class="rx" href="#ba">+ наш ремонт под ключ — от ${fmtM(it.s * 20000)}</a>` : ''}
    <div class="tags">${[it.t === 'new' ? 'Новостройка' : 'Вторичка', it.fin, it.t === 'new' ? 'Семейная ипотека' : 'Чистая сделка'].map(t => `<span>${t}</span>`).join('')}</div></div>
  <div class="rcol"><div class="price">${it.p.toLocaleString('ru-RU')} ₽</div><div class="ppm">${it.ppm.toLocaleString('ru-RU')} ₽ за м²</div>
    <button class="mort" data-i="${it.id}">В ипотеку<b>от ${Math.round(ann(it.p, r)).toLocaleString('ru-RU')} ₽/мес</b><small>${it.t === 'new' ? 'семейная' : 'рыночная'} ${r} % · взнос 20 %</small></button>
    <button class="btn dark tel-btn">Показать телефон</button></div>
</article>`;
}
function hl(i) { $$('.pin').forEach(p => p.classList.toggle('on', p.dataset.i == i)); $$('.card').forEach(c => c.classList.toggle('hl', c.dataset.i == i)); }
function counts() { [['#favCnt', fav], ['#cmpCnt', cmp]].forEach(([q, set]) => { $(q).textContent = set.size; $(q).classList.toggle('on', set.size > 0); }); }
function toggle(set, key, id, btn, lim) {
  if (!set.has(id) && lim && set.size >= lim) { toast('Сравнить можно до 4 квартир — уберите одну из сравнения'); return; }
  set.has(id) ? set.delete(id) : set.add(id); store.set(key, set); counts();
  $$(`.card[data-i="${id}"] .ib.${btn}`).forEach(b => b.setAttribute('aria-pressed', set.has(id)));
  if (set.has(id)) toast(btn === 'fav' ? 'Добавили в избранное — сердечко в шапке' : `В сравнении: ${set.size}. Откройте сравнение в шапке`);
}
function render() {
  const list = [...shown].sort(SORT[$('.seg.sort [aria-pressed=true]').dataset.s]);
  const vis = filtered || expanded ? list : list.slice(0, 6);
  $('#cards').innerHTML = vis.length ? vis.map(cardHTML).join('') : '<div class="empty"><b>Таких квартир сейчас нет<i class="o"></i></b>Оставьте заявку — подберём под ваши условия, как только появятся.<a class="btn red" href="#lead">Оставить заявку</a></div>';
  $('#pins').innerHTML = list.map((it, k) => `<button class="pin${k === 0 ? ' on' : ''}" data-i="${it.id}" style="left:${it.x / 430 * 100}%;top:${it.y / 680 * 100}%">${(it.p / 1e6).toLocaleString('ru-RU', {maximumFractionDigits: 1})} млн</button>`).join('');
  $('#cnt').textContent = `${list.length} ${plural(list.length, 'предложение', 'предложения', 'предложений')}`;
  $('#more').hidden = filtered || expanded || list.length <= 6;
  $('#moreBtn').textContent = `Показать ещё ${list.length - 6} проверенных`;
  $$('.card').forEach(c => c.addEventListener('mouseenter', () => hl(c.dataset.i)));
  $$('.pin').forEach(p => p.addEventListener('click', () => { hl(p.dataset.i); const c = $(`.card[data-i="${p.dataset.i}"]`); if (c) c.scrollIntoView({behavior: 'smooth', block: 'center'}); else { expanded = true; render(); hl(p.dataset.i); $(`.card[data-i="${p.dataset.i}"]`).scrollIntoView({behavior: 'smooth', block: 'center'}); } }));
  $$('.tel-btn').forEach(b => b.addEventListener('click', () => { b.outerHTML = '<a class="btn red" href="tel:+79655002918">+7 965 500-29-18</a>'; }));
  $$('.vbtn').forEach(b => b.addEventListener('click', e => { e.stopPropagation(); const o = b.getAttribute('aria-expanded') === 'true'; $$('.vbtn').forEach(x => x.setAttribute('aria-expanded', 'false')); b.setAttribute('aria-expanded', !o); }));
  $$('.ib.fav').forEach(b => b.addEventListener('click', () => toggle(fav, 'pn_fav', +b.closest('.card').dataset.i, 'fav')));
  $$('.ib.cmp').forEach(b => b.addEventListener('click', () => toggle(cmp, 'pn_cmp', +b.closest('.card').dataset.i, 'cmp', 4)));
  $$('button.mort').forEach(b => b.addEventListener('click', () => mortFrom(ITEMS[b.dataset.i])));
}
function mortFrom(it) {
  $('#cp').value = Math.min(20000000, it.p); $('#cd').value = 20; $('#ct').value = 30;
  $$('#rates button').forEach(x => x.setAttribute('aria-pressed', +x.dataset.r === rateOf(it))); calc();
  $('#calc').scrollIntoView({behavior: 'smooth'}); toast(`Подставили в калькулятор: ${title(it)}`);
}
function applyFilter(list, label) {
  shown = list; filtered = !!label; $('#flt').hidden = !label; $('#fltT').textContent = label || ''; render();
}
document.addEventListener('click', () => $$('.vbtn').forEach(x => x.setAttribute('aria-expanded', 'false')));
$('#moreBtn').addEventListener('click', () => { expanded = true; render(); });
$('#fltX').addEventListener('click', () => applyFilter(ITEMS, ''));
$$('.seg.sort button').forEach(b => b.addEventListener('click', () => { $$('.seg.sort button').forEach(x => x.setAttribute('aria-pressed', x === b)); render(); }));
$$('[data-c]').forEach(el => { const n = ITEMS.filter(FILTERS[el.dataset.c][1]).length; el.textContent = `${n} ${plural(n, 'квартира', 'квартиры', 'квартир')}`; });
$$('[data-f]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); const [lab, fn] = FILTERS[a.dataset.f]; applyFilter(ITEMS.filter(fn), lab); $('#list').scrollIntoView({behavior: 'smooth'}); }));

// поиск на первом экране
const TABK = ['new', 'sec', 'houses', 'fin'];
let tab = 'new';
function readForm() {
  const rooms = $$('.sf .chip').map((b, i) => b.getAttribute('aria-pressed') === 'true' ? i : -1).filter(i => i >= 0);
  let max = parseFloat(($('#pr').value || '').replace(',', '.').replace(/[^\d.]/g, '')) || 0;
  if (max && max < 1000) max *= 1e6;
  return {rooms, max, q: $('#ad').value.trim().toLowerCase()};
}
function match(it, f) {
  if (tab === 'new' && it.t !== 'new' || tab === 'sec' && it.t !== 'sec' || tab === 'fin' && it.fin === 'Без отделки') return false;
  if (f.rooms.length && !f.rooms.some(r => r === 4 ? it.r >= 4 : it.r === r)) return false;
  if (f.max && it.p > f.max) return false;
  return !f.q || (it.zk + ' ' + it.d).toLowerCase().includes(f.q);
}
function liveCount() { const f = readForm(), n = ITEMS.filter(it => match(it, f)).length; $('#goN').textContent = n; }
$$('.tabs button').forEach((b, i) => b.addEventListener('click', () => {
  if (TABK[i] === 'houses') { $('#houses').scrollIntoView({behavior: 'smooth'}); return; }
  tab = TABK[i]; $$('.tabs button').forEach(x => x.setAttribute('aria-selected', x === b)); liveCount();
}));
$$('.chip').forEach(b => b.addEventListener('click', () => { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true'); liveCount(); }));
['#pr', '#ad'].forEach(q => $(q).addEventListener('input', liveCount));
$('#sf').addEventListener('submit', e => {
  e.preventDefault(); const f = readForm();
  const lab = [{new: 'Новостройки', sec: 'Вторичка', fin: 'С отделкой или ремонтом'}[tab],
    f.rooms.length ? f.rooms.map(r => r === 0 ? 'студия' : r === 4 ? '4+' : r).join(', ') + (f.rooms.some(r => r) ? ' комн.' : '') : '',
    f.max ? 'до ' + fmtM(f.max) : '', f.q ? `«${$('#ad').value.trim()}»` : ''].filter(Boolean).join(' · ');
  applyFilter(ITEMS.filter(it => match(it, f)), lab); $('#list').scrollIntoView({behavior: 'smooth'});
});
liveCount();
$('.sw').addEventListener('click', e => { const sw = e.currentTarget; sw.setAttribute('aria-checked', 'false'); toast('Непроверенных объектов у нас нет — мы их не продаём'); setTimeout(() => sw.setAttribute('aria-checked', 'true'), 900); });

// сравнение и избранное
const dlg = $('#dlg');
function openDlg(t, html) { $('#dlgT').textContent = t; $('#dlgB').innerHTML = html; if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', ''); }
$('#dlgX').addEventListener('click', () => dlg.close());
dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
function cmpHTML() {
  const L = ITEMS.filter(it => cmp.has(it.id)), minP = Math.min(...L.map(i => i.ppm)), minPay = Math.min(...L.map(i => ann(i.p, rateOf(i))));
  const row = (h, f) => `<tr><th>${h}</th>${L.map(it => `<td>${f(it)}</td>`).join('')}</tr>`;
  return `<table class="ctab"><tbody>${row('', it => `<img src="photo/${it.img}.jpg" alt=""><b>${title(it)}</b><br><span style="color:var(--mut)">${it.zk} · ${it.d}</span>`)}
    ${row('Цена', it => `<b>${it.p.toLocaleString('ru-RU')} ₽</b>`)}${row('За м²', it => `<span class="${it.ppm === minP ? 'best' : ''}">${it.ppm.toLocaleString('ru-RU')} ₽${it.ppm === minP ? ' · дешевле всех' : ''}</span>`)}
    ${row('Платёж в ипотеку', it => { const p = ann(it.p, rateOf(it)); return `<span class="${p === minPay ? 'best' : ''}">от ${Math.round(p).toLocaleString('ru-RU')} ₽/мес</span><br><small style="color:var(--mut)">${rateOf(it)} %, взнос 20 %</small>`; })}
    ${row('Сдача', it => it.st)}${row('Отделка', it => it.fin)}${row('Проверка', it => it.t === 'sec' ? 'Юрист: сделка чистая' : 'Застройщик проверен')}
    ${row('', it => `<button class="rm" data-rm="${it.id}">Убрать из сравнения</button>`)}</tbody></table>`;
}
function showCmp() {
  if (!cmp.size) { toast('Добавьте квартиры к сравнению — кнопка на фото в карточке'); return; }
  openDlg(`Сравнение · ${cmp.size}`, cmpHTML());
  $$('#dlgB [data-rm]').forEach(b => b.addEventListener('click', () => { toggle(cmp, 'pn_cmp', +b.dataset.rm, 'cmp'); cmp.size ? showCmp() : dlg.close(); }));
}
$('#cmpBtn').addEventListener('click', showCmp);
$('#favBtn').addEventListener('click', () => {
  if (!fav.size) { toast('Пока пусто — нажмите сердечко на карточке квартиры'); return; }
  openDlg(`Избранное · ${fav.size}`, `<div class="flist">${ITEMS.filter(it => fav.has(it.id)).map(it => `<div class="fi"><img src="photo/${it.img}.jpg" alt=""><div><b>${it.p.toLocaleString('ru-RU')} ₽</b>${title(it)}<br><span style="color:var(--mut)">${it.zk} · ${it.d}</span></div></div>`).join('')}</div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px"><a class="btn red" href="#lead" onclick="dlg.close()">Записаться на просмотр</a><a class="btn white" href="tel:+79655002918">+7 965 500-29-18</a></div>`);
});
counts(); render();
'''
cut("$('#cards').innerHTML = ITEMS.map", "counter('.ib.fav', '#favCnt'); counter('.ib.cmp', '#cmpCnt');\n", LOGIC, keep_b=False)
rep("$$('.chip').forEach(b => b.addEventListener('click', () => b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true')));\n", '')
rep("single('.seg button'); single('.form .ch button');", "single('.form .ch button');")
rep("$$('.tabs button').forEach(b => b.addEventListener('click', () => $$('.tabs button').forEach(x => x.setAttribute('aria-selected', x === b))));\n", '')
rep("$('.sw').addEventListener('click', e => { const s = e.currentTarget; s.setAttribute('aria-checked', s.getAttribute('aria-checked') !== 'true'); });\n", '')

EXTRA = r'''
// телефон: маска и проверка
const lp = $('#lp');
lp.addEventListener('input', () => {
  let d = lp.value.replace(/\D/g, ''); lp.closest('.f').classList.remove('bad');
  if (!d) { lp.value = ''; return; }
  if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; const p = d.slice(1, 11);
  lp.value = '+7' + (p.length ? ' (' + p.slice(0, 3) : '') + (p.length > 3 ? ') ' + p.slice(3, 6) : '') + (p.length > 6 ? '-' + p.slice(6, 8) : '') + (p.length > 8 ? '-' + p.slice(8, 10) : '');
});
$('#leadForm').addEventListener('submit', e => {
  e.preventDefault();
  if (lp.value.replace(/\D/g, '').length !== 11) { lp.closest('.f').classList.add('bad'); lp.focus(); return; }
  e.currentTarget.classList.add('sent');
});

// меню: подсветка раздела
const navA = $$('nav.main a');
const spy = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) navA.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id)); }), {rootMargin: '-40% 0px -55% 0px'});
navA.forEach(a => { const t = $(a.getAttribute('href')); if (t) spy.observe(t); });

// отзывы: стрелки
$$('.arr button').forEach(b => b.addEventListener('click', () => { const rv = $('.rv'); rv.scrollBy({left: +b.dataset.d * ($('.rc').offsetWidth + 14), behavior: reduce ? 'auto' : 'smooth'}); }));
'''
rep("$('#leadForm').addEventListener('submit', e => e.currentTarget.classList.add('sent'));\n", '')
rep('</script>\n</body>', EXTRA + '</script>\n</body>')

open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok', len(s))
