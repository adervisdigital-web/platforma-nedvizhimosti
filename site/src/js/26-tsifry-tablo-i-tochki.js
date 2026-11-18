// цифры: табло и точки
$$('.odo').forEach(o => { const str = (+o.dataset.n).toLocaleString('ru-RU'); o.innerHTML = [...str].map(ch => /\d/.test(ch) ? `<span class="col" data-d="${ch}">${'0123456789'.repeat(2).split('').map(x => `<span>${x}</span>`).join('')}</span>` : '<span class="gap"></span>').join(''); });
$$('.sd').forEach(d => { d.innerHTML = '<i></i>'.repeat(+d.dataset.n); });
function statsGo() {
  $$('.odo').forEach((o, k) => $$('.col', o).forEach((c, j) => { c.style.transitionDelay = (k * 150 + j * 120) + 'ms'; c.style.transform = `translateY(-${10 + +c.dataset.d}em)`; }));
  $$('.sd').forEach((d, k) => $$('i', d).forEach((dot, j) => setTimeout(() => dot.classList.add('on'), reduce ? 0 : 300 + k * 150 + j * (1400 / d.children.length))));
}
new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect(); statsGo(); }, {threshold: .4}).observe($('.stats2'));

