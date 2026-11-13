"""Сайт v22 — блок «Отбор» понятнее: компактный сканер вместо большого поля точек.
Луч проходит по полю объектов, справа подсвечивается текущий пункт проверки (застройщик / вторичка / ремонт и дома),
не прошедшие гаснут прямо под лучом, счётчик «на входе → прошли»; в конце прошедшие загораются красным. «Ваш выбор» убран.
Цифры: табло с крутящимися разрядами + точки под каждой цифрой (5 лет — 5 точек; 1 точка = 50 сделок; 67; 85).
Run из корня репо после site_v21_tiles.py: py -3 tools/patches/site_v22_scan.py"""
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


cut('  <div class="mgrid">', '</div></section>', '''  <div class="scan" id="scan">
    <div class="sfield" id="sfield" role="img" aria-label="Проверка объектов: луч проходит по полю, не прошедшие проверку гаснут"><span class="beam" id="beam"></span></div>
    <div class="spanel">
      <h3>Как мы ручаемся<i class="o"></i></h3>
      <div class="ctabs" role="group" aria-label="Кого проверяем"><button aria-pressed="true" data-k="dev">Застройщик</button><button aria-pressed="false" data-k="sec">Вторичка</button><button aria-pressed="false" data-k="our">Ремонт и дома</button></div>
      <ul class="clist" id="clist"></ul>
      <div class="smeter" aria-live="polite"><div><b id="sIn">144</b><span>объекта на входе</span></div><div><b id="sOut">144</b><span id="sOutL">проходят проверку</span></div></div>
    </div>
  </div>
  <div class="stats2">
    <div class="st"><div class="odo" data-n="5" aria-label="5"></div><span>лет на рынке Екатеринбурга</span><div class="sd" data-n="5"></div></div>
    <div class="st"><div class="odo" data-n="1985" aria-label="1985"></div><span>сделок с квартирами</span><div class="sd" data-n="40"></div><small>1 точка — 50 сделок</small></div>
    <div class="st"><div class="odo" data-n="67" aria-label="67"></div><span>договоров на строительство домов</span><div class="sd" data-n="67"></div></div>
    <div class="st"><div class="odo" data-n="85" aria-label="85"></div><span>квартир с нашей отделкой</span><div class="sd" data-n="85"></div></div>
  </div>
''')

