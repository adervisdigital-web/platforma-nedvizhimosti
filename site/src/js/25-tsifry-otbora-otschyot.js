// цифры «Отбора» — отсчёт
function countUp(el, to, ms) {
  if (reduce) return; const t0 = performance.now(), fmtN = n => n >= 1000 ? Math.round(n).toLocaleString('ru-RU') : Math.round(n);
  (function f(t) { const k = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - k, 3); el.textContent = fmtN(to * e); if (k < 1) requestAnimationFrame(f); })(t0);
}
