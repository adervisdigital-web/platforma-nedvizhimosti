"""Сайт v5: весь сайт на всю ширину, первый экран — фото во весь экран, тёмный блок «Отбор» на фоне вида Екатеринбурга.
Run из корня репо: py -3 tools/patches/site_v5_fullscreen.py"""
import re, shutil

p = '08_Сайт_пример/index.html'
shutil.copy(p, '08_Сайт_пример/v4.html')
s = open(p, encoding='utf8').read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


def block(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i)
    s = s[:i] + new + s[j:]


# 1. контейнер — на всю ширину
rep('.w{max-width:2240px;margin:0 auto;padding:0 clamp(16px,3.6vw,96px)}', '.w{max-width:none;margin:0;padding:0 clamp(16px,3.4vw,110px)}')

# 2. CSS первого экрана
block('/* hero */', '.tabs{display:flex;', '''/* hero — фото во весь экран */
.hero{position:relative;min-height:calc(100vh - 76px);min-height:calc(100svh - 76px);display:flex;color:#fff;overflow:hidden;background:#2a211c}
.hbg{position:absolute;inset:0;background:url(photo/hero_window.jpg) 64% center/cover;transform:scale(1.02)}
.hbg::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,#0d0a08e6 0%,#0d0a08a8 30%,#0d0a0833 58%,#0000 74%),linear-gradient(0deg,#000a 0%,#0000 38%)}
.hin{position:relative;z-index:1;width:100%;display:flex;flex-direction:column;justify-content:space-between;gap:48px;padding-top:clamp(40px,8vh,130px);padding-bottom:clamp(24px,4.5vh,64px)}
.hl{max-width:min(1100px,58vw)}
.hero .br{color:#ffffffb8}
.hero h1{font:400 clamp(46px,6.6vw,184px)/.95 Manrope;letter-spacing:-.06em;margin:0;color:#fff}
.hero h1 em{font-style:normal;color:var(--red)}
.hero .sub{font-size:clamp(16px,1.15vw,25px);line-height:1.5;color:#ffffffd9;max-width:min(680px,90%);margin:30px 0 0}
.chipv{position:absolute;right:clamp(16px,3.4vw,110px);top:clamp(40px,8vh,130px);z-index:2;background:#ffffffeb;color:var(--ink);backdrop-filter:blur(12px);border-radius:20px;padding:16px 18px;width:clamp(290px,18vw,380px);box-shadow:0 20px 50px #0003}
.chipv h3{margin:0 0 8px;font:700 14px Manrope;display:flex;align-items:center;gap:8px}.chipv h3 i{width:10px;height:10px;border-radius:50%;background:var(--red)}
.chipv ul{list-style:none;margin:0;padding:0;font-size:13px}.chipv li{display:flex;gap:8px;align-items:center;padding:6px 0;border-top:1px solid #0000000d}.chipv li svg{color:var(--red);width:16px;height:16px}
.hcap{position:absolute;right:clamp(16px,3.4vw,110px);bottom:clamp(24px,4.5vh,64px);z-index:1;color:#fff;font-size:13px;opacity:.85}
.sbox{position:relative;z-index:3;width:min(1240px,100%);background:#fff;color:var(--ink);border-radius:26px;padding:12px;box-shadow:0 30px 70px #00000040}
.after{padding:clamp(20px,2vw,40px) 0 0}
''')

