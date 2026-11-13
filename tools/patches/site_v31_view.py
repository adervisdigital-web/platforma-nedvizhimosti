"""Сайт v31: «до/после» — вид из окна одинаковый (окно перенесено из кадра «до» пиксель в пиксель, комната дорисована
вокруг него inpaint + hi-res); точки в заявке тянутся к середине с плавным градиентом.
Run из корня репо после site_v30_header.py: py -3 tools/patches/site_v31_view.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('photo/ba_after.jpg?v=2', 'photo/ba_after.jpg?v=3')
rep('@media(prefers-reduced-motion:reduce){*{transition',
    '.lead .dotgrid{width:64%;max-width:none}\n'
    '.lead .dotgrid:not(.lit){-webkit-mask-image:linear-gradient(90deg,#0000 0%,#0006 30%,#000 70%);mask-image:linear-gradient(90deg,#0000 0%,#0006 30%,#000 70%)}\n'
    '@media(prefers-reduced-motion:reduce){*{transition')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
