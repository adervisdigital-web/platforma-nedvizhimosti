"""Сайт v8 — UI/UX: карточка объекта (быстрый просмотр), контраст кнопок (красный для текста #D83C24, 4.6:1), свои ползунки,
кнопка чата не перекрывает первый экран, звонок в шапке на телефоне, карта по кнопке на телефоне, подсказки района,
новая иерархия карточки, тень шапки, text-wrap, кнопка «Кабинет».
Run из корня репо: py -3 tools/patches/site_v8_uiux.py  (исходник — 08_Сайт_пример/v7.html)"""
P = '08_Сайт_пример/'
s = open(P + 'v7.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('--mut:#77736C;', '--mut:#6B675F;--red-ui:#D83C24;')
rep('.btn.red{background:var(--red);color:#fff}.btn.red:hover{background:var(--red-d)}', '.btn.red{background:var(--red-ui);color:#fff}.btn.red:hover{background:#C4331D}')

CSS = r'''
/* v8 — UI/UX */
h1,h2,h3,.mtext{text-wrap:balance}p,q,.lead2{text-wrap:pretty}
.btn{transition:background .2s,transform .15s,box-shadow .2s}.btn:hover{transform:translateY(-1px)}.btn:active{transform:none}
header{transition:box-shadow .25s}header.sc{box-shadow:0 1px 0 var(--line),0 12px 30px #0000000f}
.hcab{min-height:46px;padding:0 18px;font-size:14px;border:1px solid var(--line);background:#fff}
.tel-m{display:none}
.gal .tag,.pin.on,.act button,.ch-f button{background:var(--red-ui)}
.note{opacity:1}.cout .note{color:#fff}.cout.lt .note,.cout.dk .note{color:var(--mut)}.cout.dk .note{color:#B9B4AB}
/* ползунки */
input[type=range]{-webkit-appearance:none;appearance:none;background:transparent;height:30px;--p:50%;cursor:pointer}
input[type=range]::-webkit-slider-runnable-track{height:4px;border-radius:2px;background:linear-gradient(90deg,var(--red) var(--p),#DDD8D0 var(--p))}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:26px;border-radius:50%;background:#fff;border:2px solid var(--red);margin-top:-11px;box-shadow:0 4px 14px #00000026;transition:transform .15s}
input[type=range]:hover::-webkit-slider-thumb,input[type=range]:focus-visible::-webkit-slider-thumb{transform:scale(1.12)}
input[type=range]::-moz-range-track{height:4px;border-radius:2px;background:#DDD8D0}input[type=range]::-moz-range-progress{height:4px;border-radius:2px;background:var(--red)}
input[type=range]::-moz-range-thumb{width:22px;height:22px;border-radius:50%;background:#fff;border:2px solid var(--red);box-shadow:0 4px 14px #00000026}
input[type=range]:disabled{cursor:default}
/* карточка объекта */
.mid .t.qv{border:0;background:none;padding:0;text-align:left;font:600 21px/1.25 Manrope;letter-spacing:-.015em;cursor:pointer;color:var(--ink)}.mid .t.qv:hover{color:var(--red-ui)}
.gal img{cursor:pointer}
.qvg{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:28px}
.qvph{position:relative;border-radius:20px;overflow:hidden;aspect-ratio:4/3;background:var(--soft)}.qvph img{width:100%;height:100%;object-fit:cover}
.qvph .tag{position:absolute;left:12px;top:12px;background:var(--red-ui);color:#fff;font-size:12px;font-weight:700;border-radius:999px;padding:5px 11px}
.qvc{margin-top:16px;background:#fff;border-radius:20px;padding:18px 20px}.qvc b{display:flex;gap:8px;align-items:center;font-size:15px;margin-bottom:6px}.qvc b i{width:9px;height:9px;border-radius:50%;background:var(--red)}
.qvc span{display:flex;gap:10px;align-items:center;font-size:14px;padding:7px 0;border-top:1px solid #0000000d}.qvc svg{width:16px;height:16px;color:var(--red-ui);flex:none}
.qvi .price{font-size:34px}.qvi .ppm{font-size:13px}
.qvp{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:18px 0}.qvp div{background:#fff;border-radius:14px;padding:10px 14px}.qvp dt{font-size:12px;color:var(--mut)}.qvp dd{margin:2px 0 0;font-weight:700;font-size:15px}
.qvm{display:flex;align-items:center;justify-content:space-between;gap:12px;background:var(--night);color:#fff;border-radius:16px;padding:14px 16px}.qvm small{display:block;color:#B9B4AB;font-size:12px}.qvm b{font-size:19px}
.qvm button{border:0;background:#fff;color:var(--ink);border-radius:999px;padding:10px 14px;font-weight:700;font-size:13px;flex:none}
.qvr{display:block;margin-top:10px;font-size:14px;font-weight:700;color:#B8321D}
.qva{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}.qva .btn{flex:1 1 auto}
.qva .ib{width:50px;height:50px;border:1px solid var(--line);background:#fff}
/* чат-кнопка — после первого экрана */
.chatfab{opacity:0;transform:translateY(16px);pointer-events:none;transition:opacity .3s,transform .3s}.chatfab.show{opacity:1;transform:none;pointer-events:auto}
.mapbtn{display:none}
@media(max-width:1200px){.hcab{display:none}}
@media(max-width:800px){.tel-m{display:flex}.seg.view{display:none}.mapbtn{display:inline-flex;min-height:44px}.res .map{display:none}.res.showmap .map{display:block}
 .tabs{width:100%}.tabs button{flex:1;padding:10px 4px;font-size:12.5px}
 .qvg,.qvp{grid-template-columns:minmax(0,1fr)}.qvp{grid-template-columns:1fr 1fr}.qvi .price{font-size:28px}.mid .t.qv{font-size:19px}}
'''
rep('@media(prefers-reduced-motion:reduce)', CSS + '@media(prefers-reduced-motion:reduce)')

# шапка: кнопка кабинета (широкие экраны) и звонок (телефон)
rep('<symbol id="mark"', '<symbol id="phone" viewBox="0 0 24 24"><path d="M6.6 3.5h2.6l1.4 4.2-2 1.3a11 11 0 0 0 6.4 6.4l1.3-2 4.2 1.4v2.6a2 2 0 0 1-2.2 2A16.6 16.6 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>\n  <symbol id="mark"')
rep('<a class="tel" href="tel:+79655002918">', '<a class="btn hcab" href="#cab"><svg class="ico" style="width:18px;height:18px"><use href="#user"/></svg>Кабинет</a>\n  <a class="tel" href="tel:+79655002918">')
rep('<button class="hicon" id="favBtn" aria-label="Избранное">', '<a class="hicon tel-m" href="tel:+79655002918" aria-label="Позвонить: +7 965 500-29-18"><svg class="ico"><use href="#phone"/></svg></a>\n  <button class="hicon" id="favBtn" aria-label="Избранное">')

# подсказки района
rep('<input id="ad" placeholder="Академический, ЖК…">', '<input id="ad" placeholder="Академический, ЖК…" list="adList" autocomplete="off"><datalist id="adList"></datalist>')

# карта на телефоне — по кнопке
rep('<div class="seg view" role="group" aria-label="Вид">', '<button class="btn ghost mapbtn" id="mapBtn" aria-pressed="false"><svg class="ico"><use href="#pin"/></svg>На карте</button><div class="seg view" role="group" aria-label="Вид">')

# карточка: иерархия и быстрый просмотр
rep('<div class="mid"><div class="t">${title(it)}</div><div class="a">${it.zk} · ${it.d}</div>',
    '<div class="mid"><button class="t qv" data-i="${it.id}">${head(it)}</button><div class="a">${it.fl}/${it.fls} этаж · ${it.zk} · ${it.d}</div>')
rep("[it.t === 'new' ? 'Новостройка' : 'Вторичка', it.fin, it.t === 'new' ? 'Семейная ипотека' : 'Чистая сделка']",
    "[it.t === 'new' ? 'Новостройка' : 'Вторичка', it.t === 'new' ? 'Семейная ипотека' : 'Чистая сделка']")
rep("const title = it => ", "const head = it => `${it.r ? it.r + '-комн. квартира' : 'Студия'} · ${it.s.toLocaleString('ru-RU')} м²`;\nconst title = it => ")
rep("  $$('button.mort').forEach(b => b.addEventListener('click', () => mortFrom(ITEMS[b.dataset.i])));\n}",
    "  $$('button.mort').forEach(b => b.addEventListener('click', () => mortFrom(ITEMS[b.dataset.i])));\n"
    "  $$('.card .qv').forEach(b => b.addEventListener('click', () => quick(ITEMS[b.dataset.i])));\n"
    "  $$('.card .gal img').forEach(im => im.addEventListener('click', () => quick(ITEMS[im.closest('.card').dataset.i])));\n}")
rep("$('#calc').scrollIntoView({behavior: 'smooth'}); toast(", "fillAll(); $('#calc').scrollIntoView({behavior: 'smooth'}); toast(")
rep("hName = b.dataset.n; $('#ha').value = b.dataset.a; hcalc();", "hName = b.dataset.n; $('#ha').value = b.dataset.a; hcalc(); fillAll();")

JS = r'''
// быстрый просмотр объекта
function quick(it) {
  const r = rateOf(it), pay = Math.round(ann(it.p, r)), tg = tagOf(it), ck = CHECKS[it.t === 'sec' ? 'sec' : 'dev'];
  openDlg(title(it), `<div class="qvg"><div><div class="qvph"><img src="photo/${it.img}.jpg" alt="${title(it)}">${tg ? `<span class="tag">${tg}</span>` : ''}</div>
    <div class="qvc"><b><i></i>${it.t === 'sec' ? 'Что проверил юрист' : 'Что мы проверили у застройщика'}</b>${ck.map(c => `<span><svg><use href="#check"/></svg>${c[0]}</span>`).join('')}</div></div>
    <div class="qvi"><div class="price">${it.p.toLocaleString('ru-RU')} ₽</div><div class="ppm">${it.ppm.toLocaleString('ru-RU')} ₽ за м² · ${it.zk}, ${it.d}</div>
    <dl class="qvp"><div><dt>Площадь</dt><dd>${it.s.toLocaleString('ru-RU')} м²</dd></div><div><dt>Этаж</dt><dd>${it.fl} из ${it.fls}</dd></div>
      <div><dt>Сдача</dt><dd>${it.due ? it.st.replace('Сдача — ', '') : it.t === 'sec' ? 'Готовое жильё' : 'Дом сдан'}</dd></div><div><dt>Отделка</dt><dd>${it.fin}</dd></div></dl>
    <div class="qvm"><div><small>В ипотеку · ${it.t === 'new' ? 'семейная' : 'рыночная'} ${r} %, взнос 20 %</small><b>от ${pay.toLocaleString('ru-RU')} ₽/мес</b></div><button type="button" id="qvCalc">Рассчитать</button></div>
    ${it.fin === 'Без отделки' ? `<a class="qvr" href="#ba" onclick="dlg.close()">+ наш ремонт под ключ — от ${fmtM(it.s * 20000)}, гарантия 5 лет</a>` : ''}
    <div class="qva"><a class="btn red" href="tel:+79655002918">Позвонить</a><a class="btn white" href="#lead" id="qvLead">Записаться на просмотр</a>
      <button class="ib fav" id="qvFav" aria-pressed="${fav.has(it.id)}" aria-label="В избранное"><svg class="ico"><use href="#heart"/></svg></button></div></div></div>`);
  $('#qvCalc').addEventListener('click', () => { dlg.close(); mortFrom(it); });
  $('#qvLead').addEventListener('click', () => { dlg.close(); });
  $('#qvFav').addEventListener('click', e => { toggle(fav, 'pn_fav', it.id, 'fav'); e.currentTarget.setAttribute('aria-pressed', fav.has(it.id)); });
}

// ползунки: заливка до бегунка
function fillAll() { $$('input[type=range]').forEach(r => r.style.setProperty('--p', (r.value - r.min) / (r.max - r.min) * 100 + '%')); }
document.addEventListener('input', e => { if (e.target.type === 'range') fillAll(); });
fillAll();

// подсказки района и ЖК
$('#adList').innerHTML = [...new Set(ITEMS.flatMap(it => [it.d, it.zk]))].map(v => `<option value="${v}">`).join('');

// карта на телефоне
$('#mapBtn').addEventListener('click', e => { const on = $('.res').classList.toggle('showmap'); e.currentTarget.setAttribute('aria-pressed', on); e.currentTarget.lastChild.textContent = on ? 'Списком' : 'На карте'; });

$('.sline a').addEventListener('click', () => { if (innerWidth <= 800 && !$('.res').classList.contains('showmap')) $('#mapBtn').click(); });

// шапка с тенью и кнопка чата — после первого экрана
const hdr = $('header'), fab = $('#chatFab');
function onScroll() { hdr.classList.toggle('sc', scrollY > 10); fab.classList.toggle('show', scrollY > $('.hero').offsetHeight * .6); }
addEventListener('scroll', onScroll, {passive: true}); onScroll();
'''
rep('</script>\n</body>', JS + '</script>\n</body>')

open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok', len(s))
