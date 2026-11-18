// ремонт: шторка ↔ этапы
const baR = $('#baR');
function baSet(v) { baR.value = v; $('#baBox .after').style.clipPath = `inset(0 0 0 ${v}%)`; $('#baH').style.left = v + '%';
  const k = Math.min(4, Math.floor((100 - v) / 18)); $$('#bSteps li').forEach((li, i) => { li.classList.toggle('cur', i === k); li.classList.toggle('past', i < k); }); }
baR.addEventListener('input', () => baSet(+baR.value));
function baTo(to, ms = 900) { if (reduce) { baSet(to); return; } const from = +baR.value, t0 = performance.now();
  (function f(t) { const k = Math.min(1, (t - t0) / ms), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; baSet(from + (to - from) * e); if (k < 1) requestAnimationFrame(f); })(t0); }
$$('#bSteps button').forEach(b => b.addEventListener('click', () => baTo(+b.dataset.v, 600)));
baSet(50);
new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect(); baTo(92, 700); setTimeout(() => baTo(8, 1600), 750); setTimeout(() => baTo(50, 900), 2500); }, {threshold: .5}).observe($('#baBox'));

