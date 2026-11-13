"""Сайт v16 — вторая проверка глазами: фото без людей в блоке «Квартира. Дом. Ремонт.» (вкус заказчика), на телефоне
калькулятор рассрочки не вылезает за карточку, суммы не разрываются, короткая кнопка ипотеки.
Run из корня репо после site_v15_cabinet.py: py -3 tools/patches/site_v16_review.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<img src="photo/inspect.jpg" alt="Инженер проверяет строящийся дом" loading="lazy">', '<img src="photo/zhk.jpg" alt="Новый жилой комплекс в сумерках" loading="lazy">')
rep('<img src="photo/crew.jpg" alt="Бригада укладывает плитку" loading="lazy">', '<img src="photo/rem_wip.jpg" alt="Квартира в ремонте: укладка плитки" loading="lazy">')
rep('<a class="btn" href="#lead">Подобрать самую выгодную программу</a>', '<a class="btn" href="#lead">Подобрать программу</a>')
rep('@media(prefers-reduced-motion:reduce)', '.cin{grid-template-columns:minmax(0,1fr)}.cin>*{min-width:0}.crow b{white-space:nowrap}.crow{gap:12px}\n@media(prefers-reduced-motion:reduce)')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
