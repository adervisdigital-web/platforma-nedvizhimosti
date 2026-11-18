
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const fmtM = n => (n / 1e6).toLocaleString('ru-RU', {maximumFractionDigits: 2}) + ' млн ₽';
const ann = (P, r) => { const L = P * .8, m = r / 1200; return L * m / (1 - Math.pow(1 + m, -360)); };
const plural = (n, a, b, c) => { const m = n % 10, h = n % 100; return m === 1 && h !== 11 ? a : m >= 2 && m <= 4 && (h < 12 || h > 14) ? b : c; };
// демо-объекты: заказчик разрешил придуманные данные до запуска
const ITEMS = PN.items().map((it, i) => ({...it, id: i, disc: it.disc || 0, ppm: Math.round(it.p / it.s)}));
const head = it => `${it.r ? it.r + '-комн. квартира' : 'Студия'} · ${it.s.toLocaleString('ru-RU')} м²`;
const title = it => `${it.r ? it.r + '-комн. квартира' : 'Студия'}, ${it.s.toLocaleString('ru-RU')} м², ${it.fl}/${it.fls} этаж`;
const FILTERS = {
  best: ['Самые выгодные', it => it.disc || it.special],
  done: ['Сданные дома', it => it.t === 'new' && !it.due],
  fin: ['С отделкой или ремонтом', it => it.fin !== 'Без отделки'],
  fam: ['Под семейную ипотеку', it => it.t === 'new'],
  sec: ['Вторичка', it => it.t === 'sec'],
};
const CHECKS = {
  dev: [['Разрешение на строительство', 'документы'], ['Проектная декларация и эскроу-счета', 'ЕИСЖС'], ['Прошлые дома сданы в срок', 'история'], ['Нет банкротных и крупных судебных дел', 'суды'], ['Отзывы жильцов сданных домов', 'люди']],
  sec: [['Собственники и доли', 'Росреестр'], ['Обременения и аресты', 'выписка'], ['История переходов права', 'юрист'], ['Долги по коммунальным платежам', 'справки'], ['Перепланировки', 'план БТИ']],
  our: [['Замер и смета до начала работ', 'выезд'], ['Предварительный договор', 'документы'], ['Промежуточный акт на каждый этап', 'приёмка'], ['Камера на объекте в личном кабинете', '24/7'], ['Гарантия на работы', '5 лет']],
};
function showChecks(k) { $('#clist').innerHTML = CHECKS[k].map(([a, b]) => `<li>${a}<span>${b}</span></li>`).join(''); }
showChecks('dev');
$$('.ctabs button').forEach(b => b.addEventListener('click', () => { $$('.ctabs button').forEach(x => x.setAttribute('aria-pressed', x === b)); showChecks(b.dataset.k); scanStart(); }));

// карта Екатеринбурга
const GEO = PN.geo();
let lmap = null, layer = null, lastPts = [];
function mapRender(list) {
  if (!window.L) return;
  if (!lmap) {
    $('.map').classList.add('live'); $('.map').insertAdjacentHTML('afterbegin', '<div id="lmap"></div>');
    lmap = L.map('lmap', {scrollWheelZoom: false, zoomControl: false}).setView([56.84, 60.59], 11);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18, attribution: '© участники OpenStreetMap'}).addTo(lmap);
    L.control.zoom({position: 'bottomright', zoomInTitle: 'Приблизить', zoomOutTitle: 'Отдалить'}).addTo(lmap);
    lmap.attributionControl.setPrefix(false);
    layer = L.layerGroup().addTo(lmap);
  }
  layer.clearLayers(); const seen = {};
  lastPts = list.map((it, k) => {
    const g = GEO[it.d] || [56.84, 60.6], n = seen[it.d] = (seen[it.d] || 0) + 1, ll = n === 3 ? [g[0] - .004, g[1] + .024] : g;
    L.marker(ll, {riseOnHover: true, icon: L.divIcon({className: 'lpin', iconSize: null, html: `<button class="pin${k === 0 ? ' on' : ''}${n === 2 ? ' dn' : ''}" data-i="${it.id}">${(it.p / 1e6).toLocaleString('ru-RU', {maximumFractionDigits: 1})} млн</button>`})}).addTo(layer);
    return ll;
  });
  mapFit();
}
function mapFit() { if (!lmap || !lastPts.length) return; lmap.invalidateSize(); const h = $('.map').clientHeight, view = Math.min(h, Math.round(innerHeight * .85)); lmap.fitBounds(lastPts, {paddingTopLeft: [60, 70], paddingBottomRight: [60, Math.max(60, h - view + 60)], maxZoom: 13}); }
$('#mapBtn').addEventListener('click', () => setTimeout(() => { if (lmap) { lmap.invalidateSize(); mapFit(); } }, 60));
const store = {get(k) { try { return JSON.parse(localStorage.getItem(k) || '[]'); } catch (e) { return []; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify([...v])); } catch (e) {} }};
const fav = new Set(store.get('pn_fav')), cmp = new Set(store.get('pn_cmp'));
let shown = ITEMS, filtered = false, expanded = false;
const SORT = {best: (a, b) => (b.disc + (b.special ? 5 : 0)) - (a.disc + (a.special ? 5 : 0)) || a.ppm - b.ppm, cheap: (a, b) => a.p - b.p, due: (a, b) => a.due - b.due || a.p - b.p};
const tagOf = it => it.special ? 'Спецпредложение застройщика' : it.disc ? `Ниже рынка на ${it.disc} %` : it.bundle ? 'Квартира + ремонт' : '';
const progOf = it => PN.mort.def(it.t === 'new');                         // новостройка — семейная (1 ребёнок), вторичка — рыночная
const rateOf = it => PN.mort.terms(progOf(it)).rate;
const payOf = it => PN.mort.pay(it.p, 20, 30, progOf(it)).pay;           // взнос 20 %, 30 лет, сверх лимита — рыночная
function toast(t) { const el = $('#toast'); el.textContent = t; el.classList.add('on'); clearTimeout(toast.h); toast.h = setTimeout(() => el.classList.remove('on'), 3200); }
function cardHTML(it) {
  const tg = tagOf(it), r = rateOf(it);
  return `<article class="card" data-i="${it.id}">
  <div class="gal"><img src="${PN.img(it.img)}" alt="${title(it)}" loading="lazy">${tg ? `<span class="tag">${tg}</span>` : ''}
    <div class="acts"><button class="ib cmp" aria-pressed="${cmp.has(it.id)}" aria-label="Сравнить"><svg class="ico"><use href="#cmp"/></svg></button><button class="ib fav" aria-pressed="${fav.has(it.id)}" aria-label="В избранное"><svg class="ico"><use href="#heart"/></svg></button></div></div>
  <div class="mid"><button class="t qv" data-i="${it.id}">${head(it)}</button><div class="a">${it.fl}/${it.fls} этаж · ${it.zk} · ${it.d}</div>
    <button class="vbtn" aria-expanded="false"><i></i>${it.t === 'sec' ? 'Сделка проверена юристом' : 'Застройщик проверен'}<span class="vpop" role="tooltip"><b>Что мы проверили</b>${CHECKS[it.t === 'sec' ? 'sec' : 'dev'].slice(0, 4).map(c => `<span>${c[0]}</span>`).join('')}</span></button>
    <div class="line">${it.st} · ${it.fin.toLowerCase()}</div>
    ${it.fin === 'Без отделки' ? `<a class="rx" href="#ba">+ наш ремонт под ключ — от ${fmtM(it.s * 20000)}</a>` : ''}
    <div class="tags">${[it.t === 'new' ? 'Новостройка' : 'Вторичка', it.t === 'new' ? 'Семейная ипотека' : 'Чистая сделка'].map(t => `<span>${t}</span>`).join('')}</div></div>
  <div class="rcol"><div class="price">${it.p.toLocaleString('ru-RU')} ₽</div><div class="ppm">${it.ppm.toLocaleString('ru-RU')} ₽ за м²</div>
    <button class="mort" data-i="${it.id}">В ипотеку<b>от ${Math.round(payOf(it)).toLocaleString('ru-RU')} ₽/мес</b><small>${it.t === 'new' ? 'семейная' : 'рыночная'} ${r} % · взнос 20 %</small></button>
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
  mapRender(list);
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
  $$('.card .qv').forEach(b => b.addEventListener('click', () => quick(ITEMS[b.dataset.i])));
  $$('.card .gal img').forEach(im => im.addEventListener('click', () => quick(ITEMS[im.closest('.card').dataset.i])));
}
function mortFrom(it) {
  $('#cp').value = Math.min(20000000, it.p); $('#cd').value = 20; $('#ct').value = 30;
  const pi = PN.mort.cfg.progs.indexOf(progOf(it)); $$('#rates button').forEach(x => x.setAttribute('aria-pressed', +x.dataset.p === pi)); calc();
  fillAll(); $('#calc').scrollIntoView({behavior: 'smooth'}); toast(`Подставили в калькулятор: ${title(it)}`);
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

// сравнение и избранное
const dlg = $('#dlg');
function openDlg(t, html) { $('#dlgT').textContent = t; $('#dlgB').innerHTML = html; if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', ''); }
$('#dlgX').addEventListener('click', () => dlg.close());
dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
function cmpHTML() {
  const L = ITEMS.filter(it => cmp.has(it.id)), minP = Math.min(...L.map(i => i.ppm)), minPay = Math.min(...L.map(i => payOf(i)));
  const row = (h, f) => `<tr><th>${h}</th>${L.map(it => `<td>${f(it)}</td>`).join('')}</tr>`;
  return `<table class="ctab"><tbody>${row('', it => `<img src="${PN.img(it.img)}" alt=""><b>${title(it)}</b><br><span style="color:var(--mut)">${it.zk} · ${it.d}</span>`)}
    ${row('Цена', it => `<b>${it.p.toLocaleString('ru-RU')} ₽</b>`)}${row('За м²', it => `<span class="${it.ppm === minP ? 'best' : ''}">${it.ppm.toLocaleString('ru-RU')} ₽${it.ppm === minP ? ' · дешевле всех' : ''}</span>`)}
    ${row('Платёж в ипотеку', it => { const p = payOf(it); return `<span class="${p === minPay ? 'best' : ''}">от ${Math.round(p).toLocaleString('ru-RU')} ₽/мес</span><br><small style="color:var(--mut)">${rateOf(it)} %, взнос 20 %</small>`; })}
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
  openDlg(`Избранное · ${fav.size}`, `<div class="flist">${ITEMS.filter(it => fav.has(it.id)).map(it => `<div class="fi"><img src="${PN.img(it.img)}" alt=""><div><b>${it.p.toLocaleString('ru-RU')} ₽</b>${title(it)}<br><span style="color:var(--mut)">${it.zk} · ${it.d}</span></div></div>`).join('')}</div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px"><a class="btn red" href="#lead" onclick="dlg.close()">Записаться на просмотр</a><a class="btn white" href="tel:+79655002918">+7 965 500-29-18</a></div>`);
});
counts(); render();
function single(sel) { $$(sel).forEach(b => b.addEventListener('click', () => { $$(sel).forEach(x => x.setAttribute('aria-pressed', x === b)); })); }
single('.form .ch button');

