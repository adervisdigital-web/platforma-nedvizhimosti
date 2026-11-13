"""Сайт v17 — анимация и функции.
Анимация (одна постановка + отклик на действия): первый экран собирается при загрузке и точка «падает» в «ручаемся.»;
цифры в «Отборе» отсчитываются; итоги калькуляторов плавно перетекают; окна открываются мягко; сердечко «щёлкает».
Функции: запись на просмотр квартиры и в демо-дом (день, время, телефон → подтверждение + файл в календарь .ics);
в карточке квартиры без отделки — выбор уровня ремонта и итог «квартира + ремонт»; «Вы смотрели» (последние объекты).
Всё уважает prefers-reduced-motion. Run из корня репо после site_v16_review.py: py -3 tools/patches/site_v17_motion.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


CSS = r'''
/* v17 — постановка первого экрана */
@keyframes rise{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
@keyframes drop{0%{transform:translateY(-2.2em) scale(.6);opacity:0}55%{transform:translateY(.08em) scale(1.15,.82);opacity:1}75%{transform:translateY(-.12em) scale(.95,1.06)}100%{transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes zoomout{from{transform:scale(1.09)}to{transform:scale(1.02)}}
.js .hbg{animation:zoomout 2.4s cubic-bezier(.2,.7,.2,1) both}
.js .hl>*{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}
.js .hl>.br{animation-delay:.1s}.js .hl>h1{animation-delay:.2s}.js .hl>.sub{animation-delay:.45s}.js .hl>.trust{animation-delay:.6s}
.js .hero h1 i.o{animation:drop .75s cubic-bezier(.3,.9,.4,1) 1.05s both}
.js .sbox{animation:rise .9s cubic-bezier(.2,.7,.2,1) .7s both}.js .chipv{animation:rise .9s cubic-bezier(.2,.7,.2,1) .95s both}
/* отклик */
@keyframes pop{0%{transform:scale(1)}40%{transform:scale(1.35)}100%{transform:scale(1)}}
.ib.fav[aria-pressed=true] svg,#qvFav[aria-pressed=true] svg{animation:pop .35s ease}
@keyframes dlgin{from{transform:translateY(22px) scale(.98)}to{transform:none}}
.dlg[open]{animation:dlgin .32s cubic-bezier(.2,.7,.2,1)}.dlg[open]::backdrop{animation:fade .3s}
.pay{font-variant-numeric:tabular-nums}
/* ремонт в карточке квартиры */
.qvx{margin-top:12px;background:#fff;border-radius:16px;padding:14px 16px;display:grid;gap:10px}
.qvx .k{font-size:12px;color:var(--mut)}.qvx .seg2 button{padding:7px 12px;font-size:12.5px}
.qvx .tot{display:flex;justify-content:space-between;align-items:baseline;gap:10px;border-top:1px solid #0000000d;padding-top:10px}.qvx .tot b{font-size:20px}
.qvi{position:relative}.qic{position:absolute;right:0;top:0;display:flex;gap:6px}.qic .ib{width:44px;height:44px;border:1px solid var(--line);background:#fff}
/* запись */
.dlg .db{overflow-x:hidden}.bk{display:grid;gap:16px;grid-template-columns:minmax(0,1fr)}.bk>*{min-width:0}#bkGo{white-space:normal;text-align:center;padding:10px 20px}.bk h4{margin:0;font:500 18px Manrope}
.days{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px}
.days button{flex:none;width:76px;border:1px solid var(--line);background:#fff;border-radius:16px;padding:10px 6px;text-align:center;line-height:1.2}
.days button small{display:block;font-size:11px;color:var(--mut)}.days button b{display:block;font-size:22px;font-weight:500}
.days button[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}.days button[aria-pressed=true] small{color:#C9C5BE}
.slots{display:grid;grid-template-columns:repeat(auto-fill,minmax(78px,1fr));gap:8px}
.slots button{border:1px solid var(--line);background:#fff;border-radius:12px;padding:10px 0;font-weight:600;font-size:14px}
.slots button:disabled{opacity:.35;text-decoration:line-through;cursor:default}.slots button[aria-pressed=true]{background:var(--red-ui);color:#fff;border-color:var(--red-ui)}
.bkok{text-align:center;display:grid;gap:12px;justify-items:center;padding:10px 0}
.bkok .big{width:84px;height:84px;border-radius:50%;background:var(--ink);display:flex;align-items:center;justify-content:center;animation:pop .5s ease}
.bkok .big i{width:22px;height:22px;border-radius:50%;background:var(--red)}
.bkok h4{font:400 30px/1.1 Manrope;letter-spacing:-.03em}.bkok p{margin:0;color:#4A4741;max-width:420px}
/* вы смотрели */
.seen{margin-top:40px}.seen[hidden]{display:none}.seen h3{margin:0 0 14px;font:500 22px Manrope;letter-spacing:-.02em}
.seenl{display:flex;gap:10px;overflow-x:auto;padding-bottom:6px}
.seenl button{flex:none;width:220px;border:0;background:#fff;border-radius:18px;padding:8px;text-align:left;display:grid;gap:6px}
.seenl img{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:12px}.seenl b{font-size:15px;padding:0 6px}.seenl span{font-size:12px;color:var(--mut);padding:0 6px 4px}
@media(prefers-reduced-motion:reduce){.js .hbg,.js .hl>*,.js .hero h1 i.o,.js .sbox,.js .chipv,.dlg[open],.bkok .big{animation:none!important}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

rep('<div class="more" id="more"><button class="btn white" id="moreBtn"></button></div></div>',
    '<div class="more" id="more"><button class="btn white" id="moreBtn"></button></div><div class="seen" id="seen" hidden><h3>Вы смотрели<i class="o"></i></h3><div class="seenl" id="seenL"></div></div></div>')

# быстрый просмотр: ремонт + запись
rep("    ${it.fin === 'Без отделки' ? `<a class=\"qvr\" href=\"#ba\" onclick=\"dlg.close()\">+ наш ремонт под ключ — от ${fmtM(it.s * 20000)}, гарантия 5 лет</a>` : ''}",
    "    ${it.fin === 'Без отделки' ? `<div class=\"qvx\"><span class=\"k\">Добавить наш ремонт · гарантия 5 лет</span><div class=\"seg2\" id=\"qvR\">${[['Без ремонта', 0], ['Базовый', 20000], ['Комфорт', 45000], ['Премиум', 80000]].map((x, i) => `<button type=\"button\" aria-pressed=\"${i === 0}\" data-r=\"${x[1]}\">${x[0]}</button>`).join('')}</div><div class=\"tot\"><span class=\"k\" id=\"qvRk\">Квартира</span><b id=\"qvT\">${rub(it.p)}</b></div></div>` : ''}")
rep("<a class=\"btn white\" href=\"#lead\" id=\"qvLead\">Записаться на просмотр</a><button type=\"button\" class=\"ib share\" data-share aria-label=\"Поделиться ссылкой\"><svg class=\"ico\"><use href=\"#share\"/></svg></button>\n      <button class=\"ib fav\" id=\"qvFav\" aria-pressed=\"${fav.has(it.id)}\" aria-label=\"В избранное\"><svg class=\"ico\"><use href=\"#heart\"/></svg></button></div></div></div>`);",
    "<button class=\"btn white\" type=\"button\" id=\"qvLead\">Записаться на просмотр</button></div></div></div>`);")
rep("<div class=\"qvi\"><div class=\"price\">${it.p.toLocaleString('ru-RU')} ₽</div>",
    "<div class=\"qvi\"><div class=\"qic\"><button type=\"button\" class=\"ib share\" data-share aria-label=\"Поделиться ссылкой\"><svg class=\"ico\"><use href=\"#share\"/></svg></button><button class=\"ib fav\" id=\"qvFav\" aria-pressed=\"${fav.has(it.id)}\" aria-label=\"В избранное\"><svg class=\"ico\"><use href=\"#heart\"/></svg></button></div><div class=\"price\">${it.p.toLocaleString('ru-RU')} ₽</div>")
rep("  $('#qvLead').addEventListener('click', () => { dlg.close(); });",
    "  $('#qvLead').addEventListener('click', () => booking('Просмотр', title(it) + ' · ' + it.zk, `${it.zk}, ${it.d}`));\n"
    "  $$('#qvR button').forEach(b => b.addEventListener('click', () => { $$('#qvR button').forEach(x => x.setAttribute('aria-pressed', x === b)); const add = it.s * +b.dataset.r;\n"
    "    $('#qvRk').textContent = add ? `Квартира + ремонт «${b.textContent.toLowerCase()}» (${fmtM(add)})` : 'Квартира'; $('#qvT').textContent = rub(it.p + add); }));\n"
    "  remember(it.id);")
rep("<a class=\"btn white\" href=\"#lead\" id=\"hvLead\">Обсудить проект</a>", "<button class=\"btn white\" type=\"button\" id=\"hvLead\">Посетить демо-дом</button>")
rep("  $('#hvLead').addEventListener('click', () => dlg.close());", "  $('#hvLead').addEventListener('click', () => booking('Экскурсия в демо-дом', `Проект «${h.line} ${h.n}» — смотрим вживую`, 'Демо-дом, Екатеринбург'));")

JS = r'''
function rub(n) { return Math.round(n).toLocaleString('ru-RU') + ' ₽'; }
const MONTHS = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];

// запись на просмотр / в демо-дом
const DOW = ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'];
function booking(kind, subj, place) {
  const days = Array.from({length: 7}, (_, i) => { const d = new Date(); d.setDate(d.getDate() + i + 1); return d; });
  let day = 0, slot = '';
  const slotsFor = d => ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'].map((t, i) => [t, (d.getDate() * 7 + i * 3) % 5 === 0 || (d.getDay() === 0 && i > 5)]);
  const draw = () => {
    $('#dlgB').innerHTML = `<div class="bk"><p style="margin:0;color:#4A4741">${subj}</p>
      <div><h4>День</h4><div class="days" style="margin-top:10px">${days.map((d, i) => `<button type="button" data-d="${i}" aria-pressed="${i === day}"><small>${DOW[d.getDay()]}</small><b>${d.getDate()}</b><small>${MONTHS[d.getMonth()].slice(0, 3)}</small></button>`).join('')}</div></div>
      <div><h4>Время</h4><div class="slots" style="margin-top:10px">${slotsFor(days[day]).map(([t, busy]) => `<button type="button" data-t="${t}" ${busy ? 'disabled aria-label="' + t + ' занято"' : ''} aria-pressed="${t === slot}">${t}</button>`).join('')}</div></div>
      <div class="f" id="bkF"><label for="bkP">Телефон для подтверждения</label><input id="bkP" type="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" value="${$('#lp').value}"><span class="err">Введите номер полностью — 10 цифр после +7</span></div>
      <button class="btn red" type="button" id="bkGo" ${slot ? '' : 'disabled style="opacity:.45"'}>${slot ? `Записаться на ${days[day].getDate()} ${MONTHS[days[day].getMonth()]}, ${slot}` : 'Выберите время'}</button></div>`;
    $$('#dlgB [data-d]').forEach(b => b.addEventListener('click', () => { day = +b.dataset.d; slot = ''; draw(); }));
    $$('#dlgB [data-t]').forEach(b => b.addEventListener('click', () => { slot = b.dataset.t; draw(); }));
    const ip = $('#bkP'); ip.addEventListener('input', () => { lp.value = ip.value; lp.dispatchEvent(new Event('input')); ip.value = lp.value; $('#bkF').classList.remove('bad'); });
    $('#bkGo').addEventListener('click', () => {
      if (ip.value.replace(/\D/g, '').length !== 11) { $('#bkF').classList.add('bad'); ip.focus(); return; }
      const d = days[day], [hh, mm] = slot.split(':'), st = new Date(d.getFullYear(), d.getMonth(), d.getDate(), +hh, +mm), en = new Date(st.getTime() + 36e5);
      const f = x => x.toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
      const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Platforma//RU', 'BEGIN:VEVENT', `UID:${Date.now()}@p.forma196.ru`, `DTSTAMP:${f(new Date())}`, `DTSTART:${f(st)}`, `DTEND:${f(en)}`,
        `SUMMARY:${kind} — Платформа недвижимости`, `DESCRIPTION:${subj}. Телефон менеджера +7 965 500-29-18`, `LOCATION:${place}`, 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
      const url = URL.createObjectURL(new Blob([ics], {type: 'text/calendar'}));
      $('#dlgT').textContent = 'Записали';
      $('#dlgB').innerHTML = `<div class="bkok"><span class="big"><i></i></span><h4>${d.getDate()} ${MONTHS[d.getMonth()]}, ${slot}<i class="o"></i></h4>
        <p>${kind}: ${subj}. Менеджер позвонит накануне и пришлёт адрес. Поменять время — по телефону <a href="tel:+79655002918" style="font-weight:700">+7 965 500-29-18</a>.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center"><a class="btn dark" href="${url}" download="platforma-${d.getDate()}-${MONTHS[d.getMonth()]}.ics">Добавить в календарь</a><button class="btn ghost" type="button" onclick="dlg.close()">Готово</button></div></div>`;
    });
  };
  $('#dlgT').textContent = kind; dlg.classList.remove('wide'); draw();
  if (!dlg.open) dlg.showModal();
}

// вы смотрели
function seenList() { return window.PN_SEEN || (window.PN_SEEN = store.get('pn_seen')); }
function remember(id) { const seen = seenList(); const i = seen.indexOf(id); if (i >= 0) seen.splice(i, 1); seen.unshift(id); seen.length = Math.min(seen.length, 8); store.set('pn_seen', seen); drawSeen(); }
function drawSeen() {
  const seen = seenList(); if (!$('#seenL') || typeof head !== 'function') return;
  $('#seen').hidden = !seen.length;
  $('#seenL').innerHTML = seen.map(id => ITEMS[id]).filter(Boolean).map(it => `<button type="button" data-seen="${it.id}"><img src="photo/${it.img}.jpg" alt=""><b>${(it.p / 1e6).toLocaleString('ru-RU', {maximumFractionDigits: 2})} млн ₽</b><span>${head(it)} · ${it.d}</span></button>`).join('');
  $$('[data-seen]').forEach(b => b.addEventListener('click', () => quick(ITEMS[b.dataset.seen])));
}
drawSeen();

// цифры «Отбора» — отсчёт
function countUp(el, to, ms) {
  if (reduce) return; const t0 = performance.now(), fmtN = n => n >= 1000 ? Math.round(n).toLocaleString('ru-RU') : Math.round(n);
  (function f(t) { const k = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - k, 3); el.textContent = fmtN(to * e); if (k < 1) requestAnimationFrame(f); })(t0);
}
new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect(); $$('.stats b').forEach((b, i) => countUp(b, +b.textContent.replace(/\D/g, ''), 1400 + i * 150)); }, {threshold: .4}).observe($('.stats'));

// итоги калькуляторов — плавно
['#pay', '#hpay', '#rpay'].forEach(q => {
  const el = $(q); if (!el) return; let cur = parseFloat(el.textContent.replace(/[^\d,]/g, '').replace(',', '.')) || 0, raf;
  new MutationObserver(() => {
    const node = el.firstChild; if (!node || node.nodeType !== 3) return;
    const to = parseFloat(node.nodeValue.replace(/[^\d,]/g, '').replace(',', '.')); if (isNaN(to) || reduce) { cur = to; return; }
    const from = cur, t0 = performance.now(); cur = to; cancelAnimationFrame(raf);
    (function f(t) { const k = Math.min(1, (t - t0) / 380), e = 1 - Math.pow(1 - k, 3); node.nodeValue = Math.round(from + (to - from) * e).toLocaleString('ru-RU') + ' '; if (k < 1) raf = requestAnimationFrame(f); })(t0);
  }).observe(el, {childList: true});
});
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
