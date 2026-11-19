// Эффекты для ПК с мышью: курсор-точка, плавная прокрутка колесом, появление заголовков с падающей точкой.
// Ничего не включается на сенсорных экранах, при «уменьшить движение» и в режиме снимков (?shot).
(() => {
  const html = document.documentElement;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (/[?&]shot\b/.test(location.search) || reduce) return;

  // ---- заголовки разделов: всплывают, точка в конце «падает» (на всех устройствах)
  const heads = [...document.querySelectorAll('main h2, section h2, .pg-m h1')].filter(h => !h.closest('dialog, .dlg, .lb, header, .hero'));
  if ('IntersectionObserver' in window && heads.length) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('fx-in'); io.unobserve(e.target); }
    }), {rootMargin: '0px 0px -12% 0px'});
    heads.forEach(h => {
      if (h.getBoundingClientRect().top < innerHeight * .9) return;   // уже на экране при загрузке — не прячем
      h.classList.add('fx-rv'); io.observe(h);
    });
  }

  if (!fine) return;

  // ---- курсор-точка
  const dot = document.createElement('div'), ring = document.createElement('div');
  dot.className = 'fx-dot'; ring.className = 'fx-ring'; ring.innerHTML = '<span></span>';
  dot.setAttribute('aria-hidden', 'true'); ring.setAttribute('aria-hidden', 'true');
  document.body.append(ring, dot);
  html.classList.add('fx-cur');
  const label = ring.firstChild;
  let mx = -100, my = -100, rx = -100, ry = -100, dx = -100, dy = -100, shown = false, mode = '';
  const NATIVE = 'input:not([type=range]):not([type=checkbox]):not([type=radio]):not([type=button]):not([type=submit]), textarea, select, [contenteditable], .leaflet-container, iframe';
  const HOT = 'a, button, [role=button], label, summary, input[type=range], input[type=checkbox], input[type=radio], [data-open], [tabindex]:not([tabindex="-1"])';
  const setMode = (m, txt = '') => {
    if (m === mode && label.textContent === txt) return;
    mode = m; label.textContent = txt;
    html.classList.toggle('fx-hot', m === 'hot'); html.classList.toggle('fx-media', m === 'media'); html.classList.toggle('fx-native', m === 'native');
  };
  // цвет фона под курсором: на красном точка белая
  const bgCache = new WeakMap();
  const onRed = t => {
    for (let el = t; el && el !== html; el = el.parentElement) {
      if (bgCache.has(el)) return bgCache.get(el);
      const c = getComputedStyle(el).backgroundColor.match(/[\d.]+/g);
      if (c && (c.length < 4 || +c[3] > .5)) {
        const red = +c[0] > 190 && +c[1] < 120 && +c[2] < 110;
        bgCache.set(el, red); return red;
      }
    }
    return false;
  };
  const pick = t => {
    if (!t || !t.closest) return setMode('');
    html.classList.toggle('fx-red', onRed(t));
    // окна-диалоги рисуются поверх всего (top layer) — там обычная стрелка
    if (document.querySelector('dialog:modal') || t.closest('dialog')) return setMode('native');
    if (t.closest(NATIVE)) return setMode('native');
    if (t.closest('.ba, .pba')) return setMode('media', 'Тяните');
    const h = t.closest(HOT);
    if (h) {
      const img = h.querySelector('img');
      if (img && img.offsetWidth * img.offsetHeight > 30000) return setMode('media', 'Смотреть');
      return setMode('hot');
    }
    setMode('');
  };
  addEventListener('pointermove', e => {
    if (e.pointerType !== 'mouse') return;
    mx = e.clientX; my = e.clientY;
    if (!shown) { shown = true; rx = dx = mx; ry = dy = my; html.classList.add('fx-show'); }
    pick(e.target);
  }, {passive: true, capture: true});   // capture — блоки со своим stopPropagation не прячут курсор
  document.addEventListener('pointerleave', () => { shown = false; html.classList.remove('fx-show'); });
  addEventListener('blur', () => { shown = false; html.classList.remove('fx-show'); });
  addEventListener('pointerdown', () => html.classList.add('fx-down'));
  addEventListener('pointerup', () => html.classList.remove('fx-down'));
  const loop = () => {
    dx += (mx - dx) * .55; dy += (my - dy) * .55;
    rx += (mx - rx) * .18; ry += (my - ry) * .18;
    // translate, а не transform: scale (наведение, нажатие) применяется после него и не сдвигает курсор
    dot.style.translate = `${dx}px ${dy}px`;
    ring.style.translate = `${rx}px ${ry}px`;
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);

  // ---- плавная прокрутка колесом (окно; внутренние списки, окна и чат — как обычно; карты колесом не масштабируются — над ними тоже плавно)
  let target = scrollY, cur = scrollY, running = false, lastSet = -1;
  const maxY = () => document.documentElement.scrollHeight - innerHeight;
  const locked = () => {
    const b = getComputedStyle(document.body).overflowY, h = getComputedStyle(html).overflowY;
    return b === 'hidden' || h === 'hidden' || html.classList.contains('lb-on') || document.querySelector('dialog[open]');
  };
  const canScrollInside = (el, d) => {
    for (; el && el !== document.body && el !== html; el = el.parentElement) {
      const s = getComputedStyle(el).overflowY;
      if ((s === 'auto' || s === 'scroll') && el.scrollHeight > el.clientHeight + 1) {
        if (d > 0 ? el.scrollTop + el.clientHeight < el.scrollHeight - 1 : el.scrollTop > 0) return true;
      }
    }
    return false;
  };
  const step = () => {
    if (Math.abs(scrollY - lastSet) > 3 && lastSet >= 0) { running = false; target = cur = scrollY; return; }   // прокрутили иначе — отдаём управление
    cur += (target - cur) * .12;
    if (Math.abs(target - cur) < .5) cur = target;
    lastSet = Math.round(cur);
    scrollTo({top: cur, behavior: 'instant'});
    lastSet = scrollY;
    if (cur !== target) requestAnimationFrame(step); else running = false;
  };
  addEventListener('wheel', e => {
    if (e.ctrlKey || e.defaultPrevented || Math.abs(e.deltaX) > Math.abs(e.deltaY) || locked()) return;
    const d = e.deltaY * (e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? innerHeight : 1);
    if (canScrollInside(e.target, d)) return;
    e.preventDefault();
    if (!running) { target = cur = scrollY; lastSet = scrollY; }
    target = Math.max(0, Math.min(maxY(), target + d));
    if (!running) { running = true; requestAnimationFrame(step); }
  }, {passive: false});
})();
