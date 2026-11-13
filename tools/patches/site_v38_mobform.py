"""Сайт v38 — форма поиска на телефоне: одна белая карточка как список настроек iOS — строки «подпись — значение ›» с тонкими
линиями, фильтры контурными чипами, красная кнопка внутри карточки. Run из корня репо после site_v37_mobfit.py:
py -3 tools/patches/site_v38_mobform.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


CSS = r'''
/* v38 — форма на телефоне */
@media(max-width:800px){
 .hero .sbox.sbox3{background:#fff;border-radius:26px;padding:6px;box-shadow:0 30px 70px #00000059}
 .hero .sbox3 #sf{display:block;background:none;border-radius:0;padding:0;box-shadow:none}
 .hero .sbox3 .sf2 .sg{display:block;border-radius:16px;background:none;box-shadow:none!important;position:relative}
 .hero .sbox3 .sf2 .sg+.sg::after{content:'';position:absolute;left:14px;right:14px;top:0;height:1px;background:var(--line)}
 .hero .sbox3 .sf2 .sg::before{display:none}
 .hero .sbox3 .sf2 .sgb,.hero .sbox3 .sf2 .sgi{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:54px;padding:0 14px;border-radius:16px}
 .hero .sbox3 .sf2 .sg.on .sgb,.hero .sbox3 .sf2 .sgi:focus-within{background:var(--soft)}
 .hero .sbox3 .sf2 .sg small,.hero .sbox3 .sf2 .sgi label{font-size:14px;font-weight:500;color:var(--mut);flex:none}
 .hero .sbox3 .sf2 .sgb b{margin:0;font-size:16px;font-weight:600;color:var(--ink);display:flex;align-items:center;gap:8px;min-width:0}
 .hero .sbox3 .sf2 .sgb b::after{content:'';width:7px;height:7px;border-right:1.6px solid #B9B4AB;border-bottom:1.6px solid #B9B4AB;transform:rotate(-45deg);flex:none;margin-left:2px}
 .hero .sbox3 .sf2 .sgi input{text-align:right;font-weight:600;font-size:16px;min-width:0;flex:1;padding:0}
 .hero .sbox3 .sf2 .sgi input::placeholder{color:var(--ink);opacity:1}
 .hero .sbox3 .sline{background:none;box-shadow:none;border-radius:0;border-top:1px solid var(--line)!important;margin:2px 8px 0!important;padding:12px 0 6px!important}
 .hero .sbox3 .qf{display:flex!important;flex-wrap:wrap;gap:6px}
 .hero .sbox3 .qf button{flex:0 0 auto;background:none;border:1px solid var(--line);padding:7px 12px;font-size:13px}
 .hero .sbox3 .qf button[aria-pressed=true]{background:var(--ink);border-color:var(--ink);color:#fff}
 .hero .sbox3 .sf2 .sgi{flex-direction:row!important}
 .hero .sbox3 .sf2 .dd-wrap,.hero .sbox3 .sf2 .sg[data-pop]{position:relative!important}
 .hero .sbox3 .sf2 .sgi .dd,.hero .sbox3 .sf2 .pop{left:0!important;right:0!important;top:calc(100% + 4px)!important;margin:0!important;min-width:0!important}
 .hero .sbox3 .go3{margin:6px 0 0;border-radius:20px;box-shadow:none;min-height:58px}
}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')
open(P + 'index.html', 'w', encoding='utf8').write(s)

k = open(P + 'kabinet.html', encoding='utf8').read()
if '.mnav .st{display:flex' not in k:
    k = k.replace('@media(prefers-reduced-motion:reduce)', '.mnav .st{display:flex!important}\n@media(prefers-reduced-motion:reduce)', 1)
    open(P + 'kabinet.html', 'w', encoding='utf8').write(k)
print('ok')
