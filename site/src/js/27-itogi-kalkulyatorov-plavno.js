// итоги калькуляторов — плавно
['#pay', '#hpay', '#rpay'].forEach(q => {
  const el = $(q); if (!el) return; let cur = parseFloat(el.textContent.replace(/[^\d,]/g, '').replace(',', '.')) || 0, raf;
  new MutationObserver(() => {
    const node = el.firstChild; if (!node || node.nodeType !== 3) return;
    const to = parseFloat(node.nodeValue.replace(/[^\d,]/g, '').replace(',', '.')); if (isNaN(to) || reduce) { cur = to; return; }
    const from = cur, t0 = performance.now(); cur = to; cancelAnimationFrame(raf);
    (function f(t) { const k = Math.min(1, (t - t0) / 380), e = 1 - Math.pow(1 - k, 3); node.nodeValue = Math.round(from + (to - from) * e).toLocaleString('ru-RU') + ' '; if (k < 1) raf = requestAnimationFrame(f); })(t0);
  }).observe(el, {childList: true});
});