// отбор: сканер
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const SF = $('#sfield'), SC = 16, SN = SC * 9;
SF.insertAdjacentHTML('beforeend', Array.from({length: SN}, (_, i) => `<i class="${i % SC >= 12 ? 'x12' : ''}"></i>`).join(''));
const sdots = $$('#sfield i');
let scanT = [], scanRun = 0;
function scanStop() { scanT.forEach(clearTimeout); scanT = []; scanRun++; }
function scanStart() {
  if (window.__noScan) return;
  scanStop(); const run = scanRun, cols = () => innerWidth <= 1000 ? 12 : SC;
  const vis = () => sdots.filter((d, i) => i % SC < cols());
  const lis = $$('#clist li'), DUR = 1500, GAP = 450;
  sdots.forEach(d => d.classList.remove('off', 'pass', 'hit')); lis.forEach(l => l.classList.remove('act', 'pass'));
  let alive = vis(); const total = alive.length;
  $('#sIn').textContent = total; $('#sOut').textContent = total; $('#sOutL').textContent = 'проходят проверку';
  const finalN = 6, keep = new Set(alive.slice().sort(() => Math.random() - .5).slice(0, finalN));
  if (reduce) { alive.forEach(d => d.classList.add(keep.has(d) ? 'pass' : 'off')); lis.forEach(l => l.classList.add('pass')); $('#sOut').textContent = finalN; $('#sOutL').textContent = 'прошли все проверки'; return; }
  const beam = $('#beam'), W = SF.clientWidth;
  lis.forEach((li, s) => {
    scanT.push(setTimeout(() => {
      if (run !== scanRun) return;
      lis.forEach((l, k) => { l.classList.toggle('act', k === s); if (k < s) l.classList.add('pass'); });
      beam.classList.remove('go'); void beam.offsetWidth; beam.style.setProperty('--w', W + 'px'); beam.style.setProperty('--dur', DUR + 'ms'); beam.classList.add('go');
      li.style.setProperty('--dur', DUR + 'ms');
      const left = alive.filter(d => !keep.has(d)), drop = s === lis.length - 1 ? left : left.sort(() => Math.random() - .5).slice(0, Math.round(left.length * .45));
      drop.forEach(d => { const x = (d.offsetLeft + 5) / W; scanT.push(setTimeout(() => { if (run !== scanRun) return; d.classList.add('hit'); setTimeout(() => { d.classList.remove('hit'); d.classList.add('off'); }, 140); $('#sOut').textContent = +$('#sOut').textContent - 1; }, x * DUR)); });
      alive = alive.filter(d => !drop.includes(d));
    }, s * (DUR + GAP)));
  });
  scanT.push(setTimeout(() => { if (run !== scanRun) return; lis.forEach(l => { l.classList.remove('act'); l.classList.add('pass'); }); keep.forEach(d => d.classList.add('pass')); $('#sOut').textContent = finalN; $('#sOutL').textContent = 'прошли все проверки'; }, lis.length * (DUR + GAP)));
  scanT.push(setTimeout(() => { if (run === scanRun) scanStart(); }, lis.length * (DUR + GAP) + 4500));
}
new IntersectionObserver(es => { es[0].isIntersecting ? scanStart() : scanStop(); }, {threshold: .35}).observe($('#scan'));

// ипотечный калькулятор
const fmt = n => Math.round(n).toLocaleString('ru-RU') + ' ₽';
const kidsOf = () => +(($('#kids [aria-pressed=true]') || {dataset: {k: 1}}).dataset.k);
const progSel = () => PN.mort.cfg.progs[+(($('#rates [aria-pressed=true]') || {dataset: {p: 0}}).dataset.p)] || PN.mort.def(true);
function calc() {
  const P = +$('#cp').value, d = +$('#cd').value, y = +$('#ct').value, pr = progSel(), res = PN.mort.pay(P, d, y, pr, kidsOf());
  const L = res.loan, n = y * 12, pay = res.pay;
  if ($('#kids')) $('#kids').hidden = !pr.family;
  if ($('#cparts')) $('#cparts').innerHTML = res.parts.length > 1
    ? `${fmtM(res.parts[0][0])} под ${String(res.parts[0][1]).replace('.', ',')} % + ${fmtM(res.parts[1][0])} под ${String(res.parts[1][1]).replace('.', ',')} % — сверх лимита программы банк даёт по рыночной ставке`
    : `${pr.name}: ${String(res.parts[0][1]).replace('.', ',')} % на всю сумму`;
  $('#cpv').textContent = fmt(P); $('#cdv').textContent = d + ' % · ' + fmt(P * d / 100); $('#ctv').textContent = y + ' лет';
  $('#pay').innerHTML = Math.round(pay).toLocaleString('ru-RU') + ' <small>₽/мес</small>'; $('#loan').textContent = fmt(L); $('#over').textContent = fmt(pay * n - L); $('#inc').textContent = fmt(pay / .5);
}
['#cp', '#cd', '#ct'].forEach(s => $(s).addEventListener('input', calc));
$$('#rates button').forEach(b => b.addEventListener('click', () => { $$('#rates button').forEach(x => x.setAttribute('aria-pressed', x === b)); calc(); }));
$$('#kids button').forEach(b => b.addEventListener('click', () => { $$('#kids button').forEach(x => x.setAttribute('aria-pressed', x === b)); calc(); }));
calc();

$('#baR').addEventListener('input', e => { const v = e.target.value; $('#baBox .after').style.clipPath = `inset(0 0 0 ${v}%)`; $('#baH').style.left = v + '%'; });
const vbtns = $$('.view button');
function setView(v) { $('#cards').classList.toggle('grid', v === 'grid'); vbtns.forEach(b => b.setAttribute('aria-pressed', b.dataset.v === v)); }
vbtns.forEach(b => b.addEventListener('click', () => setView(b.dataset.v)));
setView(innerWidth >= 1700 ? 'grid' : 'list');

