// поиск на первом экране
const TABK = ['new', 'sec', 'houses', 'fin'];
let tab = 'new';
function readForm() {
  const rooms = $$('.sf .chip').map((b, i) => b.getAttribute('aria-pressed') === 'true' ? i : -1).filter(i => i >= 0);
  let max = parseFloat(($('#pr').value || '').replace(',', '.').replace(/[^\d.]/g, '')) || 0;
  if (max && max < 1000) max *= 1e6;
  return {rooms, max, q: $('#ad').value.trim().toLowerCase()};
}
function match(it, f) {
  if (tab === 'new' && it.t !== 'new' || tab === 'sec' && it.t !== 'sec' || tab === 'fin' && it.fin === 'Без отделки') return false;
  if (f.rooms.length && !f.rooms.some(r => r === 4 ? it.r >= 4 : it.r === r)) return false;
  if (f.max && it.p > f.max) return false;
  return !f.q || (it.zk + ' ' + it.d).toLowerCase().includes(f.q);
}
function liveCount() { const f = readForm(), n = ITEMS.filter(it => match(it, f)).length; $('#goN').textContent = n; }
$$('.tabs button').forEach((b, i) => b.addEventListener('click', () => {
  if (TABK[i] === 'houses') { $('#houses').scrollIntoView({behavior: 'smooth'}); return; }
  tab = TABK[i]; $$('.tabs button').forEach(x => x.setAttribute('aria-selected', x === b)); liveCount();
}));
$$('.chip').forEach(b => b.addEventListener('click', () => { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true'); liveCount(); }));
['#pr', '#ad'].forEach(q => $(q).addEventListener('input', liveCount));
$('#sf').addEventListener('submit', e => {
  e.preventDefault(); const f = readForm();
  const lab = [{new: 'Новостройки', sec: 'Вторичка', fin: 'С отделкой или ремонтом'}[tab],
    f.rooms.length ? f.rooms.map(r => r === 0 ? 'студия' : r === 4 ? '4+' : r).join(', ') + (f.rooms.some(r => r) ? ' комн.' : '') : '',
    f.max ? 'до ' + fmtM(f.max) : '', f.q ? `«${$('#ad').value.trim()}»` : ''].filter(Boolean).join(' · ');
  applyFilter(ITEMS.filter(it => match(it, f)), lab); $('#list').scrollIntoView({behavior: 'smooth'});
});
liveCount();