# 3. HTML первого экрана
block('<section class="hero" id="search"><div class="w">', '  <div class="cats" role="list"', '''<section class="hero" id="search">
  <div class="hbg" role="img" aria-label="Пара у панорамного окна новой квартиры, Екатеринбург на закате"></div>
  <div class="chipv"><h3><i></i>ЖК [НАЗВАНИЕ] — проверен</h3>
    <ul><li><svg><use href="#check"/></svg>Разрешение на строительство</li><li><svg><use href="#check"/></svg>Проектная декларация, эскроу</li><li><svg><use href="#check"/></svg>Прошлые дома сданы в срок</li><li><svg><use href="#check"/></svg>Нет банкротных дел</li></ul></div>
  <div class="w hin">
    <div class="hl">
      <div class="br">[ <b>●</b> Екатеринбург · новостройки и вторичка ]</div>
      <h1 style="margin-top:22px">Квартиры, за&nbsp;которые мы <em class="nw">ручаемся<i class="o w"></i></em></h1>
      <p class="sub">Продаём только то, что проверили сами: надёжные застройщики, чистые сделки, самые выгодные условия. Ремонт и дом — у партнёров, в которых мы уверены.</p>
    </div>
    <div class="sbox">
      <div class="tabs" role="tablist" aria-label="Что ищете"><button role="tab" aria-selected="true">Новостройки</button><button role="tab" aria-selected="false">Вторичка</button><button role="tab" aria-selected="false">С ремонтом</button><button role="tab" aria-selected="false">Дома</button></div>
      <form class="sf" onsubmit="return false" aria-label="Поиск">
        <div class="f"><label>Комнат</label><div class="v"><button type="button" class="chip" aria-pressed="false">Студия</button><button type="button" class="chip" aria-pressed="true">1</button><button type="button" class="chip" aria-pressed="true">2</button><button type="button" class="chip" aria-pressed="false">3</button><button type="button" class="chip" aria-pressed="false">4+</button></div></div>
        <div class="f"><label for="pr">Цена, ₽</label><input id="pr" placeholder="от — до" inputmode="numeric"></div>
        <div class="f"><label for="ad">Район, ЖК, улица</label><input id="ad" placeholder="Академический, ЖК…"></div>
        <a class="btn red go" href="#list">Показать [N]</a>
      </form>
      <div class="sline"><button class="sw" role="switch" aria-checked="true" aria-label="Только проверенные"></button>Только проверенные застройщики<a href="#list"><svg class="ico"><use href="#pin"/></svg>На карте</a></div>
    </div>
  </div>
  <span class="hcap">Ключи — после проверки, а не до.</span>
</section>

<section class="after"><div class="w">
''')

# 4. медиа-правила старой раскладки героя → новые
rep('.hgrid{grid-template-columns:minmax(0,1fr);min-height:0}.hl{padding:20px 0 0}.hph{min-height:440px}.sbox{position:relative;bottom:auto;margin-top:-90px;width:auto;margin-left:12px;margin-right:12px}.hero h1{font-size:76px}',
    '.chipv,.hcap{display:none}.hl{max-width:none}.hero h1{font-size:76px}')
rep(' .hph{min-height:360px;border-radius:24px}.chipv{left:12px;right:12px;width:auto;top:12px;padding:10px 12px}.chipv ul{display:none}\n .sbox{margin:-60px 6px 0}',
    ' .hero{min-height:0}.hbg{background-position:70% center}.hbg::after{background:linear-gradient(180deg,#0d0a08b3 0%,#0d0a0866 45%,#0d0a08cc 100%)}.hin{padding-top:36px;gap:28px}\n ')
rep('.chipv{width:340px;padding:18px 20px}.chipv ul{font-size:14px}', '.chipv ul{font-size:14px}')

# 5. тёмный блок «Отбор» — на фоне вида Екатеринбурга во всю ширину
rep('.man{background:var(--night);color:var(--milk)}',
    '.man{position:relative;background:var(--night);color:var(--milk);overflow:hidden}\n'
    '.man::before{content:\'\';position:absolute;left:0;right:0;top:0;height:clamp(420px,48vw,1100px);background:url(photo/ekb_aerial.jpg) center 40%/cover;opacity:.55}\n'
    '.man::after{content:\'\';position:absolute;left:0;right:0;top:0;height:clamp(420px,48vw,1100px);background:linear-gradient(180deg,#0e0e0f66 0%,#0e0e0f33 40%,#0e0e0f 100%)}\n'
    '.man>.w{position:relative;z-index:1}.man .mtext{padding-top:clamp(40px,8vw,240px)}')
rep('.field{position:relative;border-radius:26px;background:var(--graph);', '.field{position:relative;border-radius:26px;background:#1C1C1Ef2;backdrop-filter:blur(6px);')
rep('.checks{border-radius:26px;background:var(--graph);', '.checks{border-radius:26px;background:#1C1C1Ef2;backdrop-filter:blur(6px);')

# 6. на сверхшироких: плитка в 4 колонки, подборки крупнее
rep('@media(min-width:2200px){#cards.grid{--cols:3}', '@media(min-width:2600px){#cards.grid{--cols:4}}\n@media(min-width:2200px){#cards.grid{--cols:3}')

open(p, 'w', encoding='utf8').write(s)
print('ok')
