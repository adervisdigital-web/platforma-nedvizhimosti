// карта: пересчёт размера, когда список меняет высоту
if (window.ResizeObserver) { let mt; new ResizeObserver(() => { clearTimeout(mt); mt = setTimeout(mapFit, 120); }).observe($('.map')); }

