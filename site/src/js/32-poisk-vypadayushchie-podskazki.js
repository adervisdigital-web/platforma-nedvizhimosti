// поиск: выпадающие подсказки
function ddOpen(dd, items, pick) {
  if (!items.length) { dd.hidden = true; return; }
  dd.innerHTML = items.map((x, i) => `<button type="button" role="option" data-i="${i}">${x[0]}${x[1] ? `<small>${x[1]}</small>` : ''}</button>`).join('');
  dd.hidden = false; $$('button', dd).forEach(b => b.addEventListener('mousedown', e => { e.preventDefault(); pick(items[b.dataset.i]); dd.hidden = true; }));
}
function ddKeys(inp, dd) {
  inp.addEventListener('keydown', e => {
    const bs = $$('button', dd); if (dd.hidden || !bs.length) return; let i = bs.findIndex(b => b.classList.contains('act'));
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); i = (i + (e.key === 'ArrowDown' ? 1 : -1) + bs.length) % bs.length; bs.forEach((b, k) => b.classList.toggle('act', k === i)); }
    else if (e.key === 'Enter' && i >= 0) { e.preventDefault(); bs[i].dispatchEvent(new MouseEvent('mousedown')); }
    else if (e.key === 'Escape') dd.hidden = true;
  });
  inp.addEventListener('blur', () => setTimeout(() => dd.hidden = true, 120));
}
const pr = $('#pr'), ad = $('#ad');
const cntBy = fn => ITEMS.filter(it => fn(it) && match(it, {...readForm(), max: 0, q: ''})).length;
function prShow() { ddOpen($('#prDD'), [5, 8, 12, 15].map(m => [`до ${m} млн ₽`, `${cntBy(it => it.p <= m * 1e6)} кв.`, m]).concat([['Любая цена', '', '']]), x => { pr.value = x[2]; liveCount(); }); }
pr.addEventListener('focus', prShow); pr.addEventListener('input', () => $('#prDD').hidden = true); ddKeys(pr, $('#prDD'));
const PLACES = [...new Set(ITEMS.map(it => it.d))].map(d => [d, 'район']).concat([...new Set(ITEMS.filter(it => it.zk.startsWith('ЖК')).map(it => it.zk))].map(z => [z, 'жилой комплекс']));
function adShow() {
  const q = ad.value.trim().toLowerCase();
  ddOpen($('#adDD'), PLACES.filter(p => !q || p[0].toLowerCase().includes(q)).slice(0, 7).map(p => [p[0], `${p[1]} · ${cntBy(it => (it.zk + ' ' + it.d).includes(p[0]))} кв.`]), x => { ad.value = x[0]; liveCount(); });
}
ad.addEventListener('focus', adShow); ad.addEventListener('input', adShow); ddKeys(ad, $('#adDD'));

