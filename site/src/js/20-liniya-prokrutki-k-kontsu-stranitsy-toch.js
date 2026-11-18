// линия прокрутки: к концу страницы — точка
const prog = $('#prog');
function progUpd() { const h = document.documentElement.scrollHeight - innerHeight, k = h > 0 ? Math.min(1, scrollY / h) : 0; prog.style.setProperty('--s', k); prog.classList.toggle('end', k > .995); }
addEventListener('scroll', progUpd, {passive: true}); addEventListener('resize', progUpd); progUpd();
new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { $('.fbig').classList.add('in'); o.disconnect(); } }, {threshold: .6}).observe($('.fbig'));

