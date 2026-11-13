"""Сайт v6 — по ответам заказчика (2026-11-13): ремонт делаем сами, дома по своим проектам с рассрочкой,
реальные цифры, банки, застройщики, 0 ₽ комиссии, гарантия 5 лет, кабинет с камерой, отзывы (демо), ИИ-помощник 24/7.
Run из корня репо: py -3 tools/patches/site_v6_client.py  (исходник — 08_Сайт_пример/v5.html)"""
P = '08_Сайт_пример/'
s = open(P + 'v5.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


CSS = r'''
/* v6 */
.trust{display:flex;gap:8px;flex-wrap:wrap;margin-top:24px}
.trust span{display:inline-flex;align-items:center;gap:8px;background:#ffffff1a;border:1px solid #ffffff38;backdrop-filter:blur(6px);border-radius:999px;padding:7px 14px;font-size:13px;font-weight:600;color:#fff}
.trust span::before{content:'';width:7px;height:7px;border-radius:50%;background:var(--red)}
.devs{display:flex;flex-wrap:wrap;gap:6px}.devs span{border:1px solid var(--line);border-radius:999px;padding:5px 11px;font-size:12px;font-weight:700}
.devcap{font-size:12px;color:var(--mut)}
.banks{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:24px;font-size:14px;color:var(--mut)}
.banks span{background:#fff;border-radius:999px;padding:9px 15px;font-weight:700;color:var(--ink);font-size:14px}
/* дома */
.hgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:44px}
.hp{background:#fff;border-radius:26px;overflow:hidden;display:flex;flex-direction:column;border:2px solid transparent;text-align:left;padding:0;transition:border-color .2s,box-shadow .25s}
.hp:hover{box-shadow:0 20px 44px #00000012}.hp[aria-pressed=true]{border-color:var(--ink)}
.hp .ph{aspect-ratio:4/3;overflow:hidden;position:relative;width:100%}.hp img{width:100%;height:100%;object-fit:cover;transition:transform .6s}.hp:hover img{transform:scale(1.04)}
.hp .ph span{position:absolute;left:12px;top:12px;background:#fff;border-radius:999px;padding:5px 11px;font-size:12px;font-weight:700}
.hp .b{padding:18px 20px 20px;display:flex;flex-direction:column;gap:6px}
.hp h3{margin:0;font:500 30px/1 Manrope;letter-spacing:-.03em}.hp .m{font-size:13px;color:var(--mut)}
.hp .sel{margin-top:8px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:8px}.hp .sel::before{content:'';width:14px;height:14px;border-radius:50%;border:2px solid var(--line)}
.hp[aria-pressed=true] .sel::before{border-color:var(--red);background:var(--red);box-shadow:inset 0 0 0 2px #fff}
.cout.dk{background:var(--night)}.cout.dk .crow{border-color:#ffffff24}
.cout.lt{background:#fff;color:var(--ink)}.cout.lt .crow{border-color:var(--line)}.cout.lt .btn{background:var(--red);color:#fff}
.seg2{display:flex;gap:6px;flex-wrap:wrap}.seg2 button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:9px 15px;font-weight:600;font-size:13px}.seg2 button[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}
.calc .cin{align-content:center}
.hint{display:flex;justify-content:space-between;font-size:12px;color:var(--mut);margin-top:-4px}
/* кабинет */
.cab{background:var(--gray);overflow:hidden}
.cgrid{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:clamp(40px,6vw,160px);align-items:center}
.lead2{font-size:clamp(16px,1.1vw,22px);color:#4A4741;max-width:620px;margin:26px 0 0}
.cfeat{list-style:none;margin:40px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;max-width:900px}
.cfeat li{background:#fff;border-radius:22px;padding:20px 22px}.cfeat b{display:flex;align-items:center;gap:8px;font-size:17px}.cfeat b::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--red)}.cfeat span{display:block;color:var(--mut);font-size:14px;margin-top:4px}
.cphone{width:clamp(320px,22vw,400px);background:var(--night);border-radius:52px;padding:12px;box-shadow:0 40px 90px #0000003d;transform:rotate(-2deg)}
.scr{background:var(--milk);border-radius:42px;overflow:hidden;padding:18px 14px 20px;display:grid;gap:10px}
.scr .sh{display:flex;justify-content:space-between;align-items:center;padding:4px 6px}.scr .sh b{font-size:17px}.scr .sh small{display:block;font-size:11px;color:var(--mut)}
.scr .av{width:34px;height:34px;border-radius:50%;background:var(--ink);display:flex;align-items:center;justify-content:center}
.cam{position:relative;border-radius:22px;overflow:hidden;aspect-ratio:16/10.5;background:#333}
.cam img{width:100%;height:100%;object-fit:cover;filter:saturate(.8) contrast(1.05)}
.cam .live{position:absolute;left:10px;top:10px;background:var(--red);color:#fff;font-size:10px;font-weight:800;letter-spacing:.08em;border-radius:6px;padding:3px 7px;display:flex;align-items:center;gap:5px}
.cam .live i{width:6px;height:6px;border-radius:50%;background:#fff;animation:blink 1.4s infinite}
@keyframes blink{50%{opacity:.25}}
.cam .ts{position:absolute;right:10px;top:10px;color:#fff;font:600 10px ui-monospace,Consolas,monospace;background:#0007;border-radius:6px;padding:3px 6px}
.cam .cn{position:absolute;left:10px;bottom:10px;color:#fff;font-size:11px;font-weight:700;background:#0007;border-radius:6px;padding:3px 7px}
.box{background:#fff;border-radius:20px;padding:14px 16px}
.box .k{font-size:11px;color:var(--mut)}.box b{font-size:15px}
.bar{display:flex;gap:4px;margin-top:10px}.bar i{flex:1;height:6px;border-radius:3px;background:var(--gray)}.bar i.on{background:var(--red)}.bar i.half{background:linear-gradient(90deg,var(--red) 50%,var(--gray) 50%)}
.act{display:flex;align-items:center;gap:10px;font-size:13px;padding:8px 0;border-top:1px solid #0000000d}.act:first-of-type{border-top:0}
.act i{width:18px;height:18px;border-radius:50%;flex:none;border:2px solid var(--line)}.act i.ok{background:var(--ink);border-color:var(--ink)}
.act small{display:block;color:var(--mut);font-size:11px}.act>div{min-width:0}.act button{flex:none;margin-left:auto;border:0;background:var(--red);color:#fff;border-radius:999px;padding:7px 12px;font-size:12px;font-weight:700}
.act.done button{background:var(--ink)}
/* отзывы */
.demo{font-size:12px;color:var(--mut);border:1px dashed #C9C5BE;border-radius:999px;padding:6px 12px}
.rv{display:grid;grid-auto-flow:column;grid-auto-columns:clamp(300px,24vw,460px);gap:14px;margin-top:40px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:12px;scrollbar-width:thin}
.rc{scroll-snap-align:start;background:#fff;border-radius:26px;overflow:hidden;display:flex;flex-direction:column}
.rc .ph{aspect-ratio:16/9;position:relative;overflow:hidden;flex:none}.rc .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.rc .ph span{position:absolute;left:12px;top:12px;background:#fff;border-radius:999px;padding:5px 11px;font-size:12px;font-weight:700}
.rc .b{padding:20px 22px 22px;display:flex;flex-direction:column;gap:14px;flex:1}
.rc q{font-size:16px;line-height:1.55;quotes:none}.rc .who{margin-top:auto;display:flex;align-items:center;gap:10px;font-size:13px}
.rc .who i{width:38px;height:38px;border-radius:50%;background:var(--soft);display:flex;align-items:center;justify-content:center;font-style:normal;font-weight:700}
.rc .who b{display:block;font-size:14px}.rc .who span{color:var(--mut)}
/* гарантии */
.gstrip{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;margin-top:14px}
.gstrip div{background:var(--night);color:var(--milk);border-radius:22px;padding:22px}
.gstrip b{display:block;font:300 clamp(34px,2.6vw,64px)/1 Manrope;letter-spacing:-.04em;color:var(--red)}.gstrip span{display:block;margin-top:10px;font-size:14px;color:#C9C5BE}
/* мессенджеры */
.msg{display:flex;gap:8px;flex-wrap:wrap;margin-top:24px}.msg a{display:inline-flex;align-items:center;gap:8px;border:1px solid #ffffff80;border-radius:999px;padding:10px 18px;font-weight:700;font-size:14px}.msg a:hover{background:#fff;color:var(--red)}
/* чат */
.chatfab{position:fixed;right:clamp(16px,2vw,40px);bottom:clamp(16px,2vw,40px);z-index:45;border:0;background:var(--ink);color:#fff;border-radius:999px;padding:12px 22px 12px 14px;display:flex;align-items:center;gap:12px;box-shadow:0 18px 40px #0000004d;text-align:left}
.chatfab i{width:34px;height:34px;border-radius:50%;background:var(--red);display:flex;align-items:center;justify-content:center}
.chatfab b{display:block;font-size:15px}.chatfab small{display:block;font-size:11px;color:#C9C5BE}
.chat{position:fixed;right:clamp(16px,2vw,40px);bottom:clamp(16px,2vw,40px);z-index:50;width:min(400px,calc(100vw - 32px));height:min(620px,calc(100vh - 120px));background:#fff;border-radius:26px;box-shadow:0 30px 80px #00000040;display:flex;flex-direction:column;overflow:hidden}
.chat[hidden]{display:none}
.ch-h{display:flex;align-items:center;gap:12px;padding:16px 18px;background:var(--night);color:var(--milk)}
.ch-h b{display:block;font-size:15px}.ch-h small{font-size:12px;color:#A9A49B;display:flex;align-items:center;gap:6px}.ch-h small i{width:7px;height:7px;border-radius:50%;background:#3DD68C}
.ch-x{margin-left:auto;width:36px;height:36px;border-radius:50%;border:0;background:#ffffff1a;color:#fff;font-size:20px;line-height:1}
.ch-b{flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:10px;background:var(--soft)}
.ch-b p{margin:0;max-width:86%;padding:10px 14px;border-radius:18px;font-size:14px;line-height:1.45;background:#fff;align-self:flex-start;border-bottom-left-radius:6px}
.ch-b p.me{align-self:flex-end;background:var(--ink);color:#fff;border-radius:18px;border-bottom-right-radius:6px}
.ch-b p a{color:var(--red);font-weight:700}
.ch-b p.typing{color:var(--mut)}
.ch-q{display:flex;gap:6px;overflow-x:auto;padding:10px 14px 0;background:var(--soft)}.ch-q button{flex:none;border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 12px;font-size:12px;font-weight:600}
.ch-f{display:flex;gap:8px;padding:12px 14px;background:var(--soft)}.ch-f input{flex:1;border:1px solid var(--line);border-radius:999px;padding:0 16px;height:44px;font:500 14px Manrope;outline:none}.ch-f input:focus{border-color:var(--ink)}
.ch-f button{width:44px;height:44px;border-radius:50%;border:0;background:var(--red);color:#fff;font-size:18px}
.ch-m{display:flex;gap:6px;justify-content:center;padding:10px 14px 14px;background:var(--soft);font-size:12px;font-weight:700}.ch-m a{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 12px}
@media(min-width:1700px){.hp h3{font-size:clamp(30px,1.9vw,44px)}.hp .m,.cfeat span{font-size:15px}.cfeat b{font-size:19px}.rc q{font-size:18px}.gstrip span{font-size:16px}.banks span{font-size:15px}}
@media(max-width:1200px){.hgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.gstrip{grid-template-columns:repeat(3,minmax(0,1fr))}.cgrid{grid-template-columns:minmax(0,1fr)}.cphone{margin:0 auto}}
@media(max-width:800px){.hgrid,.cfeat{grid-template-columns:minmax(0,1fr)}.gstrip{grid-template-columns:repeat(2,minmax(0,1fr))}.inst{grid-template-columns:minmax(0,1fr)}
 .chatfab{display:none}.chat{right:8px;left:8px;bottom:8px;width:auto;height:calc(100svh - 80px)}.cphone{transform:none;width:min(340px,100%)}.trust span{font-size:12px;padding:6px 11px}.rv{grid-auto-columns:82%}}
'''
rep('@media(prefers-reduced-motion:reduce)', CSS + '@media(prefers-reduced-motion:reduce)')

rep('<title>Платформа недвижимости — квартиры в Екатеринбурге, за которые мы ручаемся</title>',
    '<title>Платформа недвижимости — квартиры, дома и ремонт в Екатеринбурге</title>')
rep('<symbol id="mark"', '<symbol id="msg" viewBox="0 0 24 24"><path d="M4 5.5h16v11H9l-5 4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>\n  <symbol id="mark"')

# шапка
rep('<a class="on" href="#search">Новостройки</a><a href="#search">Вторичка</a><a href="#calc">Ипотека</a><a href="#partners">Ремонт и дома</a><a href="#how">Как мы проверяем</a>',
    '<a class="on" href="#list">Квартиры</a><a href="#calc">Ипотека</a><a href="#houses">Дома</a><a href="#ba">Ремонт</a><a href="#cab">Кабинет</a><a href="#rev">Отзывы</a>')

# первый экран
rep('<p class="sub">Продаём только то, что проверили сами: надёжные застройщики, чистые сделки, самые выгодные условия. Ремонт и дом — у партнёров, в которых мы уверены.</p>',
    '<p class="sub">Продаём только то, что проверили сами: надёжные застройщики, сделки через эскроу, спецпредложения напрямую от застройщиков. Ремонт и дома делаем сами — с гарантией 5 лет.</p>\n'
    '      <div class="trust"><span>0 ₽ комиссии</span><span>Эскроу-счета</span><span>Только по договору</span><span>Гарантия 5 лет</span></div>')

# подборки и промо
rep('<a class="cat" role="listitem" href="#partners" style="background-image:url(photo/house.jpg)"><b>Дома за городом</b><span>от проверенных строителей</span></a>',
    '<a class="cat" role="listitem" href="#houses" style="background-image:url(photo/house.jpg)"><b>Дома по нашим проектам</b><span>рассрочка до 5 лет</span></a>')
rep('<h3>Квартира с ремонтом — под ключ<i class="o n"></i></h3><p>Купите квартиру у нас — ремонт сделает партнёр, которого мы проверили. Ведём всё сами.</p>',
    '<h3>Квартира с ремонтом — одним пакетом<i class="o n"></i></h3><p>Подберём квартиру и сделаем ремонт сами: смета, договор, акт на каждый этап, гарантия 5 лет.</p>')
rep('<a class="pt dark" href="#calc"><div><h3>Самая выгодная ипотека<i class="o"></i></h3><p>Сравним программы банков и покажем, где платёж ниже.</p>',
    '<a class="pt dark" href="#calc"><div><h3>Ипотека по индивидуальной ставке<i class="o"></i></h3><p>Сбер, ВТБ, Альфа-Банк, ДОМ.РФ, Россельхозбанк, УБРИР — сравним программы и покажем, где платёж ниже.</p>')
rep('<p>Что смотрим у застройщика, у продавца на вторичке и у подрядчика.</p>', '<p>Что смотрим у застройщика и у продавца на вторичке — и как работаем сами.</p>')

# объявления
rep("line: 'Сдача — [КВАРТАЛ] · прошлые дома сданы в срок', tags: ['Новостройка', 'Рядом метро'], tag: ''",
    "line: 'Сдача — [КВАРТАЛ] · прошлые дома сданы в срок', tags: ['Новостройка', 'Эскроу'], tag: 'Спецпредложение застройщика'")
rep("line: 'Дом сдан · ремонт от партнёра — смета до начала работ'", "line: 'Дом сдан · наш ремонт — смета до начала работ, гарантия 5 лет'")
rep("par: [['Готовые объекты и портфолио', 'выезд'], ['Договор, смета, сроки', 'документы'], ['Гарантия на работы', 'условия'], ['Отзывы прошлых заказчиков', 'люди'], ['Приёмка по этапам', 'контроль']],",
    "our: [['Замер и смета до начала работ', 'выезд'], ['Предварительный договор', 'документы'], ['Промежуточный акт на каждый этап', 'приёмка'], ['Камера на объекте в личном кабинете', '24/7'], ['Гарантия на работы', '5 лет']],")

# отбор
rep('<p class="mtext"><b>Мы не строим и не ремонтируем.</b> Мы&nbsp;проверяем тех, кто это делает, — и&nbsp;<b>продаём только то, за&nbsp;что <em class="nw">ручаемся<i class="o"></i></em></b></p>',
    '<p class="mtext"><b>Застройщиков проверяем.</b> Ремонт и&nbsp;дома делаем сами — по&nbsp;договору и&nbsp;с&nbsp;гарантией 5&nbsp;лет. <b>Продаём только то, за&nbsp;что <em class="nw">ручаемся<i class="o"></i></em></b></p>')
rep('<h3>Что мы проверяем<i class="o"></i></h3>', '<h3>Как мы ручаемся<i class="o"></i></h3>')
rep('<button aria-pressed="false" data-k="par">Подрядчик</button>', '<button aria-pressed="false" data-k="our">Наш ремонт и дома</button>')
rep('''    <div><b>[N]</b><span>застройщиков прошли нашу проверку</span></div>
    <div><b>[N]</b><span>подрядчиков по ремонту и строительству</span></div>
    <div><b>[N]</b><span>сделок закрыли в Екатеринбурге</span></div>
    <div><b>[N]</b><span>лет на рынке</span></div>''',
    '''    <div><b>5</b><span>лет на рынке Екатеринбурга</span></div>
    <div><b>1&thinsp;985</b><span>сделок с квартирами</span></div>
    <div><b>67</b><span>договоров на строительство домов</span></div>
    <div><b>85</b><span>квартир с нашей отделкой</span></div>''')

# направления (бывшие «Партнёры»)
i = s.index('<section class="sec" id="partners">'); j = s.index('</div></section>', i) + len('</div></section>')
s = s[:i] + '''<section class="sec" id="partners"><div class="w">
  <div class="br">[ <b>03</b> Что мы делаем ]</div>
  <h2 class="t">Квартира<i class="o"></i> Дом<i class="o"></i> Ремонт<i class="o"></i></h2>
  <div class="pgrid">
    <div class="pc"><div class="ph"><img src="photo/inspect.jpg" alt="Инженер проверяет строящийся дом" loading="lazy"><span>Продаём</span></div><div class="b"><h3>Квартиры<i class="o"></i></h3><p>Новостройки от проверенных застройщиков — со спецпредложениями напрямую от них. Вторичка — после проверки юриста. Комиссии для покупателя нет.</p><div class="devs"><span>Брусника</span><span>Атомстройкомплекс</span><span>УГМК</span><span>Прогресс</span><span>Атлас</span></div><a class="lk" href="#list">Смотреть квартиры</a></div></div>
    <div class="pc"><div class="ph"><img src="photo/house.jpg" alt="Двухэтажный дом с гаражом" loading="lazy"><span>Строим</span></div><div class="b"><h3>Дома<i class="o"></i></h3><p>Готовые проекты из газоблока, кирпича, керамоблока и дерева. Первый взнос 30 %, остальное — по этапам или в рассрочку до 5 лет.</p><div class="br2">[ газоблок ] [ кирпич ] [ керамоблок ] [ дерево ] [ гарантия 5 лет ]</div><a class="lk" href="#houses">Выбрать проект</a></div></div>
    <div class="pc"><div class="ph"><img src="photo/crew.jpg" alt="Бригада укладывает плитку" loading="lazy"><span>Делаем сами</span></div><div class="b"><h3>Ремонт<i class="o"></i></h3><p>Работа и материалы — от 20 000 до 100 000 ₽ за м². Смета и предварительный договор до начала, акт на каждый этап.</p><div class="br2">[ смета ] [ договор ] [ акты этапов ] [ гарантия 5 лет ]</div><a class="lk" href="#ba">Посчитать ремонт</a></div></div>
  </div>
  <div class="way"><span class="stp"><i></i>Подобрали квартиру</span><span class="ln"></span><span class="stp"><i></i>Провели сделку</span><span class="ln"></span><span class="stp"><i></i>Сделали ремонт</span><span class="ln"></span><span class="stp"><i></i>Вы получили ключи</span><a class="btn red" href="tel:+79655002918">Один менеджер на всё</a></div>
</div></section>''' + s[j:]

# ипотека: банки
rep('<h2 class="t">Посчитайте платёж — без звёздочек<i class="o"></i></h2>',
    '<h2 class="t">Посчитайте платёж — без звёздочек<i class="o"></i></h2>\n  <div class="banks">Работаем с банками: <span>Сбер</span><span>ВТБ</span><span>Альфа-Банк</span><span>ДОМ.РФ</span><span>Россельхозбанк</span><span>УБРИР</span> — и получаем для клиентов индивидуальные ставки.</div>')

HOUSES = '''<section class="sec" id="houses" style="padding-top:0"><div class="w">
  <div class="lhead"><div><div class="br">[ <b>05</b> Дома ]</div><h2 class="t">Свой дом — в рассрочку до&nbsp;5&nbsp;лет<i class="o"></i></h2></div>
    <p style="max-width:440px;color:#4A4741;margin:0">Готовые проекты, названные в честь уральских озёр. Тёплый контур — от 100 000 ₽ за м². Выберите проект и посчитайте платёж.</p></div>
  <div class="hgrid" id="hgrid">
    <button class="hp" aria-pressed="true" data-n="Шарташ" data-a="160"><div class="ph"><img src="photo/house.jpg" alt="Двухэтажный дом с гаражом" loading="lazy"><span>Газоблок</span></div><div class="b"><h3>Шарташ</h3><div class="m">2 этажа · гараж · [ПЛОЩАДЬ] м²</div><span class="sel">Выбран</span></div></button>
    <button class="hp" aria-pressed="false" data-n="Таватуй" data-a="190"><div class="ph"><img src="photo/house_stone2.jpg" alt="Дом из светлого кирпича с балконом" loading="lazy"><span>Кирпич</span></div><div class="b"><h3>Таватуй</h3><div class="m">2 этажа · балкон · [ПЛОЩАДЬ] м²</div><span class="sel">Выбрать</span></div></button>
    <button class="hp" aria-pressed="false" data-n="Балтым" data-a="130"><div class="ph"><img src="photo/prj_flat.jpg" alt="Одноэтажный дом с плоской кровлей" loading="lazy"><span>Керамоблок</span></div><div class="b"><h3>Балтым</h3><div class="m">1 этаж · плоская кровля · [ПЛОЩАДЬ] м²</div><span class="sel">Выбрать</span></div></button>
    <button class="hp" aria-pressed="false" data-n="Аять" data-a="100"><div class="ph"><img src="photo/prj_wood.jpg" alt="Деревянный дом с террасой" loading="lazy"><span>Дерево</span></div><div class="b"><h3>Аять</h3><div class="m">1 этаж · терраса · [ПЛОЩАДЬ] м²</div><span class="sel">Выбрать</span></div></button>
  </div>
  <div class="calc inst">
    <div class="cin">
      <div class="rng"><label for="ha">Площадь дома <b id="hav"></b></label><input type="range" id="ha" min="60" max="300" step="5" value="160"></div>
      <div class="rng"><label for="ht">Рассрочка <b id="htv"></b></label><input type="range" id="ht" min="1" max="5" step="1" value="3"></div>
      <div><div style="font-size:14px;color:var(--mut);margin-bottom:10px">Как платить остаток</div>
        <div class="seg2" id="hmode"><button aria-pressed="true" data-m="inst">Внутренняя рассрочка</button><button aria-pressed="false" data-m="stage">По этапам стройки</button></div></div>
    </div>
    <div class="cout dk" aria-live="polite">
      <div class="note" id="hname">Проект «Шарташ» · тёплый контур</div>
      <div class="pay" id="hpay">—</div>
      <div class="crow"><span>Стоимость тёплого контура, от</span><b id="hsum">—</b></div>
      <div class="crow"><span>Первый взнос 30 %</span><b id="hpv">—</b></div>
      <div class="crow"><span id="hrestL">Остаток</span><b id="hrest">—</b></div>
      <a class="btn" href="#lead">Обсудить проект</a>
      <div class="note">Расчёт ориентировочный: от 100 000 ₽ за м² тёплого контура, первый взнос 30 %. Точную цену и условия рассрочки назовёт менеджер.</div>
    </div>
  </div>
</div></section>

'''
rep('<section class="sec" id="ba" style="padding-top:0"><div class="w">', HOUSES + '<section class="sec" id="ba" style="padding-top:0"><div class="w">')

# ремонт
rep('<div class="br">[ <b>05</b> Ремонт от партнёров ]</div>', '<div class="br">[ <b>06</b> Ремонт — делаем сами ]</div>')
rep('''      <li><i>1</i><div><b>Покупаете квартиру у нас</b><span>Новостройка или вторичка — после нашей проверки.</span></div></li>
      <li><i>2</i><div><b>Подбираем подрядчика</b><span>Из партнёров, которых мы проверили сами.</span></div></li>
      <li><i>3</i><div><b>Смета до начала работ</b><span>Каждая позиция и итог — до того, как вы платите.</span></div></li>
      <li><i>4</i><div><b>Приёмка по этапам</b><span>Мы на вашей стороне: проверяем, что сделано.</span></div></li>
      <li><i>✓</i><div><b>Ключи от готовой квартиры</b><span>Точка.</span></div></li>''',
    '''      <li><i>1</i><div><b>Замер и смета</b><span>Каждая позиция и итог — до того, как вы платите.</span></div></li>
      <li><i>2</i><div><b>Предварительный договор</b><span>Объём работ, сроки и цена — на бумаге.</span></div></li>
      <li><i>3</i><div><b>Работа по этапам</b><span>Каждый этап закрываем промежуточным актом.</span></div></li>
      <li><i>4</i><div><b>Ход работ — в кабинете</b><span>Камера на объекте и отчёты по этапам.</span></div></li>
      <li><i>✓</i><div><b>Гарантия 5 лет</b><span>По договору. Точка.</span></div></li>''')
REN = '''  <div class="calc" style="margin-top:40px">
    <div class="cin">
      <div class="rng"><label for="ra">Площадь квартиры <b id="rav"></b></label><input type="range" id="ra" min="20" max="160" step="1" value="55"></div>
      <div class="rng"><label for="rl">Уровень отделки <b id="rlv"></b></label><input type="range" id="rl" min="20000" max="100000" step="5000" value="40000"><div class="hint"><span>20 000 ₽/м²</span><span>100 000 ₽/м²</span></div></div>
    </div>
    <div class="cout lt" aria-live="polite">
      <div class="note">Ремонт с материалами, ориентировочно</div>
      <div class="pay" id="rpay">—</div>
      <div class="crow"><span>Цена за м²</span><b id="rppm">—</b></div>
      <div class="crow"><span>Гарантия</span><b>5 лет</b></div>
      <a class="btn" href="#lead">Вызвать замерщика</a>
      <div class="note">Точную цену даст смета после замера. Работа и материалы — от 20 000 до 100 000 ₽ за м².</div>
    </div>
  </div>
'''
i = s.index('<section class="sec" id="ba"'); j = s.index('</div></section>', i)
s = s[:j] + REN + s[j:]

CAB_REV = '''<section class="sec cab" id="cab"><div class="w cgrid">
  <div>
    <div class="br">[ <b>07</b> Личный кабинет ]</div>
    <h2 class="t">Ваш дом — в&nbsp;прямом <span class="nw">эфире<i class="o"></i></span></h2>
    <p class="lead2">Камера на объекте подключается сразу после начала работ. Смотрите стройку или ремонт с телефона, подписывайте акты этапов и следите за платежами — в одном месте.</p>
    <ul class="cfeat">
      <li><b>Камера 24/7</b><span>Трансляция с объекта — в любой момент, из любого города.</span></li>
      <li><b>Этапы и акты</b><span>Каждый этап закрывается промежуточным актом.</span></li>
      <li><b>Смета и договор</b><span>Все документы по объекту — под рукой.</span></li>
      <li><b>Платежи</b><span>График рассрочки или ипотеки и напоминания.</span></li>
    </ul>
  </div>
  <div class="cphone" aria-label="Пример личного кабинета на телефоне"><div class="scr">
    <div class="sh"><div><b>Дом «Шарташ»</b><small>газоблок · [АДРЕС УЧАСТКА]</small></div><span class="av"><svg width="18" height="17" fill="#F4F2EE"><use href="#mark"/></svg></span></div>
    <div class="cam"><img src="photo/cam_build.jpg" alt="Трансляция с камеры: дом из газоблока, монтаж стропил" loading="lazy"><span class="live"><i></i>LIVE</span><span class="ts" id="camTs"></span><span class="cn">Камера 1 · участок</span></div>
    <div class="box"><div class="k">Этап 4 из 7</div><b>Кровля — монтаж стропил</b><div class="bar"><i class="on"></i><i class="on"></i><i class="on"></i><i class="half"></i><i></i><i></i><i></i></div></div>
    <div class="box">
      <div class="act done"><i class="ok"></i><div>Акт № 3 «Стены»<small>подписан</small></div></div>
      <div class="act" id="actRow"><i></i><div>Акт № 4 «Кровля»<small id="actSt">ждёт подписи</small></div><button type="button" id="actBtn">Подписать</button></div>
    </div>
    <div class="box"><div class="k">Следующий платёж по рассрочке</div><b>[СУММА] ₽ · [ДАТА]</b></div>
  </div></div>
</div></section>

<section class="sec" id="rev"><div class="w">
  <div class="lhead"><div><div class="br">[ <b>08</b> Отзывы ]</div><h2 class="t">Говорят те, у кого уже <span class="nw">точка<i class="o"></i></span></h2></div><span class="demo">Демо-отзывы для макета — заменим настоящими</span></div>
  <div class="rv" tabindex="0" aria-label="Отзывы клиентов">
    <article class="rc"><div class="ph"><img src="photo/kv_living2.jpg" alt="" loading="lazy"><span>Новостройка</span></div><div class="b"><q>Искали двушку под семейную ипотеку полгода. Здесь за неделю показали три варианта и честно сказали, почему не стоит брать четвёртый: у застройщика переносы сдачи. Купили — дом сдали в срок.</q><div class="who"><i>М</i><div><b>Марина и Олег</b><span>2-комн. квартира, ЖК [НАЗВАНИЕ]</span></div></div></div></article>
    <article class="rc"><div class="ph"><img src="photo/rem_bathroom.jpg" alt="" loading="lazy"><span>Ремонт</span></div><div class="b"><q>Больше всего боялся, что смета вырастет. Не выросла: что записали в предварительный договор, то и заплатили. После каждого этапа — акт, без «доплатите за материалы».</q><div class="who"><i>Д</i><div><b>Дмитрий</b><span>ремонт 2-комн. квартиры</span></div></div></div></article>
    <article class="rc"><div class="ph"><img src="photo/house.jpg" alt="" loading="lazy"><span>Дом</span></div><div class="b"><q>Строим «Шарташ» в рассрочку: 30 % внесли, остальное платим по этапам. Живём в городе, а стройку смотрим по камере — вечером открыл кабинет и видно, что сделали за день.</q><div class="who"><i>Е</i><div><b>Елена</b><span>дом из газоблока</span></div></div></div></article>
    <article class="rc"><div class="ph"><img src="photo/kv_bedroom.jpg" alt="" loading="lazy"><span>Вторичка</span></div><div class="b"><q>Продавец торопил с задатком. Юрист нашёл в выписке обременение, о котором продавец «забыл». Сделку провели, только когда его сняли. Спасибо, что не дали поторопиться.</q><div class="who"><i>И</i><div><b>Игорь</b><span>вторичка, Центр</span></div></div></div></article>
    <article class="rc"><div class="ph"><img src="photo/kv_kitchen.jpg" alt="" loading="lazy"><span>Квартира + ремонт</span></div><div class="b"><q>Взяли квартиру и ремонт одним пакетом. Один менеджер вёл всё — от одобрения ипотеки до ключей. И никакой комиссии с нас — до последнего не верили.</q><div class="who"><i>К</i><div><b>Ксения и Артём</b><span>1-комн. квартира с ремонтом</span></div></div></div></article>
  </div>
</div></section>

'''
rep('<section class="sec" style="padding-top:0"><div class="w">\n  <div class="br">[ <b>06</b> Обещания ]</div>',
    CAB_REV + '<section class="sec" style="padding-top:0"><div class="w">\n  <div class="br">[ <b>09</b> Обещания ]</div>')
rep('<span>Работаем только с застройщиками и подрядчиками, которых проверили сами. Красная точка рядом с объектом — наша подпись под ним.</span>',
    '<span>Продаём квартиры только от застройщиков, которых проверили сами. Ремонт и дома делаем своими силами. Красная точка рядом с объектом — наша подпись под ним.</span>')
rep('<span>Не выкладываем всё подряд. Сравниваем цены и условия — и показываем только самые выгодные предложения.</span>',
    '<span>Спецпредложения напрямую от застройщиков, индивидуальные ставки банков и 0 ₽ комиссии для покупателя. Показываем только самые выгодные варианты.</span>')
rep('''    <div><b>Ясно<i class="o"></i></b><span>Цена, срок и следующий шаг известны заранее. Без звёздочек, мелкого шрифта и многоточий.</span></div>
  </div>''', '''    <div><b>Ясно<i class="o"></i></b><span>Работаем только по договору. Цена, срок и следующий шаг известны заранее — без звёздочек и многоточий.</span></div>
  </div>
  <div class="gstrip">
    <div><b>0 ₽</b><span>комиссии для покупателя</span></div>
    <div><b>5 лет</b><span>гарантия на ремонт и дома</span></div>
    <div><b>Эскроу</b><span>деньги за новостройку — в банке до сдачи дома</span></div>
    <div><b>Договор</b><span>и акт на каждый этап работ</span></div>
    <div><b>Рядом</b><span>если партнёр подвёл — помогаем решить вопрос</span></div>
  </div>''')

# заявка
rep('<p>Подберём варианты среди проверенных предложений и перезвоним. Или позвоните сами: <a href="tel:+79655002918" style="font-weight:700;border-bottom:2px solid #fff">+7 965 500-29-18</a></p>',
    '<p>Подберём варианты среди проверенных предложений и перезвоним. Или позвоните сами: <a href="tel:+79655002918" style="font-weight:700;border-bottom:2px solid #fff">+7 965 500-29-18</a>. На вопросы отвечаем круглосуточно — в чате, Telegram и MAX.</p>\n'
    '    <div class="msg"><a href="#" data-chat>Чат на сайте</a><a href="#">Telegram</a><a href="#">MAX</a></div>')
rep('<button type="button" aria-pressed="false">С ремонтом</button><button type="button" aria-pressed="false">Ипотеку</button></div>',
    '<button type="button" aria-pressed="false">Ремонт</button><button type="button" aria-pressed="false">Ипотеку</button></div>')

# подвал
rep('<span>Екатеринбург, [адрес офиса]</span></div>', '<span>Екатеринбург, [адрес офиса]</span><span style="display:block;margin-top:4px">p.forma196.ru</span></div>')
rep('<div><h4>С партнёрами</h4><a href="#ba">Ремонт</a><a href="#partners">Дома</a><a href="#how">Как мы проверяем</a></div>',
    '<div><h4>Делаем сами</h4><a href="#ba">Ремонт</a><a href="#houses">Дома</a><a href="#cab">Личный кабинет</a></div>')
rep('<div><h4>Компания</h4><a href="#lead">Связаться</a><a href="#">Застройщикам и подрядчикам</a></div>',
    '<div><h4>Компания</h4><a href="#how">Как мы проверяем</a><a href="#rev">Отзывы</a><a href="#lead">Связаться</a><a href="#">Telegram</a><a href="#">MAX</a></div>')
rep('<span>ООО «[НАЗВАНИЕ]» · ОГРН [НОМЕР]</span><span>Пример сайта. Цены, площади, названия ЖК и цифры — заглушки до данных заказчика.</span>',
    '<span>ИП Сафоев Шерзод Рустамович · ИНН 661709849922 · ОГРНИП 326965800115079</span><span>Пример сайта. Цены объектов, площади и названия ЖК — заглушки, отзывы — демо.</span>')

# нижнее меню + чат
rep('''  <a href="#"><svg class="ico"><use href="#heart"/></svg>Избранное</a>
  <a href="#"><svg class="ico"><use href="#user"/></svg>Профиль</a>
</nav>''', '''  <a href="#cab"><svg class="ico"><use href="#user"/></svg>Кабинет</a>
  <a href="#" data-chat><svg class="ico"><use href="#msg"/></svg>Чат 24/7</a>
</nav>

<button class="chatfab" id="chatFab" aria-expanded="false" aria-controls="chat"><i><svg class="ico" style="width:18px;height:18px"><use href="#msg"/></svg></i><span><b>Спросить</b><small>ответим 24/7</small></span></button>
<div class="chat" id="chat" role="dialog" aria-label="Помощник Платформы" hidden>
  <div class="ch-h"><svg width="30" height="28" fill="#F4F2EE"><use href="#mark"/></svg><div><b>Помощник Платформы</b><small><i></i>онлайн · отвечает круглосуточно</small></div><button class="ch-x" id="chatX" aria-label="Закрыть">×</button></div>
  <div class="ch-b" id="chatLog" aria-live="polite"></div>
  <div class="ch-q" id="chatQ"></div>
  <form class="ch-f" id="chatForm"><input id="chatIn" placeholder="Напишите вопрос" aria-label="Ваш вопрос" autocomplete="off"><button aria-label="Отправить">→</button></form>
  <div class="ch-m"><a href="#">Telegram</a><a href="#">MAX</a><a href="tel:+79655002918">Позвонить</a></div>
</div>''')

JS = r'''
// дома: проект + рассрочка
let hName = 'Шарташ';
function hcalc() {
  const a = +$('#ha').value, y = +$('#ht').value, mode = $('#hmode [aria-pressed=true]').dataset.m;
  const sum = a * 100000, pv = sum * .3, rest = sum - pv;
  $('#hav').textContent = a + ' м²'; $('#htv').textContent = y + (y === 1 ? ' год' : y < 5 ? ' года' : ' лет');
  $('#hname').textContent = `Проект «${hName}» · тёплый контур`;
  $('#hsum').textContent = fmt(sum); $('#hpv').textContent = fmt(pv); $('#hrest').textContent = fmt(rest);
  if (mode === 'inst') { $('#hpay').innerHTML = Math.round(rest / (y * 12)).toLocaleString('ru-RU') + ' <small>₽/мес</small>'; $('#hrestL').textContent = `Остаток в рассрочку на ${$('#htv').textContent}`; }
  else { $('#hpay').innerHTML = Math.round(rest / 4).toLocaleString('ru-RU') + ' <small>₽/этап</small>'; $('#hrestL').textContent = 'Остаток — 4 платежа по этапам'; }
  $('#ht').disabled = mode !== 'inst'; $('#ht').closest('.rng').style.opacity = mode === 'inst' ? 1 : .4;
}
$$('#hgrid .hp').forEach(b => b.addEventListener('click', () => {
  $$('#hgrid .hp').forEach(x => { x.setAttribute('aria-pressed', x === b); $('.sel', x).textContent = x === b ? 'Выбран' : 'Выбрать'; });
  hName = b.dataset.n; $('#ha').value = b.dataset.a; hcalc();
}));
['#ha', '#ht'].forEach(q => $(q).addEventListener('input', hcalc));
$$('#hmode button').forEach(b => b.addEventListener('click', () => { $$('#hmode button').forEach(x => x.setAttribute('aria-pressed', x === b)); hcalc(); }));
hcalc();

// ремонт
function rcalc() {
  const a = +$('#ra').value, l = +$('#rl').value;
  const lvl = l <= 35000 ? 'базовый' : l <= 65000 ? 'комфорт' : 'премиум';
  $('#rav').textContent = a + ' м²'; $('#rlv').textContent = lvl + ' · ' + l.toLocaleString('ru-RU') + ' ₽/м²';
  $('#rpay').innerHTML = Math.round(a * l / 1000).toLocaleString('ru-RU') + ' <small>тыс. ₽</small>'; $('#rppm').textContent = fmt(l);
}
['#ra', '#rl'].forEach(q => $(q).addEventListener('input', rcalc)); rcalc();

// кабинет: время камеры и подпись акта
function camTime() { const d = new Date(); $('#camTs').textContent = d.toLocaleDateString('ru-RU') + ' · ' + d.toLocaleTimeString('ru-RU'); }
camTime(); setInterval(camTime, 1000);
$('#actBtn').addEventListener('click', e => { const r = $('#actRow'); r.classList.add('done'); $('i', r).classList.add('ok'); $('#actSt').textContent = 'подписан только что'; e.currentTarget.remove(); });

// помощник 24/7 (на макете — ответы по готовым темам; на сайте — ИИ + Битрикс24)
const FAQ = [
  [/комисс|сколько берёте|бесплат/i, 'С покупателя — 0 ₽. Мы не берём комиссию с клиентов.'],
  [/ипотек|банк|ставк|сбер|втб|альф|дом\.?рф|убрир|россельхоз/i, 'Работаем со Сбером, ВТБ, Альфа-Банком, ДОМ.РФ, Россельхозбанком и УБРИР. Для наших клиентов банки дают индивидуальные ставки. Прикинуть платёж можно в <a href="#calc">калькуляторе</a>, а менеджер подберёт программу.'],
  [/ремонт|смет|отделк|м2|м²/i, 'Ремонт делаем сами: работа и материалы — от 20 000 до 100 000 ₽ за м², в зависимости от уровня отделки. Сначала замер, смета и предварительный договор, потом работа по этапам с актом на каждый. Гарантия — 5 лет. <a href="#ba">Посчитать</a>'],
  [/дом|рассроч|проект|газобл|кирпич|керам|дерев|участ/i, 'Строим по готовым проектам: газоблок, кирпич, керамоблок, дерево. Тёплый контур — от 100 000 ₽ за м². Первый взнос 30 %, остальное — по этапам или во внутреннюю рассрочку от 1 до 5 лет. <a href="#houses">Выбрать проект</a>'],
  [/гарант|договор|эскроу|безопас|надёжн|надежн|обман/i, 'Работаем только по договору. Новостройки — через эскроу-счета: деньги лежат в банке до сдачи дома. На ремонт и дома — гарантия 5 лет. Если партнёр подвёл, помогаем решить вопрос.'],
  [/камер|кабинет|трансляц|онлайн/i, 'В личном кабинете — камера с объекта, этапы, акты и платежи. Доступ открываем сразу после начала работ.'],
  [/застройщ|жк|брусник|атом|угмк|прогресс|атлас|новострой/i, 'Продаём квартиры от застройщиков, которых проверили: Брусника, Атомстройкомплекс, УГМК, Прогресс, Атлас. От них — спецпредложения напрямую. <a href="#list">Смотреть квартиры</a>'],
  [/вторичк|юрист|обремен/i, 'На вторичке юрист проверяет собственников, обременения, историю переходов права и долги — до задатка.'],
  [/привет|здравств|добр/i, 'Здравствуйте! Спросите про квартиры, ипотеку, ремонт или дома — отвечу сразу.'],
];
const QUICK = ['Есть комиссия?', 'Сколько стоит ремонт?', 'Рассрочка на дом', 'Какие банки?', 'Какие гарантии?'];
const log = $('#chatLog');
function say(t, me) { const p = document.createElement('p'); if (me) { p.className = 'me'; p.textContent = t; } else p.innerHTML = t; log.appendChild(p); log.scrollTop = log.scrollHeight; return p; }
function ask(q) {
  say(q, 1); const t = say('печатает…'); t.className = 'typing';
  const hit = FAQ.find(([re]) => re.test(q));
  setTimeout(() => { t.className = ''; t.innerHTML = hit ? hit[1] : 'Передам вопрос менеджеру — он свяжется с вами. Оставьте телефон в <a href="#lead">форме</a> или позвоните: <a href="tel:+79655002918">+7 965 500-29-18</a>.'; log.scrollTop = log.scrollHeight; }, reduce ? 0 : 700);
}
$('#chatQ').innerHTML = QUICK.map(q => `<button type="button">${q}</button>`).join('');
$$('#chatQ button').forEach(b => b.addEventListener('click', () => ask(b.textContent)));
$('#chatForm').addEventListener('submit', e => { e.preventDefault(); const v = $('#chatIn').value.trim(); if (v) { ask(v); $('#chatIn').value = ''; } });
let greeted = false;
function openChat(o) {
  $('#chat').hidden = !o; $('#chatFab').hidden = o; $('#chatFab').setAttribute('aria-expanded', o);
  if (o && !greeted) { say('Здравствуйте! Я помощник Платформы и отвечаю круглосуточно. Спросите про квартиры, ипотеку, ремонт или дома.'); greeted = true; }
  if (o) $('#chatIn').focus();
}
$('#chatFab').addEventListener('click', () => openChat(true));
$('#chatX').addEventListener('click', () => openChat(false));
$$('[data-chat]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); openChat(true); }));
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('#chat').hidden) openChat(false); });
'''
rep('</script>\n</body>', JS + '</script>\n</body>')

open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok', len(s))
