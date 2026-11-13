"""Сайт v19 — блок «Личный кабинет»: вместо нарисованного телефона — MacBook и iPhone с настоящим демо-кабинетом в экранах
(iframe kabinet.html: ноутбук 1440×900, телефон 390×844, масштабом). При наведении устройства наклоняются за курсором
в 3D, телефон «ближе» (параллакс); без наведения — лёгкое покачивание телефона. Клик открывает кабинет.
Плюс правка блока «Обещания»: крупные слова не переносятся.
Run из корня репо после site_v18_promise.py: py -3 tools/patches/site_v19_devices.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


# обещания: слово не переносится
rep('.vows button{all:unset;box-sizing:border-box;display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);',
    '.vows button{all:unset;box-sizing:border-box;display:grid;grid-template-columns:auto minmax(0,1fr);')
rep('.vows b{font:300 clamp(40px,4vw,96px)/1 Manrope;', '.vows b{white-space:nowrap;min-width:5.6em;font:300 clamp(40px,3.5vw,88px)/1 Manrope;')

# устройства вместо телефона
i = s.index('  <div class="cphone" aria-label="Пример личного кабинета на телефоне">')
j = s.index('</div></section>', i)
s = s[:i] + '''  <a class="devs" id="devs" href="kabinet.html" aria-label="Открыть демо-кабинет: ноутбук и телефон">
    <span class="stage">
      <span class="mbp"><span class="lid"><span class="cam-dot"></span><span class="vp"><iframe src="kabinet.html#home" title="Личный кабинет на ноутбуке" loading="lazy" tabindex="-1" scrolling="no"></iframe></span></span><span class="base"><i></i></span></span>
      <span class="iph"><span class="vp"><iframe src="kabinet.html#home" title="Личный кабинет на телефоне" loading="lazy" tabindex="-1" scrolling="no"></iframe></span><span class="isl"></span></span>
      <span class="shadow"></span>
    </span>
    <span class="devcap"><i></i>Это настоящий демо-кабинет — нажмите, чтобы открыть</span>
  </a>
''' + s[j:]

CSS = r'''
/* v19 — MacBook + iPhone */
.cab .cgrid{grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:clamp(30px,4vw,90px)}
.devs{display:block;position:relative;perspective:1600px;--rx:0deg;--ry:0deg;--px:0px;--py:0px;cursor:pointer}
.stage{display:block;position:relative;aspect-ratio:1.42;transform-style:preserve-3d;transform:rotateX(var(--rx)) rotateY(var(--ry));transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.devs.move .stage{transition:transform .12s linear}
.mbp{position:absolute;left:0;top:4%;width:88%;display:block;transform:translateZ(0)}
.lid{display:block;position:relative;background:#1A1A1C;border-radius:3.2% 3.2% 0 0/5% 5% 0 0;padding:2.6% 2.6% 3.4%;box-shadow:inset 0 0 0 1.5px #3A3A3E}
.cam-dot{position:absolute;left:50%;top:1.1%;width:.7%;aspect-ratio:1;border-radius:50%;background:#2E2E33;transform:translateX(-50%)}
.mbp .vp{display:block;position:relative;aspect-ratio:1440/900;overflow:hidden;border-radius:4px;background:#F4F2EE}
.mbp iframe{position:absolute;left:0;top:0;width:1440px;height:900px;border:0;transform-origin:0 0;transform:scale(var(--ks,.5));pointer-events:none}
.base{display:block;position:relative;height:0;padding-bottom:3.6%;margin:0 -7%;background:linear-gradient(180deg,#D9D7D3 0%,#B8B5B0 55%,#8E8B86 100%);border-radius:0 0 14px 14px / 0 0 60% 60%}
.base i{position:absolute;left:50%;top:0;width:15%;height:40%;background:#A8A5A0;border-radius:0 0 8px 8px;transform:translateX(-50%)}
.iph{position:absolute;right:0;bottom:3%;width:24%;display:block;background:#1A1A1C;border-radius:16%/7.4%;padding:2.3%;box-shadow:0 30px 60px #0000004d,inset 0 0 0 1.5px #3A3A3E;transform:translateZ(90px) translate(var(--px),var(--py));transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.devs.move .iph{transition:transform .12s linear}
.iph .vp{display:block;position:relative;aspect-ratio:390/844;overflow:hidden;border-radius:13%/6%;background:#F4F2EE}
.iph iframe{position:absolute;left:0;top:0;width:390px;height:844px;border:0;transform-origin:0 0;transform:scale(var(--kp,.4));pointer-events:none}
.isl{position:absolute;left:50%;top:3.6%;width:30%;height:2.6%;background:#0B0B0C;border-radius:99px;transform:translateX(-50%)}
.shadow{position:absolute;left:4%;right:6%;bottom:-2%;height:8%;background:radial-gradient(closest-side,#0000003d,#0000);transform:translateZ(-40px);filter:blur(6px)}
.devcap{display:flex;align-items:center;gap:8px;justify-content:center;margin-top:18px;font-size:13px;font-weight:600;color:var(--mut);transition:color .2s}
.devcap i{width:8px;height:8px;border-radius:50%;background:var(--red)}
.devs:hover .devcap,.devs:focus-visible .devcap{color:var(--ink)}
@keyframes bob{0%,100%{translate:0 0}50%{translate:0 -8px}}
.devs:not(.move) .iph{animation:bob 5s ease-in-out infinite}
@media(max-width:1200px){.cab .cgrid{grid-template-columns:minmax(0,1fr)}.devs{max-width:820px;margin:10px auto 0}}
@media(prefers-reduced-motion:reduce){.devs .iph{animation:none!important}.stage,.iph{transition:none!important}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

rep("function camTime() { const d = new Date(); $('#camTs').textContent = d.toLocaleDateString('ru-RU') + ' · ' + d.toLocaleTimeString('ru-RU'); }\ncamTime(); setInterval(camTime, 1000);\n", '')
i = s.index("$('#actBtn').addEventListener('click'"); j = s.index('\n', i)
s = s[:i] + s[j + 1:]

JS = r'''
// MacBook + iPhone: масштаб экранов и наклон за курсором
const devs = $('#devs');
function fitDevs() { const m = $('.mbp .vp'), p = $('.iph .vp'); if (!m) return; devs.style.setProperty('--ks', m.clientWidth / 1440); devs.style.setProperty('--kp', p.clientWidth / 390); }
addEventListener('resize', fitDevs); fitDevs(); new ResizeObserver(fitDevs).observe(devs);
if (!reduce && matchMedia('(hover:hover)').matches) {
  devs.addEventListener('mousemove', e => {
    const r = devs.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
    devs.classList.add('move');
    devs.style.setProperty('--ry', (x * 14).toFixed(2) + 'deg'); devs.style.setProperty('--rx', (-y * 10).toFixed(2) + 'deg');
    devs.style.setProperty('--px', (x * 22).toFixed(1) + 'px'); devs.style.setProperty('--py', (y * 16).toFixed(1) + 'px');
  });
  devs.addEventListener('mouseleave', () => { devs.classList.remove('move'); ['--rx', '--ry'].forEach(v => devs.style.setProperty(v, '0deg')); ['--px', '--py'].forEach(v => devs.style.setProperty(v, '0px')); });
}
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
