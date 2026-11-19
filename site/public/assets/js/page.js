// Страницы квартиры и дома: галерея (вкладки, стрелки, миниатюры, свайп), просмотр на весь экран, калькуляторы, карта, «Поделиться».
(() => {
  const $ = (q, r = document) => r.querySelector(q), $$ = (q, r = document) => [...r.querySelectorAll(q)];
  const rub = n => Math.round(n).toLocaleString('ru-RU').replace(/,/g, ' ') + ' ₽';
  const plural = (n, a, b, c) => { const m = n % 10, h = n % 100; return m === 1 && h !== 11 ? a : m >= 2 && m <= 4 && (h < 12 || h > 14) ? b : c; };

  // ---- просмотр на весь экран
  const lb = document.createElement('div');
  lb.className = 'lb'; lb.hidden = true; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Просмотр');
  lb.innerHTML = '<img alt=""><button type="button" class="lb-x" aria-label="Закрыть">×</button>'
    + '<button type="button" class="lb-n prev" aria-label="Назад">‹</button><button type="button" class="lb-n next" aria-label="Вперёд">›</button><span class="lb-c"></span>';
  document.body.append(lb);
  let set = [], at = 0, back = null;
  const show = () => {
    const im = set[at]; $('img', lb).src = im.currentSrc || im.src; $('img', lb).alt = im.alt;
    lb.classList.toggle('lb-pl', !!im.closest('[data-pane="pl"], .ob-planbig'));
    $('.lb-c', lb).textContent = set.length > 1 ? `${at + 1} / ${set.length}` : '';
    $$('.lb-n', lb).forEach(b => b.hidden = set.length < 2);
  };
  const open = (list, i) => { set = list; at = i; back = document.activeElement; show(); lb.hidden = false; document.documentElement.classList.add('lb-on'); $('.lb-x', lb).focus(); };
  const close = () => { lb.hidden = true; document.documentElement.classList.remove('lb-on'); back && back.focus(); };
  const step = d => { at = (at + d + set.length) % set.length; show(); };
  lb.addEventListener('click', e => {
    if (e.target.closest('.lb-x') || e.target === lb) close();
    else if (e.target.closest('.prev')) step(-1); else if (e.target.closest('.next')) step(1);
  });
  addEventListener('keydown', e => {
    if (lb.hidden) return;
    if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') step(-1); if (e.key === 'ArrowRight') step(1);
  });
  let sx = null;
  lb.addEventListener('touchstart', e => sx = e.touches[0].clientX, {passive: true});
  lb.addEventListener('touchend', e => { if (sx !== null) { const d = e.changedTouches[0].clientX - sx; if (Math.abs(d) > 40) step(d < 0 ? 1 : -1); } sx = null; });

  // ---- галерея
  $$('[data-gal]').forEach(g => {
    const slides = $$('.ob-slide', g), thumbs = $$('.ob-thumbs button', g), cnt = $('.ob-count b', g);
    const photos = slides.map(s => $('img', s));
    const plans = $$('.ob-plan img', document).concat([]);
    let cur = 0;
    const go = i => {
      cur = (i + slides.length) % slides.length;
      slides.forEach((s, k) => s.classList.toggle('is-cur', k === cur));
      thumbs.forEach((t, k) => t.classList.toggle('is-cur', k === cur));
      if (cnt) cnt.textContent = cur + 1;
      thumbs[cur] && thumbs[cur].scrollIntoView({block: 'nearest', inline: 'center', behavior: 'smooth'});
    };
    g.addEventListener('click', e => {
      const t = e.target.closest('button'); if (!t) return;
      if (t.dataset.step) go(cur + +t.dataset.step);
      else if (t.dataset.go) go(+t.dataset.go);
      else if (t.classList.contains('ob-slide')) open(photos, cur);
      else if (t.dataset.tab) {
        $$('[data-tab]', g).forEach(b => b.setAttribute('aria-selected', b === t));
        $$('[data-pane]', g).forEach(p => p.hidden = p.dataset.pane !== t.dataset.tab);
      } else if (t.dataset.fl) {
        $$('[data-fl]', g).forEach(b => b.classList.toggle('is-cur', b === t));
        $$('[data-flp]', g).forEach(p => p.hidden = p.dataset.flp !== t.dataset.fl);
      } else if (t.dataset.plan) open(plans, +t.dataset.plan);
    });
    const st = $('.ob-stage', g); let x0 = null;
    st && st.addEventListener('touchstart', e => x0 = e.touches[0].clientX, {passive: true});
    st && st.addEventListener('touchend', e => { if (x0 !== null) { const d = e.changedTouches[0].clientX - x0; if (Math.abs(d) > 40) go(cur + (d < 0 ? 1 : -1)); } x0 = null; });
  });
  // планировки вне галереи («Открыть крупно» в разделе)
  document.addEventListener('click', e => {
    const b = e.target.closest('.ob-planbig'); if (!b) return;
    open($$('.ob-plan img'), +b.dataset.plan || 0);
  });

  // ---- ипотека
  $$('[data-mort]').forEach(c => {
    const o = n => $(`[data-o="${n}"]`, c), i = n => $(`[data-i="${n}"]`, c);
    // программы с лимитами и ступенями семейной (как app/mortgage.php и PN.mort в data.js)
    const cfg = Object.assign({progs: [], tiers: [], market: 20}, JSON.parse(c.dataset.mcfg || '{}'));
    let pi = +(($('[aria-checked="true"]', c) || {dataset: {pi: 0}}).dataset.pi), kids = 1;
    const ann = (L, r, n) => L <= 0 ? 0 : r > 0 ? L * (r / 1200) / (1 - Math.pow(1 + r / 1200, -n)) : L / n;
    const terms = p => {
      if (p && p.family && cfg.tiers.length) { let t = null; cfg.tiers.forEach(x => { if (x.kids <= kids && (!t || x.kids > t.kids)) t = x; }); if (t) return {rate: +t.rate, limit: t.limit}; }
      return {rate: +(p ? p.rate : cfg.market), limit: p && p.limit || null};
    };
    const pct = r => String(r).replace('.', ',') + ' %';
    const pin = i('price');   // на странице ипотеки цену вводят сами: «6» или «6,5» — миллионы
    const getPrice = () => {
      if (!pin) return +c.dataset.price;
      const v = pin.value.replace(/\s/g, '').replace(',', '.').replace(/[^\d.]/g, ''); const n = +v || 0;
      return n && n < 1000 ? n * 1e6 : n;
    };
    if (pin) pin.addEventListener('blur', () => { const p = getPrice(); if (p) pin.value = Math.round(p).toLocaleString('ru-RU').replace(/,/g, ' '); });
    const calc = () => {
      const price = getPrice();
      const dp = +i('down').value, yrs = +i('term').value, L = price * (1 - dp / 100), n = yrs * 12, p = cfg.progs[pi], t = terms(p);
      const parts = t.limit && L > t.limit ? [[t.limit, t.rate], [L - t.limit, +cfg.market]] : [[L, t.rate]];
      const pay = parts.reduce((s, [a, r]) => s + ann(a, r, n), 0);
      const kb = $('[data-kids]', c); if (kb) kb.hidden = !(p && p.family);
      if (o('parts')) o('parts').textContent = parts.length > 1
        ? `${rub(parts[0][0])} под ${pct(parts[0][1])} + ${rub(parts[1][0])} под ${pct(parts[1][1])}: сверх лимита программы банк даёт по рыночной ставке.`
        : `${p ? p.name : 'Ставка'}: ${pct(t.rate)} на всю сумму.`;
      o('down').textContent = `${rub(price * dp / 100)} · ${dp} %`; o('term').textContent = `${yrs} ${plural(yrs, 'год', 'года', 'лет')}`;
      o('pay').textContent = rub(pay); o('loan').textContent = rub(L); o('over').textContent = rub(Math.max(0, pay * n - L)); o('inc').textContent = rub(pay * 2);
      $$('input[type=range]', c).forEach(r => r.style.setProperty('--p', (r.value - r.min) / (r.max - r.min) * 100 + '%'));
    };
    c.addEventListener('input', calc);
    c.addEventListener('click', e => {
      const b = e.target.closest('[data-pi]'), k = e.target.closest('[data-k]');
      if (b) { $$('[data-pi]', c).forEach(x => x.setAttribute('aria-checked', x === b)); pi = +b.dataset.pi; calc(); }
      if (k) { $$('[data-k]', c).forEach(x => x.setAttribute('aria-pressed', x === k)); kids = +k.dataset.k; calc(); }
    });
    calc();
  });
  // ---- рассрочка дома (0 %)
  $$('[data-inst]').forEach(c => {
    const price = +c.dataset.price, o = n => $(`[data-o="${n}"]`, c), i = n => $(`[data-i="${n}"]`, c);
    const calc = () => {
      const dp = +i('down').value, yrs = +i('term').value, rest = price * (1 - dp / 100);
      o('down').textContent = `${rub(price * dp / 100)} · ${dp} %`; o('term').textContent = `${yrs} ${plural(yrs, 'год', 'года', 'лет')}`;
      o('pay').textContent = rub(rest / (yrs * 12)); o('rest').textContent = rub(rest);
      $$('input[type=range]', c).forEach(r => r.style.setProperty('--p', (r.value - r.min) / (r.max - r.min) * 100 + '%'));
    };
    c.addEventListener('input', calc); calc();
  });
  // ---- ремонт: площадь × цена уровня
  $$('[data-ren]').forEach(c => {
    const prices = JSON.parse(c.dataset.prices || '[]'), o = n => $(`[data-o="${n}"]`, c), inp = $('[data-i="area"]', c);
    let lv = +(($('[aria-checked="true"]', c) || {dataset: {lv: 1}}).dataset.lv);
    const calc = () => {
      const a = +inp.value, p = prices[lv] || 0;
      o('area').textContent = a + ' м²'; o('sum').textContent = rub(a * p); o('ppm').textContent = rub(p);
      inp.style.setProperty('--p', (inp.value - inp.min) / (inp.max - inp.min) * 100 + '%');
    };
    c.addEventListener('input', calc);
    c.addEventListener('click', e => { const b = e.target.closest('[data-lv]'); if (!b) return;
      $$('[data-lv]', c).forEach(x => x.setAttribute('aria-checked', x === b)); lv = +b.dataset.lv; calc(); });
    calc();
  });

  // ---- шторка «до / после»: тянуть мышью или пальцем по всему фото, стрелками — с клавиатуры; при первом показе проходит сама
  $$('[data-cur]').forEach(c => {
    const r = $('input', c), set = v => { v = Math.max(0, Math.min(100, v)); c.style.setProperty('--p', v + '%'); r.value = v; };
    const at = e => { const b = c.getBoundingClientRect(); set((e.clientX - b.left) / b.width * 100); };
    let drag = false;
    c.addEventListener('pointerdown', e => { drag = true; c.setPointerCapture(e.pointerId); at(e); c.classList.add('is-drag'); });
    c.addEventListener('pointermove', e => { if (drag) at(e); });
    const end = () => { drag = false; c.classList.remove('is-drag'); };
    c.addEventListener('pointerup', end); c.addEventListener('pointercancel', end);
    r.addEventListener('input', () => set(+r.value));
    if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
    new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect();
      const t0 = performance.now(), ease = x => (1 - Math.cos(x * Math.PI)) / 2;
      const path = t => t < .3 ? 50 - 32 * ease(t / .3) : t < .75 ? 18 + 64 * ease((t - .3) / .45) : 82 - 32 * ease((t - .75) / .25);
      const run = now => { if (drag) return; const t = Math.min(1, (now - t0) / 2800); set(path(t)); if (t < 1) requestAnimationFrame(run); };
      setTimeout(() => requestAnimationFrame(run), 300); }, {threshold: .5}).observe(c);
  });

  // ---- поделиться
  document.addEventListener('click', async e => {
    const b = e.target.closest('[data-share]'); if (!b) return;
    const url = location.href.split('#')[0];
    try {
      if (navigator.share) await navigator.share({title: document.title, url});
      else { await navigator.clipboard.writeText(url); const t = b.lastChild.textContent; b.lastChild.textContent = 'Ссылка скопирована'; setTimeout(() => b.lastChild.textContent = t, 1800); }
    } catch (_) {}
  });

  // ---- карта (Leaflet + OpenStreetMap, обесцвеченная, красная точка)
  const m = $('[data-map]');
  if (m) {
    const init = () => {   // Leaflet подгружается только здесь — не задерживает галерею и калькуляторы
      if (!window.L) {
        if (!document.getElementById('leafletJs')) { const sc = document.createElement('script'); sc.id = 'leafletJs'; sc.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'; document.head.append(sc); }
        return setTimeout(init, 200);
      }
      const ll = [+m.dataset.lat, +m.dataset.lng];
      const map = L.map(m, {scrollWheelZoom: false, attributionControl: true, zoomControl: true}).setView(ll, 14);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18, attribution: '© OpenStreetMap'}).addTo(map);
      L.marker(ll, {icon: L.divIcon({className: 'ob-pin', html: '<i></i>', iconSize: [28, 28], iconAnchor: [14, 14]}), title: m.dataset.title}).addTo(map);
    };
    'IntersectionObserver' in window ? new IntersectionObserver((es, ob) => { if (es[0].isIntersecting) { ob.disconnect(); init(); } }, {rootMargin: '300px'}).observe(m) : init();
  }
})();
