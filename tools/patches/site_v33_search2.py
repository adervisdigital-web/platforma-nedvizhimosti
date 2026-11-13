"""Сайт v33 — форма поиска в два ряда в одной карточке: ряд 1 — «Что ищем · Комнаты · Бюджет · Район» + кнопка,
ряд 2 (через тонкую линию) — быстрые фильтры «Быстро: Готовые · С отделкой · …» и живой счётчик. Стеклянные чипы
под формой убраны внутрь карточки. Run из корня репо после site_v32_iosfix.py: py -3 tools/patches/site_v33_search2.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<div class="sline"><span class="qf" role="group" aria-label="Быстрые фильтры">',
    '<div class="sline"><span class="qfl">Быстро:</span><span class="qf" role="group" aria-label="Быстрые фильтры">')

CSS = r'''
/* v33 — поиск: два ряда в одной карточке */
.hero .sbox{background:#fff;border-radius:30px;padding:8px;box-shadow:0 30px 70px #00000059,0 0 0 1px #ffffff40}
.hero .sf.sf2,.hero .sf2.open{background:transparent;box-shadow:none;padding:0;border-radius:999px}
.hero .sline{display:flex;align-items:center;gap:10px;margin:8px 6px 2px;padding:10px 10px 4px;border-top:1px solid var(--line);color:var(--mut)}
.hero .qfl{font-size:12px;font-weight:700;color:var(--ink);flex:none}
.hero .qf{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;margin:0;padding:0}.hero .qf::-webkit-scrollbar{display:none}
.hero .qf button{flex:none;background:var(--soft);border:1px solid transparent;color:var(--ink);backdrop-filter:none;-webkit-backdrop-filter:none;padding:7px 14px;font-size:13px;font-weight:600;transition:background .2s,border-color .2s}
.hero .qf button:hover{background:#fff;border-color:var(--line)}
.hero .qf button[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}
@media(max-width:800px){
 .hero .sbox{border-radius:26px;padding:8px}
 .hero .sf.sf2{display:grid;grid-template-columns:1fr 1fr;gap:6px;border-radius:0}
 .hero .sf2 .sg{border-radius:16px;background:var(--soft)}.hero .sf2 .sg::before{display:none}
 .hero .sf2 .sg.on,.hero .sf2 .sg:focus-within{background:#fff;box-shadow:0 0 0 1px var(--ink)}
 .hero .sf2 .sgb,.hero .sf2 .sgi{padding:10px 14px}.hero .sf2 .sg b,.hero .sf2 .sgi input{font-size:16px}
 .hero .sf2 .go2{grid-column:1/-1;margin:2px 0 0;height:54px}
 .hero .sf2 .pop{min-width:calc(200% + 6px)}.hero .sf2 .sg:nth-child(2) .pop{left:auto;right:0}
 .hero .sline{display:flex;margin:6px 4px 2px;padding:10px 8px 4px}
 .hero .qf{margin:0 -12px 0 0;padding:0 12px 0 0}
}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
