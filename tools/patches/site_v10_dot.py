"""Сайт v10 — характер бренда и функции: линия прокрутки, которая заканчивается точкой (и точка «встаёт» в «Ставим точку.»),
рубрики без ложной нумерации (красная точка вместо 01–09), ссылки с точкой вместо «→», подбор за 3 шага вместо простой
формы (живой результат по квартирам, домам, ремонту и ипотеке), ссылки на объект и дом (#obj-N, #house-ID) и «Поделиться».
Run из корня репо: py -3 tools/patches/site_v10_dot.py  (исходник — 08_Сайт_пример/v9.html)"""
import re
P = '08_Сайт_пример/'
s = open(P + 'v9.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


def cut(a, b, new, keep_b=True):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + (s[j:] if keep_b else s[j + len(b):])


# рубрики: не последовательность — без номеров, с точкой бренда
s, n = re.subn(r'\[ <b>0\d</b> ', '[ <b>●</b> ', s)
assert n == 9, n
rep('[ <b>●</b> Ремонт — делаем сами ]', '[ <b>●</b> Ремонт ]')
rep(".pc a.lk::after{content:'→';color:var(--red)}", ".pc a.lk::after{content:'';width:7px;height:7px;border-radius:50%;background:var(--red)}")

CSS = r'''
/* v10 — линия прокрутки с точкой */
.prog{position:fixed;left:0;right:0;top:0;height:2px;z-index:36;pointer-events:none}
.prog i{position:absolute;left:0;top:0;height:2px;width:calc(var(--s,0) * 100%);background:var(--ink)}
.prog b{position:absolute;top:-4px;left:calc(var(--s,0) * 100% - 5px);width:10px;height:10px;border-radius:50%;background:var(--red);transition:opacity .3s}
.prog.end b{opacity:0}
.js .fbig i.o{transform:scale(0);transform-origin:50% 100%;transition:transform .8s cubic-bezier(.3,1.7,.5,1) .15s}
.js .fbig.in i.o{transform:scale(1)}
/* подбор за 3 шага */
.quiz fieldset{border:0;margin:0;padding:0;display:none;gap:12px}.quiz fieldset.on{display:grid}
.quiz legend{font:500 24px/1.2 Manrope;letter-spacing:-.02em;padding:0;margin-bottom:12px}
.qh{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:var(--mut)}
.qd{display:flex;gap:6px}.qd i{width:9px;height:9px;border-radius:50%;background:var(--line);transition:background .3s}.qd i.on{background:var(--red)}
.ch2{display:flex;gap:6px;flex-wrap:wrap}.ch2 button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font-size:13px;font-weight:600;min-height:40px}.ch2 button[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}
.qm{margin:0;background:var(--soft);border-radius:16px;padding:14px 16px;font-size:14px;line-height:1.45}.qm b{font-size:17px}
.qnav{display:flex;gap:8px}.qnav .btn{flex:1}.qnav [hidden]{display:none}
.quiz .rng label b{font-size:18px}
.ib.share svg{fill:none}
'''
rep('@media(prefers-reduced-motion:reduce)', CSS + '@media(prefers-reduced-motion:reduce)')
rep('<meta charset="utf-8">', '<meta charset="utf-8"><script>document.documentElement.classList.add("js")</script>')
rep('<symbol id="mark"', '<symbol id="share" viewBox="0 0 24 24"><path d="M12 15V4M7.5 8.5 12 4l4.5 4.5M5 13v6h14v-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>\n  <symbol id="mark"')
rep('<header>', '<div class="prog" id="prog" aria-hidden="true"><i></i><b></b></div>\n<header>')

QUIZ = '''<form class="form quiz" id="leadForm" novalidate>
    <div class="qh"><span id="qStep">Шаг 1 из 3</span><span class="qd" aria-hidden="true"><i class="on"></i><i></i><i></i></span></div>
    <fieldset class="on" data-s="1"><legend>Что ищете?</legend>
      <div class="ch" role="group" aria-label="Что ищете"><button type="button" aria-pressed="true" data-q="flat">Квартиру</button><button type="button" aria-pressed="false" data-q="house">Дом</button><button type="button" aria-pressed="false" data-q="reno">Ремонт</button><button type="button" aria-pressed="false" data-q="mort">Ипотеку</button></div></fieldset>
    <fieldset data-s="2"><legend id="q2l">Какой бюджет?</legend>
      <div class="rng"><label for="qb"><span id="qbl">Бюджет до</span> <b id="qbv"></b></label><input type="range" id="qb" min="3" max="30" step="0.5" value="9"></div>
      <div class="ch2" id="qr" role="group" aria-label="Комнат"><button type="button" aria-pressed="false" data-r="0">Студия</button><button type="button" aria-pressed="true" data-r="1">1</button><button type="button" aria-pressed="true" data-r="2">2</button><button type="button" aria-pressed="false" data-r="3">3</button><button type="button" aria-pressed="false" data-r="4">4+</button></div>
      <p class="qm" id="qMatch" aria-live="polite"></p></fieldset>
    <fieldset data-s="3"><legend>Куда прислать подборку?</legend>
      <div class="f"><label for="ln">Как к вам обращаться</label><input id="ln" autocomplete="name" placeholder="Имя"></div>
      <div class="f"><label for="lp">Телефон</label><input id="lp" type="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" aria-describedby="lpErr"><span class="err" id="lpErr">Введите номер полностью — 10 цифр после +7</span></div></fieldset>
    <div class="qnav"><button type="button" class="btn ghost" id="qBack" hidden>Назад</button><button type="button" class="btn red" id="qNext">Дальше</button><button class="btn red" type="submit" id="qSend" hidden>Получить подборку</button></div>
    <small>Нажимая «Получить подборку», вы соглашаетесь на обработку персональных данных.</small>
    <div class="done"><b>Заявка принята<i class="o"></i></b>Менеджер позвонит и пришлёт подборку. Если удобнее — напишите в чат на сайте.</div>
  '''
cut('<form class="form" id="leadForm" novalidate>', '</form>', QUIZ)

# ссылки на объект и дом + «Поделиться»
SHARE = '<button type="button" class="ib share" data-share aria-label="Поделиться ссылкой"><svg class="ico"><use href="#share"/></svg></button>'
rep('<a class="btn white" href="#lead" id="qvLead">Записаться на просмотр</a>', '<a class="btn white" href="#lead" id="qvLead">Записаться на просмотр</a>' + SHARE)
rep('<a class="btn white" href="#lead" id="hvLead">Обсудить проект</a>', '<a class="btn white" href="#lead" id="hvLead">Обсудить проект</a>' + SHARE)
rep('function quick(it) {\n', "function quick(it) {\n  setHash('obj-' + it.id);\n")
rep("function houseView(h) {\n  dlg.classList.add('wide');", "function houseView(h) {\n  dlg.classList.add('wide'); setHash('house-' + h.id);")
rep("dlg.addEventListener('close', () => dlg.classList.remove('wide'));",
    "dlg.addEventListener('close', () => { dlg.classList.remove('wide'); if (/^#(obj|house)-/.test(location.hash)) history.replaceState(null, '', location.pathname + location.search); });")

JS = r'''
// ссылки на объект и дом
function setHash(h) { try { history.replaceState(null, '', '#' + h); } catch (e) {} }
document.addEventListener('click', async e => {
  if (!e.target.closest('[data-share]')) return;
  const url = location.href, title = $('#dlgT').textContent + ' — Платформа недвижимости';
  try { if (navigator.share) { await navigator.share({title, url}); return; } await navigator.clipboard.writeText(url); toast('Ссылка скопирована — отправьте её родным'); }
  catch (x) { if (x.name !== 'AbortError') toast('Скопируйте ссылку из адресной строки'); }
});
(() => { const m = location.hash.match(/^#(obj|house)-(\w+)$/); if (!m) return;
  const t = m[1] === 'obj' ? ITEMS[+m[2]] : byId(m[2]); if (t) (m[1] === 'obj' ? quick : houseView)(t); })();

// линия прокрутки: к концу страницы — точка
const prog = $('#prog');
function progUpd() { const h = document.documentElement.scrollHeight - innerHeight, k = h > 0 ? Math.min(1, scrollY / h) : 0; prog.style.setProperty('--s', k); prog.classList.toggle('end', k > .995); }
addEventListener('scroll', progUpd, {passive: true}); addEventListener('resize', progUpd); progUpd();
new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { $('.fbig').classList.add('in'); o.disconnect(); } }, {threshold: .6}).observe($('.fbig'));

// подбор за 3 шага
let qs = 1, qType = 'flat';
const Q2 = {
  flat: {l: 'Какой бюджет на квартиру?', bl: 'Бюджет до', min: 3, max: 20, step: .5, v: 9, rooms: true},
  house: {l: 'Какой бюджет на дом?', bl: 'Бюджет до', min: 10, max: 40, step: 1, v: 20},
  reno: {l: 'Какая площадь квартиры?', bl: 'Площадь', min: 20, max: 160, step: 1, v: 55},
  mort: {l: 'Сколько стоит квартира?', bl: 'Стоимость', min: 3, max: 20, step: .5, v: 8},
};
function qMatch() {
  const c = Q2[qType], v = +$('#qb').value, mil = v * 1e6;
  $('#qbv').textContent = qType === 'reno' ? v + ' м²' : v.toLocaleString('ru-RU') + ' млн ₽';
  let t;
  if (qType === 'flat') {
    const rooms = $$('#qr [aria-pressed=true]').map(b => +b.dataset.r);
    const n = ITEMS.filter(it => it.p <= mil && (!rooms.length || rooms.some(r => r === 4 ? it.r >= 4 : it.r === r))).length;
    t = n ? `Подходит <b>${n} ${plural(n, 'квартира', 'квартиры', 'квартир')}</b> из проверенных. Пришлём их и новые, как только появятся.` : 'Сейчас таких нет — подберём под ваши условия и сообщим первыми.';
  } else if (qType === 'house') {
    const ok = HOUSES.filter(h => hFrom(h) <= mil);
    t = ok.length ? `Укладываются: <b>${ok.map(h => h.line + ' ' + h.n).join(', ')}</b>. Остаток можно платить по этапам или в рассрочку до 5 лет.` : 'Подберём площадь и материал под ваш бюджет — проекты настраиваются.';
  } else if (qType === 'reno') {
    t = `Ориентир с материалами: <b>от ${fmtM(v * 20000)}</b> за базовую отделку до ${fmtM(v * 100000)} за премиум. Точную цену даст смета после замера.`;
  } else {
    t = `По семейной ипотеке 6 % со взносом 20 % на 30 лет: <b>от ${Math.round(ann(mil, 6)).toLocaleString('ru-RU')} ₽/мес</b>. Подберём банк с индивидуальной ставкой.`;
  }
  $('#qMatch').innerHTML = t;
  $('#qr').hidden = !c.rooms;
}
function qSet(type) {
  qType = type; const c = Q2[type], r = $('#qb');
  Object.assign(r, {min: c.min, max: c.max, step: c.step}); r.value = c.v;
  $('#q2l').textContent = c.l; $('#qbl').textContent = c.bl; qMatch(); fillAll();
}
function qGo(n) {
  qs = n; $$('#leadForm fieldset').forEach(f => f.classList.toggle('on', +f.dataset.s === n));
  $('#qStep').textContent = `Шаг ${n} из 3`; $$('.qd i').forEach((d, i) => d.classList.toggle('on', i < n));
  $('#qBack').hidden = n === 1; $('#qNext').hidden = n === 3; $('#qSend').hidden = n !== 3;
  if (n === 3) $('#ln').focus();
}
$$('#leadForm .ch button').forEach(b => b.addEventListener('click', () => qSet(b.dataset.q)));
$$('#qr button').forEach(b => b.addEventListener('click', () => { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true'); qMatch(); }));
$('#qb').addEventListener('input', qMatch);
$('#qNext').addEventListener('click', () => qGo(qs + 1));
$('#qBack').addEventListener('click', () => qGo(qs - 1));
qSet('flat');
'''
rep('</script>\n</body>', JS + '</script>\n</body>')

open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok', len(s))
