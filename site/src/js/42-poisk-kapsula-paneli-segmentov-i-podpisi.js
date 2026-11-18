// поиск-капсула: панели сегментов и подписи
const sf2 = $('#sf');
function segClose(except) { $$('.sg[data-pop]').forEach(g => { if (g !== except) { g.classList.remove('on'); $('.sgb', g).setAttribute('aria-expanded', 'false'); } }); sf2.classList.toggle('open', !!except); }
$$('.sg[data-pop]').forEach(g => $('.sgb', g).addEventListener('click', e => { e.stopPropagation(); const on = !g.classList.contains('on'); segClose(on ? g : null); g.classList.toggle('on', on); e.currentTarget.setAttribute('aria-expanded', on); }));
$$('.sgi input').forEach(inp => inp.addEventListener('focus', () => segClose(null)));
document.addEventListener('click', e => { if (!e.target.closest('.sg')) segClose(null); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') segClose(null); });
function segLabels() {
  $('#sgType').textContent = ($('.pop .tabs [aria-selected=true]') || {}).textContent || 'Новостройки';
  const r = $$('.sf .chip').filter(c => c.getAttribute('aria-pressed') === 'true').map(c => c.textContent);
  $('#sgRooms').textContent = r.length ? r.join(', ') : 'Любые';
}
$$('.pop .tabs button').forEach(b => b.addEventListener('click', () => { segLabels(); if (b.textContent !== 'Дома') setTimeout(() => segClose(null), 120); }));
$$('.sf .chip').forEach(c => c.addEventListener('click', segLabels));
segLabels();

