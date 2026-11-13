"""Сайт v37: на телефоне быстрые фильтры в два ряда (без обрезки), «Быстро:» скрыто, подсказка района «Любой».
Run из корня репо после site_v36_review.py: py -3 tools/patches/site_v37_mobfit.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<input id="ad" placeholder="Академический, ЖК…"', '<input id="ad" placeholder="Любой"')
rep('@media(prefers-reduced-motion:reduce){*{transition',
    '@media(max-width:800px){.hero .sbox3 .qfl{display:none}.hero .sbox3 .qf{display:grid;grid-template-columns:1fr 1fr;overflow:visible;margin:0;padding:0;gap:6px;width:100%}'
    '.hero .sbox3 .qf button{flex:1 1 auto;text-align:center;padding:8px 10px}}\n'
    '@media(prefers-reduced-motion:reduce){*{transition')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
