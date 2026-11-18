// мессенджеры: ников пока нет — ведём в чат на сайте
$$('[data-soon]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); openChat(true); toast(`${a.dataset.soon} подключим к запуску — пока пишите здесь, ответим сразу`); }));

function rub(n) { return Math.round(n).toLocaleString('ru-RU') + ' ₽'; }
const MONTHS = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];