// дома: проект + рассрочка
const HOUSES = PN.houses();
let hSel = HOUSES[0], hName = 'Северный Урал 235';
const WARM = +(PN.settings().warm_contour_from || 75000);                 // ₽/м² тёплого контура — из админки (Настройки → Цены)
const hFrom = h => h.n * WARM, hMonth = (h, y = 5) => Math.round(hFrom(h) * .7 / (y * 12));
const flTxt = n => n === 1 ? '1 этаж' : n + ' этажа';
$('#hx').innerHTML = HOUSES.map(h => `<article class="hc" data-h="${h.id}">
  <button class="ph" type="button" data-open="${h.id}" aria-label="Подробнее: ${h.line} ${h.n}"><img src="${PN.img(h.ph[0], 'houses')}" alt="Дом «${h.line} ${h.n}»" loading="lazy"><span class="ln" style="--c:${h.c}"><i></i>${h.line}</span></button>
  <div class="b"><h3>${h.line}<span>${h.n}</span></h3><div class="mt">«${h.motto}»</div>
    <div class="sp"><span>${h.n} м²</span><span>${flTxt(h.fl)}</span><span>${h.rooms.replace(" + кабинет", "")} комн.${h.rooms.includes("кабинет") ? " + кабинет" : ""}</span><span>потолки ${h.ceil}</span></div>
    <div class="pr">Тёплый контур — от <b>${fmtM(hFrom(h))}</b> · <span class="nw">в рассрочку от ${hMonth(h).toLocaleString('ru-RU')} ₽/мес</span></div>
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
  dlg.classList.add('wide'); setHash('house-' + h.id);
  openDlg(`${h.line} ${h.n}`, `<div class="hdl"><div><div class="hmain"><img id="hvMain" src="${PN.img(h.ph[0], 'houses')}" alt="${h.line} ${h.n}"></div>
      <div class="hth">${h.ph.map((p, i) => `<button type="button" data-p="${p}" aria-pressed="${i === 0}" aria-label="Фото ${i + 1}"><img src="${PN.img(p, 'houses')}" alt=""></button>`).join('')}</div></div>
    <div><span class="ln" style="--c:${h.c}"><i></i>Линейка «${h.line}»</span><p class="mt2">«${h.motto}»</p>
      <dl class="qvp"><div><dt>Площадь</dt><dd>${h.n} м²</dd></div><div><dt>Этажность</dt><dd>${flTxt(h.fl)}</dd></div><div><dt>Жилых комнат</dt><dd>${h.rooms}</dd></div><div><dt>Потолки</dt><dd>${h.ceil}</dd></div></dl>
      <ul class="feats">${h.feats.map(f => `<li><svg><use href="#check"/></svg>${f}</li>`).join('')}</ul>
      <div class="qvm" style="margin-top:16px"><div><small>Тёплый контур от ${fmtM(hFrom(h))} · взнос 30 %</small><b>от ${hMonth(h).toLocaleString('ru-RU')} ₽/мес</b><small>рассрочка на 5 лет без процентов</small></div><button type="button" id="hvCalc">Рассчитать</button></div>
      <div class="qva"><a class="btn red" href="tel:+79655002918">Позвонить</a><button class="btn white" type="button" id="hvLead">Посетить демо-дом</button><button type="button" class="ib share" data-share aria-label="Поделиться ссылкой"><svg class="ico"><use href="#share"/></svg></button></div>
      <p class="hnote">Планировку и фасад настроим под вашу семью. Материал стен — на выбор.</p></div></div>
    <p class="hidea">${h.idea}</p><div class="htext">${h.text.map(t => `<p>${t}</p>`).join('')}</div>
    <div class="hpl"><h4>Планировка</h4>${h.plans.length > 1 ? `<div class="seg2" id="plTabs">${h.plans.map((p, i) => `<button type="button" aria-pressed="${i === 0}" data-i="${i}">${p[0]}</button>`).join('')}</div>` : `<span style="color:var(--mut)">${h.plans[0][0]}</span>`}</div>
    <a class="plan" id="plLink" href="${PN.img(h.plans[0][1], 'houses')}" target="_blank" rel="noopener" title="Открыть в полном размере"><img id="plImg" src="${PN.img(h.plans[0][1], 'houses')}" alt="Планировка: ${h.plans[0][0]}"></a>`);
  $$('#dlgB .hth button').forEach(b => b.addEventListener('click', () => { $('#hvMain').src = `${PN.img(b.dataset.p, 'houses')}`; $$('#dlgB .hth button').forEach(x => x.setAttribute('aria-pressed', x === b)); }));
  $$('#plTabs button').forEach(b => b.addEventListener('click', () => { const p = h.plans[b.dataset.i]; $('#plImg').src = $('#plLink').href = `${PN.img(p[1], 'houses')}`; $('#plImg').alt = 'Планировка: ' + p[0]; $$('#plTabs button').forEach(x => x.setAttribute('aria-pressed', x === b)); }));
  $('#hvCalc').addEventListener('click', () => { dlg.close(); pickHouse(h, true); });
  $('#hvLead').addEventListener('click', () => booking('Экскурсия в демо-дом', `Проект «${h.line} ${h.n}» — смотрим вживую`, 'Демо-дом, Екатеринбург'));
}
dlg.addEventListener('close', () => { dlg.classList.remove('wide'); if (/^#(obj|house)-/.test(location.hash)) history.replaceState(null, '', location.pathname + location.search); });
function hcalc() {
  const a = +$('#ha').value, y = +$('#ht').value, mode = $('#hmode [aria-pressed=true]').dataset.m;
  const sum = a * WARM, pv = sum * .3, rest = sum - pv;
  $('#hav').textContent = a + ' м²'; $('#htv').textContent = y + (y === 1 ? ' год' : y < 5 ? ' года' : ' лет');
  $('#hname').textContent = `Проект «${hName}» · тёплый контур`;
  $('#hsum').textContent = fmt(sum); $('#hpv').textContent = fmt(pv); $('#hrest').textContent = fmt(rest);
  if (mode === 'inst') { $('#hpay').innerHTML = Math.round(rest / (y * 12)).toLocaleString('ru-RU') + ' <small>₽/мес</small>'; $('#hrestL').textContent = `Остаток в рассрочку на ${$('#htv').textContent}`; }
  else { $('#hpay').innerHTML = Math.round(rest / 4).toLocaleString('ru-RU') + ' <small>₽/этап</small>'; $('#hrestL').textContent = 'Остаток — 4 платежа по этапам'; }
  $('#ht').disabled = mode !== 'inst'; $('#ht').closest('.rng').style.opacity = mode === 'inst' ? 1 : .4;
}
['#ha', '#ht'].forEach(q => $(q).addEventListener('input', hcalc));
$$('#hmode button').forEach(b => b.addEventListener('click', () => { $$('#hmode button').forEach(x => x.setAttribute('aria-pressed', x === b)); hcalc(); }));
pickHouse(hSel);

// ремонт
function rcalc() {
  const a = +$('#ra').value, l = +$('#rl').value;
  const lvl = l <= 35000 ? 'базовый' : l <= 65000 ? 'комфорт' : 'премиум';
  $('#rav').textContent = a + ' м²'; $('#rlv').textContent = lvl + ' · ' + l.toLocaleString('ru-RU') + ' ₽/м²';
  $('#rpay').innerHTML = Math.round(a * l / 1000).toLocaleString('ru-RU') + ' <small>тыс. ₽</small>'; $('#rppm').textContent = fmt(l);
}
['#ra', '#rl'].forEach(q => $(q).addEventListener('input', rcalc)); rcalc();

// кабинет: время камеры и подпись акта

// помощник 24/7 (на макете — ответы по готовым темам; на сайте — ИИ + своя CRM заказчика)
const FAQ = PN.faq();
const QUICK = PN.quick();
const log = $('#chatLog');
function say(t, me) { const p = document.createElement('p'); if (me) { p.className = 'me'; p.textContent = t; } else p.innerHTML = t; log.appendChild(p); log.scrollTop = log.scrollHeight; return p; }
function ask(q) {
  say(q, 1); const t = say('печатает…'); t.className = 'typing';
  const hit = FAQ.find(([re]) => re.test(q));
  setTimeout(() => { t.className = ''; t.innerHTML = hit ? hit[1] : 'Передам вопрос менеджеру — он свяжется с вами. Оставьте телефон в <a href="#lead">форме</a> или позвоните: <a href="tel:+79655002918">+7 965 500-29-18</a>.'; log.scrollTop = log.scrollHeight; }, reduce ? 0 : 700);
}
$('#chatQ').innerHTML = QUICK.map(q => `<button type="button">${q}</button>`).join('');
$$('#chatQ button').forEach(b => b.addEventListener('click', () => ask(b.textContent)));
$('#chatForm').addEventListener('submit', e => { e.preventDefault(); const v = $('#chatIn').value.trim(); if (v) { ask(v); $('#chatIn').value = ''; } });
let greeted = false;
function openChat(o) {
  $('#chat').hidden = !o; $('#chatFab').hidden = o; $('#chatFab').setAttribute('aria-expanded', o);
  if (o && !greeted) { say('Здравствуйте! Я помощник Платформы и отвечаю круглосуточно. Спросите про квартиры, ипотеку, ремонт или дома.'); greeted = true; }
  if (o && matchMedia('(hover:hover)').matches) $('#chatIn').focus();
  const mob = innerWidth <= 800; document.documentElement.classList.toggle('chat-lock', o && mob); if (o && mob) fitChat();
}
function fitChat() { const v = window.visualViewport, c = $('#chat'); if (!v || innerWidth > 800 || c.hidden) { c.style.height = c.style.top = ''; return; }
  c.style.top = v.offsetTop + 'px'; c.style.height = v.height + 'px'; const lg = $('#chatLog'); lg.scrollTop = lg.scrollHeight; }
if (window.visualViewport) { visualViewport.addEventListener('resize', fitChat); visualViewport.addEventListener('scroll', fitChat); }
$('#chatFab').addEventListener('click', () => openChat(true));
$('#chatX').addEventListener('click', () => openChat(false));
$$('[data-chat]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); openChat(true); }));
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('#chat').hidden) openChat(false); });

// телефон: маска и проверка
const lp = $('#lp');
lp.addEventListener('input', () => {
  let d = lp.value.replace(/\D/g, ''); lp.closest('.f').classList.remove('bad');
  if (!d) { lp.value = ''; return; }
  if (/^\s*\+\s*[0-689]/.test(lp.value)) return;   // номер не российский — не переделываем в +7, проверка его отклонит
  if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; const p = d.slice(1, 11);
  lp.value = '+7' + (p.length ? ' (' + p.slice(0, 3) : '') + (p.length > 3 ? ') ' + p.slice(3, 6) : '') + (p.length > 6 ? '-' + p.slice(6, 8) : '') + (p.length > 8 ? '-' + p.slice(8, 10) : '');
});
$('#leadForm').addEventListener('submit', e => {
  e.preventDefault();
  if (!/^\+7/.test(lp.value) || lp.value.replace(/\D/g, '').length !== 11) { lp.closest('.f').classList.add('bad'); lp.focus(); return; }
  if (!$('#lc').checked) { $('#lcL').classList.add('bad'); $('#lc').focus(); return; }
  const form = e.currentTarget, btn = $('#qSend'); btn.disabled = true;
  PN.send({kind: 'quiz', want: (($('#leadForm .ch [aria-pressed=true]') || {}).textContent || '') + ($('#leadForm').dataset.pack ? ' + ремонт (пакет)' : ''), budget: $('#qbv').textContent,
    area: $$('#qr [aria-pressed=true]').map(b => b.textContent).join(', '), name: $('#ln').value, phone: lp.value},
    () => { btn.disabled = false; form.classList.add('sent'); }, () => { btn.disabled = false; });
});

// меню: подсветка раздела
const navA = $$('nav.main a');
const spy = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) navA.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id)); }), {rootMargin: '-40% 0px -55% 0px'});
navA.forEach(a => { const t = $(a.getAttribute('href')); if (t) spy.observe(t); });

// отзывы: стрелки
$$('.arr button').forEach(b => b.addEventListener('click', () => { const rv = $('.rv'); rv.scrollBy({left: +b.dataset.d * ($('.rc').offsetWidth + 14), behavior: reduce ? 'auto' : 'smooth'}); }));

// быстрый просмотр объекта
function quick(it) {
  setHash('obj-' + it.id);
  const r = rateOf(it), pay = Math.round(payOf(it)), tg = tagOf(it), ck = CHECKS[it.t === 'sec' ? 'sec' : 'dev'];
  openDlg(title(it), `<div class="qvg"><div><div class="qvph"><img src="${PN.img(it.img)}" alt="${title(it)}">${tg ? `<span class="tag">${tg}</span>` : ''}</div>
    <div class="qvc"><b><i></i>${it.t === 'sec' ? 'Что проверил юрист' : 'Что мы проверили у застройщика'}</b>${ck.map(c => `<span><svg><use href="#check"/></svg>${c[0]}</span>`).join('')}</div></div>
    <div class="qvi"><div class="qic"><button type="button" class="ib share" data-share aria-label="Поделиться ссылкой"><svg class="ico"><use href="#share"/></svg></button><button class="ib fav" id="qvFav" aria-pressed="${fav.has(it.id)}" aria-label="В избранное"><svg class="ico"><use href="#heart"/></svg></button></div><div class="price">${it.p.toLocaleString('ru-RU')} ₽</div><div class="ppm">${it.ppm.toLocaleString('ru-RU')} ₽ за м² · ${it.zk}, ${it.d}</div>
    <dl class="qvp"><div><dt>Площадь</dt><dd>${it.s.toLocaleString('ru-RU')} м²</dd></div><div><dt>Этаж</dt><dd>${it.fl} из ${it.fls}</dd></div>
      <div><dt>Сдача</dt><dd>${it.due ? it.st.replace('Сдача — ', '') : it.t === 'sec' ? 'Готовое жильё' : 'Дом сдан'}</dd></div><div><dt>Отделка</dt><dd>${it.fin}</dd></div></dl>
    <div class="qvm"><div><small>В ипотеку · ${it.t === 'new' ? 'семейная' : 'рыночная'} ${r} %, взнос 20 %</small><b>от ${pay.toLocaleString('ru-RU')} ₽/мес</b></div><button type="button" id="qvCalc">Рассчитать</button></div>
    ${it.fin === 'Без отделки' ? `<div class="qvx"><span class="k">Добавить наш ремонт · гарантия 5 лет</span><div class="seg2" id="qvR">${[['Без ремонта', 0], ['Базовый', 20000], ['Комфорт', 45000], ['Премиум', 80000]].map((x, i) => `<button type="button" aria-pressed="${i === 0}" data-r="${x[1]}">${x[0]}</button>`).join('')}</div><div class="tot"><span class="k" id="qvRk">Квартира</span><b id="qvT">${rub(it.p)}</b></div></div>` : ''}
    <div class="qva"><a class="btn red" href="tel:+79655002918">Позвонить</a><button class="btn white" type="button" id="qvLead">Записаться на просмотр</button></div></div></div>`);
  $('#qvCalc').addEventListener('click', () => { dlg.close(); mortFrom(it); });
  $('#qvLead').addEventListener('click', () => booking('Просмотр', title(it) + ' · ' + it.zk, `${it.zk}, ${it.d}`));
  $$('#qvR button').forEach(b => b.addEventListener('click', () => { $$('#qvR button').forEach(x => x.setAttribute('aria-pressed', x === b)); const add = it.s * +b.dataset.r;
    $('#qvRk').textContent = add ? `Квартира + ремонт «${b.textContent.toLowerCase()}» (${fmtM(add)})` : 'Квартира'; $('#qvT').textContent = rub(it.p + add); }));
  remember(it.id);
  $('#qvFav').addEventListener('click', e => { toggle(fav, 'pn_fav', it.id, 'fav'); e.currentTarget.setAttribute('aria-pressed', fav.has(it.id)); });
}

// ползунки: заливка до бегунка
function fillAll() { $$('input[type=range]').forEach(r => r.style.setProperty('--p', (r.value - r.min) / (r.max - r.min) * 100 + '%')); }
document.addEventListener('input', e => { if (e.target.type === 'range') fillAll(); });
fillAll();

// подсказки района и ЖК
$('#adList').innerHTML = [...new Set(ITEMS.flatMap(it => [it.d, it.zk]))].map(v => `<option value="${v}">`).join('');

// карта на телефоне
$('#mapBtn').addEventListener('click', e => { const on = $('.res').classList.toggle('showmap'); e.currentTarget.setAttribute('aria-pressed', on); e.currentTarget.lastChild.textContent = on ? 'Списком' : 'На карте'; });


// шапка с тенью и кнопка чата — после первого экрана
const hdr = $('header'), fab = $('#chatFab');
function onScroll() { hdr.classList.toggle('sc', scrollY > 10); fab.classList.toggle('show', scrollY > $('.hero').offsetHeight * .6); fab.classList.toggle('mini', scrollY > $('.hero').offsetHeight * 1.4); }
addEventListener('scroll', onScroll, {passive: true}); onScroll();

// ссылки на объект и дом
function setHash(h) { try { history.replaceState(null, '', '#' + h); } catch (e) {} }
document.addEventListener('click', async e => {
  if (!e.target.closest('[data-share]')) return;
  const url = location.href, title = $('#dlgT').textContent + ' — Платформа недвижимости';
  try { if (navigator.share) { await navigator.share({title, url}); return; } await navigator.clipboard.writeText(url); toast('Ссылка скопирована — отправьте её родным'); }
  catch (x) { if (x.name !== 'AbortError') toast('Скопируйте ссылку из адресной строки'); }
});
(() => { const m = location.hash.match(/^#(obj|house)-(\w+)$/); if (!m) return;
  const t = m[1] === 'obj' ? ITEMS[+m[2]] : byId(m[2]); if (t) (m[1] === 'obj' ? quick : houseView)(t); })();

// линия прокрутки: к концу страницы — точка
const prog = $('#prog');
function progUpd() { const h = document.documentElement.scrollHeight - innerHeight, k = h > 0 ? Math.min(1, scrollY / h) : 0; prog.style.setProperty('--s', k); prog.classList.toggle('end', k > .995); }
addEventListener('scroll', progUpd, {passive: true}); addEventListener('resize', progUpd); progUpd();
new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { $('.fbig').classList.add('in'); o.disconnect(); } }, {threshold: .6}).observe($('.fbig'));

// подбор за 3 шага
let qs = 1, qType = 'flat';
const Q2 = {
  flat: {l: 'Какой бюджет на квартиру?', bl: 'Бюджет до', min: 3, max: 20, step: .5, v: 9, rooms: true},
  house: {l: 'Какой бюджет на дом?', bl: 'Бюджет до', min: 10, max: 40, step: 1, v: 20},
  reno: {l: 'Какая площадь квартиры?', bl: 'Площадь', min: 20, max: 160, step: 1, v: 55},
  mort: {l: 'Сколько стоит квартира?', bl: 'Стоимость', min: 3, max: 20, step: .5, v: 8},
};
function qMatch() {
  const c = Q2[qType], v = +$('#qb').value, mil = v * 1e6;
  $('#qbv').textContent = qType === 'reno' ? v + ' м²' : v.toLocaleString('ru-RU') + ' млн ₽';
  let t;
  if (qType === 'flat') {
    const rooms = $$('#qr [aria-pressed=true]').map(b => +b.dataset.r);
    const n = ITEMS.filter(it => it.p <= mil && (!rooms.length || rooms.some(r => r === 4 ? it.r >= 4 : it.r === r))).length;
    t = n ? `Подходит <b>${n} ${plural(n, 'квартира', 'квартиры', 'квартир')}</b> из проверенных. Пришлём их и новые, как только появятся.` : 'Сейчас таких нет — подберём под ваши условия и сообщим первыми.';
  } else if (qType === 'house') {
    const ok = HOUSES.filter(h => hFrom(h) <= mil);
    t = ok.length ? `Укладываются: <b>${ok.map(h => h.line + ' ' + h.n).join(', ')}</b>. Остаток можно платить по этапам или в рассрочку без процентов до 5 лет.` : 'Подберём площадь и материал под ваш бюджет — проекты настраиваются.';
  } else if (qType === 'reno') {
    t = `Ориентир с материалами: <b>от ${fmtM(v * 20000)}</b> за базовую отделку до ${fmtM(v * 100000)} за премиум. Точную цену даст смета после замера.`;
  } else {
    const fp = PN.mort.def(true);
    t = `По семейной ипотеке (${PN.mort.terms(fp).rate} % с одним ребёнком, с двумя и больше — ниже) со взносом 20 % на 30 лет: <b>от ${Math.round(PN.mort.pay(mil, 20, 30, fp).pay).toLocaleString('ru-RU')} ₽/мес</b>. Подберём банк с индивидуальной ставкой.`;
  }
  $('#qMatch').innerHTML = t;
  $('#qr').hidden = !c.rooms;
}
function qSet(type) {
  qType = type; const c = Q2[type], r = $('#qb');
  Object.assign(r, {min: c.min, max: c.max, step: c.step}); r.value = c.v;
  $('#q2l').textContent = c.l; $('#qbl').textContent = c.bl; qMatch(); fillAll();
}
function qGo(n) {
  qs = n; $$('#leadForm fieldset').forEach(f => f.classList.toggle('on', +f.dataset.s === n));
  $('#qStep').textContent = `Шаг ${n} из 3`; $$('.qd i').forEach((d, i) => d.classList.toggle('on', i < n));
  $('#qBack').hidden = n === 1; $('#qNext').hidden = n === 3; $('#qSend').hidden = n !== 3;
  if (n === 3) $('#ln').focus();
}
$$('#leadForm .ch button').forEach(b => b.addEventListener('click', () => qSet(b.dataset.q)));
$$('#qr button').forEach(b => b.addEventListener('click', () => { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true'); qMatch(); }));
$('#qb').addEventListener('input', qMatch);
$('#qNext').addEventListener('click', () => qGo(qs + 1));
$('#qBack').addEventListener('click', () => qGo(qs - 1));
qSet('flat');

// мессенджеры: ников пока нет — ведём в чат на сайте
$$('[data-soon]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); openChat(true); toast(`${a.dataset.soon} подключим к запуску — пока пишите здесь, ответим сразу`); }));

function rub(n) { return Math.round(n).toLocaleString('ru-RU') + ' ₽'; }
const MONTHS = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];

// запись на просмотр / в демо-дом
const DOW = ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'];
function booking(kind, subj, place) {
  const days = Array.from({length: 7}, (_, i) => { const d = new Date(); d.setDate(d.getDate() + i + 1); return d; });
  let day = 0, slot = '';
  const slotsFor = d => ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'].map((t, i) => [t, (d.getDate() * 7 + i * 3) % 5 === 0 || (d.getDay() === 0 && i > 5)]);
  const draw = () => {
    $('#dlgB').innerHTML = `<div class="bk"><p style="margin:0;color:#4A4741">${subj}</p>
      <div><h4>День</h4><div class="days" style="margin-top:10px">${days.map((d, i) => `<button type="button" data-d="${i}" aria-pressed="${i === day}"><small>${DOW[d.getDay()]}</small><b>${d.getDate()}</b><small>${MONTHS[d.getMonth()].slice(0, 3)}</small></button>`).join('')}</div></div>
      <div><h4>Время</h4><div class="slots" style="margin-top:10px">${slotsFor(days[day]).map(([t, busy]) => `<button type="button" data-t="${t}" ${busy ? 'disabled aria-label="' + t + ' занято"' : ''} aria-pressed="${t === slot}">${t}</button>`).join('')}</div></div>
      <div class="f" id="bkF"><label for="bkP">Телефон для подтверждения</label><input id="bkP" type="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" value="${$('#lp').value}"><span class="err">Введите номер полностью — 10 цифр после +7</span></div>
      <label class="cns" id="bkCL"><input type="checkbox" id="bkC"> <span>Согласен на <a href="privacy/" target="_blank">обработку персональных данных</a></span></label>
      <button class="btn red" type="button" id="bkGo" ${slot ? '' : 'disabled style="opacity:.45"'}>${slot ? `Записаться на ${days[day].getDate()} ${MONTHS[days[day].getMonth()]}, ${slot}` : 'Выберите время'}</button></div>`;
    $$('#dlgB [data-d]').forEach(b => b.addEventListener('click', () => { day = +b.dataset.d; slot = ''; draw(); }));
    $$('#dlgB [data-t]').forEach(b => b.addEventListener('click', () => { slot = b.dataset.t; draw(); }));
    const ip = $('#bkP'); ip.addEventListener('input', () => { lp.value = ip.value; lp.dispatchEvent(new Event('input')); ip.value = lp.value; $('#bkF').classList.remove('bad'); });
    $('#bkGo').addEventListener('click', () => {
      if (!/^\+7/.test(ip.value) || ip.value.replace(/\D/g, '').length !== 11) { $('#bkF').classList.add('bad'); ip.focus(); return; }
      if (!$('#bkC').checked) { $('#bkCL').classList.add('bad'); $('#bkC').focus(); return; }
      { const d0 = days[day], p2 = n => String(n).padStart(2, '0');
        PN.send({kind: 'viewing', want: kind, object_ref: subj, slot: `${d0.getFullYear()}-${p2(d0.getMonth() + 1)}-${p2(d0.getDate())} ${slot}`, phone: ip.value}, () => {
      const d = days[day], [hh, mm] = slot.split(':'), st = new Date(d.getFullYear(), d.getMonth(), d.getDate(), +hh, +mm), en = new Date(st.getTime() + 36e5);
      const f = x => x.toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
      const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Platforma//RU', 'BEGIN:VEVENT', `UID:${Date.now()}@p.forma196.ru`, `DTSTAMP:${f(new Date())}`, `DTSTART:${f(st)}`, `DTEND:${f(en)}`,
        `SUMMARY:${kind} — Платформа недвижимости`, `DESCRIPTION:${subj}. Телефон менеджера +7 965 500-29-18`, `LOCATION:${place}`, 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
      const url = URL.createObjectURL(new Blob([ics], {type: 'text/calendar'}));
      $('#dlgT').textContent = 'Записали';
      $('#dlgB').innerHTML = `<div class="bkok"><span class="big"><i></i></span><h4>${d.getDate()} ${MONTHS[d.getMonth()]}, ${slot}<i class="o"></i></h4>
        <p>${kind}: ${subj}. Менеджер позвонит накануне и пришлёт адрес. Поменять время — по телефону <a href="tel:+79655002918" style="font-weight:700">+7 965 500-29-18</a>.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center"><a class="btn dark" href="${url}" download="platforma-${d.getDate()}-${MONTHS[d.getMonth()]}.ics">Добавить в календарь</a><button class="btn ghost" type="button" onclick="dlg.close()">Готово</button></div></div>`;
      }); }
    });
  };
  $('#dlgT').textContent = kind; dlg.classList.remove('wide'); draw();
  if (!dlg.open) dlg.showModal();
}

