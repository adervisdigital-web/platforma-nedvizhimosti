"""Сайт v34 — заявка: одно живое поле точек на canvas вместо двух CSS-слоёв (фон с градиентом + подсветка у курсора
давали заметный стык). Размер и яркость каждой точки = градиент по ширине (слева пусто → справа плотно) + близость курсора
(точки плавно «надуваются», курсор догоняется с инерцией) + медленная волна в покое. Работает только когда блок на экране,
учитывает DPR и prefers-reduced-motion. Run из корня репо после site_v33_search2.py: py -3 tools/patches/site_v34_leaddots.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<section class="lead" id="lead"><span class="dotgrid" aria-hidden="true"></span><span class="dotgrid lit" aria-hidden="true"></span>',
    '<section class="lead" id="lead"><canvas class="ldots" id="ldots" aria-hidden="true"></canvas>')
rep('@media(prefers-reduced-motion:reduce){*{transition',
    '.ldots{position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none}\n.lead .lgrid{z-index:1}\n'
    '@media(prefers-reduced-motion:reduce){*{transition')

JS = r'''
// заявка: живое поле точек
(() => {
  const cv = $('#ldots'), sec = $('#lead'); if (!cv) return;
  const ctx = cv.getContext('2d'); let W = 0, H = 0, dpr = 1, pts = [], run = false, raf = 0;
  const m = {x: -9999, y: -9999, tx: -9999, ty: -9999, on: 0, ton: 0};
  const ss = (a, b, x) => { const t = Math.max(0, Math.min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  function build() {
    const r = sec.getBoundingClientRect(); dpr = Math.min(2, devicePixelRatio || 1); W = r.width; H = r.height;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const step = W < 800 ? 24 : 28, mob = W < 800; pts = [];
    for (let y = step / 2; y < H; y += step) for (let x = step / 2; x < W; x += step) {
      const g = mob ? ss(-.2, 1.2, (y / H) * .6 + (x / W) * .4) * .7 : ss(.32, .82, x / W);
      pts.push([x, y, g]);
    }
    draw(performance.now());
  }
  function draw(t) {
    ctx.clearRect(0, 0, W, H);
    m.x += (m.tx - m.x) * .14; m.y += (m.ty - m.y) * .14; m.on += (m.ton - m.on) * .08;
    const R = Math.max(140, Math.min(220, W * .11)), wave = reduce ? 0 : t / 1600;
    for (const [x, y, g] of pts) {
      const dx = x - m.x, dy = y - m.y, k = Math.exp(-(dx * dx + dy * dy) / (R * R)) * m.on * (W < 800 ? 1 : .3 + .7 * ss(.22, .5, x / W));
      const w = reduce ? 0 : (Math.sin(wave + x * .012 + y * .018) + 1) * .5 * .25 * g;
      const a = Math.min(.95, .1 + .3 * g + w * .4 + .55 * k), rad = 1.4 + 3.4 * g + 3.2 * k;
      if (a < .03 || rad < .6) continue;
      ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(x, y, rad, 0, 6.2832); ctx.fillStyle = '#fff'; ctx.fill();
    }
    ctx.globalAlpha = 1;
    if (run) raf = requestAnimationFrame(draw);
  }
  function start() { if (run) return; run = true; raf = requestAnimationFrame(draw); }
  function stop() { run = false; cancelAnimationFrame(raf); }
  sec.addEventListener('pointermove', e => { const r = sec.getBoundingClientRect(); m.tx = e.clientX - r.left; m.ty = e.clientY - r.top; if (m.x < -9000) { m.x = m.tx; m.y = m.ty; } m.ton = 1; });
  sec.addEventListener('pointerleave', () => { m.ton = 0; });
  new IntersectionObserver(es => { es[0].isIntersecting ? (reduce ? draw(0) : start()) : stop(); }).observe(sec);
  new ResizeObserver(build).observe(sec); build();
})();
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
