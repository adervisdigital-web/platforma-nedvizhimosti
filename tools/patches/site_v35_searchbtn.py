"""Сайт v35 — поиск: кнопка вынесена справа отдельной высокой плиткой на высоту обоих рядов (крупный живой счётчик
«5 квартир»), в карточке — строка статуса «данные обновлены сегодня · проверено N из 144»; при смене условий по стыку рядов
пробегает линия-сканер, цифра перекатывается. Кнопка вне формы — form="sf". Телефон: плитка на всю ширину под карточкой.
Run из корня репо после site_v34_leaddots.py: py -3 tools/patches/site_v35_searchbtn.py"""
import re
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


old_btn = re.search(r'\s*<button class="go2" type="submit"[^>]*>.*?</button>', s, re.S).group(0)
s = s.replace(old_btn, '', 1)
i = s.index('<div class="sline"><span class="qfl">Быстро:</span>'); j = s.index('</div>', i) + len('</div>')
sline = s[i:j]
new_sline = sline[:-len('</div>')] + '<span class="sstat" aria-live="polite"><i></i><span id="sStat"></span></span></div>'
s = s[:i] + new_sline + '''
      <button class="go3" type="submit" form="sf" aria-label="Показать подходящие квартиры"><span class="g3-top"><span class="g3-ic"><svg class="ico"><use href="#search"/></svg></span><span class="g3-l">Показать</span></span>
        <span class="g3-n"><b id="goN"></b><small id="goL">квартир</small></span><span class="g3-sw" aria-hidden="true"></span></button>''' + s[j:]
rep('<div class="sbox">', '<div class="sbox sbox3">')

CSS = r'''
/* v35 — кнопка справа, статус и сканер */
.hero .sbox.sbox3{display:grid;grid-template-columns:minmax(0,1fr) clamp(180px,14vw,230px);grid-template-areas:"f b" "s b";column-gap:10px;row-gap:0;background:none;padding:0;box-shadow:none;border-radius:0;width:min(1240px,calc(100% - clamp(290px,19vw,400px) - 24px))}
.sbox3 #sf{grid-area:f;background:#fff;border-radius:30px 30px 0 0;padding:8px 8px 0;box-shadow:0 30px 70px #00000059}
.sbox3 .sline{grid-area:s;position:relative;background:#fff;border-radius:0 0 30px 30px;margin:0!important;padding:12px 18px 14px!important;border-top:1px solid var(--line)!important;box-shadow:0 30px 70px #00000040}
.sbox3 .sline::before{content:'';position:absolute;left:0;top:-1px;height:1px;width:30%;background:linear-gradient(90deg,#F5553C00,var(--red),#F5553C00);opacity:0;transform:translateX(-40%)}
.sbox3 .sline.scan::before{animation:sscan .9s cubic-bezier(.4,0,.2,1)}
@keyframes sscan{0%{opacity:1;transform:translateX(-40%)}100%{opacity:1;transform:translateX(370%)}}
.sbox3 .sline{display:flex!important;flex-wrap:nowrap;align-items:center;gap:10px}.sbox3 .qf{flex:1 1 auto;min-width:0}
.sstat{margin-left:auto;flex:none;display:flex;align-items:center;gap:8px;font-size:12px;color:var(--mut);white-space:nowrap;font-variant-numeric:tabular-nums}
.sstat i{width:6px;height:6px;border-radius:50%;background:#2FB36B;box-shadow:0 0 0 0 #2FB36B88;animation:livep 2s infinite}
.sstat b{color:var(--ink);font-weight:700}
.go3{grid-area:b;position:relative;overflow:hidden;border:0;border-radius:30px;background:var(--red-ui);color:#fff;cursor:pointer;display:flex;flex-direction:column;justify-content:space-between;align-items:flex-start;padding:18px 20px 16px;text-align:left;font:inherit;box-shadow:0 30px 60px #D83C2459;transition:background .2s,transform .15s}
.go3:hover{background:#C4331D}.go3:active{transform:scale(.98)}.go3:focus-visible{outline:2px solid #fff;outline-offset:-6px}
.g3-top{display:flex;align-items:center;gap:10px;font-weight:700;font-size:15px}
.g3-ic{width:36px;height:36px;border-radius:50%;background:#ffffff26;display:flex;align-items:center;justify-content:center;transition:transform .3s}
.go3:hover .g3-ic{transform:scale(1.08) rotate(-8deg)}
.g3-n{display:flex;align-items:baseline;gap:8px}
.g3-n b{font:300 clamp(46px,3.6vw,64px)/.9 Manrope;letter-spacing:-.04em;font-variant-numeric:tabular-nums;display:inline-block}
.g3-n b.roll{animation:groll .45s cubic-bezier(.2,.8,.2,1)}
@keyframes groll{0%{transform:translateY(40%);opacity:0}100%{transform:none;opacity:1}}
.g3-n small{font-size:13px;font-weight:600;opacity:.85}
.g3-sw{position:absolute;inset:0;background:linear-gradient(105deg,#fff0 35%,#ffffff33 50%,#fff0 65%);transform:translateX(-100%);pointer-events:none}
.go3.sweep .g3-sw{animation:gsw .8s ease}
@keyframes gsw{to{transform:translateX(100%)}}
@media(max-width:1200px){.hero .sbox.sbox3{width:100%}}
@media(max-width:1600px){.sstat .lg{display:none}}
@media(max-width:1000px){.sstat{display:none}}
@media(max-width:800px){
 .hero .sbox.sbox3{grid-template-columns:minmax(0,1fr);grid-template-areas:"f" "s" "b";row-gap:0}
 .sbox3 #sf{border-radius:26px 26px 0 0;padding:8px 8px 0}
 .sbox3 .sline{border-radius:0 0 26px 26px;padding:10px 12px 12px!important}
 .go3{margin-top:10px;flex-direction:row;align-items:center;border-radius:22px;padding:12px 18px;min-height:64px}
 .g3-n b{font-size:36px}
}
@media(prefers-reduced-motion:reduce){.sstat i{animation:none}.sbox3 .sline.scan::before,.g3-n b.roll,.go3.sweep .g3-sw{animation:none}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

JS = r'''
// поиск: статус, сканер, перекат счётчика
(() => {
  const n = $('#goN'), btn = $('.go3'), line = $('.sbox3 .sline'); let last = n.textContent, t;
  const tm = new Date(); tm.setMinutes(tm.getMinutes() - 7);
  const hhmm = `${String(tm.getHours()).padStart(2, '0')}:${String(tm.getMinutes()).padStart(2, '0')}`;
  function upd() {
    const v = +n.textContent || 0;
    $('#goL').textContent = plural(v, 'квартира', 'квартиры', 'квартир');
    $('#sStat').innerHTML = `<span class="lg">обновлено в ${hhmm} · </span>подходит <b>${v}</b> из 144<span class="lg"> проверенных</span>`;
    if (n.textContent !== last) { last = n.textContent;
      [n, btn, line].forEach(el => el.classList.remove('roll', 'sweep', 'scan')); void n.offsetWidth;
      n.classList.add('roll'); btn.classList.add('sweep'); line.classList.add('scan'); }
  }
  new MutationObserver(upd).observe(n, {childList: true, characterData: true, subtree: true});
  upd();
})();
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
