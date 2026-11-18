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

