"""Сайт v4, шаг 2: мелкий текст и точки отбора масштабируются на широких экранах. Run из корня репо."""
p = '08_Сайт_пример/index.html'
s = open(p, encoding='utf8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)


rep('.field i{display:block;width:10px;height:10px;border-radius:50%;background:#4A484D;margin:7px auto;',
    '.field i{display:block;width:clamp(10px,.62vw,18px);height:clamp(10px,.62vw,18px);border-radius:50%;background:#4A484D;margin:clamp(7px,.6vw,16px) auto;')
rep('@media(min-width:2200px){#cards.grid{--cols:3}}', '''@media(min-width:1700px){.br{font-size:14px}nav.main{font-size:15px;gap:30px}.tel{font-size:16px}
 .mid .t{font-size:20px}.mid .a,.mid .line{font-size:14px}.tags span{font-size:13px}.vbtn{font-size:13px}.price{font-size:27px}.ppm,.mort{font-size:13px}.mort b{font-size:15px}
 .cat span{font-size:13px}.pc .br2,.clist li span{font-size:14px}.stats span{font-size:17px;max-width:280px}.tl b{font-size:19px}.tl span{font-size:15px}
 .rng label{font-size:16px}.rates button{font-size:14px}.crow{font-size:16px}.note{font-size:13px}.way .stp{font-size:16px}.fcap{font-size:15px}.mapcap{font-size:13px}.pin{font-size:13px}}
@media(min-width:2200px){#cards.grid{--cols:3}body{font-size:17px}.br{font-size:15px}.pc p,.prom span{font-size:19px}}''')
open(p, 'w', encoding='utf8').write(s)
print('ok')
