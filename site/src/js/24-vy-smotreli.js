// вы смотрели
function seenList() { return window.PN_SEEN || (window.PN_SEEN = store.get('pn_seen')); }
function remember(id) { const seen = seenList(); const i = seen.indexOf(id); if (i >= 0) seen.splice(i, 1); seen.unshift(id); seen.length = Math.min(seen.length, 8); store.set('pn_seen', seen); drawSeen(); }
function drawSeen() {
  const seen = seenList(); if (!$('#seenL') || typeof head !== 'function') return;
  $('#seen').hidden = !seen.length;
  $('#seenL').innerHTML = seen.map(id => ITEMS[id]).filter(Boolean).map(it => `<button type="button" data-seen="${it.id}"><img src="${PN.img(it.img)}" alt=""><b>${(it.p / 1e6).toLocaleString('ru-RU', {maximumFractionDigits: 2})} млн ₽</b><span>${head(it)} · ${it.d}</span></button>`).join('');
  $$('[data-seen]').forEach(b => b.addEventListener('click', () => quick(ITEMS[b.dataset.seen])));
}
drawSeen();

