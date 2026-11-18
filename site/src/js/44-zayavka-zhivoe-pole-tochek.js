// заявка: живое поле точек
(() => {
  const cv = $('#ldots'), sec = $('#lead'); if (!cv) return;
  const ctx = cv.getContext('2d'); let W = 0, H = 0, dpr = 1, pts = [], run = false, raf = 0;
  const m = {x: -9999, y: -9999, tx: -9999, ty: -9999, on: 0, ton: 0};
  const ss = (a, b, x) => { const t = Math.max(0, Math.min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  function build() {
    const r = sec.getBoundingClientRect(); dpr = Math.min(2, devicePixelRatio || 1); W = r.width; H = r.height;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const step = W < 800 ? 18 : 24, mob = W < 800; pts = [];
    for (let y = step / 2; y < H; y += step) for (let x = step / 2; x < W; x += step) {
      const g = mob ? ss(.5, .95, y / H) * (.55 + .45 * ss(0, 1, x / W)) : ss(.34, .86, x / W);
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
      const a = Math.min(.9, .06 + .34 * g + w * .3 + .5 * k), rad = (W < 800 ? .6 + 1.6 * g : .9 + 2.5 * g) + 2.6 * k;
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

