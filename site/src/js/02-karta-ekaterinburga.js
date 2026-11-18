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
const rateOf = it => it.t === 'new' ? 6 : 20;
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
  $$('#rates button').forEach(x => x.setAttribute('aria-pressed', +x.dataset.r === rateOf(it))); calc();
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