// вы смотрели
function seenList() { return window.PN_SEEN || (window.PN_SEEN = store.get('pn_seen')); }
function remember(id) { const seen = seenList(); const i = seen.indexOf(id); if (i >= 0) seen.splice(i, 1); seen.unshift(id); seen.length = Math.min(seen.length, 8); store.set('pn_seen', seen); drawSeen(); }
function drawSeen() {
  const seen = seenList(); if (!$('#seenL') || typeof head !== 'function') return;
  $('#seen').hidden = !seen.length;
  $('#seenL').innerHTML = seen.map(id => ITEMS[id]).filter(Boolean).map(it => `<button type="button" data-seen="${it.id}"><img src="${PN.img(it.img)}" alt=""><b>${(it.p / 1e6).toLocaleString('ru-RU', {maximumFractionDigits: 2})} млн ₽</b><span>${head(it)} · ${it.d}</span></button>`).join('');
  $$('[data-seen]').forEach(b => b.addEventListener('click', () => quick(ITEMS[b.dataset.seen])));
}
drawSeen();

// цифры «Отбора» — отсчёт
function countUp(el, to, ms) {
  if (reduce) return; const t0 = performance.now(), fmtN = n => n >= 1000 ? Math.round(n).toLocaleString('ru-RU') : Math.round(n);
  (function f(t) { const k = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - k, 3); el.textContent = fmtN(to * e); if (k < 1) requestAnimationFrame(f); })(t0);
}
// цифры: табло и точки
$$('.odo').forEach(o => { const str = (+o.dataset.n).toLocaleString('ru-RU'); o.innerHTML = [...str].map(ch => /\d/.test(ch) ? `<span class="col" data-d="${ch}">${'0123456789'.repeat(2).split('').map(x => `<span>${x}</span>`).join('')}</span>` : '<span class="gap"></span>').join(''); });
$$('.sd').forEach(d => { d.innerHTML = '<i></i>'.repeat(+d.dataset.n); });
function statsGo() {
  $$('.odo').forEach((o, k) => $$('.col', o).forEach((c, j) => { c.style.transitionDelay = (k * 150 + j * 120) + 'ms'; c.style.transform = `translateY(-${10 + +c.dataset.d}em)`; }));
  $$('.sd').forEach((d, k) => $$('i', d).forEach((dot, j) => setTimeout(() => dot.classList.add('on'), reduce ? 0 : 300 + k * 150 + j * (1400 / d.children.length))));
}
new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect(); statsGo(); }, {threshold: .4}).observe($('.stats2'));

