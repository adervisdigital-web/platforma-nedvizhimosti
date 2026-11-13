"""Сайт v21 — подборки и промо живее, карта статично на всю высоту списка.
Подборки: при наведении карточка приподнимается, фото приближается, появляется красная точка, соседние приглушаются;
в красной «Самые выгодные» — живое поле точек: точки гаснут по одной, остаётся одна (отбор), цикл.
Промо: точки-декор стали настоящими точками — при наведении расходятся волной от угла; карточка приподнимается.
Карта: больше не «едет» за прокруткой — стоит рядом со списком на всю его высоту.
Run из корня репо после site_v20_hero.py: py -3 tools/patches/site_v21_tiles.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<a class="cat red" role="listitem" href="#list" data-f="best"><b>', '<a class="cat red" role="listitem" href="#list" data-f="best"><span class="cfield" aria-hidden="true"></span><b>')

CSS = r'''
/* v21 — подборки */
.cats{isolation:isolate}
.cat{transition:transform .45s cubic-bezier(.2,.7,.2,1),box-shadow .45s,opacity .35s;background-size:cover;will-change:transform}
.cat::after{content:'';position:absolute;right:16px;top:16px;width:12px;height:12px;border-radius:50%;background:var(--red);transform:scale(0);transition:transform .4s cubic-bezier(.3,1.6,.5,1);box-shadow:0 0 0 0 #F5553C66}
.cat.red::after{background:#fff}
.cat b,.cat span{transition:transform .45s cubic-bezier(.2,.7,.2,1)}
@media(hover:hover){
 .cats:hover .cat:not(:hover){opacity:.72}
 .cat:hover{transform:translateY(-8px);box-shadow:0 26px 50px #0000002e}
 .cat:hover::after{transform:scale(1);animation:catp 1.6s .4s infinite}
 .cat:hover b,.cat:hover span{transform:translateY(-4px)}
}
@keyframes catp{70%{box-shadow:0 0 0 10px #F5553C00}100%{box-shadow:0 0 0 0 #F5553C00}}
.cat.red{overflow:hidden}
.cfield{position:absolute;inset:16px 16px auto 16px;height:58%;display:grid;grid-template-columns:repeat(7,1fr);align-content:start;gap:9px 0}
.cfield i{width:7px;height:7px;border-radius:50%;background:#ffffffb3;justify-self:center;transition:opacity .5s,transform .5s,background .5s}
.cfield i.off{opacity:.18}.cfield i.win{background:var(--night);transform:scale(2.4);opacity:1}
/* промо */
.pt{transition:transform .45s cubic-bezier(.2,.7,.2,1),box-shadow .45s}
@media(hover:hover){.pt:hover{transform:translateY(-6px);box-shadow:0 26px 50px #0000002a}}
.pt .dotgrid{background:none!important;display:grid;grid-template-columns:repeat(7,1fr);grid-auto-rows:22px;align-items:center;width:160px;height:auto;right:10px;bottom:10px}
.pt .dotgrid i{width:9px;height:9px;border-radius:50%;justify-self:center;background:#ffffff40}
.pt.dark .dotgrid i{background:#ffffff2e}.pt.white .dotgrid i{background:var(--red)}
.pt .dotgrid i.hot{background:#fff}.pt.dark .dotgrid i.hot{background:var(--red)}.pt.white .dotgrid i.hot{background:var(--ink)}
@keyframes wave{0%,100%{transform:scale(1)}40%{transform:scale(1.7)}}
.pt:hover .dotgrid i{animation:wave .7s calc(var(--d) * 55ms) ease-out}
.pt .gl{transition:background .25s,color .25s,padding .25s}
.pt:hover .gl{padding-right:30px;position:relative}
.pt .gl::after{content:'';position:absolute;right:14px;top:50%;width:7px;height:7px;margin-top:-3.5px;border-radius:50%;background:var(--red);opacity:0;transition:opacity .25s}
.pt:hover .gl::after{opacity:1}
/* карта статично на всю высоту списка */
.res{align-items:stretch}
.map{position:relative;top:auto;height:auto;min-height:560px}
@media(max-width:1200px){.map{height:380px;min-height:0}}
@media(prefers-reduced-motion:reduce){.cat,.pt{transition:none}.cat:hover::after{animation:none}.pt:hover .dotgrid i{animation:none}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

rep("function mapFit() { if (lmap && lastPts.length) lmap.fitBounds(lastPts, {padding: [60, 60], maxZoom: 13}); }",
    "function mapFit() { if (!lmap || !lastPts.length) return; lmap.invalidateSize(); const h = $('.map').clientHeight, view = Math.min(h, Math.round(innerHeight * .85)); "
    "lmap.fitBounds(lastPts, {paddingTopLeft: [60, 70], paddingBottomRight: [60, Math.max(60, h - view + 60)], maxZoom: 13}); }")

JS = r'''
// подборки: живое поле точек в «Самые выгодные»
(() => {
  const f = $('.cfield'), N = 42, W = 23; f.innerHTML = '<i></i>'.repeat(N); const ds = $$('i', f);
  if (reduce) { ds.forEach((d, i) => d.classList.toggle('off', i !== W)); ds[W].classList.add('win'); return; }
  function run() {
    ds.forEach(d => d.classList.remove('off', 'win')); const order = ds.map((_, i) => i).filter(i => i !== W).sort(() => Math.random() - .5); let k = 0;
    const t = setInterval(() => { for (let j = 0; j < 3 && k < order.length; j++, k++) ds[order[k]].classList.add('off');
      if (k >= order.length) { clearInterval(t); ds[W].classList.add('win'); setTimeout(run, 2600); } }, 110);
  }
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { run(); o.disconnect(); } }).observe(f);
})();
// промо: точки волной
$$('.pt .dotgrid').forEach(g => { const C = 7, R = 5; g.innerHTML = Array.from({length: C * R}, (_, i) => { const x = i % C, y = Math.floor(i / C); return `<i style="--d:${(C - 1 - x) + (R - 1 - y)}"${(x + y) % 9 === 4 ? ' class="hot"' : ''}></i>`; }).join(''); });
// карта: пересчёт размера, когда список меняет высоту
if (window.ResizeObserver) { let mt; new ResizeObserver(() => { clearTimeout(mt); mt = setTimeout(mapFit, 120); }).observe($('.map')); }
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
