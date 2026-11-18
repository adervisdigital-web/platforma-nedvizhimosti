// Админка: подтверждение опасных действий, порядок фото (‹/›), зона перетаскивания фото, клик по строке списка, «несохранённая» заявка.
document.addEventListener('submit', e => { const m = e.target.dataset.confirm; if (m && !confirm(m)) e.preventDefault(); });
document.addEventListener('click', e => {
  const b = e.target.closest('[data-move]');
  if (b) {
    const fig = b.closest('figure'), box = fig.parentElement, d = +b.dataset.move;
    if (d < 0 && fig.previousElementSibling) box.insertBefore(fig, fig.previousElementSibling);
    if (d > 0 && fig.nextElementSibling) box.insertBefore(fig.nextElementSibling, fig);
    return;
  }
  const tr = e.target.closest('tr[data-href]');   // строка списка открывает запись (кроме ссылок, кнопок и выделения текста)
  if (tr && !e.target.closest('a,button,input,select,label') && !String(getSelection())) location.href = tr.dataset.href;
});
document.querySelectorAll('.ad-drop').forEach(z => {
  const inp = z.querySelector('input[type=file]'), t = z.querySelector('.ad-drop-t'), t0 = t.textContent;
  ['dragenter', 'dragover'].forEach(k => z.addEventListener(k, e => { e.preventDefault(); z.classList.add('on'); }));
  ['dragleave', 'drop'].forEach(k => z.addEventListener(k, () => z.classList.remove('on')));
  z.addEventListener('drop', e => { e.preventDefault(); inp.files = e.dataTransfer.files; inp.dispatchEvent(new Event('change')); });
  inp.addEventListener('change', () => {
    const n = inp.files.length; z.dataset.n = n; z.classList.toggle('has', n > 0);
    t.textContent = n ? `Выбрано фото: ${n} — загрузятся при сохранении` : t0;
  });
});
document.querySelectorAll('.ad-lf').forEach(f => {   // заявка: кнопка «Сохранить» загорается, когда есть изменения
  const mark = () => f.classList.add('dirty');
  f.addEventListener('input', mark); f.addEventListener('change', e => {
    mark(); if (e.target.name === 'status') e.target.className = 'ad-st st-' + e.target.value;
  });
});
