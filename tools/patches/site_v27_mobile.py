"""Сайт v27 — порядок в мобильной версии (≤800 px):
первый экран без пустоты (высота по содержимому), быстрые фильтры — лента с прокруткой; компактные карточки квартир
(фото 16:10, меньше отступов); «Квартира. Дом. Ремонт.» — точка не уезжает на новую строку; чек-лист сканера с постоянным
отступом; калькулятор ремонта — подпись и значение в две строки; договор на телефоне — читаемый лист на деревянной рамке
(без масштабирования фото); заявка — без точек под текстом; ровные отступы секций; подвал в две колонки.
Run из корня репо после site_v26_loader.py: py -3 tools/patches/site_v27_mobile.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<h2 class="t">Квартира<i class="o"></i> Дом<i class="o"></i> Ремонт<i class="o"></i></h2>',
    '<h2 class="t"><span class="nw">Квартира<i class="o"></i></span> <span class="nw">Дом<i class="o"></i></span> <span class="nw">Ремонт<i class="o"></i></span></h2>')

CSS = r'''
/* v27 — мобильная версия */
.scan .clist li{padding-left:22px}.scan .clist li::before{left:2px}
@media(max-width:800px){
 .sec{padding:56px 0}.sec[style*="padding-top:0"]{padding-top:0!important}
 h2.t{font-size:34px;line-height:1.04}
 /* первый экран */
 .hero{min-height:0}.hero .hin{justify-content:flex-start;gap:26px;padding-bottom:22px}
 .hero h1{font-size:44px}.trust{margin-top:18px}
 .hero .sline{display:block;margin:12px 0 0}
 .hero .qf{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;margin:0 -16px;padding:0 16px}.hero .qf::-webkit-scrollbar{display:none}
 .hero .qf button{flex:none}
 .hero .sline a{display:inline-flex;margin-top:12px}
 /* подборки */
 .cats{gap:8px}.cat{aspect-ratio:1/1;padding:12px;border-radius:18px}.cat b{font-size:15px}
 .promo{gap:8px}.pt{min-height:0;padding:22px;gap:18px}.pt h3{font-size:26px}
 .pt .dotgrid{display:none}.pt p{max-width:none}.cfield{height:40%;inset:12px 12px auto 12px;gap:6px 0}.cfield i{width:5px;height:5px}
 /* карточки квартир */
 .card{padding:10px;gap:10px;border-radius:22px}
 .gal{aspect-ratio:16/10}
 .mid{padding:2px 4px;gap:6px}.mid .t.qv{font-size:18px}
 .rcol{padding:10px 4px 2px}.price{font-size:22px}
 .rcol{display:grid;grid-template-columns:1fr auto;column-gap:10px;align-items:end}
 .rcol .price{grid-column:1}.rcol .ppm{grid-column:1}.rcol .mort{grid-column:1/-1;margin-top:8px}.rcol .btn,.rcol a.btn{grid-column:1/-1;margin-top:8px}
 .seen{margin-top:28px}
 /* блок отбора */
 .mtext{font-size:26px}.scan{margin-top:34px}.sfield{min-height:200px;gap:10px 0;padding:20px}
 .stats2{gap:28px 16px;margin-top:40px}.odo{font-size:52px}.st>span{font-size:13px}
 /* направления */
 .pgrid{gap:10px;margin-top:30px}.pc .b{padding:18px 18px 20px}.pc h3{font-size:26px}
 .way{padding:18px;gap:10px 14px}.way .btn{margin:6px 0 0;width:100%}
 /* калькуляторы */
 .cin,.cout{padding:22px;border-radius:22px}.calc{gap:10px;margin-top:28px}
 .rng label{flex-wrap:wrap;gap:2px 10px;align-items:baseline}.rng label b{font-size:17px}
 .cout .pay{font-size:46px}
 .banks{gap:6px;font-size:13px}.banks span{padding:7px 12px;font-size:13px}
 /* дома */
 .hx{gap:10px}.hc .b{padding:18px}
 /* ремонт */
 .bsteps{gap:6px}.bsteps button{padding:12px 14px;border-radius:16px}
 /* кабинет */
 .cfeat{gap:8px;margin-top:26px}.cfeat li{padding:16px 18px}
 /* отзывы */
 .rvh{width:100%}.rv{margin-top:26px}
 /* договор — читаемый лист на деревянной рамке */
 .desk{border-radius:22px;overflow:visible;box-shadow:none}
 .dk-in{width:auto;margin:0;aspect-ratio:auto;border-radius:22px;padding:18px;background:#2B1D14 url(photo/desk_contract.jpg) 50% 85%/cover;box-shadow:0 30px 60px #00000080}
 .dk-ph{display:none}
 .paper{position:relative;left:auto;top:auto;width:auto;height:auto;padding:20px 18px 18px;background:#FBFAF7;mix-blend-mode:normal;border-radius:4px;box-shadow:0 12px 30px #0000004d}
 .pp-h{font-size:10px;gap:8px;padding-bottom:10px;border-bottom-width:1px}.pp-logo{font-size:9px;gap:6px}.pp-logo svg{width:18px;height:17px}
 .pp-t{font-size:15px;margin:14px 0 6px}
 .desk .cl li{grid-template-columns:30px 1fr;padding:7px 6px;margin:0 -6px;border-radius:6px}
 .desk .cl li span{font-size:11px}.desk .cl li p{font-size:13.5px}
 .desk .cl li span::after{left:-14px;top:4px;width:8px;height:4px;border-width:2px}
 .desk .sign{gap:16px;margin-top:16px}.desk .sign .k{font-size:10px}.desk .sign .ln{height:34px;border-bottom-width:1px}
 .sig{width:96px;height:28px}.desk .seal{left:78px;width:20px;height:20px;bottom:5px}
 .you{font-size:11px}.you::after{width:1px;height:12px}
 .desk figcaption{background:none;padding:12px 0 0}
 /* заявка и подвал */
 .lead .dotgrid{display:none}.lead{padding:56px 0}
 .fbig{font-size:54px;margin-bottom:34px;white-space:nowrap}
 .fgr{grid-template-columns:1fr 1fr;gap:26px 16px}.fgr>div:first-child{grid-column:1/-1}
 footer{padding:50px 0 110px}
}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
