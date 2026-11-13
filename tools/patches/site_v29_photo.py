"""Сайт v29: «На карте» убрано с первого экрана (просьба заказчика); фото «до/после» — новая пара 2688×1120
(RealVisXL: пустая квартира → img2img 0.55 отделка → inpaint мебели по маске пола → hi-res 2× 0.38/0.25), кадр 21:9 без обрезки.
Run из корня репо после site_v28_folder.py: py -3 tools/patches/site_v29_photo.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('</span><a href="#list"><svg class="ico"><use href="#pin"/></svg>На карте</a>', '</span>')
i = s.index("$('.sline a').addEventListener('click'"); j = s.index('\n', i)
s = s[:i] + s[j + 1:]
rep('<img src="photo/ba_before.jpg" alt="Квартира без отделки: бетон, большие окна">', '<img src="photo/ba_before.jpg?v=2" alt="Квартира без отделки: бетонные стены и пол, панорамное окно">')
rep('<img class="after" src="photo/ba_after.jpg" alt="Та же квартира после нашего ремонта: гостиная с диваном">', '<img class="after" src="photo/ba_after.jpg?v=2" alt="Та же квартира после нашего ремонта: гостиная с диваном и креслом">')
rep('@media(prefers-reduced-motion:reduce){*{transition', '.ba.wide{aspect-ratio:2688/1120}.ba img{object-position:50% 50%}\n@media(prefers-reduced-motion:reduce){*{transition')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
