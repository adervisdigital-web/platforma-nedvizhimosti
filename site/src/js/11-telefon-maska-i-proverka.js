// телефон: маска и проверка
const lp = $('#lp');
lp.addEventListener('input', () => {
  let d = lp.value.replace(/\D/g, ''); lp.closest('.f').classList.remove('bad');
  if (!d) { lp.value = ''; return; }
  if (/^\s*\+\s*[0-689]/.test(lp.value)) return;   // номер не российский — не переделываем в +7, проверка его отклонит
  if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; const p = d.slice(1, 11);
  lp.value = '+7' + (p.length ? ' (' + p.slice(0, 3) : '') + (p.length > 3 ? ') ' + p.slice(3, 6) : '') + (p.length > 6 ? '-' + p.slice(6, 8) : '') + (p.length > 8 ? '-' + p.slice(8, 10) : '');
});
$('#leadForm').addEventListener('submit', e => {
  e.preventDefault();
  if (!/^\+7/.test(lp.value) || lp.value.replace(/\D/g, '').length !== 11) { lp.closest('.f').classList.add('bad'); lp.focus(); return; }
  if (!$('#lc').checked) { $('#lcL').classList.add('bad'); $('#lc').focus(); return; }
  const form = e.currentTarget, btn = $('#qSend'); btn.disabled = true;
  PN.send({kind: 'quiz', want: (($('#leadForm .ch [aria-pressed=true]') || {}).textContent || '') + ($('#leadForm').dataset.pack ? ' + ремонт (пакет)' : ''), budget: $('#qbv').textContent,
    area: $$('#qr [aria-pressed=true]').map(b => b.textContent).join(', '), name: $('#ln').value, phone: lp.value},
    () => { btn.disabled = false; form.classList.add('sent'); }, () => { btn.disabled = false; });
});

