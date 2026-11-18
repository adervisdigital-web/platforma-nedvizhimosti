// ссылки на объект и дом
function setHash(h) { try { history.replaceState(null, '', '#' + h); } catch (e) {} }
document.addEventListener('click', async e => {
  if (!e.target.closest('[data-share]')) return;
  const url = location.href, title = $('#dlgT').textContent + ' — Платформа недвижимости';
  try { if (navigator.share) { await navigator.share({title, url}); return; } await navigator.clipboard.writeText(url); toast('Ссылка скопирована — отправьте её родным'); }
  catch (x) { if (x.name !== 'AbortError') toast('Скопируйте ссылку из адресной строки'); }
});
(() => { const m = location.hash.match(/^#(obj|house)-(\w+)$/); if (!m) return;
  const t = m[1] === 'obj' ? ITEMS[+m[2]] : byId(m[2]); if (t) (m[1] === 'obj' ? quick : houseView)(t); })();