// итоги калькуляторов — плавно
['#pay', '#hpay', '#rpay'].forEach(q => {
  const el = $(q); if (!el) return; let cur = parseFloat(el.textContent.replace(/[^\d,]/g, '').replace(',', '.')) || 0, raf;
  new MutationObserver(() => {
    const node = el.firstChild; if (!node || node.nodeType !== 3) return;
    const to = parseFloat(node.nodeValue.replace(/[^\d,]/g, '').replace(',', '.')); if (isNaN(to) || reduce) { cur = to; return; }
    const from = cur, t0 = performance.now(); cur = to; cancelAnimationFrame(raf);
    (function f(t) { const k = Math.min(1, (t - t0) / 380), e = 1 - Math.pow(1 - k, 3); node.nodeValue = Math.round(from + (to - from) * e).toLocaleString('ru-RU') + ' '; if (k < 1) raf = requestAnimationFrame(f); })(t0);
  }).observe(el, {childList: true});
});

// обещания ↔ пункты договора
const cl = $('.cl');
function vow(b) { const on = b && b.dataset.cl.split(','); $$('.vows button').forEach(x => x.classList.toggle('on', x === b)); cl.classList.toggle('hl', !!b); $$('.cl li').forEach(li => li.classList.toggle('on', !!on && on.includes(li.dataset.n))); }
$$('.vows button').forEach(b => { b.addEventListener('mouseenter', () => vow(b)); b.addEventListener('focus', () => vow(b)); b.addEventListener('click', () => vow(b.classList.contains('on') ? null : b)); });
$('.vows').addEventListener('mouseleave', () => vow(null));
(() => { const desk = $('#desk');
  function play() { const lis = $$('.cl li', desk); desk.classList.add('in'); const st = reduce ? 0 : 260;
    lis.forEach((li, k) => setTimeout(() => li.classList.add('ok'), st * (k + 1)));
    setTimeout(() => desk.classList.add('signed'), st * (lis.length + 1)); setTimeout(() => desk.classList.add('sealed'), st * (lis.length + 1) + (reduce ? 0 : 1300)); }
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { play(); o.disconnect(); } }, {threshold: .45}).observe(desk);
  if (!reduce && matchMedia('(hover:hover)').matches) {
    desk.addEventListener('mousemove', e => { const r = desk.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      desk.classList.add('move'); desk.style.setProperty('--dry', (x * 6).toFixed(2) + 'deg'); desk.style.setProperty('--drx', (-y * 5).toFixed(2) + 'deg'); });
    desk.addEventListener('mouseleave', () => { desk.classList.remove('move'); desk.style.setProperty('--dry', '0deg'); desk.style.setProperty('--drx', '0deg'); });
  } })();

