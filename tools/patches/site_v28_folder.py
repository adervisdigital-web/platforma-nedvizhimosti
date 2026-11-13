"""Сайт v28 — «Обещания»: договор в фирменной папке вместо стола с кофе (по просьбе заказчика).
Раскрытая графитовая папка: левая створка — тиснёный знак, «Договор с Платформой», данные (объект, менеджер, гарантия),
карман с визиткой; правая створка — лист договора в уголках-держателях. Без фото — чистый CSS, в фирменных цветах.
Динамика: при появлении папка раскрывается (левая створка поворачивается), лист выезжает, галочки, подпись, печать;
наведение на обещание подсвечивает пункты; папка слегка наклоняется за курсором. На телефоне — только правая створка.
Run из корня репо после site_v27_mobile.py: py -3 tools/patches/site_v28_folder.py"""
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<figure class="desk" id="desk" aria-label="Договор с обязательствами Платформы на столе">\n    <div class="dk-in"><img src="photo/desk_contract.jpg" alt="" loading="lazy" class="dk-ph">\n      <div class="paper">',
    '''<figure class="desk fold" id="desk" aria-label="Договор с обязательствами Платформы в фирменной папке">
    <div class="dk-in">
      <div class="flap" aria-hidden="true"><div class="flap-in">
        <svg class="emb" viewBox="0 0 76 72"><path d="M0 72 V24 A24 24 0 0 1 48 24 V72 H33 V26 A9 9 0 0 0 15 26 V72 Z"/><circle cx="67" cy="63" r="9"/></svg>
        <div class="fl-t">Договор<br>с Платформой<i class="o"></i></div>
        <dl class="fl-d"><div><dt>Объект</dt><dd>2-комн., ЖК Кварц</dd></div><div><dt>Менеджер</dt><dd>Ольга · +7 965 500-29-18</dd></div><div><dt>Гарантия</dt><dd>5 лет по договору</dd></div></dl>
        <div class="pocket"><span class="card"><svg viewBox="0 0 76 72"><use href="#mark"/></svg><b>ПЛАТФОРМА</b><small>НЕДВИЖИМОСТИ</small></span></div>
      </div></div>
      <div class="leaf"><span class="crn c1"></span><span class="crn c2"></span>
      <div class="paper">''')
rep('''          <div><span class="k">Клиент</span><span class="ln"><a class="you" href="#lead">ваша подпись</a></span></div></div>
      </div>
    </div>''', '''          <div><span class="k">Клиент</span><span class="ln"><a class="you" href="#lead">ваша подпись</a></span></div></div>
      </div>
    </div></div>''')

