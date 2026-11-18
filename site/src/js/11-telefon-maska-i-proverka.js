// телефон: маска и проверка
const lp = $('#lp');
lp.addEventListener('input', () => {
  let d = lp.value.replace(/\D/g, ''); lp.closest('.f').classList.remove('bad');
  if (!d) { lp.value = ''; return; }
  if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; const p = d.slice(1, 11);
  lp.value = '+7' + (p.length ? ' (' + p.slice(0, 3) : '') + (p.length > 3 ? ') ' + p.slice(3, 6) : '') + (p.length > 6 ? '-' + p.slice(6, 8) : '') + (p.length > 8 ? '-' + p.slice(8, 10) : '');
});
$('#leadForm').addEventListener('submit', e => {
  e.preventDefault();
  if (lp.value.replace(/\D/g, '').length !== 11) { lp.closest('.f').classList.add('bad'); lp.focus(); return; }
  e.currentTarget.classList.add('sent');
});

