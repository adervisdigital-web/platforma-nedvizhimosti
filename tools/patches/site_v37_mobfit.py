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

# путь клиента на телефоне — вертикальная линия времени
s = open(P + 'index.html', encoding='utf8').read()
s = s.replace('@media(prefers-reduced-motion:reduce){*{transition',
    '@media(max-width:800px){.way{flex-direction:column;align-items:stretch;gap:0;padding:20px 20px 18px}'
    '.way .stp{white-space:normal;font-size:15px;gap:14px;padding:2px 0}.way .stp i{width:12px;height:12px;flex:none}'
    '.way .ln{display:block!important;flex:none;width:2px;min-width:0;height:18px;margin:4px 0 4px 5px;background:repeating-linear-gradient(180deg,#56545A 0 4px,transparent 4px 8px)}'
    '.way .ln::after{transform:scaleY(0);transform-origin:top;width:2px;height:100%}.way .ln.fill::after{transform:scaleY(1)}'
    '.way .btn{margin:16px 0 0!important;width:100%}}\n'
    '@media(prefers-reduced-motion:reduce){*{transition', 1)
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('way ok')

# телефоны не переносятся
s = open(P + 'index.html', encoding='utf8').read()
if 'a[href^="tel:"]{white-space:nowrap}' not in s:
    s = s.replace('@media(prefers-reduced-motion:reduce){*{transition', 'a[href^="tel:"]{white-space:nowrap}\n@media(prefers-reduced-motion:reduce){*{transition', 1)
open(P + 'index.html', 'w', encoding='utf8').write(s)
k = open(P + 'kabinet.html', encoding='utf8').read()
if 'a[href^="tel:"]{white-space:nowrap}' not in k:
    k = k.replace('@media(prefers-reduced-motion:reduce)', 'a[href^="tel:"]{white-space:nowrap}\n@media(prefers-reduced-motion:reduce)', 1)
    open(P + 'kabinet.html', 'w', encoding='utf8').write(k)
print('tel ok')
