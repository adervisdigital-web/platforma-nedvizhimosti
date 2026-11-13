"""Сайт v23 — ещё живее: путь клиента прорисовывается, ипотека с полосой «кредит/переплата» и сравнением трёх программ,
точки в заявке загораются вокруг курсора, карточки направлений и отзывов приподнимаются.
Run из корня репо после site_v22_scan.py: py -3 tools/patches/site_v23_life.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('      <div class="pay" id="pay">—</div>\n',
    '      <div class="pay" id="pay">—</div>\n'
    '      <div class="cbar" aria-hidden="true"><i id="cbL"></i><i id="cbO"></i></div><div class="cleg"><span><i></i>Кредит <b id="cbLv"></b></span><span><i></i>Переплата <b id="cbOv"></b></span></div>\n')
rep('      <div class="crow"><span>Нужный доход, от</span><b id="inc">—</b></div>\n',
    '      <div class="crow"><span>Нужный доход, от</span><b id="inc">—</b></div>\n      <div class="cprog" id="cprog" role="group" aria-label="Сравнение программ"></div>\n')
rep('<section class="lead" id="lead"><span class="dotgrid" aria-hidden="true"></span>', '<section class="lead" id="lead"><span class="dotgrid" aria-hidden="true"></span><span class="dotgrid lit" aria-hidden="true"></span>')

CSS = r'''
/* v23 — путь клиента */
.way .ln{position:relative}.way .ln::after{content:'';position:absolute;left:0;right:0;top:0;height:2px;background:var(--red);transform:scaleX(0);transform-origin:left;transition:transform .7s cubic-bezier(.5,0,.3,1)}
.way .ln.fill::after{transform:scaleX(1)}
.way .stp i{transition:background .3s,box-shadow .3s}.way .stp{transition:color .3s;color:#8A867F}.way .stp.lit{color:var(--milk)}
.way .stp.lit i{background:var(--milk)}.way .stp:last-of-type.lit i{background:var(--red);box-shadow:0 0 0 6px #F5553C33}
.pc,.rc{transition:transform .45s cubic-bezier(.2,.7,.2,1),box-shadow .45s}
@media(hover:hover){.pc:hover,.rc:hover{transform:translateY(-6px);box-shadow:0 24px 50px #0000001f}}
/* ипотека: кредит / переплата и сравнение программ */
.cbar{display:flex;height:12px;border-radius:6px;overflow:hidden;background:#ffffff33;margin-top:-4px}
.cbar i{display:block;height:100%;transition:width .5s cubic-bezier(.2,.7,.2,1)}#cbL{background:#fff}#cbO{background:var(--night)}
.cleg{display:flex;gap:18px;flex-wrap:wrap;font-size:12px;opacity:.95}.cleg span{display:flex;align-items:center;gap:6px}.cleg i{width:9px;height:9px;border-radius:50%;background:#fff}.cleg span+span i{background:var(--night)}
.cprog{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.cprog button{all:unset;box-sizing:border-box;cursor:pointer;border-radius:14px;padding:10px 12px;background:#ffffff1f;display:grid;gap:2px;transition:background .25s}
.cprog button small{font-size:11px;opacity:.85}.cprog button b{font-size:16px;font-variant-numeric:tabular-nums}
.cprog button[aria-pressed=true]{background:#fff;color:var(--ink)}.cprog button:hover{background:#ffffff38}.cprog button[aria-pressed=true]:hover{background:#fff}
.cprog button:focus-visible{outline:2px solid #fff;outline-offset:2px}
/* заявка: точки загораются у курсора */
.lead .dotgrid.lit{background-image:radial-gradient(circle,#fff 6px,transparent 6.5px);-webkit-mask-image:radial-gradient(circle 150px at var(--mx,-999px) var(--my,-999px),#000 0,#0008 45%,#0000 100%);mask-image:radial-gradient(circle 150px at var(--mx,-999px) var(--my,-999px),#000 0,#0008 45%,#0000 100%)}
@media(max-width:800px){.cprog{grid-template-columns:minmax(0,1fr)}}
@media(prefers-reduced-motion:reduce){.way .ln::after,.cbar i{transition:none}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

JS = r'''
// путь клиента: прорисовка шагов
(() => { const way = $('.way'); if (!way) return; const parts = [...way.children].filter(e => e.matches('.stp,.ln'));
  function play() { parts.forEach(p => p.classList.remove('lit', 'fill')); parts.forEach((p, i) => setTimeout(() => p.classList.add(p.matches('.stp') ? 'lit' : 'fill'), reduce ? 0 : 250 + i * 330)); }
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { play(); o.disconnect(); } }, {threshold: .6}).observe(way);
  way.addEventListener('mouseenter', play); })();

// ипотека: полоса и сравнение программ
const PROGS = [['Семейная', 6], ['IT-ипотека', 12], ['Рыночная', 20]];
function calcExtra() {
  const P = +$('#cp').value, d = +$('#cd').value, y = +$('#ct').value, r = +$('#rates [aria-pressed=true]').dataset.r, L = P * (1 - d / 100), n = y * 12;
  const pm = rr => { const m = rr / 1200; return m ? L * m / (1 - Math.pow(1 + m, -n)) : L / n; }, over = pm(r) * n - L;
  $('#cbL').style.width = L / (L + over) * 100 + '%'; $('#cbO').style.width = over / (L + over) * 100 + '%';
  $('#cbLv').textContent = fmtM(L); $('#cbOv').textContent = fmtM(over);
  $('#cprog').innerHTML = PROGS.map(([nm, rr]) => `<button type="button" data-r="${rr}" aria-pressed="${rr === r}"><small>${nm} · ${rr} %</small><b>${Math.round(pm(rr)).toLocaleString('ru-RU')} ₽</b></button>`).join('');
  $$('#cprog button').forEach(b => b.addEventListener('click', () => $(`#rates [data-r="${b.dataset.r}"]`).click()));
}
new MutationObserver(calcExtra).observe($('#loan'), {childList: true, characterData: true, subtree: true});
calcExtra();

// заявка: точки у курсора
(() => { const lead = $('#lead'), lit = $('.lead .dotgrid.lit'); if (!lit || !matchMedia('(hover:hover)').matches) return;
  lead.addEventListener('mousemove', e => { const r = lit.getBoundingClientRect(); lit.style.setProperty('--mx', e.clientX - r.left + 'px'); lit.style.setProperty('--my', e.clientY - r.top + 'px'); });
  lead.addEventListener('mouseleave', () => { lit.style.setProperty('--mx', '-999px'); }); })();
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')

# шторка «до/после»: общий стиль ползунков (height:30px) сжимал невидимый слой — тянуть по фото было нельзя
s = open(P + 'index.html', encoding='utf8').read()
s = s.replace('@media(prefers-reduced-motion:reduce){*{transition',
              '.ba img.after{padding:0}\n.ba input[type=range]{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:ew-resize;z-index:3}\n.ba{cursor:ew-resize;touch-action:pan-y}.ba .hdl::after{transition:transform .2s}.ba.drag .hdl::after{transform:translate(-50%,-50%) scale(1.12)}\n'
              '@media(prefers-reduced-motion:reduce){*{transition', 1)
JS2 = r'''
// шторка: тянуть мышью и пальцем по всему фото
(() => { const box = $('#baBox'); if (!box) return; let on = false;
  const at = e => { const r = box.getBoundingClientRect(); baSet(Math.max(0, Math.min(100, (e.clientX - r.left) / r.width * 100))); };
  box.addEventListener('pointerdown', e => { on = true; box.classList.add('drag'); box.setPointerCapture(e.pointerId); at(e); e.preventDefault(); });
  box.addEventListener('pointermove', e => { if (on) at(e); });
  ['pointerup', 'pointercancel'].forEach(t => box.addEventListener(t, () => { on = false; box.classList.remove('drag'); })); })();
'''
s = s.replace('</script>\n</body>', JS2 + '</script>\n</body>', 1)
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ba ok')
