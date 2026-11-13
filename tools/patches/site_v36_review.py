"""Сайт v36 — по просмотру всей страницы глазами.
Телефон: нижнее меню — тёмная плавающая капсула со своими иконками в стиле точки (активный пункт — красная точка),
прячется при прокрутке вниз и возвращается при прокрутке вверх, подсвечивает раздел на экране, «Карта» сразу открывает
карту; в шапке — кнопка меню вместо звонка → полноэкранная навигация (разделы, телефон, чат, кабинет, статус).
Договор: галочки внутри листа. «Как мы ручаемся»: вкладки в одну строку.
Компьютер: убран дубль выбора программы ипотеки слева (выбор — плитками справа); кнопка «Спросить» после первого экрана
сворачивается в круг и разворачивается при наведении.
Run из корня репо после site_v35_searchbtn.py: py -3 tools/patches/site_v36_review.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


# --- иконки в стиле знака: тонкая линия + точка (красная у активного)
ICONS = '''
  <symbol id="t-search" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M15.5 15.5l4.5 4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle class="td" cx="10.5" cy="10.5" r="2"/></symbol>
  <symbol id="t-map" viewBox="0 0 24 24"><path d="M12 21.5s-6.5-6-6.5-11.5a6.5 6.5 0 0 1 13 0c0 5.5-6.5 11.5-6.5 11.5z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle class="td" cx="12" cy="10" r="2.4"/></symbol>
  <symbol id="t-pct" viewBox="0 0 24 24"><path d="M18 5L6 19" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="7" cy="7" r="2.6" fill="none" stroke="currentColor" stroke-width="1.6"/><circle class="td" cx="17" cy="17" r="2.8"/></symbol>
  <symbol id="t-door" viewBox="0 0 24 24"><path d="M4.5 21V10a6 6 0 0 1 12 0v11" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M8.5 21v-9.5a2 2 0 0 1 4 0V21" fill="none" stroke="currentColor" stroke-width="1.6"/><circle class="td" cx="20" cy="19" r="2.2"/></symbol>
  <symbol id="t-chat" viewBox="0 0 24 24"><path d="M4 5.5h16v11H10l-5 4v-4H4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="8.5" cy="11" r="1.1" fill="currentColor"/><circle cx="12" cy="11" r="1.1" fill="currentColor"/><circle class="td" cx="15.5" cy="11" r="1.5"/></symbol>
  <symbol id="t-menu" viewBox="0 0 24 24"><path d="M4 8h16M4 15h10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><circle cx="18.5" cy="15" r="2" fill="#F5553C"/></symbol>
  <symbol id="mark"'''
rep('\n  <symbol id="mark"', ICONS)

i = s.index('<nav class="tabbar"'); j = s.index('</nav>', i) + len('</nav>')
s = s[:i] + '''<nav class="tabbar tb2" id="tabbar" aria-label="Меню приложения">
  <a class="on" href="#search" data-sec="search"><svg class="tic"><use href="#t-search"/></svg><span>Поиск</span></a>
  <a href="#list" data-sec="list" data-map><svg class="tic"><use href="#t-map"/></svg><span>Карта</span></a>
  <a href="#calc" data-sec="calc"><svg class="tic"><use href="#t-pct"/></svg><span>Ипотека</span></a>
  <a href="#cab" data-sec="cab"><svg class="tic"><use href="#t-door"/></svg><span>Кабинет</span></a>
  <a href="#" data-chat><svg class="tic"><use href="#t-chat"/></svg><span>Чат 24/7</span></a>
</nav>
<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Меню" hidden>
  <div class="mn-top"><span class="mn-st"><i></i><span id="mnSt">на связи</span></span><button type="button" class="mn-x" id="mnX" aria-label="Закрыть меню">×</button></div>
  <nav class="mn-l" aria-label="Разделы">
    <a href="#list">Квартиры</a><a href="#houses">Дома</a><a href="#ba">Ремонт</a><a href="#calc">Ипотека</a><a href="#how">Как мы проверяем</a><a href="#rev">Отзывы</a>
  </nav>
  <div class="mn-c">
    <a class="mn-tel" href="tel:+79655002918">+7 965 500-29-18</a>
    <div class="mn-b"><a class="btn red" href="tel:+79655002918">Позвонить</a><button type="button" class="btn ghost" data-chat>Чат 24/7</button></div>
    <a class="mn-cab" href="kabinet.html"><svg viewBox="0 0 76 72" aria-hidden="true"><use href="#mark"/></svg>Личный кабинет</a>
  </div>
</div>''' + s[j:]
rep('<a class="hicon tel-m" href="tel:+79655002918" aria-label="Позвонить: +7 965 500-29-18"><svg class="ico"><use href="#phone"/></svg></a>',
    '<button type="button" class="hicon tel-m" id="mnBtn" aria-label="Открыть меню" aria-expanded="false" aria-controls="mnav"><svg class="ico"><use href="#t-menu"/></svg></button>')
rep('<span><b>Спросить</b><small>ответим 24/7</small></span></button>', '<span class="cf-t"><b>Спросить</b><small>ответим 24/7</small></span></button>')

CSS = r'''
/* v36 — мобильное меню, иконки, правки */
.tic{width:22px;height:22px;color:currentColor}.tic .td{fill:#8A867F;transition:fill .25s}
.tb2 a.on .tic .td,.mn-l a:hover::before{fill:var(--red)}
@media(max-width:800px){
 .tabbar.tb2{left:10px;right:10px;bottom:calc(10px + env(safe-area-inset-bottom));padding:6px;border:0;border-radius:24px;background:#0E0E0Fe6;backdrop-filter:blur(16px) saturate(1.3);-webkit-backdrop-filter:blur(16px) saturate(1.3);box-shadow:0 18px 40px #00000059,inset 0 0 0 1px #ffffff14;justify-content:space-between;transition:transform .35s cubic-bezier(.3,.8,.2,1)}
 .tabbar.tb2.hide{transform:translateY(calc(100% + 24px))}
 .tb2 a{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;gap:3px;padding:8px 2px 6px;border-radius:18px;color:#A9A49B;font-size:10px;font-weight:600;position:relative;transition:color .2s,background .2s}
 .tb2 a.on{color:#fff;background:#ffffff12}
 .tb2 a.on::after{content:'';position:absolute;top:4px;right:calc(50% - 16px);width:5px;height:5px;border-radius:50%;background:var(--red)}
 .tb2 a.on .tic .td{fill:var(--red)}
 .tb2 a:active{transform:scale(.94)}
 footer{padding-bottom:120px}
 .chat{z-index:60}
 /* шапка — кнопка меню */
 #mnBtn{cursor:pointer}
}
.mnav{position:fixed;inset:0;z-index:70;background:var(--night);color:var(--milk);display:flex;flex-direction:column;padding:max(16px,env(safe-area-inset-top)) 22px max(22px,env(safe-area-inset-bottom));overflow:auto}
.mnav[hidden]{display:none}
.mnav:not([hidden]){animation:mnin .35s cubic-bezier(.2,.8,.2,1)}
@keyframes mnin{from{transform:translateY(-12px)}to{transform:none}}
.mn-top{display:flex;align-items:center;justify-content:space-between;height:56px}
.mn-st{display:flex;align-items:center;gap:8px;font-size:13px;color:#A9A49B}.mn-st i{width:7px;height:7px;border-radius:50%;background:#2FB36B;animation:livep 2s infinite}
.mn-x{width:46px;height:46px;border-radius:50%;border:1px solid #ffffff2e;background:#ffffff12;color:#fff;font-size:22px;cursor:pointer}
.mn-l{display:flex;flex-direction:column;margin-top:18px}
.mn-l a{display:flex;align-items:center;gap:14px;font:300 38px/1.15 Manrope;letter-spacing:-.04em;padding:10px 0;border-bottom:1px solid #ffffff14;opacity:0;transform:translateY(10px);animation:mnit .45s cubic-bezier(.2,.8,.2,1) forwards}
.mn-l a::after{content:'';width:9px;height:9px;border-radius:50%;background:var(--red);margin-left:auto;opacity:0;transition:opacity .2s}
.mn-l a:hover::after,.mn-l a:focus-visible::after{opacity:1}
.mn-l a:nth-child(2){animation-delay:.04s}.mn-l a:nth-child(3){animation-delay:.08s}.mn-l a:nth-child(4){animation-delay:.12s}.mn-l a:nth-child(5){animation-delay:.16s}.mn-l a:nth-child(6){animation-delay:.2s}
@keyframes mnit{to{opacity:1;transform:none}}
.mn-c{margin-top:auto;padding-top:28px;display:grid;gap:12px}
.mn-tel{font:600 26px Manrope;letter-spacing:-.01em}
.mn-b{display:grid;grid-template-columns:1fr 1fr;gap:8px}.mn-b .btn.ghost{background:#ffffff12;border-color:#ffffff2e;color:#fff}
.mn-cab{display:flex;align-items:center;gap:10px;font-weight:700;padding:14px 16px;border-radius:18px;background:#ffffff0d}.mn-cab svg{width:22px;height:21px;fill:#fff}
html.mn-lock,html.mn-lock body{overflow:hidden}
/* договор: галочки внутри листа */
.desk.fold .cl li{grid-template-columns:46px 1fr}.desk.fold .cl li span{padding-left:16px}
.desk.fold .cl li span::after{left:0}
/* вкладки «Как мы ручаемся» в одну строку */
.scan .ctabs{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}.scan .ctabs::-webkit-scrollbar{display:none}.scan .ctabs button{white-space:nowrap;flex:none}
/* ипотека: без дубля выбора программы */
.cin>div:has(> #rates){display:none}
/* кнопка чата сворачивается в круг */
.chatfab .cf-t{display:block;max-width:160px;overflow:hidden;white-space:nowrap;transition:max-width .35s cubic-bezier(.3,.8,.2,1),opacity .25s}
.chatfab.mini{padding:10px;gap:0}.chatfab.mini .cf-t{max-width:0;opacity:0}
.chatfab.mini:hover,.chatfab.mini:focus-visible{padding:12px 22px 12px 14px;gap:12px}.chatfab.mini:hover .cf-t,.chatfab.mini:focus-visible .cf-t{max-width:160px;opacity:1}
@media(prefers-reduced-motion:reduce){.mnav:not([hidden]),.mn-l a{animation:none;opacity:1;transform:none}.tabbar.tb2{transition:none}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

rep("function onScroll() { hdr.classList.toggle('sc', scrollY > 10); fab.classList.toggle('show', scrollY > $('.hero').offsetHeight * .6); }",
    "function onScroll() { hdr.classList.toggle('sc', scrollY > 10); fab.classList.toggle('show', scrollY > $('.hero').offsetHeight * .6); fab.classList.toggle('mini', scrollY > $('.hero').offsetHeight * 1.4); }")

JS = r'''
// мобильное меню: капсула снизу и полноэкранная навигация
(() => {
  const tb = $('#tabbar'), mn = $('#mnav'), mb = $('#mnBtn'); let lastY = scrollY;
  addEventListener('scroll', () => { const y = scrollY, d = y - lastY;
    if (Math.abs(d) > 6) { tb.classList.toggle('hide', d > 0 && y > 300); lastY = y; } }, {passive: true});
  const links = $$('a[data-sec]', tb);
  const spy = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) links.forEach(a => a.classList.toggle('on', a.dataset.sec === e.target.id)); }), {rootMargin: '-45% 0px -50% 0px'});
  links.forEach(a => { const t = document.getElementById(a.dataset.sec); if (t) spy.observe(t); });
  $('[data-map]', tb).addEventListener('click', () => { if (innerWidth <= 800 && !$('.res').classList.contains('showmap')) $('#mapBtn').click(); });
  function openMn(o) { mn.hidden = !o; mb.setAttribute('aria-expanded', o); document.documentElement.classList.toggle('mn-lock', o);
    if (o) { const st = $('#hbStatus'); $('#mnSt').textContent = st ? st.textContent : 'на связи'; $('#mnX').focus(); } else mb.focus(); }
  mb.addEventListener('click', () => openMn(true)); $('#mnX').addEventListener('click', () => openMn(false));
  $$('.mn-l a, .mn-c [data-chat], .mn-cab', mn).forEach(a => a.addEventListener('click', () => openMn(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !mn.hidden) openMn(false); });
})();
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')

# дубли id: иконки <symbol id="search|calc"> перехватывали якоря #search/#calc (ссылка «Ипотека» вела наверх)
s = open(P + 'index.html', encoding='utf8').read()
for k in ('search', 'calc'):
    s = s.replace(f'<symbol id="{k}"', f'<symbol id="i-{k}"').replace(f'<use href="#{k}"/>', f'<use href="#i-{k}"/>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ids ok')
