"""Сайт v30 — правая часть меню: единая панель вместо отдельных кнопок.
[ ● на связи · Екб 14:32 / +7 965 500-29-18 ▾ | ⇅ 2 | ♡ 2 | (П.) Кабинет ]
Телефон раскрывает меню: «Позвонить», «Перезвоним за 30 секунд» (поле телефона с маской → подтверждение),
«Написать в чат», часы работы. Статус и часы — по времени Екатеринбурга (UTC+5): 9–21 «на связи», иначе «перезвоним с 9:00».
Run из корня репо после site_v29_photo.py: py -3 tools/patches/site_v30_header.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''  <a class="btn hcab" href="kabinet.html"><svg class="ico" style="width:18px;height:18px"><use href="#user"/></svg>Кабинет</a>
  <a class="tel" href="tel:+79655002918">+7 965 500-29-18<small><i class="live-dot"></i>на связи до 21:00</small></a>
  <button class="hicon hide-m" id="cmpBtn" aria-label="Сравнение"><svg class="ico"><use href="#cmp"/></svg><span class="cnt" id="cmpCnt">0</span></button>
  <a class="hicon tel-m" href="tel:+79655002918" aria-label="Позвонить: +7 965 500-29-18"><svg class="ico"><use href="#phone"/></svg></a>
  <button class="hicon" id="favBtn" aria-label="Избранное"><svg class="ico"><use href="#heart"/></svg><span class="cnt" id="favCnt">0</span></button>''',
'''  <a class="hicon tel-m" href="tel:+79655002918" aria-label="Позвонить: +7 965 500-29-18"><svg class="ico"><use href="#phone"/></svg></a>
  <div class="hb" role="group" aria-label="Связь, сравнение, избранное и кабинет">
    <div class="hb-call">
      <button type="button" class="hb-ph" id="hbPh" aria-expanded="false" aria-controls="hbPop">
        <span class="hb-st"><i class="hb-dot" id="hbDot"></i><span id="hbStatus">на связи</span><span class="hb-clk">Екб <b id="hbClk">--:--</b></span></span>
        <span class="hb-num">+7 965 500-29-18<svg class="hb-car" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3"/></svg></span>
      </button>
      <div class="hb-pop" id="hbPop" hidden>
        <a class="hb-it" href="tel:+79655002918"><span class="hb-i"><svg class="ico"><use href="#phone"/></svg></span><span><b>Позвонить</b><small>+7 965 500-29-18</small></span></a>
        <form class="hb-cb" id="hbCb" novalidate><label for="hbTel"><b>Перезвоним за 30 секунд</b><small id="hbCbNote">Оставьте номер — менеджер наберёт сам</small></label>
          <div class="hb-row"><input id="hbTel" type="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__"><button type="submit" aria-label="Заказать звонок"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4.5L12 8l-3.5 3.5"/></svg></button></div></form>
        <button type="button" class="hb-it" data-chat><span class="hb-i"><svg class="ico"><use href="#msg"/></svg></span><span><b>Написать в чат</b><small>отвечаем сразу, 24/7</small></span></button>
        <div class="hb-hrs"><span>Офис</span><span>ежедневно 9:00–21:00</span></div>
      </div>
    </div>
    <span class="hb-sep" aria-hidden="true"></span>
    <button type="button" class="hb-ic" id="cmpBtn" aria-label="Сравнение" title="Сравнение"><svg class="ico"><use href="#cmp"/></svg><span class="cnt" id="cmpCnt">0</span></button>
    <button type="button" class="hb-ic" id="favBtn" aria-label="Избранное" title="Избранное"><svg class="ico"><use href="#heart"/></svg><span class="cnt" id="favCnt">0</span></button>
    <span class="hb-sep" aria-hidden="true"></span>
    <a class="hb-cab" href="kabinet.html"><span class="hb-av"><svg viewBox="0 0 76 72" aria-hidden="true"><use href="#mark"/></svg></span><span>Кабинет</span></a>
  </div>''')

CSS = r'''
/* v30 — панель справа в меню */
.hb{display:flex;align-items:center;gap:2px;height:48px;padding:3px;border-radius:999px;background:#fff;border:1px solid var(--line);transition:background .35s,border-color .35s}
header.ontop .hb{background:#ffffff14;border-color:#ffffff2e}
.hb-sep{width:1px;height:22px;background:var(--line);margin:0 4px}header.ontop .hb-sep{background:#ffffff2e}
.hb-call{position:relative}
.hb-ph{all:unset;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center;height:40px;padding:0 14px 0 16px;border-radius:999px;cursor:pointer;transition:background .2s}
.hb-ph:hover,.hb-ph[aria-expanded=true]{background:var(--soft)}header.ontop .hb-ph:hover,header.ontop .hb-ph[aria-expanded=true]{background:#ffffff1a}
.hb-ph:focus-visible{outline:2px solid var(--red);outline-offset:2px}
.hb-st{display:flex;align-items:center;gap:6px;font-size:10.5px;font-weight:600;color:var(--mut);line-height:1}
header.ontop .hb-st{color:#ffffffa6}
.hb-dot{width:6px;height:6px;border-radius:50%;background:#2FB36B;box-shadow:0 0 0 0 #2FB36B88;animation:livep 2s infinite}
.hb-dot.off{background:#C9C5BE;animation:none}
.hb-clk{font-variant-numeric:tabular-nums;padding-left:6px;border-left:1px solid currentColor;border-color:#0000001f}header.ontop .hb-clk{border-color:#ffffff33}
.hb-clk b{font-weight:700;color:inherit}
.hb-num{display:flex;align-items:center;gap:6px;font-size:15px;font-weight:700;margin-top:3px;font-variant-numeric:tabular-nums;letter-spacing:.01em}
.hb-car{width:12px;height:12px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;transition:transform .25s;opacity:.7}
.hb-ph[aria-expanded=true] .hb-car{transform:rotate(180deg)}
.hb-ic{all:unset;box-sizing:border-box;position:relative;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:background .2s}
.hb-ic:hover{background:var(--soft)}header.ontop .hb-ic:hover{background:#ffffff1a}.hb-ic:focus-visible{outline:2px solid var(--red)}
.hb-ic .ico{width:19px;height:19px}
.hb-ic .cnt{position:absolute;top:3px;right:2px;min-width:16px;height:16px;border-radius:8px;background:var(--red-ui);color:#fff;font-size:9.5px;font-weight:800;display:none;align-items:center;justify-content:center;padding:0 4px;box-shadow:0 0 0 2px #fff}
header.ontop .hb-ic .cnt{box-shadow:none}.hb-ic .cnt.on{display:flex}
.hb-cab{display:flex;align-items:center;gap:9px;height:40px;padding:0 16px 0 4px;border-radius:999px;background:var(--ink);color:#fff;font-size:14px;font-weight:700;transition:background .2s,transform .15s}
.hb-cab:hover{background:#000}header.ontop .hb-cab{background:#fff;color:var(--ink)}header.ontop .hb-cab:hover{background:var(--milk)}
.hb-av{width:32px;height:32px;border-radius:50%;background:#ffffff1a;display:flex;align-items:center;justify-content:center}
header.ontop .hb-av{background:var(--ink)}
.hb-av svg{width:15px;height:14px;fill:#fff}
.hb-pop{position:absolute;right:-6px;top:calc(100% + 14px);width:320px;background:#fff;color:var(--ink);border-radius:22px;padding:8px;box-shadow:0 24px 60px #00000038,0 0 0 1px #0000000a;z-index:5;transform-origin:top right;animation:hbin .22s cubic-bezier(.2,.8,.2,1)}
.hb-pop[hidden]{display:none}
@keyframes hbin{from{transform:translateY(-8px) scale(.97)}to{transform:none}}
.hb-it{all:unset;box-sizing:border-box;display:flex;align-items:center;gap:12px;width:100%;padding:10px;border-radius:14px;cursor:pointer}
.hb-it:hover,.hb-it:focus-visible{background:var(--soft)}
.hb-i{width:40px;height:40px;border-radius:12px;background:var(--soft);display:flex;align-items:center;justify-content:center;flex:none}
.hb-it:first-child .hb-i{background:var(--red-ui);color:#fff}
.hb-it b,.hb-cb b{display:block;font-size:14px}.hb-it small,.hb-cb small{display:block;font-size:12px;color:var(--mut);margin-top:1px}
.hb-cb{margin:4px 0;padding:12px 10px;border-radius:14px;background:var(--soft)}
.hb-row{display:flex;gap:6px;margin-top:10px}
.hb-row input{flex:1;min-width:0;height:42px;border:1px solid var(--line);border-radius:12px;padding:0 12px;font:600 14px Manrope;outline:none;background:#fff}
.hb-row input:focus{border-color:var(--ink)}.hb-cb.bad input{border-color:#E0442C;background:#FFF5F3}
.hb-row button{width:42px;height:42px;border:0;border-radius:12px;background:var(--ink);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;flex:none}
.hb-row button svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.hb-cb.sent .hb-row{display:none}.hb-cb.sent b::before{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;background:#2FB36B;margin-right:8px;vertical-align:1px}
.hb-hrs{display:flex;justify-content:space-between;padding:10px 10px 6px;font-size:12px;color:var(--mut);border-top:1px solid #0000000d;margin-top:4px}
@media(max-width:1300px){.hb-st{display:none}.hb-num{margin:0}}
@media(max-width:1200px){.hb-cab span:last-child{display:none}.hb-cab{padding:0 4px}}
@media(max-width:800px){.hb-call,.hb-sep,#cmpBtn,.hb-cab{display:none}.hb{height:auto;padding:0;border:0;background:none!important}.hb-ic{width:46px;height:46px;border:1px solid var(--line);background:#fff}header.ontop .hb-ic{background:#ffffff1f;border-color:#ffffff40;color:#fff}}
@media(prefers-reduced-motion:reduce){.hb-dot{animation:none}.hb-pop{animation:none}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

JS = r'''
// панель связи в меню
(() => {
  const ph = $('#hbPh'), pop = $('#hbPop'), cb = $('#hbCb'), inp = $('#hbTel');
  const ekb = () => { const d = new Date(), u = d.getTime() + d.getTimezoneOffset() * 6e4; return new Date(u + 5 * 36e5); };
  function clock() { const t = ekb(), h = t.getHours(), open = h >= 9 && h < 21;
    $('#hbClk').textContent = String(h).padStart(2, '0') + ':' + String(t.getMinutes()).padStart(2, '0');
    $('#hbStatus').textContent = open ? 'на связи' : 'перезвоним с 9:00'; $('#hbDot').classList.toggle('off', !open);
    $('#hbCbNote').textContent = cb.classList.contains('sent') ? $('#hbCbNote').textContent : open ? 'Оставьте номер — менеджер наберёт сам' : 'Сейчас офис закрыт — позвоним в 9:00'; }
  clock(); setInterval(clock, 15000);
  function open(o) { pop.hidden = !o; ph.setAttribute('aria-expanded', o); if (o) setTimeout(() => inp.focus(), 50); }
  ph.addEventListener('click', e => { e.stopPropagation(); open(pop.hidden); });
  pop.addEventListener('click', e => e.stopPropagation());
  document.addEventListener('click', () => open(false));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !pop.hidden) { open(false); ph.focus(); } });
  $$('[data-chat]', pop).forEach(b => b.addEventListener('click', () => open(false)));
  inp.addEventListener('input', () => { cb.classList.remove('bad'); let d = inp.value.replace(/\D/g, ''); if (!d) { inp.value = ''; return; }
    if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; const p = d.slice(1, 11);
    inp.value = '+7' + (p.length ? ' (' + p.slice(0, 3) : '') + (p.length > 3 ? ') ' + p.slice(3, 6) : '') + (p.length > 6 ? '-' + p.slice(6, 8) : '') + (p.length > 8 ? '-' + p.slice(8, 10) : ''); });
  cb.addEventListener('submit', e => { e.preventDefault();
    if (inp.value.replace(/\D/g, '').length !== 11) { cb.classList.add('bad'); inp.focus(); return; }
    const h = ekb().getHours(), openNow = h >= 9 && h < 21; cb.classList.add('sent');
    $('#hbCbNote').textContent = openNow ? `Звоним на ${inp.value} — держите телефон рядом` : `Позвоним на ${inp.value} завтра в 9:00`;
    cb.querySelector('b').textContent = openNow ? 'Уже набираем' : 'Заявка принята';
    toast(openNow ? 'Перезвоним в течение 30 секунд' : 'Перезвоним завтра в 9:00'); });
})();
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
