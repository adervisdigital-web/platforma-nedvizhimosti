// Админка: подтверждение опасных действий, порядок фото (←/→), подсветка зоны перетаскивания и предпросмотр выбранных файлов.
document.addEventListener('submit', e => { const m = e.target.dataset.confirm; if (m && !confirm(m)) e.preventDefault(); });
document.addEventListener('click', e => {
  const b = e.target.closest('[data-move]'); if (!b) return;
  const fig = b.closest('figure'), box = fig.parentElement, d = +b.dataset.move;
  if (d < 0 && fig.previousElementSibling) box.insertBefore(fig, fig.previousElementSibling);
  if (d > 0 && fig.nextElementSibling) box.insertBefore(fig.nextElementSibling, fig);
});
document.querySelectorAll('.ad-drop').forEach(z => {
  const inp = z.querySelector('input[type=file]');
  ['dragenter', 'dragover'].forEach(t => z.addEventListener(t, e => { e.preventDefault(); z.classList.add('on'); }));
  ['dragleave', 'drop'].forEach(t => z.addEventListener(t, () => z.classList.remove('on')));
  z.addEventListener('drop', e => { e.preventDefault(); inp.files = e.dataTransfer.files; inp.dispatchEvent(new Event('change')); });
  inp.addEventListener('change', () => { const n = inp.files.length; z.dataset.n = n; z.firstChild.textContent = n ? `Выбрано файлов: ${n} — они загрузятся при сохранении ` : 'Перетащите фото сюда или выберите файлы (JPG, PNG, WebP до 25 МБ)'; });
});
