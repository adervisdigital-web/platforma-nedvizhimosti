// Админка: подтверждение опасных действий; загрузка фото перетаскиванием и сортировка (задача 11).
document.addEventListener('submit', e => { const m = e.target.dataset.confirm; if (m && !confirm(m)) e.preventDefault(); });
