"""Сайт v20 — по замечаниям заказчика:
1) Верхнее меню — плавающая капсула: на первом экране тёмное стекло поверх фото, при прокрутке светлая; красная точка
   скользит под пунктами (за курсором и за разделом на экране); у телефона — индикатор «на связи».
2) Поиск на первом экране: выпадающие подсказки цены (пресеты) и района/ЖК (со счётчиком квартир, клавиатура),
   быстрые фильтры вместо пустого переключателя «только проверенные».
3) Карточка «ЖК проверен» — живая: перебирает проверенные ЖК, галочки ставятся по одной, «Проверен» + ссылка
   на квартиры этого ЖК; точки-переключатели, пауза при наведении.
4) Ремонт: одна комната «до/после» на одном кадре во всю ширину (photo/ba_before.jpg / ba_after.jpg — RealVisXL img2img
   + inpaint по маске пола, геометрия совпадает), этапы ремонта привязаны к шторке; при появлении шторка один раз
   проходит сама.
5) MacBook + iPhone в кабинете — без 3D-слоёв (давали артефакты), наклон через perspective() в transform.
Run из корня репо после site_v19_devices.py: py -3 tools/patches/site_v20_hero.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


def cut(a, b, new, keep_b=True):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + (s[j:] if keep_b else s[j + len(b):])


# --- 5) устройства без 3D-слоёв; класс .devs уже занят чипами застройщиков (их стиль span ломал корпуса) → .dvx
rep('<a class="devs" id="devs"', '<a class="dvx" id="devs"')
for a in ('.devs{display:block;position:relative;perspective', '.devs.move .stage', '.devs.move .iph', '.devs:not(.move) .iph', '.devs:hover .devcap,.devs:focus-visible .devcap',
          '.devs{max-width:820px', '.devs .iph{animation'):
    rep(a, a.replace('.devs', '.dvx'))
rep('.dvx{display:block;position:relative;perspective:1600px;', '.dvx{display:block;position:relative;')
rep('transform-style:preserve-3d;transform:rotateX(var(--rx)) rotateY(var(--ry));', 'transform:perspective(1500px) rotateX(var(--rx)) rotateY(var(--ry));')
rep('.mbp{position:absolute;left:0;top:4%;width:88%;display:block;transform:translateZ(0)}', '.mbp{position:absolute;left:0;top:4%;width:88%;display:block}')
rep('transform:translateZ(90px) translate(var(--px),var(--py));', 'transform:translate(var(--px),var(--py));')
rep('transform:translateZ(-40px);filter:blur(6px)}', 'filter:blur(6px)}')

# --- 1) меню-капсула
rep('<nav class="main" aria-label="Разделы">', '<nav class="main" aria-label="Разделы"><i class="nd" aria-hidden="true"></i>')
rep('<a class="tel" href="tel:+79655002918">+7 965 500-29-18<small>Екатеринбург, ежедневно</small></a>',
    '<a class="tel" href="tel:+79655002918">+7 965 500-29-18<small><i class="live-dot"></i>на связи до 21:00</small></a>')
rep('<header>', '<header class="ontop">')

# --- 2) поиск
rep('<div class="f"><label for="pr">Цена до, млн ₽</label><input id="pr" placeholder="например, 8" inputmode="decimal"></div>',
    '<div class="f dd-wrap"><label for="pr">Цена до, млн ₽</label><input id="pr" placeholder="любая" inputmode="decimal" autocomplete="off" aria-controls="prDD"><div class="dd" id="prDD" role="listbox" hidden></div></div>')
rep('<input id="ad" placeholder="Академический, ЖК…" list="adList" autocomplete="off"><datalist id="adList"></datalist></div>',
    '<input id="ad" placeholder="Академический, ЖК…" autocomplete="off" aria-controls="adDD" aria-autocomplete="list"><datalist id="adList"></datalist><div class="dd" id="adDD" role="listbox" hidden></div></div>')
rep('<div class="f"><label for="ad">', '<div class="f dd-wrap"><label for="ad">')
rep('<div class="sline"><button class="sw" role="switch" aria-checked="true" aria-label="Только проверенные"></button>Только проверенные застройщики<a href="#list">',
    '<div class="sline"><span class="qf" role="group" aria-label="Быстрые фильтры"><button type="button" aria-pressed="false" data-qf="ready">Готовые</button><button type="button" aria-pressed="false" data-qf="fin">С отделкой</button><button type="button" aria-pressed="false" data-qf="fam">Семейная ипотека</button><button type="button" aria-pressed="false" data-qf="deal">Спецпредложения</button></span><a href="#list">')
cut("$('.sw').addEventListener('click'", "\n", '', keep_b=False)

# --- 3) живая карточка ЖК
cut('<div class="chipv"><h3><i></i>ЖК Липовый сквер — проверен</h3>', '<div class="w hin">',
    '<div class="chipv" id="chipv" aria-live="polite"><div class="cv-h"><span class="cv-st" id="cvSt">Проверяем</span><span class="cv-dots" id="cvDots"></span></div>'
    '<h3 id="cvName"></h3><small id="cvSub"></small><ul id="cvList"></ul><a class="cv-go" id="cvGo" href="#list"></a></div>\n  ')

# --- 4) ремонт
cut('    <div class="ba" id="baBox">', '  <div class="calc" style="margin-top:40px">', '''    <div class="ba wide" id="baBox"><img src="photo/ba_before.jpg" alt="Квартира без отделки: бетон, большие окна"><img class="after" src="photo/ba_after.jpg" alt="Та же квартира после нашего ремонта: гостиная с диваном"><span class="hdl" id="baH"></span><span class="l1">До</span><span class="l2">После</span>
      <span class="bacap">Одна и та же комната · 63 м² · 9 недель</span><input type="range" min="0" max="100" value="50" id="baR" aria-label="Сравнить до и после ремонта"></div>
    <ol class="bsteps" id="bSteps">
      <li><button type="button" data-v="85"><i>1</i><b>Замер и смета</b><span>Каждая позиция и итог — до оплаты.</span></button></li>
      <li><button type="button" data-v="67"><i>2</i><b>Договор</b><span>Объём, сроки и цена — на бумаге.</span></button></li>
      <li><button type="button" data-v="49"><i>3</i><b>Работа по этапам</b><span>Каждый этап — по акту.</span></button></li>
      <li><button type="button" data-v="31"><i>4</i><b>Ход работ в кабинете</b><span>Камера и отчёты по этапам.</span></button></li>
      <li><button type="button" data-v="10"><i>✓</i><b>Гарантия 5 лет</b><span>По договору. Точка.</span></button></li>
    </ol>
  </div>
''')
rep('  <div class="rgrid">\n    <div class="ba wide"', '  <div class="rwrap">\n    <div class="ba wide"')

CSS = r'''
/* v20 — меню-капсула */
:root{--hh:84px}
header,header.sc{position:fixed;left:0;right:0;top:12px;z-index:30;background:transparent;backdrop-filter:none;box-shadow:none;pointer-events:none}
header .hd{pointer-events:auto;height:64px;max-width:calc(100% - 2 * clamp(16px,3.4vw,110px));margin:0 auto;padding:0 10px 0 24px!important;border-radius:999px;gap:26px;
  background:#F4F2EEe0;backdrop-filter:blur(18px) saturate(1.4);-webkit-backdrop-filter:blur(18px) saturate(1.4);box-shadow:0 12px 34px #0000001f,inset 0 0 0 1px #ffffff99;transition:background .35s,box-shadow .35s,color .35s}
header.ontop .hd{background:#0E0E0F47;color:#fff;box-shadow:inset 0 0 0 1px #ffffff2e}
header.ontop .logo svg{fill:#fff}header.ontop .logo small,header.ontop .tel small{color:#ffffffb3}
header.ontop .hicon,header.ontop .hcab{background:#ffffff1f;border-color:#ffffff40;color:#fff}
nav.main{position:relative;align-self:stretch;align-items:center}
nav.main a{position:relative;padding:8px 2px;opacity:.72;transition:opacity .2s}nav.main a.on::after{display:none}
nav.main .nd{position:absolute;bottom:12px;left:0;width:6px;height:6px;border-radius:50%;background:var(--red);transform:translateX(var(--nx,-20px));opacity:var(--no,0);transition:transform .45s cubic-bezier(.3,1.4,.5,1),opacity .3s}
.tel small{display:flex;align-items:center;justify-content:flex-end;gap:6px}
.live-dot{width:7px;height:7px;border-radius:50%;background:#2FB36B;box-shadow:0 0 0 0 #2FB36B88;animation:livep 2s infinite}
@keyframes livep{70%{box-shadow:0 0 0 7px #2FB36B00}100%{box-shadow:0 0 0 0 #2FB36B00}}
.hero{min-height:clamp(640px,100svh,1400px)}
.hero .hin{padding-top:calc(var(--hh) + clamp(28px,6vh,100px))}
main section[id],.after{scroll-margin-top:96px}
.map{top:96px}
@media(max-width:800px){:root{--hh:70px}header,header.sc{top:8px}header .hd{height:56px;padding:0 6px 0 16px!important;max-width:calc(100% - 16px)}}
/* поиск */
.sbox{border-radius:28px;padding:12px;box-shadow:0 30px 70px #00000052,0 0 0 1px #ffffff26}
.dd-wrap{position:relative}
.dd{position:absolute;left:-1px;right:-1px;top:calc(100% + 6px);z-index:20;background:#fff;border-radius:16px;box-shadow:0 20px 50px #0000002e;padding:6px;display:grid;gap:2px;max-height:300px;overflow:auto}
.dd[hidden]{display:none}
.dd button{all:unset;box-sizing:border-box;display:flex;justify-content:space-between;gap:10px;padding:10px 12px;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer;color:var(--ink)}
.dd button small{color:var(--mut);font-weight:500}.dd button:hover,.dd button.act{background:var(--soft)}
.qf{display:flex;gap:6px;flex-wrap:wrap}.qf button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 12px;font-size:12.5px;font-weight:600;color:var(--ink)}
.qf button[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}
/* живая карточка ЖК */
.chipv{padding:18px 20px 16px;width:clamp(300px,19vw,400px)}
.cv-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.cv-st{display:inline-flex;align-items:center;gap:7px;font-size:11px;font-weight:800;letter-spacing:.04em;color:var(--mut)}
.cv-st::before{content:'';width:8px;height:8px;border-radius:50%;background:#C9C5BE;transition:background .3s}
.cv-st.ok{color:#B8321D}.cv-st.ok::before{background:var(--red);box-shadow:0 0 0 4px #F5553C2e}
.cv-dots{display:flex;gap:5px}.cv-dots button{width:7px;height:7px;border-radius:50%;border:0;padding:0;background:#D9D5CE}.cv-dots button[aria-current=true]{background:var(--ink);width:16px;border-radius:4px}
.chipv h3{font:600 17px Manrope;margin:0}.chipv>small{display:block;font-size:12px;color:var(--mut);margin:2px 0 6px}
.chipv li{opacity:.35;transition:opacity .3s}.chipv li svg{transform:scale(0);transition:transform .35s cubic-bezier(.3,1.6,.5,1)}
.chipv li.ok{opacity:1}.chipv li.ok svg{transform:none}
.cv-go{display:flex;justify-content:space-between;margin-top:10px;padding-top:10px;border-top:1px solid #0000000f;font-size:13px;font-weight:700;opacity:0;transition:opacity .3s}.cv-go.on{opacity:1}
.cv-go::after{content:'';width:8px;height:8px;border-radius:50%;background:var(--red);align-self:center}
/* ремонт: одна комната */
.rwrap{margin-top:44px}
.ba.wide{aspect-ratio:21/9;border-radius:30px}
.ba.wide .l1,.ba.wide .l2{top:18px;font-size:13px;padding:7px 14px}.ba.wide .l1{left:18px}.ba.wide .l2{right:18px}
.bacap{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);background:#0E0E0Fb3;backdrop-filter:blur(8px);color:#fff;font-size:13px;font-weight:600;border-radius:999px;padding:8px 16px;pointer-events:none;white-space:nowrap}
.bsteps{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.bsteps button{all:unset;box-sizing:border-box;display:grid;grid-template-columns:30px 1fr;column-gap:12px;row-gap:2px;width:100%;height:100%;background:#fff;border-radius:20px;padding:16px;cursor:pointer;transition:background .3s,color .3s}
.bsteps i{grid-row:span 2;width:30px;height:30px;border-radius:50%;border:2px solid var(--line);display:flex;align-items:center;justify-content:center;font-style:normal;font-size:12px;font-weight:700;transition:all .3s}
.bsteps b{font-size:15px}.bsteps span{font-size:13px;color:var(--mut);transition:color .3s}
.bsteps li.cur button{background:var(--ink);color:#fff}.bsteps li.cur i{background:var(--red);border-color:var(--red);color:#fff}.bsteps li.cur span{color:#C9C5BE}
.bsteps li.past i{border-color:var(--ink);background:var(--ink);color:#fff}
.bsteps button:focus-visible{outline:2px solid var(--red);outline-offset:2px}
@media(max-width:1100px){.bsteps{grid-template-columns:repeat(2,minmax(0,1fr))}.ba.wide{aspect-ratio:16/10}}
@media(max-width:800px){.bsteps{grid-template-columns:minmax(0,1fr)}.ba.wide{aspect-ratio:4/3.4}.bacap{font-size:11px;padding:6px 12px}}
@media(prefers-reduced-motion:reduce){.live-dot{animation:none}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

JS = r'''
// меню: капсула и скользящая точка
const hdrEl = $('header'), nav = $('nav.main'), nd = $('nav.main .nd');
function ndTo(a) { if (!a) { nav.style.setProperty('--no', 0); return; } nav.style.setProperty('--nx', (a.offsetLeft + a.offsetWidth / 2 - 3) + 'px'); nav.style.setProperty('--no', 1); }
const ndActive = () => ndTo($('nav.main a.on'));
$$('nav.main a').forEach(a => a.addEventListener('mouseenter', () => ndTo(a)));
nav.addEventListener('mouseleave', ndActive);
new MutationObserver(ndActive).observe(nav, {subtree: true, attributes: true, attributeFilter: ['class']});
setTimeout(ndActive, 300); addEventListener('resize', ndActive);
function hdrUpd() { hdrEl.classList.toggle('ontop', scrollY < $('.hero').offsetHeight - 90); }
addEventListener('scroll', hdrUpd, {passive: true}); hdrUpd();

// поиск: быстрые фильтры
const QF = {ready: it => !it.due, fin: it => it.fin !== 'Без отделки', fam: it => it.t === 'new', deal: it => it.disc || it.special};
const qfOn = () => $$('.qf [aria-pressed=true]').map(b => b.dataset.qf);
const _match = match;
match = (it, f) => _match(it, f) && qfOn().every(k => QF[k](it));
$$('.qf button').forEach(b => b.addEventListener('click', () => { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true'); liveCount(); }));

// поиск: выпадающие подсказки
function ddOpen(dd, items, pick) {
  if (!items.length) { dd.hidden = true; return; }
  dd.innerHTML = items.map((x, i) => `<button type="button" role="option" data-i="${i}">${x[0]}${x[1] ? `<small>${x[1]}</small>` : ''}</button>`).join('');
  dd.hidden = false; $$('button', dd).forEach(b => b.addEventListener('mousedown', e => { e.preventDefault(); pick(items[b.dataset.i]); dd.hidden = true; }));
}
function ddKeys(inp, dd) {
  inp.addEventListener('keydown', e => {
    const bs = $$('button', dd); if (dd.hidden || !bs.length) return; let i = bs.findIndex(b => b.classList.contains('act'));
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); i = (i + (e.key === 'ArrowDown' ? 1 : -1) + bs.length) % bs.length; bs.forEach((b, k) => b.classList.toggle('act', k === i)); }
    else if (e.key === 'Enter' && i >= 0) { e.preventDefault(); bs[i].dispatchEvent(new MouseEvent('mousedown')); }
    else if (e.key === 'Escape') dd.hidden = true;
  });
  inp.addEventListener('blur', () => setTimeout(() => dd.hidden = true, 120));
}
const pr = $('#pr'), ad = $('#ad');
const cntBy = fn => ITEMS.filter(it => fn(it) && match(it, {...readForm(), max: 0, q: ''})).length;
function prShow() { ddOpen($('#prDD'), [5, 8, 12, 15].map(m => [`до ${m} млн ₽`, `${cntBy(it => it.p <= m * 1e6)} кв.`, m]).concat([['Любая цена', '', '']]), x => { pr.value = x[2]; liveCount(); }); }
pr.addEventListener('focus', prShow); pr.addEventListener('input', () => $('#prDD').hidden = true); ddKeys(pr, $('#prDD'));
const PLACES = [...new Set(ITEMS.map(it => it.d))].map(d => [d, 'район']).concat([...new Set(ITEMS.filter(it => it.zk.startsWith('ЖК')).map(it => it.zk))].map(z => [z, 'жилой комплекс']));
function adShow() {
  const q = ad.value.trim().toLowerCase();
  ddOpen($('#adDD'), PLACES.filter(p => !q || p[0].toLowerCase().includes(q)).slice(0, 7).map(p => [p[0], `${p[1]} · ${cntBy(it => (it.zk + ' ' + it.d).includes(p[0]))} кв.`]), x => { ad.value = x[0]; liveCount(); });
}
ad.addEventListener('focus', adShow); ad.addEventListener('input', adShow); ddKeys(ad, $('#adDD'));

// живая карточка «ЖК проверен»
const ZKS = [...new Set(ITEMS.filter(it => it.zk.startsWith('ЖК')).map(it => it.zk))].map(z => ({z, d: ITEMS.find(it => it.zk === z).d, n: ITEMS.filter(it => it.zk === z).length}));
const ZCHK = ['Разрешение на строительство', 'Проектная декларация, эскроу', 'Прошлые дома сданы в срок', 'Нет банкротных дел'];
let zi = 0, zt = [], zPause = false;
function zShow(i) {
  zt.forEach(clearTimeout); zt = []; zi = (i + ZKS.length) % ZKS.length; const z = ZKS[zi];
  $('#cvName').textContent = z.z; $('#cvSub').textContent = `${z.d} · новостройка`;
  $('#cvList').innerHTML = ZCHK.map(c => `<li><svg><use href="#check"/></svg>${c}</li>`).join('');
  $('#cvDots').innerHTML = ZKS.map((_, k) => `<button type="button" aria-label="${ZKS[k].z}" aria-current="${k === zi}"></button>`).join('');
  $$('#cvDots button').forEach((b, k) => b.addEventListener('click', () => zShow(k)));
  const st = $('#cvSt'), go = $('#cvGo'); st.textContent = 'Проверяем'; st.classList.remove('ok'); go.classList.remove('on');
  go.textContent = `${z.n} ${plural(z.n, 'квартира', 'квартиры', 'квартир')} в этом ЖК`;
  const step = reduce ? 0 : 450;
  $$('#cvList li').forEach((li, k) => zt.push(setTimeout(() => li.classList.add('ok'), step * (k + 1))));
  zt.push(setTimeout(() => { st.textContent = 'Проверен'; st.classList.add('ok'); go.classList.add('on'); }, step * 5));
  zt.push(setTimeout(function nx() { if (zPause) { zt.push(setTimeout(nx, 1500)); return; } zShow(zi + 1); }, step * 5 + 4200));
}
$('#cvGo').addEventListener('click', e => { e.preventDefault(); const z = ZKS[zi].z; applyFilter(ITEMS.filter(it => it.zk === z), z); $('#list').scrollIntoView({behavior: 'smooth'}); });
$('#chipv').addEventListener('mouseenter', () => zPause = true); $('#chipv').addEventListener('mouseleave', () => zPause = false);
zShow(0);

// ремонт: шторка ↔ этапы
const baR = $('#baR');
function baSet(v) { baR.value = v; $('#baBox .after').style.clipPath = `inset(0 0 0 ${v}%)`; $('#baH').style.left = v + '%';
  const k = Math.min(4, Math.floor((100 - v) / 18)); $$('#bSteps li').forEach((li, i) => { li.classList.toggle('cur', i === k); li.classList.toggle('past', i < k); }); }
baR.addEventListener('input', () => baSet(+baR.value));
function baTo(to, ms = 900) { if (reduce) { baSet(to); return; } const from = +baR.value, t0 = performance.now();
  (function f(t) { const k = Math.min(1, (t - t0) / ms), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; baSet(from + (to - from) * e); if (k < 1) requestAnimationFrame(f); })(t0); }
$$('#bSteps button').forEach(b => b.addEventListener('click', () => baTo(+b.dataset.v, 600)));
baSet(50);
new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect(); baTo(92, 700); setTimeout(() => baTo(8, 1600), 750); setTimeout(() => baTo(50, 900), 2500); }, {threshold: .5}).observe($('#baBox'));
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
