"""Сайт v26 — заставка при запуске: знак «П» рисуется линией и заливается, падает красная точка, проявляется
ПЛАТФОРМА НЕДВИЖИМОСТИ, внизу — полоска загрузки с процентами (по событию load страницы, минимум 1,4 с, максимум 4 с).
Затем заставка уезжает вверх шторкой, и только после этого стартует постановка первого экрана (html.ready).
Повторный заход в той же вкладке — короткая версия (0,5 с); prefers-reduced-motion — простое затухание.
Run из корня репо после site_v25_contract.py: py -3 tools/patches/site_v26_loader.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


ARCH = 'M0 72 V24 A24 24 0 0 1 48 24 V72 H33 V26 A9 9 0 0 0 15 26 V72 Z'
CSS = r'''
/* v26 — заставка */
.ldr{position:fixed;inset:0;z-index:200;background:var(--night);color:var(--milk);display:flex;align-items:center;justify-content:center;transition:transform .8s cubic-bezier(.75,0,.2,1)}
.ldr.out{transform:translateY(-100%)}.ldr.gone{display:none}
.ldr-in{display:flex;align-items:center;gap:26px}
.ldr-mark{width:96px;height:91px;overflow:visible}
.ldr-arch{fill:#F4F2EE00;stroke:var(--milk);stroke-width:1.2;stroke-dasharray:330;stroke-dashoffset:330;animation:ldraw .9s cubic-bezier(.6,0,.3,1) .1s forwards,lfill .35s ease .95s forwards}
.ldr-dot{fill:var(--red);transform-box:fill-box;transform-origin:50% 100%;transform:translateY(-140px) scale(.6);opacity:0;animation:ldrop .7s cubic-bezier(.3,.9,.4,1) 1.05s forwards}
@keyframes ldraw{to{stroke-dashoffset:0}}@keyframes lfill{to{fill:#F4F2EE;stroke-width:0}}
@keyframes ldrop{0%{transform:translateY(-140px) scale(.6);opacity:0}55%{transform:translateY(4px) scale(1.15,.82);opacity:1}75%{transform:translateY(-6px) scale(.95,1.05);opacity:1}100%{transform:none;opacity:1}}
.ldr-word b{display:block;font:300 30px/1 Manrope;letter-spacing:.9em;opacity:0;animation:lword .9s cubic-bezier(.2,.7,.2,1) .7s forwards}
.ldr-word small{display:block;font:400 11px/1 Manrope;letter-spacing:.5em;color:#8A867F;margin-top:12px;opacity:0;animation:lfade .6s ease 1.1s forwards}
@keyframes lword{to{letter-spacing:.42em;opacity:1}}@keyframes lfade{to{opacity:1}}
.ldr-bar{position:absolute;left:clamp(16px,3.4vw,110px);right:clamp(16px,3.4vw,110px);bottom:clamp(28px,6vh,64px);height:2px;background:#ffffff1a}
.ldr-bar i{display:block;height:100%;width:0;background:var(--red);transition:width .3s ease}
.ldr-pc{position:absolute;right:clamp(16px,3.4vw,110px);bottom:calc(clamp(28px,6vh,64px) + 14px);font:500 13px Manrope;color:#8A867F;font-variant-numeric:tabular-nums}
.ldr-city{position:absolute;left:clamp(16px,3.4vw,110px);bottom:calc(clamp(28px,6vh,64px) + 14px);font:500 13px Manrope;color:#8A867F}
.ldr.quick .ldr-arch{animation-duration:.01s,.01s;animation-delay:0s,0s}.ldr.quick .ldr-dot{animation-duration:.3s;animation-delay:.05s}.ldr.quick .ldr-word b,.ldr.quick .ldr-word small{animation-duration:.2s;animation-delay:0s}
.js:not(.ready) .hbg,.js:not(.ready) .hl>*,.js:not(.ready) .hero h1 i.o,.js:not(.ready) .sbox,.js:not(.ready) .chipv{animation-play-state:paused}
@media(max-width:800px){.ldr-in{flex-direction:column;gap:22px;text-align:center}.ldr-mark{width:72px;height:68px}.ldr-word b{font-size:22px}}
@media(prefers-reduced-motion:reduce){.ldr{transition:opacity .4s}.ldr.out{transform:none;opacity:0}.ldr-arch{animation:none;fill:var(--milk);stroke-width:0}.ldr-dot,.ldr-word b,.ldr-word small{animation:none;opacity:1;transform:none;letter-spacing:.42em}.ldr-word small{letter-spacing:.5em}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

LDR = f'''<div class="ldr" id="ldr" aria-hidden="true">
  <div class="ldr-in"><svg class="ldr-mark" viewBox="0 0 76 72"><path class="ldr-arch" d="{ARCH}"/><circle class="ldr-dot" cx="67" cy="63" r="9"/></svg>
    <div class="ldr-word"><b>ПЛАТФОРМА</b><small>НЕДВИЖИМОСТИ</small></div></div>
  <span class="ldr-city">Екатеринбург</span><span class="ldr-pc" id="ldrPc">0 %</span><div class="ldr-bar"><i id="ldrBar"></i></div>
</div>
<script>
(() => {{
  const L = document.getElementById('ldr'), bar = document.getElementById('ldrBar'), pc = document.getElementById('ldrPc'), html = document.documentElement;
  let seen = false; try {{ seen = sessionStorage.getItem('pn_ldr') === '1'; sessionStorage.setItem('pn_ldr', '1'); }} catch (e) {{}}
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, MIN = seen || reduce ? 500 : 1700, MAX = 4000, t0 = performance.now();
  if (seen) L.classList.add('quick');
  let p = 0, loaded = false, done = false;
  const set = v => {{ p = v; bar.style.width = v + '%'; pc.textContent = Math.round(v) + ' %'; }};
  const tick = setInterval(() => {{ const el = performance.now() - t0; const target = loaded ? 100 : Math.min(92, 92 * (1 - Math.exp(-el / 900))); set(p + (target - p) * .25);
    if ((loaded && el > MIN && p > 99) || el > MAX) finish(); }}, 40);
  function finish() {{ if (done) return; done = true; clearInterval(tick); set(100);
    setTimeout(() => {{ html.classList.add('ready'); L.classList.add('out'); setTimeout(() => L.classList.add('gone'), 900); }}, 120); }}
  addEventListener('load', () => {{ loaded = true; }});
}})();
</script>
'''
rep('<body>\n', '<body>\n' + LDR)
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