// MacBook + iPhone: масштаб экранов и наклон за курсором
const devs = $('#devs');
function fitDevs() { const m = $('.mbp .vp'), p = $('.iph .vp'); if (!m) return; devs.style.setProperty('--ks', m.clientWidth / 1440); devs.style.setProperty('--kp', p.clientWidth / 390); }
addEventListener('resize', fitDevs); fitDevs(); new ResizeObserver(fitDevs).observe(devs);
if (!reduce && matchMedia('(hover:hover)').matches) {
  devs.addEventListener('mousemove', e => {
    const r = devs.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
    devs.classList.add('move');
    devs.style.setProperty('--ry', (x * 14).toFixed(2) + 'deg'); devs.style.setProperty('--rx', (-y * 10).toFixed(2) + 'deg');
    devs.style.setProperty('--px', (x * 22).toFixed(1) + 'px'); devs.style.setProperty('--py', (y * 16).toFixed(1) + 'px');
  });
  devs.addEventListener('mouseleave', () => { devs.classList.remove('move'); ['--rx', '--ry'].forEach(v => devs.style.setProperty(v, '0deg')); ['--px', '--py'].forEach(v => devs.style.setProperty(v, '0px')); });
}

// меню: капсула и скользящая точка
const hdrEl = $('header'), nav = $('nav.main'), nd = $('nav.main .nd');
function ndTo(a) { if (!a) { nav.style.setProperty('--no', 0); return; } nav.style.setProperty('--nx', (a.offsetLeft + a.offsetWidth / 2 - 3) + 'px'); nav.style.setProperty('--no', 1); }
const ndActive = () => ndTo($('nav.main a.on'));
$$('nav.main a').forEach(a => a.addEventListener('mouseenter', () => ndTo(a)));
nav.addEventListener('mouseleave', ndActive);
new MutationObserver(ndActive).observe(nav, {subtree: true, attributes: true, attributeFilter: ['class']});
setTimeout(ndActive, 300); addEventListener('resize', ndActive);
function hdrUpd() { hdrEl.classList.toggle('ontop', scrollY < $('.hero').offsetHeight - 90); }
addEventListener('scroll', hdrUpd, {passive: true}); hdrUpd();

// поиск: быстрые фильтры
const QF = {ready: it => !it.due, fin: it => it.fin !== 'Без отделки', fam: it => it.t === 'new', deal: it => it.disc || it.special};
const qfOn = () => $$('.qf [aria-pressed=true]').map(b => b.dataset.qf);
const _match = match;
match = (it, f) => _match(it, f) && qfOn().every(k => QF[k](it));
$$('.qf button').forEach(b => b.addEventListener('click', () => { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true'); liveCount(); }));

// поиск: выпадающие подсказки
function ddOpen(dd, items, pick) {
  if (!items.length) { dd.hidden = true; return; }
  dd.innerHTML = items.map((x, i) => `<button type="button" role="option" data-i="${i}">${x[0]}${x[1] ? `<small>${x[1]}</small>` : ''}</button>`).join('');
  dd.hidden = false; $$('button', dd).forEach(b => b.addEventListener('mousedown', e => { e.preventDefault(); pick(items[b.dataset.i]); dd.hidden = true; }));
}
function ddKeys(inp, dd) {
  inp.addEventListener('keydown', e => {
    const bs = $$('button', dd); if (dd.hidden || !bs.length) return; let i = bs.findIndex(b => b.classList.contains('act'));
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); i = (i + (e.key === 'ArrowDown' ? 1 : -1) + bs.length) % bs.length; bs.forEach((b, k) => b.classList.toggle('act', k === i)); }
    else if (e.key === 'Enter' && i >= 0) { e.preventDefault(); bs[i].dispatchEvent(new MouseEvent('mousedown')); }
    else if (e.key === 'Escape') dd.hidden = true;
  });
  inp.addEventListener('blur', () => setTimeout(() => dd.hidden = true, 120));
}
const pr = $('#pr'), ad = $('#ad');
const cntBy = fn => ITEMS.filter(it => fn(it) && match(it, {...readForm(), max: 0, q: ''})).length;
function prShow() { ddOpen($('#prDD'), [5, 8, 12, 15].map(m => [`до ${m} млн ₽`, `${cntBy(it => it.p <= m * 1e6)} кв.`, m]).concat([['Любая цена', '', '']]), x => { pr.value = x[2]; liveCount(); }); }
pr.addEventListener('focus', prShow); pr.addEventListener('input', () => $('#prDD').hidden = true); ddKeys(pr, $('#prDD'));
const PLACES = [...new Set(ITEMS.map(it => it.d))].map(d => [d, 'район']).concat([...new Set(ITEMS.filter(it => it.zk.startsWith('ЖК')).map(it => it.zk))].map(z => [z, 'жилой комплекс']));
function adShow() {
  const q = ad.value.trim().toLowerCase();
  ddOpen($('#adDD'), PLACES.filter(p => !q || p[0].toLowerCase().includes(q)).slice(0, 7).map(p => [p[0], `${p[1]} · ${cntBy(it => (it.zk + ' ' + it.d).includes(p[0]))} кв.`]), x => { ad.value = x[0]; liveCount(); });
}
ad.addEventListener('focus', adShow); ad.addEventListener('input', adShow); ddKeys(ad, $('#adDD'));

// живая карточка «ЖК проверен»
const ZKS = [...new Set(ITEMS.filter(it => it.zk.startsWith('ЖК')).map(it => it.zk))].map(z => ({z, d: ITEMS.find(it => it.zk === z).d, n: ITEMS.filter(it => it.zk === z).length}));
const ZCHK = ['Разрешение на строительство', 'Проектная декларация, эскроу', 'Прошлые дома сданы в срок', 'Нет банкротных дел'];
let zi = 0, zt = [], zPause = false;
function zShow(i) {
  zt.forEach(clearTimeout); zt = []; zi = (i + ZKS.length) % ZKS.length; const z = ZKS[zi];
  $('#cvName').textContent = z.z; $('#cvSub').textContent = `${z.d} · новостройка`;
  $('#cvList').innerHTML = ZCHK.map(c => `<li><svg><use href="#check"/></svg>${c}</li>`).join('');
  $('#cvDots').innerHTML = ZKS.map((_, k) => `<button type="button" aria-label="${ZKS[k].z}" aria-current="${k === zi}"></button>`).join('');
  $$('#cvDots button').forEach((b, k) => b.addEventListener('click', () => zShow(k)));
  const st = $('#cvSt'), go = $('#cvGo'); st.textContent = 'Проверяем'; st.classList.remove('ok'); go.classList.remove('on');
  go.textContent = `${z.n} ${plural(z.n, 'квартира', 'квартиры', 'квартир')} в этом ЖК`;
  const step = reduce ? 0 : 450;
  $$('#cvList li').forEach((li, k) => zt.push(setTimeout(() => li.classList.add('ok'), step * (k + 1))));
  zt.push(setTimeout(() => { st.textContent = 'Проверен'; st.classList.add('ok'); go.classList.add('on'); }, step * 5));
  zt.push(setTimeout(function nx() { if (zPause) { zt.push(setTimeout(nx, 1500)); return; } zShow(zi + 1); }, step * 5 + 4200));
}
$('#cvGo').addEventListener('click', e => { e.preventDefault(); const z = ZKS[zi].z; applyFilter(ITEMS.filter(it => it.zk === z), z); $('#list').scrollIntoView({behavior: 'smooth'}); });
$('#chipv').addEventListener('mouseenter', () => zPause = true); $('#chipv').addEventListener('mouseleave', () => zPause = false);
zShow(0);

// ремонт: шторка ↔ этапы
const baR = $('#baR');
function baSet(v) { baR.value = v; $('#baBox .after').style.clipPath = `inset(0 0 0 ${v}%)`; $('#baH').style.left = v + '%';
  const k = Math.min(4, Math.floor((100 - v) / 18)); $$('#bSteps li').forEach((li, i) => { li.classList.toggle('cur', i === k); li.classList.toggle('past', i < k); }); }
baR.addEventListener('input', () => baSet(+baR.value));
function baTo(to, ms = 900) { if (reduce) { baSet(to); return; } const from = +baR.value, t0 = performance.now();
  (function f(t) { const k = Math.min(1, (t - t0) / ms), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; baSet(from + (to - from) * e); if (k < 1) requestAnimationFrame(f); })(t0); }
$$('#bSteps button').forEach(b => b.addEventListener('click', () => baTo(+b.dataset.v, 600)));
baSet(50);
new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect(); baTo(92, 700); setTimeout(() => baTo(8, 1600), 750); setTimeout(() => baTo(50, 900), 2500); }, {threshold: .5}).observe($('#baBox'));

