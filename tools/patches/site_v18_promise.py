"""Сайт v18 — блок «Обещания» переделан: «Обещаем — и пишем это в договор» показано буквально.
Слева три обещания крупно; справа лист договора с пунктами-обязательствами, внизу подпись — красная точка встаёт печатью,
когда лист появляется на экране. Наведение / нажатие на обещание подсвечивает пункты договора, которые его подтверждают.
Run из корня репо после site_v17_motion.py: py -3 tools/patches/site_v18_promise.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


i = s.index('<section class="sec" style="padding-top:0"><div class="w">\n  <div class="br">[ <b>●</b> Обещания ]</div>')
j = s.index('</div></section>', i) + len('</div></section>')
s = s[:i] + '''<section class="sec pact" id="pact"><div class="w pgrid2">
  <div class="pl">
    <div class="br">[ <b>●</b> Обещания ]</div>
    <h2 class="t">Обещаем — и&nbsp;пишем это в&nbsp;<span class="nw">договор<i class="o"></i></span></h2>
    <ol class="vows" role="list">
      <li><button type="button" data-cl="3,5" aria-describedby="vw1"><b>Проверено<i class="o"></i></b><span id="vw1">Квартиры — только от застройщиков, которых проверили сами. Ремонт и дома делают наши бригады.</span></button></li>
      <li><button type="button" data-cl="1,2" aria-describedby="vw2"><b>Выгодно<i class="o"></i></b><span id="vw2">Спецпредложения напрямую от застройщиков и индивидуальные ставки банков. Комиссии для покупателя нет.</span></button></li>
      <li><button type="button" data-cl="4,6" aria-describedby="vw3"><b>Ясно<i class="o"></i></b><span id="vw3">Цена, срок и следующий шаг — на бумаге до начала работ. Без звёздочек и многоточий.</span></button></li>
    </ol>
  </div>
  <figure class="sheet" aria-label="Обязательства Платформы в договоре">
    <div class="sh-h"><span>Договор № ПН-2026</span><span>г. Екатеринбург</span></div>
    <div class="sh-t">Раздел 3. Обязательства Платформы</div>
    <ol class="cl">
      <li data-n="1"><span>3.1</span><p>Комиссия с покупателя — <b>0&nbsp;₽</b>. Мы получаем вознаграждение от застройщика.</p></li>
      <li data-n="2"><span>3.2</span><p>Ставку по ипотеке подбираем среди <b>6 банков-партнёров</b> и показываем расчёт до подачи заявки.</p></li>
      <li data-n="3"><span>3.3</span><p>Деньги за новостройку хранятся на <b>эскроу-счёте</b> в банке до сдачи дома.</p></li>
      <li data-n="4"><span>3.4</span><p>Каждый этап ремонта и стройки закрываем <b>промежуточным актом</b>. Цена в смете не меняется без вашей подписи.</p></li>
      <li data-n="5"><span>3.5</span><p>Гарантия на ремонт и дома — <b>5&nbsp;лет</b>. Устраняем недостатки за свой счёт.</p></li>
      <li data-n="6"><span>3.6</span><p>Если партнёр подвёл — <b>решаем вопрос за вас</b>: переговоры, претензия, замена подрядчика.</p></li>
    </ol>
    <div class="sign"><div><span class="k">Платформа недвижимости</span><span class="ln"><i class="seal" aria-hidden="true"></i></span></div><div><span class="k">Клиент</span><span class="ln"></span></div></div>
    <figcaption>Пример раздела договора. Точные формулировки — в договоре по вашему объекту.</figcaption>
  </figure>
</div></section>''' + s[j:]

CSS = r'''
/* v18 — обещания = договор */
.pact{background:var(--night);color:var(--milk);overflow:hidden}
.pact .br{color:#8A867F}.pact h2.t{color:var(--milk);max-width:780px}
.pgrid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.95fr);gap:clamp(40px,6vw,140px);align-items:center}
.vows{list-style:none;margin:48px 0 0;padding:0;counter-reset:none}
.vows li{border-top:1px solid #ffffff1f}.vows li:last-child{border-bottom:1px solid #ffffff1f}
.vows button{all:unset;box-sizing:border-box;display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:24px;align-items:baseline;width:100%;padding:26px 0;cursor:pointer}
.vows b{font:300 clamp(40px,4vw,96px)/1 Manrope;letter-spacing:-.05em;color:#ffffff59;transition:color .3s}
.vows span{color:#8A867F;font-size:clamp(15px,1vw,18px);transition:color .3s}
.vows button:hover b,.vows button:focus-visible b,.vows button.on b{color:var(--milk)}
.vows button:hover span,.vows button.on span{color:#C9C5BE}
.vows button:focus-visible{outline:2px solid var(--red);outline-offset:4px}
.sheet{margin:0;background:#FBFAF7;color:var(--ink);border-radius:6px;padding:clamp(26px,2.6vw,48px);box-shadow:0 40px 90px #00000080,0 0 0 1px #ffffff0d;transform:rotate(1.2deg);position:relative;
  background-image:linear-gradient(#0000 calc(100% - 1px),#0000000a 0);background-size:100% 30px}
.sheet::before{content:'';position:absolute;inset:10px -10px -10px 10px;background:#E9E5DE;border-radius:6px;z-index:-1;transform:rotate(-2.2deg)}
.sh-h{display:flex;justify-content:space-between;font-size:12px;color:var(--mut);border-bottom:1px solid var(--ink);padding-bottom:10px}
.sh-t{font:600 15px Manrope;margin:18px 0 6px}
.cl{list-style:none;margin:0;padding:0}
.cl li{display:grid;grid-template-columns:38px 1fr;gap:6px;padding:10px 8px;margin:0 -8px;border-radius:8px;transition:background .3s,opacity .3s}
.cl li span{font:600 13px Manrope;color:var(--mut);padding-top:2px}.cl li p{margin:0;font-size:15px;line-height:1.5}
.cl li b{font-weight:700}
.cl.hl li{opacity:.35}.cl.hl li.on{opacity:1;background:#FEECE8}.cl.hl li.on span{color:var(--red-ui)}
.sign{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:22px}
.sign .k{display:block;font-size:12px;color:var(--mut)}.sign .ln{display:block;position:relative;height:40px;border-bottom:1px solid var(--ink)}
.seal{position:absolute;left:30%;bottom:6px;width:26px;height:26px;border-radius:50%;background:var(--red)}
.js .seal{transform:scale(4);opacity:0;transition:transform .45s cubic-bezier(.5,1.6,.5,1),opacity .2s}
.js .sheet.in .seal{transform:none;opacity:1}
.sheet figcaption{margin-top:18px;font-size:12px;color:var(--mut)}
@media(min-width:1700px){.cl li p{font-size:17px}.sh-t{font-size:17px}}
@media(max-width:1100px){.pgrid2{grid-template-columns:minmax(0,1fr)}.sheet{transform:none;max-width:640px}}
@media(max-width:800px){.vows button{grid-template-columns:minmax(0,1fr);gap:8px;padding:20px 0}.vows b{font-size:44px}.sheet{padding:22px 18px}.sheet::before{display:none}.cl li p{font-size:14px}.sign{gap:14px}}
@media(prefers-reduced-motion:reduce){.js .seal{transform:none;opacity:1}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

JS = r'''
// обещания ↔ пункты договора
const cl = $('.cl');
function vow(b) { const on = b && b.dataset.cl.split(','); $$('.vows button').forEach(x => x.classList.toggle('on', x === b)); cl.classList.toggle('hl', !!b); $$('.cl li').forEach(li => li.classList.toggle('on', !!on && on.includes(li.dataset.n))); }
$$('.vows button').forEach(b => { b.addEventListener('mouseenter', () => vow(b)); b.addEventListener('focus', () => vow(b)); b.addEventListener('click', () => vow(b.classList.contains('on') ? null : b)); });
$('.vows').addEventListener('mouseleave', () => vow(null));
new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { $('.sheet').classList.add('in'); o.disconnect(); } }, {threshold: .6}).observe($('.sheet'));
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
