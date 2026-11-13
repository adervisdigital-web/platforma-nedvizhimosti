"""Сайт v25 — «Обещания»: мокап договора на столе вместо плоского листа.
Фото стола с чистым листом (RealVisXL + hi-res, photo/desk_contract.jpg), текст договора наложен на лист по замеренным
границам (left 29.6 %, top 10.4 %, w 44.3 %, h 63.7 %) с multiply — тени бумаги сохраняются; размеры шрифта в cqw.
Динамика: при появлении пункты проступают по одному с красными галочками, подпись Платформы прорисовывается линией,
падает красная точка-печать; наведение на обещание слева подсвечивает пункты маркером; карточка чуть следует за курсором.
Run из корня репо после site_v24_search.py: py -3 tools/patches/site_v25_contract.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


i = s.index('  <figure class="sheet"'); j = s.index('</figure>', i) + len('</figure>')
s = s[:i] + '''  <figure class="desk" id="desk" aria-label="Договор с обязательствами Платформы на столе">
    <div class="dk-in"><img src="photo/desk_contract.jpg" alt="" loading="lazy" class="dk-ph">
      <div class="paper">
        <div class="pp-h"><span class="pp-logo"><svg viewBox="0 0 76 72" aria-hidden="true"><use href="#mark"/></svg>ПЛАТФОРМА НЕДВИЖИМОСТИ</span><span>Договор № ПН-2026-0147</span></div>
        <div class="pp-t">3. Обязательства Платформы</div>
        <ol class="cl">
          <li data-n="1"><span>3.1</span><p>Комиссия с покупателя — <b>0&nbsp;₽</b>. Вознаграждение платит застройщик.</p></li>
          <li data-n="2"><span>3.2</span><p>Ставку подбираем среди <b>6 банков</b> и показываем расчёт до заявки.</p></li>
          <li data-n="3"><span>3.3</span><p>Деньги за новостройку — на <b>эскроу-счёте</b> до сдачи дома.</p></li>
          <li data-n="4"><span>3.4</span><p>Каждый этап закрываем <b>актом</b>. Смета не меняется без вашей подписи.</p></li>
          <li data-n="5"><span>3.5</span><p>Гарантия на ремонт и дома — <b>5&nbsp;лет</b>.</p></li>
          <li data-n="6"><span>3.6</span><p>Если партнёр подвёл — <b>решаем вопрос за вас</b>.</p></li>
        </ol>
        <div class="sign"><div><span class="k">Платформа</span><span class="ln"><svg class="sig" viewBox="0 0 120 34" aria-hidden="true"><path d="M3 26c8-3 12-18 18-19 5-1-2 21 4 20 6-1 9-15 14-15 4 0 0 13 5 13 6 0 9-12 15-12 5 0 2 9 7 9 9 0 20-10 36-14"/></svg><i class="seal"></i></span></div>
          <div><span class="k">Клиент</span><span class="ln"><a class="you" href="#lead">ваша подпись</a></span></div></div>
      </div>
    </div>
    <figcaption>Пример раздела договора. Точные формулировки — в договоре по вашему объекту.</figcaption>
  </figure>''' + s[j:]

CSS = r'''
/* v25 — договор на столе */
.desk{margin:0;position:relative}
.dk-in{position:relative;border-radius:28px;overflow:hidden;aspect-ratio:1824/1536;box-shadow:0 40px 90px #00000080;container-type:inline-size;transform:perspective(1600px) rotateX(var(--drx,0deg)) rotateY(var(--dry,0deg));transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.desk.move .dk-in{transition:transform .12s linear}
.dk-ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.paper{position:absolute;left:29.6%;top:10.4%;width:44.3%;height:63.7%;padding:3.4cqw 3.2cqw 2.6cqw;display:flex;flex-direction:column;color:#1B1A19;mix-blend-mode:multiply}
.pp-h{display:flex;justify-content:space-between;align-items:center;gap:1cqw;font-size:1.05cqw;color:#6B675F;border-bottom:.12cqw solid #1B1A19;padding-bottom:1cqw}
.pp-logo{display:flex;align-items:center;gap:.7cqw;letter-spacing:.18em;font-size:.95cqw;color:#1B1A19}.pp-logo svg{width:2.2cqw;height:2.1cqw;fill:#1B1A19}
.pp-t{font:700 1.6cqw/1.2 Manrope;margin:1.8cqw 0 .8cqw}
.desk .cl{list-style:none;margin:0;padding:0}
.desk .cl li{display:grid;grid-template-columns:3cqw 1fr;gap:.4cqw;padding:.7cqw .6cqw;margin:0 -.6cqw;border-radius:.6cqw;transition:background .35s,opacity .5s,transform .5s}
.desk .cl li span{font:700 1.15cqw/1.45 Manrope;color:#6B675F;position:relative}
.desk .cl li p{margin:0;font-size:1.3cqw;line-height:1.45}
.desk .cl li span::after{content:'';position:absolute;left:-1.6cqw;top:.35cqw;width:.9cqw;height:.45cqw;border-left:.25cqw solid var(--red);border-bottom:.25cqw solid var(--red);transform:rotate(-45deg) scale(0);transition:transform .35s cubic-bezier(.3,1.6,.5,1)}
.js .desk .cl li{opacity:0;transform:translateY(.6cqw)}
.desk.in .cl li{opacity:1;transform:none}.desk.in .cl li.ok span::after{transform:rotate(-45deg) scale(1)}
.desk .cl.hl li{opacity:.3}.desk .cl.hl li.on{opacity:1;background:#F5553C40}
.desk .sign{display:grid;grid-template-columns:1fr 1fr;gap:2cqw;margin-top:auto}
.desk .sign .k{display:block;font-size:1cqw;color:#6B675F}
.desk .sign .ln{display:block;position:relative;height:3.6cqw;border-bottom:.12cqw solid #1B1A19}
.sig{position:absolute;left:0;bottom:.2cqw;width:11cqw;height:3.2cqw;fill:none;stroke:#1F2A5A;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:260;stroke-dashoffset:260}
.desk.signed .sig{transition:stroke-dashoffset 1.3s cubic-bezier(.6,0,.3,1);stroke-dashoffset:0}
.desk .seal{position:absolute;left:9cqw;bottom:.6cqw;width:2.4cqw;height:2.4cqw;border-radius:50%;background:var(--red);transform:scale(3.5);opacity:0;transition:transform .45s cubic-bezier(.5,1.6,.5,1),opacity .2s}
.desk.sealed .seal{transform:none;opacity:1}
.you{position:absolute;left:0;bottom:.5cqw;font-size:1.05cqw;font-weight:700;color:var(--red-ui);border-bottom:1px dashed var(--red-ui);mix-blend-mode:normal}
.you::after{content:'';display:inline-block;width:.12cqw;height:1.2cqw;background:var(--red-ui);margin-left:.3cqw;vertical-align:-.15cqw;animation:caret 1s steps(1) infinite}
@keyframes caret{50%{opacity:0}}
.desk figcaption{margin-top:14px;font-size:12px;color:#8A867F;text-align:center}
@media(min-width:1101px){.pgrid2{grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr)}}
@media(max-width:1100px){.desk{max-width:720px}}
@media(max-width:800px){.desk{border-radius:20px;overflow:hidden;box-shadow:0 30px 60px #00000080}.dk-in{width:210%;margin:-13% 0 -27% -55%;border-radius:0;transform:none!important;box-shadow:none}.desk figcaption{margin:0;padding:12px 0 2px;background:var(--night)}}
@media(prefers-reduced-motion:reduce){.js .desk .cl li{opacity:1;transform:none}.sig{stroke-dashoffset:0}.desk .seal{transform:none;opacity:1}.you::after{animation:none}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

a = "new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { $('.sheet').classList.add('in'); o.disconnect(); } }, {threshold: .6}).observe($('.sheet'));"
rep(a, r'''(() => { const desk = $('#desk');
  function play() { const lis = $$('.cl li', desk); desk.classList.add('in'); const st = reduce ? 0 : 260;
    lis.forEach((li, k) => setTimeout(() => li.classList.add('ok'), st * (k + 1)));
    setTimeout(() => desk.classList.add('signed'), st * (lis.length + 1)); setTimeout(() => desk.classList.add('sealed'), st * (lis.length + 1) + (reduce ? 0 : 1300)); }
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { play(); o.disconnect(); } }, {threshold: .45}).observe(desk);
  if (!reduce && matchMedia('(hover:hover)').matches) {
    desk.addEventListener('mousemove', e => { const r = desk.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      desk.classList.add('move'); desk.style.setProperty('--dry', (x * 6).toFixed(2) + 'deg'); desk.style.setProperty('--drx', (-y * 5).toFixed(2) + 'deg'); });
    desk.addEventListener('mouseleave', () => { desk.classList.remove('move'); desk.style.setProperty('--dry', '0deg'); desk.style.setProperty('--drx', '0deg'); });
  } })();''')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
