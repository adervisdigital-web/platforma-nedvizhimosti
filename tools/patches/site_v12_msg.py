"""Сайт v12 — ников Telegram/MAX пока нет (заказчик, 2026-11-13): ссылки не ведут в никуда, а открывают чат на сайте
с подсказкой. Застройщиков-партнёров заказчик разрешил называть. Когда появятся ники — заменить data-soon на ссылки
https://t.me/<ник> и https://max.ru/<ник>.  Run из корня репо: py -3 tools/patches/site_v12_msg.py  (исходник — v11.html)"""
P = '08_Сайт_пример/'
s = open(P + 'v11.html', encoding='utf8').read()
a = '<a href="#">Telegram</a><a href="#">MAX</a>'
assert s.count(a) == 3
s = s.replace(a, '<a href="#" data-soon="Telegram">Telegram</a><a href="#" data-soon="MAX">MAX</a>')
JS = r'''
// мессенджеры: ников пока нет — ведём в чат на сайте
$$('[data-soon]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); openChat(true); toast(`${a.dataset.soon} подключим к запуску — пока пишите здесь, ответим сразу`); }));
'''
s = s.replace('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