// подборки: живое поле точек в «Самые выгодные»
(() => {
  const f = $('.cfield'), N = 42, W = 23; f.innerHTML = '<i></i>'.repeat(N); const ds = $$('i', f);
  if (reduce) { ds.forEach((d, i) => d.classList.toggle('off', i !== W)); ds[W].classList.add('win'); return; }
  function run() {
    ds.forEach(d => d.classList.remove('off', 'win')); const order = ds.map((_, i) => i).filter(i => i !== W).sort(() => Math.random() - .5); let k = 0;
    const t = setInterval(() => { for (let j = 0; j < 3 && k < order.length; j++, k++) ds[order[k]].classList.add('off');
      if (k >= order.length) { clearInterval(t); ds[W].classList.add('win'); setTimeout(run, 2600); } }, 110);
  }
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { run(); o.disconnect(); } }).observe(f);
})();
// промо: точки волной
$$('.pt .dotgrid').forEach(g => { const C = 7, R = 5; g.innerHTML = Array.from({length: C * R}, (_, i) => { const x = i % C, y = Math.floor(i / C); return `<i style="--d:${(C - 1 - x) + (R - 1 - y)}"${(x + y) % 9 === 4 ? ' class="hot"' : ''}></i>`; }).join(''); });
// карта: пересчёт размера, когда список меняет высоту
if (window.ResizeObserver) { let mt; new ResizeObserver(() => { clearTimeout(mt); mt = setTimeout(mapFit, 120); }).observe($('.map')); }

// путь клиента: прорисовка шагов
(() => { const way = $('.way'); if (!way) return; const parts = [...way.children].filter(e => e.matches('.stp,.ln'));
  function play() { parts.forEach(p => p.classList.remove('lit', 'fill')); parts.forEach((p, i) => setTimeout(() => p.classList.add(p.matches('.stp') ? 'lit' : 'fill'), reduce ? 0 : 250 + i * 330)); }
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { play(); o.disconnect(); } }, {threshold: .6}).observe(way);
  way.addEventListener('mouseenter', play); })();

// ипотека: полоса и сравнение программ
const PROGS = PN.progs();
function calcExtra() {
  const P = +$('#cp').value, d = +$('#cd').value, y = +$('#ct').value, sel = progSel(), L = P * (1 - d / 100), n = y * 12, k = kidsOf();
  const pm = p => PN.mort.pay(P, d, y, p, k).pay, over = pm(sel) * n - L;
  $('#cbL').style.width = L / (L + over) * 100 + '%'; $('#cbO').style.width = over / (L + over) * 100 + '%';
  $('#cbLv').textContent = fmtM(L); $('#cbOv').textContent = fmtM(over);
  $('#cprog').innerHTML = PN.mort.cfg.progs.map((p, i) => `<button type="button" data-p="${i}" aria-pressed="${p === sel}"><small>${p.name} · ${String(PN.mort.terms(p, k).rate).replace('.', ',')} %</small><b>${Math.round(pm(p)).toLocaleString('ru-RU')} ₽</b></button>`).join('');
  $$('#cprog button').forEach(b => b.addEventListener('click', () => $(`#rates [data-p="${b.dataset.p}"]`).click()));
}
new MutationObserver(calcExtra).observe($('#loan'), {childList: true, characterData: true, subtree: true});
calcExtra();

// заявка: точки у курсора
(() => { const lead = $('#lead'), lit = $('.lead .dotgrid.lit'); if (!lit || !matchMedia('(hover:hover)').matches) return;
  lead.addEventListener('mousemove', e => { const r = lit.getBoundingClientRect(); lit.style.setProperty('--mx', e.clientX - r.left + 'px'); lit.style.setProperty('--my', e.clientY - r.top + 'px'); });
  lead.addEventListener('mouseleave', () => { lit.style.setProperty('--mx', '-999px'); }); })();

// шторка: тянуть мышью и пальцем по всему фото
(() => { const box = $('#baBox'); if (!box) return; let on = false;
  const at = e => { const r = box.getBoundingClientRect(); baSet(Math.max(0, Math.min(100, (e.clientX - r.left) / r.width * 100))); };
  box.addEventListener('pointerdown', e => { on = true; box.classList.add('drag'); box.setPointerCapture(e.pointerId); at(e); e.preventDefault(); });
  box.addEventListener('pointermove', e => { if (on) at(e); });
  ['pointerup', 'pointercancel'].forEach(t => box.addEventListener(t, () => { on = false; box.classList.remove('drag'); })); })();