CSS = r'''
/* v22 — сканер отбора */
.scan{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);gap:0;margin-top:60px;background:#1C1C1E;border-radius:28px;overflow:hidden}
.sfield{position:relative;display:grid;grid-template-columns:repeat(16,1fr);align-content:center;gap:14px 0;padding:34px 30px;background:#161618;min-height:340px;overflow:hidden}
.sfield i{width:10px;height:10px;border-radius:50%;background:#55535A;justify-self:center;transition:opacity .35s,transform .35s,background .35s}
.sfield i.off{opacity:.12;transform:scale(.6)}
.sfield i.hit{background:#fff}
.sfield i.pass{background:var(--red);transform:scale(1.5);opacity:1}
.beam{position:absolute;top:0;bottom:0;left:0;width:90px;transform:translateX(-110px);pointer-events:none;
  background:linear-gradient(90deg,#F5553C00 0%,#F5553C1f 70%,#F5553Cb3 97%,#fff 100%);mix-blend-mode:screen;opacity:0}
.beam.go{opacity:1;animation:sweep var(--dur,1.5s) linear forwards}
@keyframes sweep{from{transform:translateX(-110px)}to{transform:translateX(var(--w,600px))}}
.spanel{padding:30px;display:flex;flex-direction:column}
.spanel h3{margin:0;font:500 26px/1.15 Manrope;letter-spacing:-.02em}
.scan .clist li{position:relative;transition:color .3s,padding .3s}
.scan .clist li::before{content:'';position:absolute;left:0;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:transparent;transition:background .3s}
.scan .clist li::after{content:'';position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--red);transform:scaleX(0);transform-origin:left}
.scan .clist li.act{padding-left:22px;color:#fff}.scan .clist li.act::before{background:var(--red)}
.scan .clist li.act::after{animation:fillx var(--dur,1.5s) linear forwards}
@keyframes fillx{to{transform:scaleX(1)}}
.scan .clist li.pass{padding-left:22px;color:var(--milk)}.scan .clist li.pass::before{background:none;border-left:2px solid var(--red);border-bottom:2px solid var(--red);width:8px;height:4px;border-radius:0;transform:rotate(-45deg);margin-top:-5px}
.scan .clist li{color:#A9A49B}
.smeter{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:auto;padding-top:22px}
.smeter b{display:block;font:300 44px/1 Manrope;letter-spacing:-.04em;color:var(--milk);font-variant-numeric:tabular-nums}
.smeter div:last-child b{color:var(--red)}.smeter span{display:block;font-size:13px;color:#8A867F;margin-top:6px}
/* цифры: табло + точки */
.stats2{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px;margin-top:60px;border-top:1px solid #ffffff1f;padding-top:36px}
.odo{display:flex;font:300 clamp(56px,5.4vw,140px)/1 Manrope;letter-spacing:-.05em;color:var(--red);height:1em;overflow:hidden}
.odo .col{display:flex;flex-direction:column;transition:transform 1.8s cubic-bezier(.15,.8,.2,1)}
.odo .col span{display:block;height:1em;line-height:1}
.odo .gap{width:.22em}
.st>span{display:block;color:#A9A49B;font-size:14px;margin-top:10px;max-width:240px}
.sd{display:grid;grid-template-columns:repeat(17,8px);gap:6px;margin-top:16px}
.sd i{width:8px;height:8px;border-radius:50%;background:#2E2D31;transition:background .3s}
.sd i.on{background:var(--red)}
.st small{display:block;font-size:11px;color:#6E6A64;margin-top:8px}
@media(min-width:1700px){.st>span{font-size:17px;max-width:280px}.smeter b{font-size:56px}}
@media(max-width:1000px){.scan{grid-template-columns:minmax(0,1fr)}.sfield{min-height:240px;grid-template-columns:repeat(12,1fr);padding:24px}.sfield i.x12{display:none}}
@media(max-width:800px){.stats2{grid-template-columns:repeat(2,minmax(0,1fr))}.odo{font-size:56px}.sd{grid-template-columns:repeat(12,7px);gap:5px}.sd i{width:7px;height:7px}.spanel{padding:22px 20px}}
@media(prefers-reduced-motion:reduce){.beam{display:none}.odo .col{transition:none}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

cut('// отбор: сотни точек → одна красная', "new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { runFunnel(); o.disconnect(); } }, {threshold: .35}).observe(field);", r'''// отбор: сканер
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const SF = $('#sfield'), SC = 16, SN = SC * 9;
SF.insertAdjacentHTML('beforeend', Array.from({length: SN}, (_, i) => `<i class="${i % SC >= 12 ? 'x12' : ''}"></i>`).join(''));
const sdots = $$('#sfield i');
let scanT = [], scanRun = 0;
function scanStop() { scanT.forEach(clearTimeout); scanT = []; scanRun++; }
function scanStart() {
  if (window.__noScan) return;
  scanStop(); const run = scanRun, cols = () => innerWidth <= 1000 ? 12 : SC;
  const vis = () => sdots.filter((d, i) => i % SC < cols());
  const lis = $$('#clist li'), DUR = 1500, GAP = 450;
  sdots.forEach(d => d.classList.remove('off', 'pass', 'hit')); lis.forEach(l => l.classList.remove('act', 'pass'));
  let alive = vis(); const total = alive.length;
  $('#sIn').textContent = total; $('#sOut').textContent = total; $('#sOutL').textContent = 'проходят проверку';
  const finalN = 6, keep = new Set(alive.slice().sort(() => Math.random() - .5).slice(0, finalN));
  if (reduce) { alive.forEach(d => d.classList.add(keep.has(d) ? 'pass' : 'off')); lis.forEach(l => l.classList.add('pass')); $('#sOut').textContent = finalN; $('#sOutL').textContent = 'прошли все проверки'; return; }
  const beam = $('#beam'), W = SF.clientWidth;
  lis.forEach((li, s) => {
    scanT.push(setTimeout(() => {
      if (run !== scanRun) return;
      lis.forEach((l, k) => { l.classList.toggle('act', k === s); if (k < s) l.classList.add('pass'); });
      beam.classList.remove('go'); void beam.offsetWidth; beam.style.setProperty('--w', W + 'px'); beam.style.setProperty('--dur', DUR + 'ms'); beam.classList.add('go');
      li.style.setProperty('--dur', DUR + 'ms');
      const left = alive.filter(d => !keep.has(d)), drop = s === lis.length - 1 ? left : left.sort(() => Math.random() - .5).slice(0, Math.round(left.length * .45));
      drop.forEach(d => { const x = (d.offsetLeft + 5) / W; scanT.push(setTimeout(() => { if (run !== scanRun) return; d.classList.add('hit'); setTimeout(() => { d.classList.remove('hit'); d.classList.add('off'); }, 140); $('#sOut').textContent = +$('#sOut').textContent - 1; }, x * DUR)); });
      alive = alive.filter(d => !drop.includes(d));
    }, s * (DUR + GAP)));
  });
  scanT.push(setTimeout(() => { if (run !== scanRun) return; lis.forEach(l => { l.classList.remove('act'); l.classList.add('pass'); }); keep.forEach(d => d.classList.add('pass')); $('#sOut').textContent = finalN; $('#sOutL').textContent = 'прошли все проверки'; }, lis.length * (DUR + GAP)));
  scanT.push(setTimeout(() => { if (run === scanRun) scanStart(); }, lis.length * (DUR + GAP) + 4500));
}
new IntersectionObserver(es => { es[0].isIntersecting ? scanStart() : scanStop(); }, {threshold: .35}).observe($('#scan'));''', keep_b=False)
rep("$$('.ctabs button').forEach(b => b.addEventListener('click', () => { $$('.ctabs button').forEach(x => x.setAttribute('aria-pressed', x === b)); showChecks(b.dataset.k); }));",
    "$$('.ctabs button').forEach(b => b.addEventListener('click', () => { $$('.ctabs button').forEach(x => x.setAttribute('aria-pressed', x === b)); showChecks(b.dataset.k); scanStart(); }));")
cut("new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect(); $$('.stats b')", '\n', r'''// цифры: табло и точки
$$('.odo').forEach(o => { const str = (+o.dataset.n).toLocaleString('ru-RU'); o.innerHTML = [...str].map(ch => /\d/.test(ch) ? `<span class="col" data-d="${ch}">${'0123456789'.repeat(2).split('').map(x => `<span>${x}</span>`).join('')}</span>` : '<span class="gap"></span>').join(''); });
$$('.sd').forEach(d => { d.innerHTML = '<i></i>'.repeat(+d.dataset.n); });
function statsGo() {
  $$('.odo').forEach((o, k) => $$('.col', o).forEach((c, j) => { c.style.transitionDelay = (k * 150 + j * 120) + 'ms'; c.style.transform = `translateY(-${10 + +c.dataset.d}em)`; }));
  $$('.sd').forEach((d, k) => $$('i', d).forEach((dot, j) => setTimeout(() => dot.classList.add('on'), reduce ? 0 : 300 + k * 150 + j * (1400 / d.children.length))));
}
new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect(); statsGo(); }, {threshold: .4}).observe($('.stats2'));
''', keep_b=False)
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
