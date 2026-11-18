// шторка: тянуть мышью и пальцем по всему фото
(() => { const box = $('#baBox'); if (!box) return; let on = false;
  const at = e => { const r = box.getBoundingClientRect(); baSet(Math.max(0, Math.min(100, (e.clientX - r.left) / r.width * 100))); };
  box.addEventListener('pointerdown', e => { on = true; box.classList.add('drag'); box.setPointerCapture(e.pointerId); at(e); e.preventDefault(); });
  box.addEventListener('pointermove', e => { if (on) at(e); });
  ['pointerup', 'pointercancel'].forEach(t => box.addEventListener(t, () => { on = false; box.classList.remove('drag'); })); })();

