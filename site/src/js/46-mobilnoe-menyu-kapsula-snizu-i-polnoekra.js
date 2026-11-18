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
