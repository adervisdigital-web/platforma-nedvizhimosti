// Каталог и страница ЖК: фильтры (сохраняются в адресе), сортировка, «Показать ещё», вид «На карте».
(() => {
  const $ = (q, r = document) => r.querySelector(q), $$ = (q, r = document) => [...r.querySelectorAll(q)];
  // ---- проекты домов: фильтр по линейке и этажности
  const dm = $$('.dm-card');
  if (dm.length) {
    let line = '', fl = '';
    const apply = () => {
      let n = 0;
      dm.forEach(c => { const ok = (!line || c.dataset.l === line) && (!fl || c.dataset.fl === fl); c.hidden = !ok; n += ok; });
      $('[data-dm-empty]').hidden = n > 0;
      $$('[data-line]').forEach(b => b.setAttribute('aria-pressed', b.dataset.line === line));
      $$('.dm-f [data-fl]').forEach(b => b.setAttribute('aria-pressed', b.dataset.fl === fl));
    };
    $$('[data-line]').forEach(b => b.addEventListener('click', () => { line = b.dataset.line; apply(); }));
    $$('.dm-f [data-fl]').forEach(b => b.addEventListener('click', () => { fl = fl === b.dataset.fl ? '' : b.dataset.fl; apply(); }));
  }
  const list = $('[data-ct-list]'); if (!list) return;
  const form = $('[data-ct-form]'), sortSel = $('[data-ct-sort]'), cntEl = $('[data-ct-count]');
  const moreWrap = $('[data-ct-more-wrap]'), moreBtn = $('[data-ct-more]'), empty = $('[data-ct-empty]'), map = $('[data-ct-map]');
  const cards = $$('.ct-card', list), STEP = 12;
  let shown = STEP, view = 'list', lmap = null, layer = null;
  // Серверный режим (больше 200 квартир): фильтр, сортировка, «Показать ещё» и карта — запросами ?part=cards|map, в странице только 24 карточки.
  const SERVER = list.dataset.ctServer === '1', SSTEP = +(list.dataset.ctStep || 24);
  let sTotal = +(list.dataset.ctTotal || 0), sNext = sTotal > SSTEP ? SSTEP : null, sReq = 0, sTimer = 0;
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
    return q;
  };

  const sState = () => {
    if (cntEl) cntEl.textContent = sTotal;
    if (empty) empty.hidden = sTotal > 0;
    const rest = sTotal - list.children.length;
    if (moreWrap) { moreWrap.hidden = view !== 'list' || sNext === null; if (sNext !== null) moreBtn.textContent = `Показать ещё ${Math.min(SSTEP, rest)} из ${rest}`; }
    list.hidden = view !== 'list';
  };
  const sLoad = async (part, offset = 0) => {
    const q = syncUrl(); q.delete('view'); q.set('part', part); if (part === 'cards') q.set('offset', offset);
    const my = ++sReq; list.setAttribute('aria-busy', 'true'); if (moreBtn) moreBtn.disabled = true;
    try {
      const r = await fetch(location.pathname + '?' + q, {headers: {Accept: 'application/json'}});
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const d = await r.json(); if (my !== sReq) return null;
      return d;
    } catch (e) {
      if (my === sReq && window.toast) toast('Не удалось загрузить квартиры — проверьте интернет и попробуйте ещё раз');
      return null;
    } finally { if (my === sReq) { list.removeAttribute('aria-busy'); if (moreBtn) moreBtn.disabled = false; } }
  };
  const sCards = async (append) => {
    const d = await sLoad('cards', append ? sNext : 0); if (!d) return;
    if (append) list.insertAdjacentHTML('beforeend', d.html); else list.innerHTML = d.html;
    sTotal = d.total; sNext = d.next; sState();
    document.dispatchEvent(new Event('pn:cards'));                 // отметки «избранное»/«сравнить» на новых карточках
  };
  const sMap = async () => {
    const d = await sLoad('map'); if (!d) return;
    sTotal = d.total; sState(); if (map) { map.hidden = false; drawMap(null, d.groups); }
  };
  const sApply = (now = false) => {
    syncUrl(); clearTimeout(sTimer);
    const go = () => (view === 'map' ? sMap() : (map && (map.hidden = true), sCards(false)));
    now ? go() : (sTimer = setTimeout(go, 280));
  };

  const apply = (reset = true) => {
    if (SERVER) return sApply();
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
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const drawMap = (ok, groups) => {
    if (!window.L) {
      if (!document.getElementById('leafletJs')) { const sc = document.createElement('script'); sc.id = 'leafletJs'; sc.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'; document.head.append(sc); }
      return setTimeout(() => drawMap(ok, groups), 200);
    }
    if (!lmap) {
      lmap = L.map(map, {scrollWheelZoom: false}).setView([56.84, 60.6], 11);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18, attribution: '© OpenStreetMap'}).addTo(lmap);
    }
    setTimeout(() => lmap.invalidateSize(), 50);
    if (layer) layer.remove();
    layer = L.layerGroup().addTo(lmap);
    const pts = [];
    if (groups) {
      groups.forEach(g => {
        const p = [g.lat, g.lng]; pts.push(p);
        const more = g.n > g.items.length ? `<p class="ct-pop-more">и ещё ${g.n - g.items.length} — уточните фильтры</p>` : '';
        const html = '<div class="ct-pop">' + g.items.map(i => `<a href="${esc(i.href)}"><b>${esc(i.t)}</b><span>${esc(i.p)}</span></a>`).join('') + more + '</div>';
        L.marker(p, {icon: L.divIcon({className: 'ct-pin', html: `<span>${g.n > 1 ? g.n + ' кв. · от ' : ''}${(g.min / 1e6).toFixed(1).replace('.', ',')} млн</span>`, iconSize: null})})
          .bindPopup(html, {maxWidth: 280}).addTo(layer);
      });
      if (pts.length) lmap.fitBounds(pts, {padding: [50, 50], maxZoom: 14});
      return;
    }
    const groups2 = {};
    ok.forEach(c => { if (c.dataset.lat) (groups2[c.dataset.lat + ',' + c.dataset.lng] ||= []).push(c); });
    Object.entries(groups2).forEach(([ll, cs]) => {
      const p = ll.split(',').map(Number); pts.push(p);
      const min = Math.min(...cs.map(c => +c.dataset.p));
      const html = '<div class="ct-pop">' + cs.map(c => { const a = $('h3 a', c); return `<a href="${a.getAttribute('href')}"><b>${a.textContent}</b><span>${$('.ct-price b', c).textContent}</span></a>`; }).join('') + '</div>';
      L.marker(p, {icon: L.divIcon({className: 'ct-pin', html: `<span>${cs.length > 1 ? cs.length + ' кв. · от ' : ''}${(min / 1e6).toFixed(1).replace('.', ',')} млн</span>`, iconSize: null})})
        .bindPopup(html, {maxWidth: 280}).addTo(layer);
    });
    if (pts.length) lmap.fitBounds(pts, {padding: [50, 50], maxZoom: 14});
  };

  if (form) { form.addEventListener('input', () => apply()); form.addEventListener('change', () => apply()); }
  // телефон: фильтры свёрнуты в кнопку «Фильтры», на ней — сколько условий включено
  const ftog = $('[data-ct-ftog]'), fn = $('[data-ct-fn]');
  if (ftog && form) {
    const fcount = () => { let n = 0; for (const el of form.elements) if (el.name && (el.type === 'checkbox' ? el.checked : el.value.trim())) n++;
      fn.textContent = n; fn.hidden = !n; };
    ftog.addEventListener('click', () => { const o = !form.classList.contains('is-open'); form.classList.toggle('is-open', o); ftog.setAttribute('aria-expanded', o);
      if (o) { const f = form.querySelector('input, select'); f && setTimeout(() => f.focus({preventScroll: true}), 60); } });
    form.addEventListener('input', fcount); form.addEventListener('change', fcount);
    $('[data-ct-reset]') && $('[data-ct-reset]').addEventListener('click', () => setTimeout(fcount, 0));
    fcount();
  }
  if (sortSel) sortSel.addEventListener('change', () => apply(false));
  if (moreBtn) moreBtn.addEventListener('click', () => { if (SERVER) { if (sNext !== null) sCards(true); return; } shown += STEP; apply(false); });
  $$('[data-ct-reset]').forEach(b => b.addEventListener('click', () => {
    if (form) { form.reset(); $$('[data-ct-extra]', form).forEach(x => x.remove()); }       // фильтры, пришедшие с главной, — тоже
    if (sortSel) sortSel.value = ''; apply();
  }));
  $$('[data-view]').forEach(b => b.addEventListener('click', () => {
    view = b.dataset.view; $$('[data-view]').forEach(x => x.setAttribute('aria-pressed', x === b)); SERVER ? sApply(true) : apply(false);
  }));
  $$('[data-view]').forEach(x => x.setAttribute('aria-pressed', x.dataset.view === view));
  if (SERVER) { syncUrl(); sState(); if (view === 'map') sApply(true); }   // первая страница уже отфильтрована сервером
  else apply(false);
})();
