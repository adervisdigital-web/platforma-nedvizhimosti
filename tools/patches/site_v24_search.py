"""Сайт v24 — форма поиска на первом экране: одна капсула «Что ищем · Комнаты · Бюджет · Район» + круглая кнопка со счётчиком.
Каждый сегмент открывает свою панель (тип, комнаты, бюджет с пресетами и ползунком, район/ЖК с подсказками); быстрые
фильтры — стеклянные чипы под капсулой. Ид-шники прежние (#sf, .sf .chip, .tabs, #pr, #ad, #goN), логика поиска та же.
Run из корня репо после site_v23_life.py: py -3 tools/patches/site_v24_search.py"""
import re
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


i = s.index('    <div class="sbox">'); j = s.index('<div class="sline">', i)
old = s[i:j]
tabs = re.search(r'<div class="tabs".*?</div>', old, re.S).group(0).replace('<button role="tab"', '<button type="button" role="tab"')
chips = re.search(r'<div class="v">(.*?)</div>', old, re.S).group(1)
s = s[:i] + f'''    <div class="sbox">
      <form class="sf sf2" id="sf" aria-label="Поиск квартир">
        <div class="sg" data-pop><button type="button" class="sgb" aria-expanded="false" aria-haspopup="true"><small>Что ищем</small><b id="sgType">Новостройки</b></button>
          <div class="pop">{tabs}</div></div>
        <div class="sg" data-pop><button type="button" class="sgb" aria-expanded="false" aria-haspopup="true"><small>Комнаты</small><b id="sgRooms">1, 2</b></button>
          <div class="pop"><div class="v rooms">{chips}</div><span class="pnote">Можно выбрать несколько</span></div></div>
        <div class="sg sgi dd-wrap"><label for="pr">Бюджет до, млн ₽</label><input id="pr" placeholder="Любой" inputmode="decimal" autocomplete="off" aria-controls="prDD"><div class="dd" id="prDD" role="listbox" hidden></div></div>
        <div class="sg sgi grow dd-wrap"><label for="ad">Район или ЖК</label><input id="ad" placeholder="Академический, ЖК…" autocomplete="off" aria-controls="adDD" aria-autocomplete="list"><datalist id="adList"></datalist><div class="dd" id="adDD" role="listbox" hidden></div></div>
        <button class="go2" type="submit" aria-label="Показать квартиры"><svg class="ico" aria-hidden="true"><use href="#search"/></svg><span>Показать <b id="goN"></b></span></button>
      </form>
      ''' + s[j:]

