"""Сайт v15 — ссылки на демо личного кабинета (08_Сайт_пример/kabinet.html): кнопка «Кабинет» в шапке, кнопка в разделе
«Личный кабинет», ссылка в подвале; в макете телефона — двухэтажный «Северный Урал 235» (как на камере).
Run из корня репо после site_v14_polish.py: py -3 tools/patches/site_v15_cabinet.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<a class="btn hcab" href="#cab">', '<a class="btn hcab" href="kabinet.html">')
rep('<b>Южный Урал 140</b><small>газоблок · Берёзовский</small>', '<b>Северный Урал 235</b><small>газоблок · Берёзовский</small>')
rep('      <li><b>Платежи</b><span>График рассрочки или ипотеки и напоминания.</span></li>\n    </ul>',
    '      <li><b>Платежи</b><span>График рассрочки или ипотеки и напоминания.</span></li>\n    </ul>\n'
    '    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:26px"><a class="btn red" href="kabinet.html">Открыть демо-кабинет</a><a class="btn ghost" href="#lead">Как получить доступ</a></div>')
rep('<a href="#cab">Личный кабинет</a>', '<a href="kabinet.html">Личный кабинет</a>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
