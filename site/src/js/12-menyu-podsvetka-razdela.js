// меню: подсветка раздела
const navA = $$('nav.main a');
const spy = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) navA.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id)); }), {rootMargin: '-40% 0px -55% 0px'});
navA.forEach(a => { const t = $(a.getAttribute('href')); if (t) spy.observe(t); });

