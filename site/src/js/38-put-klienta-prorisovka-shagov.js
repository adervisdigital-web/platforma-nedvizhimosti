// путь клиента: прорисовка шагов
(() => { const way = $('.way'); if (!way) return; const parts = [...way.children].filter(e => e.matches('.stp,.ln'));
  function play() { parts.forEach(p => p.classList.remove('lit', 'fill')); parts.forEach((p, i) => setTimeout(() => p.classList.add(p.matches('.stp') ? 'lit' : 'fill'), reduce ? 0 : 250 + i * 330)); }
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { play(); o.disconnect(); } }, {threshold: .6}).observe(way);
  way.addEventListener('mouseenter', play); })();