CSS = r'''
/* v28 — договор в папке */
.fold .dk-in{aspect-ratio:auto;display:grid;grid-template-columns:.82fr 1fr;border-radius:0;overflow:visible;box-shadow:none;perspective:none;
  transform:perspective(1800px) rotateX(var(--drx,0deg)) rotateY(var(--dry,0deg));filter:drop-shadow(0 40px 60px #00000099)}
.fold .flap,.fold .leaf{position:relative;background:linear-gradient(135deg,#2A2A2D 0%,#1E1E21 60%,#18181A 100%);padding:clamp(18px,1.8vw,30px)}
.fold .flap{border-radius:22px 4px 4px 22px;transform-origin:right center;box-shadow:inset -18px 0 30px -18px #000c;transition:transform 1s cubic-bezier(.3,.8,.25,1)}
.fold .leaf{border-radius:4px 22px 22px 4px;box-shadow:inset 18px 0 30px -18px #000c}
.fold .flap::after,.fold .leaf::after{content:'';position:absolute;inset:0;border-radius:inherit;background:repeating-linear-gradient(45deg,#ffffff03 0 2px,#0000 2px 5px);pointer-events:none}
.js .fold .flap{transform:perspective(1400px) rotateY(-100deg)}.fold.in .flap{transform:none}
.flap-in{height:100%;display:flex;flex-direction:column;gap:clamp(14px,1.4vw,24px);color:#C9C5BE}
.emb{width:clamp(44px,4vw,70px);height:auto;fill:#2F2F33;filter:drop-shadow(0 1px 0 #ffffff14) drop-shadow(0 -1px 0 #0009)}
.emb circle{fill:#3A3A3E}
.fl-t{font:300 clamp(24px,2vw,38px)/1.05 Manrope;letter-spacing:-.03em;color:var(--milk)}
.fl-d{margin:0;display:grid;gap:10px}.fl-d dt{font-size:11px;color:#8A867F;letter-spacing:.04em}.fl-d dd{margin:2px 0 0;font-size:14px;color:#E4E1DB}
.pocket{margin-top:auto;position:relative;height:clamp(90px,8vw,130px)}.pocket::before{content:'';position:absolute;inset:0;z-index:2;border-radius:10px 10px 14px 14px;background:linear-gradient(180deg,#252528,#1B1B1E);box-shadow:inset 0 1px 0 #ffffff12,0 -6px 14px #0006}
.pocket .card{position:absolute;left:12%;bottom:38%;width:64%;aspect-ratio:1.75;background:#F4F2EE;border-radius:4px;display:flex;flex-direction:column;justify-content:center;padding:0 9%;box-shadow:0 6px 14px #0006;transform:rotate(-4deg);z-index:1}
.pocket .card svg{width:14%;height:auto;fill:var(--ink);margin-bottom:6%}.pocket .card b{font:300 clamp(8px,.7vw,11px) Manrope;letter-spacing:.35em;color:var(--ink)}.pocket .card small{font-size:clamp(5px,.42vw,7px);letter-spacing:.4em;color:#6B675F;margin-top:3px}
.fold .paper{position:relative;left:auto;top:auto;width:auto;height:auto;mix-blend-mode:normal;background:#FBFAF7;border-radius:3px;box-shadow:0 14px 34px #00000073;
  padding:clamp(18px,2vw,34px) clamp(16px,1.8vw,30px) clamp(16px,1.6vw,26px);min-height:100%;transition:transform 1s cubic-bezier(.2,.8,.2,1) .25s}
.js .fold .paper{transform:translateY(16px)}.fold.in .paper{transform:none}
.fold .crn{position:absolute;z-index:2;width:46px;height:46px;background:linear-gradient(135deg,#2B2B2E 50%,#0000 50%);filter:drop-shadow(2px 2px 2px #0006)}
.fold .crn.c1{left:calc(clamp(18px,1.8vw,30px) - 2px);top:calc(clamp(18px,1.8vw,30px) - 2px)}
.fold .crn.c2{right:calc(clamp(18px,1.8vw,30px) - 2px);bottom:calc(clamp(18px,1.8vw,30px) - 2px);transform:rotate(180deg)}
.fold .pp-h{font-size:clamp(9px,.72vw,12px);padding-bottom:12px;border-bottom-width:1px}.fold .pp-logo{font-size:clamp(8px,.62vw,11px);gap:8px}.fold .pp-logo svg{width:20px;height:19px}
.fold .pp-t{font-size:clamp(14px,1.05vw,18px);margin:18px 0 8px}
.fold .cl li{grid-template-columns:34px 1fr;padding:8px 8px;margin:0 -8px;border-radius:7px}
.fold .cl li span{font-size:clamp(11px,.78vw,13px)}.fold .cl li p{font-size:clamp(12.5px,.9vw,15px)}
.fold .cl li span::after{left:-16px;top:5px;width:9px;height:5px;border-width:2px}
.fold .sign{gap:20px;margin-top:22px}.fold .sign .k{font-size:11px}.fold .sign .ln{height:38px;border-bottom-width:1px}
.fold .sig{width:110px;height:32px}.fold .seal{left:88px;width:22px;height:22px;bottom:6px}
.fold .you{font-size:12px}.fold .you::after{width:1px;height:13px}
.fold figcaption{margin-top:18px}
@media(max-width:1100px){.fold{max-width:760px}}
@media(max-width:800px){
 .fold .dk-in{grid-template-columns:minmax(0,1fr);padding:0;background:none;filter:drop-shadow(0 26px 40px #0009)}
 .fold .flap{display:none}.fold .leaf{border-radius:22px;padding:16px}
 .fold .crn{width:34px;height:34px}.fold .crn.c1{left:14px;top:14px}.fold .crn.c2{right:14px;bottom:14px}
 .fold .paper{padding:20px 16px 16px}.fold .cl li p{font-size:13.5px}
}
@media(prefers-reduced-motion:reduce){.js .fold .flap,.js .fold .paper{transform:none}}
'''
rep('@media(prefers-reduced-motion:reduce){*{transition', CSS + '@media(prefers-reduced-motion:reduce){*{transition')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
