"""Сайт v32 — исправления для iPhone (по скриншоту заказчика: чат при открытой клавиатуре).
1) Поля ввода на телефоне — 16 px: Safari увеличивал страницу при фокусе на полях < 16 px, кнопка «Отправить» уходила за край.
2) Чат на телефоне — лист во весь видимый экран: высота и положение по window.visualViewport (клавиатура не прячет шапку
   и сообщения), страница под чатом не прокручивается, на сенсорных экранах поле не фокусируется само при открытии.
То же для kabinet.html (поля 16 px). Run из корня репо после site_v31_view.py: py -3 tools/patches/site_v32_iosfix.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('@media(prefers-reduced-motion:reduce){*{transition',
    '@media(max-width:800px){input,select,textarea,.sgi input,.hb-row input,.ch-f input,.f input{font-size:16px!important}'
    '.chat{left:0;right:0;top:0;bottom:auto;width:100%;height:100%;border-radius:0;box-shadow:none}.chat .ch-h{padding-top:max(16px,env(safe-area-inset-top))}'
    '.ch-f{padding-bottom:max(12px,env(safe-area-inset-bottom))}.ch-m{display:none}.ch-f button{flex:none}}\n'
    'html.chat-lock,html.chat-lock body{overflow:hidden}\n'
    '@media(prefers-reduced-motion:reduce){*{transition')
rep("  if (o) $('#chatIn').focus();\n}",
    "  if (o && matchMedia('(hover:hover)').matches) $('#chatIn').focus();\n"
    "  const mob = innerWidth <= 800; document.documentElement.classList.toggle('chat-lock', o && mob); if (o && mob) fitChat();\n}\n"
    "function fitChat() { const v = window.visualViewport, c = $('#chat'); if (!v || innerWidth > 800 || c.hidden) { c.style.height = c.style.top = ''; return; }\n"
    "  c.style.top = v.offsetTop + 'px'; c.style.height = v.height + 'px'; const lg = $('#chatLog'); lg.scrollTop = lg.scrollHeight; }\n"
    "if (window.visualViewport) { visualViewport.addEventListener('resize', fitChat); visualViewport.addEventListener('scroll', fitChat); }")
open(P + 'index.html', 'w', encoding='utf8').write(s)

k = open(P + 'kabinet.html', encoding='utf8').read()
if 'v32 ios' not in k:
    k = k.replace('@media(prefers-reduced-motion:reduce)', '/* v32 ios */@media(max-width:1000px){input{font-size:16px!important}}\n@media(prefers-reduced-motion:reduce)', 1)
    open(P + 'kabinet.html', 'w', encoding='utf8').write(k)
print('ok')