// поиск-капсула: панели сегментов и подписи
const sf2 = $('#sf');
function segClose(except) { $$('.sg[data-pop]').forEach(g => { if (g !== except) { g.classList.remove('on'); $('.sgb', g).setAttribute('aria-expanded', 'false'); } }); sf2.classList.toggle('open', !!except); }
$$('.sg[data-pop]').forEach(g => $('.sgb', g).addEventListener('click', e => { e.stopPropagation(); const on = !g.classList.contains('on'); segClose(on ? g : null); g.classList.toggle('on', on); e.currentTarget.setAttribute('aria-expanded', on); }));
$$('.sgi input').forEach(inp => inp.addEventListener('focus', () => segClose(null)));
document.addEventListener('click', e => { if (!e.target.closest('.sg')) segClose(null); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') segClose(null); });
function segLabels() {
  $('#sgType').textContent = ($('.pop .tabs [aria-selected=true]') || {}).textContent || 'Новостройки';
  const r = $$('.sf .chip').filter(c => c.getAttribute('aria-pressed') === 'true').map(c => c.textContent);
  $('#sgRooms').textContent = r.length ? r.join(', ') : 'Любые';
}
$$('.pop .tabs button').forEach(b => b.addEventListener('click', () => { segLabels(); if (b.textContent !== 'Дома') setTimeout(() => segClose(null), 120); }));
$$('.sf .chip').forEach(c => c.addEventListener('click', segLabels));
segLabels();

// панель связи в меню
(() => {
  const ph = $('#hbPh'), pop = $('#hbPop'), cb = $('#hbCb'), inp = $('#hbTel');
  const ekb = () => { const d = new Date(), u = d.getTime() + d.getTimezoneOffset() * 6e4; return new Date(u + 5 * 36e5); };
  function clock() { const t = ekb(), h = t.getHours(), open = h >= 9 && h < 21;
    $('#hbClk').textContent = String(h).padStart(2, '0') + ':' + String(t.getMinutes()).padStart(2, '0');
    $('#hbStatus').textContent = open ? 'на связи' : 'перезвоним с 9:00'; $('#hbDot').classList.toggle('off', !open);
    $('#hbCbNote').textContent = cb.classList.contains('sent') ? $('#hbCbNote').textContent : open ? 'Оставьте номер — менеджер наберёт сам' : 'Сейчас офис закрыт — позвоним в 9:00'; }
  clock(); setInterval(clock, 15000);
  function open(o) { pop.hidden = !o; ph.setAttribute('aria-expanded', o); if (o) setTimeout(() => inp.focus(), 50); }
  ph.addEventListener('click', e => { e.stopPropagation(); open(pop.hidden); });
  pop.addEventListener('click', e => e.stopPropagation());
  document.addEventListener('click', () => open(false));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !pop.hidden) { open(false); ph.focus(); } });
  $$('[data-chat]', pop).forEach(b => b.addEventListener('click', () => open(false)));
  inp.addEventListener('input', () => { cb.classList.remove('bad'); let d = inp.value.replace(/\D/g, ''); if (!d) { inp.value = ''; return; }
    if (/^\s*\+\s*[0-689]/.test(inp.value)) return;   // номер не российский — не переделываем в +7, проверка его отклонит
    if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; const p = d.slice(1, 11);
    inp.value = '+7' + (p.length ? ' (' + p.slice(0, 3) : '') + (p.length > 3 ? ') ' + p.slice(3, 6) : '') + (p.length > 6 ? '-' + p.slice(6, 8) : '') + (p.length > 8 ? '-' + p.slice(8, 10) : ''); });
  cb.addEventListener('submit', e => { e.preventDefault();
    if (!/^\+7/.test(inp.value) || inp.value.replace(/\D/g, '').length !== 11) { cb.classList.add('bad'); inp.focus(); return; }
    if (!$('#hbCc').checked) { $('#hbCcL').classList.add('bad'); $('#hbCc').focus(); return; }
    PN.send({kind: 'callback', phone: inp.value}, () => {
    const h = ekb().getHours(), openNow = h >= 9 && h < 21; cb.classList.add('sent');
    $('#hbCbNote').textContent = openNow ? `Звоним на ${inp.value} — держите телефон рядом` : `Позвоним на ${inp.value} завтра в 9:00`;
    cb.querySelector('b').textContent = openNow ? 'Уже набираем' : 'Заявка принята';
    toast(openNow ? 'Перезвоним в течение 30 секунд' : 'Перезвоним завтра в 9:00'); }); });
})();

// заявка: живое поле точек
(() => {
  const cv = $('#ldots'), sec = $('#lead'); if (!cv) return;
  const ctx = cv.getContext('2d'); let W = 0, H = 0, dpr = 1, pts = [], run = false, raf = 0;
  const m = {x: -9999, y: -9999, tx: -9999, ty: -9999, on: 0, ton: 0};
  const ss = (a, b, x) => { const t = Math.max(0, Math.min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  function build() {
    const r = sec.getBoundingClientRect(); dpr = Math.min(2, devicePixelRatio || 1); W = r.width; H = r.height;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const step = W < 800 ? 18 : 24, mob = W < 800; pts = [];
    for (let y = step / 2; y < H; y += step) for (let x = step / 2; x < W; x += step) {
      const g = mob ? ss(.5, .95, y / H) * (.55 + .45 * ss(0, 1, x / W)) : ss(.34, .86, x / W);
      pts.push([x, y, g]);
    }
    draw(performance.now());
  }
  function draw(t) {
    ctx.clearRect(0, 0, W, H);
    m.x += (m.tx - m.x) * .14; m.y += (m.ty - m.y) * .14; m.on += (m.ton - m.on) * .08;
    const R = Math.max(140, Math.min(220, W * .11)), wave = reduce ? 0 : t / 1600;
    for (const [x, y, g] of pts) {
      const dx = x - m.x, dy = y - m.y, k = Math.exp(-(dx * dx + dy * dy) / (R * R)) * m.on * (W < 800 ? 1 : .3 + .7 * ss(.22, .5, x / W));
      const w = reduce ? 0 : (Math.sin(wave + x * .012 + y * .018) + 1) * .5 * .25 * g;
      const a = Math.min(.9, .06 + .34 * g + w * .3 + .5 * k), rad = (W < 800 ? .6 + 1.6 * g : .9 + 2.5 * g) + 2.6 * k;
      if (a < .03 || rad < .6) continue;
      ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(x, y, rad, 0, 6.2832); ctx.fillStyle = '#fff'; ctx.fill();
    }
    ctx.globalAlpha = 1;
    if (run) raf = requestAnimationFrame(draw);
  }
  function start() { if (run) return; run = true; raf = requestAnimationFrame(draw); }
  function stop() { run = false; cancelAnimationFrame(raf); }
  sec.addEventListener('pointermove', e => { const r = sec.getBoundingClientRect(); m.tx = e.clientX - r.left; m.ty = e.clientY - r.top; if (m.x < -9000) { m.x = m.tx; m.y = m.ty; } m.ton = 1; });
  sec.addEventListener('pointerleave', () => { m.ton = 0; });
  new IntersectionObserver(es => { es[0].isIntersecting ? (reduce ? draw(0) : start()) : stop(); }).observe(sec);
  new ResizeObserver(build).observe(sec); build();
})();

// поиск: статус, сканер, перекат счётчика
(() => {
  const n = $('#goN'), btn = $('.go3'), line = $('.sbox3 .sline'); let last = n.textContent, t;
  const tm = new Date(); tm.setMinutes(tm.getMinutes() - 7);
  const hhmm = `${String(tm.getHours()).padStart(2, '0')}:${String(tm.getMinutes()).padStart(2, '0')}`;
  function upd() {
    const v = +n.textContent || 0;
    $('#goL').textContent = plural(v, 'квартира', 'квартиры', 'квартир');
    $('#sStat').innerHTML = `<span class="lg">обновлено в ${hhmm} · </span>подходит <b>${v}</b> из 144<span class="lg"> проверенных</span>`;
    if (n.textContent !== last) { last = n.textContent;
      [n, btn, line].forEach(el => el.classList.remove('roll', 'sweep', 'scan')); void n.offsetWidth;
      n.classList.add('roll'); btn.classList.add('sweep'); line.classList.add('scan'); }
  }
  new MutationObserver(upd).observe(n, {childList: true, characterData: true, subtree: true});
  upd();
})();

// мобильное меню: капсула снизу и полноэкранная навигация
(() => {
  const tb = $('#tabbar'), mn = $('#mnav'), mb = $('#mnBtn'); let lastY = scrollY;
  addEventListener('scroll', () => { const y = scrollY, d = y - lastY;
    if (Math.abs(d) > 6) { tb.classList.toggle('hide', d > 0 && y > 300); lastY = y; } }, {passive: true});
  const links = $$('a[data-sec]', tb);
  const spy = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) links.forEach(a => a.classList.toggle('on', a.dataset.sec === e.target.id)); }), {rootMargin: '-45% 0px -50% 0px'});
  links.forEach(a => { const t = document.getElementById(a.dataset.sec); if (t) spy.observe(t); });
  $('[data-map]', tb).addEventListener('click', () => { if (innerWidth <= 800 && !$('.res').classList.contains('showmap')) $('#mapBtn').click(); });
  function openMn(o) { mn.hidden = !o; mb.setAttribute('aria-expanded', o); document.documentElement.classList.toggle('mn-lock', o);
    if (o) { const st = $('#hbStatus'); $('#mnSt').textContent = st ? st.textContent : 'на связи'; $('#mnX').focus(); } else mb.focus(); }
  mb.addEventListener('click', () => openMn(true)); $('#mnX').addEventListener('click', () => openMn(false));
  $$('.mn-l a, .mn-c [data-chat], .mn-cab', mn).forEach(a => a.addEventListener('click', () => openMn(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !mn.hidden) openMn(false); });
})();
// «Квартира. Дом. Ремонт.»: на сенсорных экранах фото ремонта само переключается «до → после»; «Один менеджер на всё» открывает заявку с пакетом «квартира + ремонт».
(() => {
  const pba = document.querySelector('[data-pba]');
  if (pba && matchMedia('(hover: none)').matches && !matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
    let t = null;
    new IntersectionObserver(([e]) => {
      clearInterval(t);
      if (e.isIntersecting) { pba.classList.add('is-after'); t = setInterval(() => pba.classList.toggle('is-after'), 2800); }
    }, {threshold: .5}).observe(pba);
  }
  const pack = document.querySelector('[data-pack]'), form = document.getElementById('leadForm');
  if (pack && form) pack.addEventListener('click', () => {
    form.dataset.pack = '1';
    const flat = form.querySelector('[data-q="flat"]'); if (flat && flat.getAttribute('aria-pressed') !== 'true') flat.click();
    const lg = form.querySelector('fieldset[data-s="1"] legend'); if (lg && !lg.querySelector('.qpack')) lg.insertAdjacentHTML('beforeend', ' <span class="qpack">· квартира + ремонт</span>');
  });
})();
