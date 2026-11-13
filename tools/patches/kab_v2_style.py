"""Кабинет v2 — стиль основной страницы: плавающая капсула сверху (статус и время Екб, «Выйти», аватар; на телефоне — логотип и
кнопка меню), заголовок объекта «[ ● Мой дом ]» + крупное светлое название с точкой, иконки в стиле точки (как в меню сайта),
нижнее меню телефона — тёмная плавающая капсула, полноэкранная навигация по кнопке меню.
Run из корня репо: py -3 tools/patches/kab_v2_style.py  (исходник — 08_Сайт_пример/kabinet_v1.html)"""
P = '08_Сайт_пример/'
s = open(P + 'kabinet_v1.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


ICONS = '''  <symbol id="t-door" viewBox="0 0 24 24"><path d="M4.5 21V10a6 6 0 0 1 12 0v11" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M8.5 21v-9.5a2 2 0 0 1 4 0V21" fill="none" stroke="currentColor" stroke-width="1.6"/><circle class="td" cx="20" cy="19" r="2.2"/></symbol>
  <symbol id="t-cam" viewBox="0 0 24 24"><rect x="2.5" y="6.5" width="13.5" height="11" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M16 10.5l5-3v9l-5-3" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle class="td" cx="6.5" cy="10.5" r="1.8"/></symbol>
  <symbol id="t-act" viewBox="0 0 24 24"><path d="M6 3.5h8l4 4V20.5H6z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M8.8 13.5l2 2 3.5-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><circle class="td" cx="18" cy="19" r="2.4"/></symbol>
  <symbol id="t-pct" viewBox="0 0 24 24"><path d="M18 5L6 19" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="7" cy="7" r="2.6" fill="none" stroke="currentColor" stroke-width="1.6"/><circle class="td" cx="17" cy="17" r="2.8"/></symbol>
  <symbol id="t-doc" viewBox="0 0 24 24"><path d="M5.5 3.5h9l4 4V20.5h-13z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M8.5 11.5h7M8.5 15h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle class="td" cx="16.5" cy="15" r="1.6"/></symbol>
  <symbol id="t-chat" viewBox="0 0 24 24"><path d="M4 5.5h16v11H10l-5 4v-4H4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="8.5" cy="11" r="1.1" fill="currentColor"/><circle cx="12" cy="11" r="1.1" fill="currentColor"/><circle class="td" cx="15.5" cy="11" r="1.5"/></symbol>
  <symbol id="t-menu" viewBox="0 0 24 24"><path d="M4 8h16M4 15h10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><circle cx="18.5" cy="15" r="2" fill="#F5553C"/></symbol>
  <symbol id="mark"'''
rep('  <symbol id="mark"', ICONS)
rep("const NAV = [['home', 'Обзор', 'i-home'], ['cams', 'Камеры', 'i-cam'], ['steps', 'Этапы и акты', 'i-act'], ['pay', 'Платежи', 'i-pay'], ['docs', 'Документы', 'i-doc'], ['chat', 'Чат', 'i-chat']];",
    "const NAV = [['home', 'Обзор', 't-door'], ['cams', 'Камеры', 't-cam'], ['steps', 'Этапы и акты', 't-act'], ['pay', 'Платежи', 't-pct'], ['docs', 'Документы', 't-doc'], ['chat', 'Чат', 't-chat']];")
rep('<svg class="ico"><use href="#${n[2]}"/></svg>${n[1]}${n[0] === \'steps\'', '<svg class="tic"><use href="#${n[2]}"/></svg>${n[1]}${n[0] === \'steps\'')
rep('<svg class="ico"><use href="#${n[2]}"/></svg>${n[1].split(\' \')[0]}</button>', '<svg class="tic"><use href="#${n[2]}"/></svg><span>${n[1].split(\' \')[0]}</span></button>')

rep('<div class="top"><div><h1 id="tName"></h1><small id="tSub"></small></div><span class="sp"></span><button class="out" id="logout" type="button">Выйти</button><span class="av" title="Анна">А</span></div>',
    '''<div class="top"><div class="top-in">
      <a class="lg-m" href="index.html" aria-label="На сайт"><svg viewBox="0 0 76 72" aria-hidden="true"><use href="#mark"/></svg><span><b>ПЛАТФОРМА</b><small>НЕДВИЖИМОСТИ</small></span></a>
      <span class="st"><i id="stDot"></i><span id="stTxt">на связи</span><span class="clk">Екб <b id="stClk">--:--</b></span></span>
      <span class="sp"></span>
      <a class="mgr" href="tel:+79655002918">Ольга, менеджер<small>+7 965 500-29-18</small></a>
      <button class="out" id="logout" type="button">Выйти</button>
      <button type="button" class="mn-b" id="mnBtn" aria-label="Открыть меню" aria-expanded="false" aria-controls="mnav"><svg class="tic"><use href="#t-menu"/></svg></button>
      <span class="av" title="Анна">А</span></div></div>
    <div class="phd"><div class="br">[ <b>●</b> <span id="tKind">Мой дом</span> ]</div><h1 id="tName"></h1><small id="tSub"></small></div>''')
rep("$('#tName').textContent = o.name; $('#tSub').textContent = o.sub;",
    "$('#tName').textContent = o.name; $('#tSub').textContent = o.sub; $('#tKind').textContent = cur === 'house' ? 'Мой дом' : 'Мой ремонт';")

rep('<dialog id="dlg"', '''<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Меню кабинета" hidden>
  <div class="mn-top"><span class="st"><i></i><span id="mnSt">на связи</span></span><button type="button" class="mn-x" id="mnX" aria-label="Закрыть меню">×</button></div>
  <div class="mn-k">Мои объекты</div><div class="mn-o"><button type="button" data-obj="house">Северный Урал 235</button><button type="button" data-obj="reno">Ремонт квартиры</button></div>
  <nav class="mn-l" aria-label="Разделы"><button type="button" data-go="home">Обзор</button><button type="button" data-go="cams">Камеры</button><button type="button" data-go="steps">Этапы и акты</button><button type="button" data-go="pay">Платежи</button><button type="button" data-go="docs">Документы</button><button type="button" data-go="chat">Чат</button></nav>
  <div class="mn-c"><a class="mn-tel" href="tel:+79655002918">+7 965 500-29-18</a><div class="mn-bb"><a href="index.html">На сайт</a><button type="button" id="mnOut">Выйти</button></div></div>
</div>
<dialog id="dlg"''')

CSS = r'''
/* v2 — стиль основной страницы */
.tic{width:22px;height:22px;flex:none;color:currentColor}.tic .td{fill:#8A867F;transition:fill .25s}
.snav button[aria-current=page] .tic .td,.tabs button[aria-current=page] .tic .td{fill:var(--red)}
.snav button .tic{width:20px;height:20px}
.br{font-size:12px;letter-spacing:.06em;color:var(--mut)}.br b{color:var(--red);font-weight:600}
.top{position:sticky;top:0;z-index:15;padding:14px 0 6px;background:none;backdrop-filter:none;display:block}
.top-in{display:flex;align-items:center;gap:10px;height:60px;padding:0 8px 0 22px;border-radius:999px;background:#F4F2EEe6;backdrop-filter:blur(18px) saturate(1.4);-webkit-backdrop-filter:blur(18px) saturate(1.4);box-shadow:0 12px 34px #0000001a,inset 0 0 0 1px #ffffffb3}
.lg-m{display:none;align-items:center;gap:10px}.lg-m svg{width:30px;height:28px;fill:var(--ink)}.lg-m b{display:block;font:300 12px/1 Manrope;letter-spacing:.42em}.lg-m small{display:block;font:400 6.6px/1 Manrope;letter-spacing:.5em;color:var(--mut);margin-top:5px}
.st{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:600;color:var(--mut)}
.st i{width:7px;height:7px;border-radius:50%;background:#2FB36B;box-shadow:0 0 0 0 #2FB36B88;animation:livep 2s infinite}.st i.off{background:#C9C5BE;animation:none}
@keyframes livep{70%{box-shadow:0 0 0 7px #2FB36B00}100%{box-shadow:0 0 0 0 #2FB36B00}}
.st .clk{padding-left:8px;border-left:1px solid #0000001f;font-variant-numeric:tabular-nums}.st .clk b{color:var(--ink)}
.top .sp{flex:1}
.mgr{font-size:13px;font-weight:700;text-align:right;line-height:1.2;padding:0 8px}.mgr small{display:block;font-size:11px;font-weight:500;color:var(--mut)}
.out{border:0;background:#16161712;border-radius:999px;padding:0 18px;height:44px;font-weight:700;font-size:13px}.out:hover{background:#1616171f}
.mn-b{display:none;width:44px;height:44px;border-radius:50%;border:0;background:#16161712;align-items:center;justify-content:center;color:var(--ink)}
.av{width:44px;height:44px}
.phd{padding:26px 0 18px}
.phd h1{font:300 clamp(34px,3.4vw,58px)/1.02 Manrope;letter-spacing:-.045em;margin:12px 0 0}
.phd h1::after{content:'';display:inline-block;width:.15em;height:.15em;border-radius:50%;background:var(--red);margin-left:.05em}
.phd small{display:block;color:var(--mut);font-size:14px;margin-top:8px}
.side{padding:26px 16px}
.mnav{position:fixed;inset:0;z-index:70;background:var(--night);color:var(--milk);display:flex;flex-direction:column;padding:max(16px,env(safe-area-inset-top)) 22px max(22px,env(safe-area-inset-bottom));overflow:auto}
.mnav[hidden]{display:none}.mnav:not([hidden]){animation:mnin .35s cubic-bezier(.2,.8,.2,1)}@keyframes mnin{from{transform:translateY(-12px)}to{transform:none}}
.mn-top{display:flex;align-items:center;justify-content:space-between;height:56px}.mn-top .st{color:#A9A49B}
.mn-x{width:46px;height:46px;border-radius:50%;border:1px solid #ffffff2e;background:#ffffff12;color:#fff;font-size:22px}
.mn-k{font-size:12px;color:#8A867F;margin:16px 0 8px}
.mn-o{display:flex;gap:6px;flex-wrap:wrap}.mn-o button{border:1px solid #ffffff2e;background:#ffffff0d;color:#fff;border-radius:999px;padding:10px 16px;font-weight:600;font-size:14px}
.mn-l{display:flex;flex-direction:column;margin-top:18px}
.mn-l button{all:unset;cursor:pointer;display:flex;align-items:center;font:300 34px/1.15 Manrope;letter-spacing:-.04em;padding:9px 0;border-bottom:1px solid #ffffff14}
.mn-l button::after{content:'';width:9px;height:9px;border-radius:50%;background:var(--red);margin-left:auto;opacity:0}.mn-l button.cur::after{opacity:1}
.mn-c{margin-top:auto;padding-top:24px;display:grid;gap:12px}.mn-tel{font:600 24px Manrope}
.mn-bb{display:grid;grid-template-columns:1fr 1fr;gap:8px}.mn-bb a,.mn-bb button{display:flex;align-items:center;justify-content:center;height:50px;border-radius:999px;border:1px solid #ffffff2e;background:#ffffff12;color:#fff;font-weight:700;font-size:14px}
html.mn-lock,html.mn-lock body{overflow:hidden}
@media(max-width:1000px){
 .top{padding:10px 0 4px}.top-in{height:56px;padding:0 6px 0 14px;gap:6px}
 .lg-m{display:flex}.st,.mgr,.out{display:none}.mn-b{display:flex;width:40px;height:40px}.av{width:40px;height:40px;font-size:14px}
 .phd{padding:18px 2px 14px}.phd h1{font-size:36px}
 .tabs{left:10px;right:10px;bottom:calc(10px + env(safe-area-inset-bottom));padding:6px;border:0;border-radius:24px;background:#0E0E0Fe6;backdrop-filter:blur(16px) saturate(1.3);-webkit-backdrop-filter:blur(16px) saturate(1.3);box-shadow:0 18px 40px #00000059,inset 0 0 0 1px #ffffff14;justify-content:space-between}
 .tabs button{flex:1;min-width:0;color:#A9A49B;gap:3px;padding:8px 0 6px;border-radius:18px;position:relative}
 .tabs button[aria-current=page]{color:#fff;background:#ffffff12}.tabs button[aria-current=page] svg{stroke:none}
 .tabs button[aria-current=page]::after{content:'';position:absolute;top:4px;right:calc(50% - 15px);width:5px;height:5px;border-radius:50%;background:var(--red)}
 .main{padding-bottom:110px}
}
@media(prefers-reduced-motion:reduce){.st i{animation:none}.mnav:not([hidden]){animation:none}}
'''
rep('@media(prefers-reduced-motion:reduce)', CSS + '@media(prefers-reduced-motion:reduce)')

JS = r'''
// v2: статус, часы Екб, меню
(() => {
  const ekb = () => { const d = new Date(); return new Date(d.getTime() + d.getTimezoneOffset() * 6e4 + 5 * 36e5); };
  function clock() { const t = ekb(), h = t.getHours(), on = h >= 9 && h < 21, txt = on ? 'на связи' : 'ответим с 9:00';
    $('#stClk').textContent = String(h).padStart(2, '0') + ':' + String(t.getMinutes()).padStart(2, '0');
    $('#stTxt').textContent = txt; $('#mnSt').textContent = 'прораб и менеджер ' + txt; $('#stDot').classList.toggle('off', !on); }
  clock(); setInterval(clock, 15000);
  const mn = $('#mnav'), mb = $('#mnBtn');
  function openMn(o) { mn.hidden = !o; mb.setAttribute('aria-expanded', o); document.documentElement.classList.toggle('mn-lock', o);
    if (o) { $$('.mn-l button', mn).forEach(b => b.classList.toggle('cur', b.dataset.go === view)); $$('.mn-o button', mn).forEach(b => b.style.background = b.dataset.obj === cur ? '#ffffff2e' : ''); $('#mnX').focus(); } }
  mb.addEventListener('click', () => openMn(true)); $('#mnX').addEventListener('click', () => openMn(false));
  mn.addEventListener('click', e => { if (e.target.closest('[data-go],[data-obj]')) setTimeout(() => openMn(false), 0); });
  $('#mnOut').addEventListener('click', () => { openMn(false); $('#logout').click(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !mn.hidden) openMn(false); });
})();
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'kabinet.html', 'w', encoding='utf8').write(s)
print('ok')