CSS = r'''
/* v24 — поиск-капсула */
.hero .sbox{background:transparent;box-shadow:none;padding:0;border-radius:0;width:min(1180px,calc(100% - clamp(290px,19vw,400px) - 24px))}
.sf.sf2{display:flex;align-items:stretch;gap:0;margin:0;background:#fff;border-radius:999px;padding:8px;box-shadow:0 30px 70px #00000059,0 0 0 1px #ffffff40;transition:background .25s}
.sf2.open{background:#ECEAE6}
.sg{position:relative;flex:1 1 0;min-width:0;border-radius:999px;transition:background .2s,box-shadow .2s}
.sg.grow{flex:1.45 1 0}
.sg+.sg::before{content:'';position:absolute;left:0;top:22%;bottom:22%;width:1px;background:var(--line);transition:opacity .2s}
.sg:hover::before,.sg:hover+.sg::before,.sg.on::before,.sg.on+.sg::before,.sg:focus-within::before,.sg:focus-within+.sg::before{opacity:0}
.sg:hover{background:var(--soft)}.sf2.open .sg:hover{background:#ffffff8c}
.sg.on,.sg:focus-within{background:#fff;box-shadow:0 8px 26px #00000024}
.sgb{all:unset;box-sizing:border-box;display:block;width:100%;height:100%;padding:12px 26px;cursor:pointer;border-radius:999px}
.sg small,.sgi label{display:block;font-size:12px;font-weight:700;color:var(--ink);letter-spacing:.01em}
.sg b{display:block;font-size:15px;font-weight:500;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:2px}
.sgi{display:flex;flex-direction:column;justify-content:center;padding:12px 26px;cursor:text}
.sgi input{border:0;background:transparent;font:500 15px Manrope;padding:2px 0 0;width:100%;outline:none;color:var(--ink)}
.sgi input::placeholder{color:var(--mut)}
.go2{flex:none;align-self:center;display:flex;align-items:center;gap:10px;height:62px;padding:0 26px 0 22px;margin-left:6px;border:0;border-radius:999px;background:var(--red-ui);color:#fff;font:700 16px Manrope;cursor:pointer;transition:background .2s,transform .15s}
.go2:hover{background:#C4331D}.go2:active{transform:scale(.97)}.go2 .ico{width:22px;height:22px}.go2 b{font-weight:800}
.pop{position:absolute;left:0;top:calc(100% + 12px);z-index:25;min-width:260px;background:#fff;border-radius:26px;box-shadow:0 24px 60px #00000038;padding:12px;opacity:0;transform:translateY(-6px);pointer-events:none;transition:opacity .2s,transform .2s}
.sg.on .pop{opacity:1;transform:none;pointer-events:auto}
.pop .tabs{display:grid;gap:4px;background:none;padding:0;width:auto}
.pop .tabs button{text-align:left;padding:12px 16px;border-radius:14px;font-size:15px}
.pop .tabs button[aria-selected=true]{background:var(--ink);color:#fff}
.pop .rooms{display:flex;gap:6px;margin:0}.pop .rooms .chip{min-width:48px;height:48px;border:1px solid var(--line);border-radius:999px;padding:0 14px;font-size:15px}
.pop .rooms .chip[aria-pressed=true]{border-color:var(--ink)}
.pnote{display:block;font-size:12px;color:var(--mut);margin:10px 4px 2px}
.sgi .dd{top:calc(100% + 12px);left:0;right:auto;min-width:100%;border-radius:22px;padding:8px}
.hero .sline{margin:14px 4px 0;color:#fff}
.hero .qf button{background:#ffffff1f;border-color:#ffffff40;color:#fff;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);padding:8px 14px;font-size:13px}
.hero .qf button:hover{background:#ffffff33}.hero .qf button[aria-pressed=true]{background:#fff;color:var(--ink);border-color:#fff}
.hero .sline a{color:#fff}
@media(max-width:1200px){.hero .sbox{width:100%}}
@media(max-width:800px){
 .sf.sf2{flex-direction:column;border-radius:26px;padding:8px;gap:2px}
 .sg{border-radius:18px}.sg+.sg::before{left:18px;right:18px;top:0;bottom:auto;width:auto;height:1px}
 .sgb,.sgi{padding:12px 16px}.go2{width:100%;justify-content:center;margin:6px 0 0;height:56px}
 .pop{left:0;right:0;min-width:0}.pop .rooms{flex-wrap:wrap}
}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')

JS = r'''
// поиск-капсула: панели сегментов и подписи
const sf2 = $('#sf');
function segClose(except) { $$('.sg[data-pop]').forEach(g => { if (g !== except) { g.classList.remove('on'); $('.sgb', g).setAttribute('aria-expanded', 'false'); } }); sf2.classList.toggle('open', !!except); }
$$('.sg[data-pop]').forEach(g => $('.sgb', g).addEventListener('click', e => { e.stopPropagation(); const on = !g.classList.contains('on'); segClose(on ? g : null); g.classList.toggle('on', on); e.currentTarget.setAttribute('aria-expanded', on); }));
$$('.sgi input').forEach(inp => inp.addEventListener('focus', () => segClose(null)));
document.addEventListener('click', e => { if (!e.target.closest('.sg')) segClose(null); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') segClose(null); });
function segLabels() {
  $('#sgType').textContent = ($('.pop .tabs [aria-selected=true]') || {}).textContent || 'Новостройки';
  const r = $$('.sf .chip').filter(c => c.getAttribute('aria-pressed') === 'true').map(c => c.textContent);
  $('#sgRooms').textContent = r.length ? r.join(', ') : 'Любые';
}
$$('.pop .tabs button').forEach(b => b.addEventListener('click', () => { segLabels(); if (b.textContent !== 'Дома') setTimeout(() => segClose(null), 120); }));
$$('.sf .chip').forEach(c => c.addEventListener('click', segLabels));
segLabels();
'''
rep('</script>\n</body>', JS + '</script>\n</body>')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
