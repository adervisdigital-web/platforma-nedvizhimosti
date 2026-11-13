"""Сайт v14 — правки после просмотра глазами: «₽/мес» не разрывается, короткие подписи актов в кабинете,
заголовок у блока обещаний. Run из корня репо после site_v13_map.py: py -3 tools/patches/site_v14_polish.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep("· в рассрочку от ${hMonth(h).toLocaleString('ru-RU')} ₽/мес</div>", "· <span class=\"nw\">в рассрочку от ${hMonth(h).toLocaleString('ru-RU')} ₽/мес</span></div>")
rep('<div>Акт № 3 «Стены»<small>подписан</small></div>', '<div>Акт 3 · стены<small>подписан</small></div>')
rep('<div>Акт № 4 «Кровля»<small id="actSt">ждёт подписи</small></div>', '<div>Акт 4 · кровля<small id="actSt">ждёт подписи</small></div>')
rep('<div class="br">[ <b>●</b> Обещания ]</div>', '<div class="br">[ <b>●</b> Обещания ]</div><h2 class="t">Обещаем — и&nbsp;пишем это в&nbsp;<span class="nw">договор<i class="o"></i></span></h2>')
rep('.prom{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:50px}', '.prom{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:44px}')
rep('@media(prefers-reduced-motion:reduce)', '@media(max-width:800px){.hfl,#hproj{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}.hfl button,#hproj button{flex:none}}\n@media(prefers-reduced-motion:reduce)')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
