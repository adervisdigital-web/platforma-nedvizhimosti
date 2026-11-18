// Каталог и страница ЖК: фильтры (сохраняются в адресе), сортировка, «Показать ещё», вид «На карте».
(() => {
  const $ = (q, r = document) => r.querySelector(q), $$ = (q, r = document) => [...r.querySelectorAll(q)];
  const list = $('[data-ct-list]'); if (!list) return;
  const form = $('[data-ct-form]'), sortSel = $('[data-ct-sort]'), cntEl = $('[data-ct-count]');
  const moreWrap = $('[data-ct-more-wrap]'), moreBtn = $('[data-ct-more]'), empty = $('[data-ct-empty]'), map = $('[data-ct-map]');
  const cards = $$('.ct-card', list), STEP = 12;
  let shown = STEP, view = 'list', lmap = null, layer = null;
  // «6» или «6,5» в поле цены — это миллионы; «6 500 000» — рубли
  const price = v => { v = String(v || '').replace(/\s/g, '').replace(',', '.').replace(/[^\d.]/g, ''); if (!v) return null; const n = +v; return n < 1000 ? n * 1e6 : n; };
  const dec = v => { v = String(v || '').replace(',', '.').replace(/[^\d.]/g, ''); return v ? +v : null; };
  const params = new URLSearchParams(location.search);

  if (form) {   // из адреса — в поля
    for (const el of form.elements) {
      if (!el.name || !params.has(el.name)) continue;
      el.type === 'checkbox' ? (el.checked = params.get(el.name) === '1') : (el.value = params.get(el.name));
    }
  }
  if (sortSel && params.has('sort')) sortSel.value = params.get('sort');
  if (params.get('view') === 'map') view = 'map';

  const crit = () => {
    if (!form) return {};
    const f = form.elements, g = n => f[n] ? f[n].value : '';
    return {pmin: price(g('pmin')), pmax: price(g('pmax')), amin: dec(g('amin')), d: g('d'), z: g('z'), fin: f.fin && f.fin.checked, ready: f.ready && f.ready.checked};
  };
  const match = (c, k) => {
    const d = c.dataset;
    return !(k.pmin && +d.p < k.pmin || k.pmax && +d.p > k.pmax || k.amin && +d.a < k.amin || k.d && d.d !== k.d || k.z && d.z !== k.z
      || k.fin && d.f !== '1' || k.ready && d.ready !== '1');
  };
  const sorters = {p: (a, b) => a.dataset.p - b.dataset.p, '-p': (a, b) => b.dataset.p - a.dataset.p, ppm: (a, b) => a.dataset.ppm - b.dataset.ppm,
    '-a': (a, b) => b.dataset.a - a.dataset.a, '': (a, b) => a.dataset.i - b.dataset.i};

  const syncUrl = () => {
    const q = new URLSearchParams();
    if (form) for (const el of form.elements) {
      if (!el.name) continue;
      if (el.type === 'checkbox') { if (el.checked) q.set(el.name, '1'); } else if (el.value.trim()) q.set(el.name, el.value.trim());
    }
    if (sortSel && sortSel.value) q.set('sort', sortSel.value);
    if (view === 'map') q.set('view', 'map');
    const s = q.toString();
    history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + location.hash);
    const has = [...q.keys()].some(k => k !== 'view' && k !== 'sort');
    $$('[data-ct-reset]').forEach(b => { if (!b.closest('[data-ct-empty]')) b.hidden = !has; });
  };

  const apply = (reset = true) => {
    if (reset) shown = STEP;
    const k = crit(), ok = cards.filter(c => match(c, k));
    ok.sort(sorters[sortSel ? sortSel.value : ''] || sorters['']).forEach(c => list.append(c));
    cards.forEach(c => { c.hidden = !ok.includes(c); c.classList.remove('ct-off'); });
    ok.forEach((c, i) => c.classList.toggle('ct-off', view === 'list' && i >= shown));
    if (cntEl) cntEl.textContent = ok.length;
    if (empty) empty.hidden = ok.length > 0;
    if (moreWrap) {
      const rest = ok.length - shown;
      moreWrap.hidden = view !== 'list' || rest <= 0;
      if (rest > 0) moreBtn.textContent = `Показать ещё ${Math.min(STEP, rest)} из ${rest}`;
    }
    list.hidden = view !== 'list';
    if (map) { map.hidden = view !== 'map'; if (view === 'map') drawMap(ok); }
    syncUrl();
  };

  // ---- карта: точки по ЖК / району, в подсказке — квартиры точки
  const drawMap = ok => {
    if (!window.L) {
      if (!document.getElementById('leafletJs')) { const sc = document.createElement('script'); sc.id = 'leafletJs'; sc.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'; document.head.append(sc); }
      return setTimeout(() => drawMap(ok), 200);
    }
    if (!lmap) {
      lmap = L.map(map, {scrollWheelZoom: false}).setView([56.84, 60.6], 11);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18, attribution: '© OpenStreetMap'}).addTo(lmap);
    }
    setTimeout(() => lmap.invalidateSize(), 50);
    if (layer) layer.remove();
    layer = L.layerGroup().addTo(lmap);
    const groups = {};
    ok.forEach(c => { if (c.dataset.lat) (groups[c.dataset.lat + ',' + c.dataset.lng] ||= []).push(c); });
    const pts = [];
    Object.entries(groups).forEach(([ll, cs]) => {
      const p = ll.split(',').map(Number); pts.push(p);
      const min = Math.min(...cs.map(c => +c.dataset.p));
      const html = '<div class="ct-pop">' + cs.map(c => { const a = $('h3 a', c); return `<a href="${a.getAttribute('href')}"><b>${a.textContent}</b><span>${$('.ct-price b', c).textContent}</span></a>`; }).join('') + '</div>';
      L.marker(p, {icon: L.divIcon({className: 'ct-pin', html: `<span>${cs.length > 1 ? cs.length + ' кв. · от ' : ''}${(min / 1e6).toFixed(1).replace('.', ',')} млн</span>`, iconSize: null})})
        .bindPopup(html, {maxWidth: 280}).addTo(layer);
    });
    if (pts.length) lmap.fitBounds(pts, {padding: [50, 50], maxZoom: 14});
  };

  if (form) { form.addEventListener('input', () => apply()); form.addEventListener('change', () => apply()); }
  if (sortSel) sortSel.addEventListener('change', () => apply(false));
  if (moreBtn) moreBtn.addEventListener('click', () => { shown += STEP; apply(false); });
  $$('[data-ct-reset]').forEach(b => b.addEventListener('click', () => { if (form) form.reset(); if (sortSel) sortSel.value = ''; apply(); }));
  $$('[data-view]').forEach(b => b.addEventListener('click', () => {
    view = b.dataset.view; $$('[data-view]').forEach(x => x.setAttribute('aria-pressed', x === b)); apply(false);
  }));
  $$('[data-view]').forEach(x => x.setAttribute('aria-pressed', x.dataset.view === view));
  apply(false);
})();
