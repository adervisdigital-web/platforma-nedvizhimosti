// ползунки: заливка до бегунка
function fillAll() { $$('input[type=range]').forEach(r => r.style.setProperty('--p', (r.value - r.min) / (r.max - r.min) * 100 + '%')); }
document.addEventListener('input', e => { if (e.target.type === 'range') fillAll(); });
fillAll();

