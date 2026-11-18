// подборки: живое поле точек в «Самые выгодные»
(() => {
  const f = $('.cfield'), N = 42, W = 23; f.innerHTML = '<i></i>'.repeat(N); const ds = $$('i', f);
  if (reduce) { ds.forEach((d, i) => d.classList.toggle('off', i !== W)); ds[W].classList.add('win'); return; }
  function run() {
    ds.forEach(d => d.classList.remove('off', 'win')); const order = ds.map((_, i) => i).filter(i => i !== W).sort(() => Math.random() - .5); let k = 0;
    const t = setInterval(() => { for (let j = 0; j < 3 && k < order.length; j++, k++) ds[order[k]].classList.add('off');
      if (k >= order.length) { clearInterval(t); ds[W].classList.add('win'); setTimeout(run, 2600); } }, 110);
  }
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { run(); o.disconnect(); } }).observe(f);
})();
