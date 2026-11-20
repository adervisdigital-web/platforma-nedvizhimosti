"""Проверка функционала сайта, как у посетителя и менеджера: главная (окна заявок, поиск, избранное, сравнение, чат, подбор за 3 шага, меню телефона),
каталог, квартира, ЖК, дома, ремонт, ипотека, риелторам, застройщикам, 404, политика; админка (заявки, настройки, выгрузка фида).
ЗАПУСКАТЬ ТОЛЬКО НА КОПИИ БАЗЫ: отправляет заявки и меняет настройки. Пример:
  копия базы + обёртка роутера с $GLOBALS['PN_DSN'] → php -S 127.0.0.1:8092 -t site/public <обёртка>;
  фид для выгрузки: py -3 -m http.server 8093 в папке с feed.xml (site/tests/fixtures/feed_ekb.xml);
  py -3 -X utf8 tools/qa_site.py <папка для отчёта> [http://127.0.0.1:8092/]
Лимит заявок — 5 в час с одного IP: на одной копии базы запускать один раз."""
import sys, time, json
sys.path.insert(0, r'C:\Users\MSI\Desktop\ПЛАТФОРМА -приложение\tools')
from cdp import Browser
OUT = sys.argv[1]; B = sys.argv[2] if len(sys.argv) > 2 else 'http://127.0.0.1:8092/'
RES = []
def ok(name, cond, info=''):
    RES.append(('OK  ' if cond else 'FAIL') + ' ' + name + (f' — {info}' if info else '')); print(RES[-1], flush=True)
b = Browser(profile=OUT + '/prof_' + str(int(time.time())))
b.call('Page.addScriptToEvaluateOnNewDocument', source="window.__errs=[];addEventListener('error',e=>__errs.push(e.message+' @'+(e.filename||'').split('/').pop()+':'+e.lineno));addEventListener('unhandledrejection',e=>__errs.push(String(e.reason)))")
E = lambda js: b.ev(js)
def errs(page):
    e = E("JSON.stringify(__errs)"); ok(f'{page}: нет ошибок JS', e == '[]', e if e != '[]' else '')
def go(path, wait=3, w=1440, mob=False):
    b.viewport(w, 900 if not mob else 844, mob); b.open(B + path, wait=wait)
def lq_open(sel, idx=0):
    E(f"window.scrollTo(0,0); document.querySelectorAll({json.dumps(sel)})[{idx}].click()"); time.sleep(.6)
    return E("(()=>{const d=document.querySelector('dialog.lq'); return d&&d.open ? {t:document.querySelector('#lqT').textContent, w:d._ctx.want, k:d._ctx.kind, when:!document.querySelector('.lq-when').hidden} : null})()")
def lq_submit(phone='9001234567', name='Тест'):
    E(f"(()=>{{const f=document.querySelector('dialog.lq form'); f.elements.name.value='{name}'; const p=f.elements.phone; p.value='{phone}'; p.dispatchEvent(new Event('input')); f.elements.cc.checked=true; f.requestSubmit();}})()")
    time.sleep(1.8)
    return E("(()=>{const d=document.querySelector('dialog.lq'); return {ok:!d.querySelector('.lq-ok').hidden, msg:(d.querySelector('#lqOk')||{}).textContent, err:document.querySelector('#lqN').textContent}})()")
def lq_close(): E("document.querySelector('dialog.lq')&&document.querySelector('dialog.lq').close()")
try:
    # ---------------- главная
    go('?shot', 4)
    btns = E("[...document.querySelectorAll('main [href*=\"#lead\"], .sec [href*=\"#lead\"], footer [href*=\"#lead\"]')].map(a=>(a.textContent.trim()||'?')+(a.hasAttribute('data-lead')?'':' [БЕЗ ОКНА]')).join(' | ')")
    ok('главная: все кнопки к заявке открывают окно', '[БЕЗ ОКНА]' not in btns, btns)
    for sel, name in [('#calc [data-lead]', 'ипотека'), ('#ba [data-lead]', 'ремонт'), ('#houses .cout [data-lead]', 'дом'), ('[data-pack]', 'один менеджер'), ('#cab [data-lead]', 'кабинет'), ('footer [data-lead]', 'подвал «Связаться»')]:
        r = lq_open(sel)
        ok(f'главная: окно «{name}»', bool(r), json.dumps(r, ensure_ascii=False)[:230] if r else 'не открылось'); lq_close()
    r = lq_open('#calc [data-lead]')
    ok('главная: к заявке по ипотеке приложен расчёт', r and 'стоимость квартиры' in r['w'] and 'итог' in r['w'], r and r['w'])
    time.sleep(2.5); s = lq_submit(); ok('главная: заявка по ипотеке отправлена', s['ok'], json.dumps(s, ensure_ascii=False)[:200]); lq_close()
    # поиск, избранное, сравнение, окно избранного → запись
    E("document.querySelectorAll('.tabs button')[0].click(); document.querySelector('#sf').requestSubmit()"); time.sleep(.6)
    ok('главная: поиск фильтрует список', E("document.querySelectorAll('#cards .card').length") > 0, f"карточек {E('document.querySelectorAll(\"#cards .card\").length')}")
    E("document.querySelector('#fltX') && document.querySelector('#fltX').click()"); time.sleep(.3)
    E("document.querySelectorAll('.card .ib.fav')[0].click(); document.querySelectorAll('.card .ib.cmp')[0].click(); document.querySelectorAll('.card .ib.cmp')[1].click()"); time.sleep(.3)
    ok('главная: избранное и сравнение — счётчики', E("document.querySelector('#favCnt').textContent") == '1' and E("document.querySelector('#cmpCnt').textContent") == '2',
       f"fav={E('document.querySelector(\"#favCnt\").textContent')} cmp={E('document.querySelector(\"#cmpCnt\").textContent')}")
    E("document.querySelector('#cmpBtn').click()"); time.sleep(.6)
    ok('главная: таблица сравнения', E("document.querySelectorAll('.ctab td').length") >= 4); E("document.querySelector('#dlg').close()")
    E("document.querySelector('#favBtn').click()"); time.sleep(.8)
    r = lq_open('#dlgB [data-lead]'); ok('избранное → «Записаться на просмотр» — окно с датой', bool(r) and r['k'] == 'viewing' and r['when'], json.dumps(r, ensure_ascii=False)[:200]); lq_close()
    # быстрый просмотр и запись
    E("document.querySelectorAll('.card .qv')[0].click()"); time.sleep(.6)
    ok('главная: быстрый просмотр квартиры', E("document.querySelector('#dlg').open") is True, E("document.querySelector('#dlgT').textContent")); E("document.querySelector('#dlg').close()")
    # чат
    E("document.querySelector('#chatFab, .fab, [data-chat]').click()"); time.sleep(.6)
    for q, want in [('Замер бесплатный?', 'Замер бесплатный'), ('Где ваш офис?', 'Амундсена'), ('Рассрочка на дом', '95 000')]:
        E(f"(()=>{{const i=document.querySelector('#chatIn'); i.value={json.dumps(q)}; document.querySelector('#chatForm').requestSubmit();}})()"); time.sleep(1.6)
        last = E("[...document.querySelectorAll('#chatLog > *')].pop().textContent")
        ok(f'чат: «{q}»', want in (last or ''), (last or '')[:120])
    E("document.querySelector('#chatX').click()")
    # заявка внизу (подбор за 3 шага)
    E("document.querySelector('#lead').scrollIntoView()"); time.sleep(.5)
    E("document.querySelector('#qNext').click(); document.querySelector('#qNext').click()"); time.sleep(.4)
    E("(()=>{const f=document.querySelector('#leadForm'); const p=f.querySelector('input[type=tel]'); p.value='9001234568'; p.dispatchEvent(new Event('input')); const c=f.querySelector('input[type=checkbox]'); if(c) c.checked=true; f.requestSubmit();})()"); time.sleep(1.8)
    ok('главная: заявка «Подбор за 3 шага»', 'Спасибо' in (E("document.querySelector('#lead').innerText") or '') or E("document.querySelector('#leadForm').classList.contains('sent')"), (E("document.querySelector('#lead .ok, #qOk, .sent') && document.querySelector('#lead .ok, #qOk, .sent').textContent") or '')[:100])
    errs('главная')
    # телефон: меню
    go('?shot', 3, 390, True)
    E("document.querySelector('#mnBtn').click()"); time.sleep(.4)
    links = E("[...document.querySelectorAll('#mnav .mn-l a')].map(a=>a.textContent).join(', ')")
    ok('телефон: меню открывается, есть «Риелторам»', E("!document.querySelector('#mnav').hidden") and 'Риелторам' in links, links)
    E("document.querySelector('#mnX').click()"); errs('главная (телефон)')

    # ---------------- подстраницы
    go('kvartiry/')
    n0 = E("document.querySelectorAll('.ct-card').length")
    E("const f=document.querySelector('[name=pmax]'); f.value='6'; f.dispatchEvent(new Event('input',{bubbles:true}))"); time.sleep(.5)
    n1 = E("[...document.querySelectorAll('.ct-card')].filter(c=>!c.hidden).length")
    ok('каталог: фильтр по цене', 0 < n1 < n0, f'{n0} → {n1}, адрес {E("location.search")}')
    r = lq_open('.ct-cta [data-lead]'); ok('каталог: «Подобрать квартиру» с фильтрами', r and 'фильтры' in r['w'], r and r['w']); lq_close()
    E("document.querySelector('[data-view=map]').click()"); time.sleep(3.5)
    ok('каталог: карта', E("document.querySelectorAll('.ct-pin').length") > 0, f"меток {E('document.querySelectorAll(\".ct-pin\").length')}")
    errs('каталог')
    slug = E("document.querySelector('.ct-card h3 a').getAttribute('href')")
    go(slug)
    E("document.querySelectorAll('.ob-gal [role=tab], .ob-tabs button')[1] && document.querySelectorAll('.ob-gal [role=tab], .ob-tabs button')[1].click()"); time.sleep(.3)
    r = lq_open('[data-lead="viewing"]'); ok('квартира: «Записаться на просмотр» — окно с датой', r and r['when'], json.dumps(r, ensure_ascii=False)[:180]); lq_close()
    E("const r=document.querySelector('[data-mort] [data-i=down]'); if(r){r.value=40; r.dispatchEvent(new Event('input',{bubbles:true}))}"); time.sleep(.3)
    ok('квартира: ипотечный калькулятор пересчитывает', '40' in (E("(document.querySelector('[data-mort] [data-o=down]')||{}).textContent") or ''), E("(document.querySelector('[data-mort] [data-o=down]')||{}).textContent"))
    errs('квартира')
    go('zhk/kvarts/'); ok('страница ЖК', E("document.querySelectorAll('.ct-card').length") > 0); errs('ЖК')
    go('doma/'); E("document.querySelectorAll('[data-line]')[1] && document.querySelectorAll('[data-line]')[1].click()"); time.sleep(.3)
    ok('дома: фильтр по линейке', E("[...document.querySelectorAll('.dm-card')].filter(c=>!c.hidden).length") < E("document.querySelectorAll('.dm-card').length")); errs('дома')
    h = E("document.querySelector('.dm-card a').getAttribute('href')"); go(h)
    r = lq_open('[data-lead]'); ok('дом: заявка из страницы проекта', bool(r), r and r['w']); lq_close(); errs('дом')
    go('remont/')
    E("const r=document.querySelector('[data-ren] [data-i=area]'); r.value=80; r.dispatchEvent(new Event('input',{bubbles:true}))"); time.sleep(.3)
    ok('ремонт: калькулятор', '80' in E("document.querySelector('[data-ren] [data-o=area]').textContent"), E("document.querySelector('[data-ren] [data-o=sum]').textContent"))
    r = lq_open('[data-ren] [data-lead]'); ok('ремонт: смета с расчётом', r and 'итого' in r['w'], r and r['w']); lq_close(); errs('ремонт')
    go('ipoteka/')
    r = lq_open('[data-mort] [data-lead]'); ok('ипотека: заявка с расчётом', r and 'платёж' in r['w'], r and r['w'])
    time.sleep(2.5); s = lq_submit('9001234569'); ok('ипотека: заявка отправлена', s['ok'], json.dumps(s, ensure_ascii=False)[:160]); lq_close(); errs('ипотека')
    go('rieltoram/'); time.sleep(2.5)
    r = lq_open('.sv-band [data-lead]'); s = lq_submit('9001234570', 'Риелтор Тест'); ok('риелторам: заявка «Стать партнёром»', s['ok'], json.dumps(s, ensure_ascii=False)[:160]); lq_close(); errs('риелторам')
    go('zastroyshchikam/'); r = lq_open('.sv-band [data-lead]'); ok('застройщикам: окно', bool(r)); lq_close(); errs('застройщикам')
    go('net-takoy-stranicy/'); ok('404 для несуществующей', '404' in (E("document.body.innerText") or ''));
    go('privacy/'); ok('политика ПДн открывается', 'персональных' in (E("document.body.innerText") or ''))

    # ---------------- админка
    go('admin/login', 2)
    E("document.querySelector('[name=login]').value='admin'; document.querySelector('[name=password]').value='admin'; document.querySelector('form').submit()"); time.sleep(2)
    go('admin/leads', 2)
    txt = E("document.body.innerText")
    ok('админка: заявки дошли (ипотека, риелтор)', 'Ипотека: подобрать программу' in txt and 'Риелтор' in txt, '')
    ok('админка: к заявке приложен расчёт', 'итог' in txt or 'платёж' in txt)
    go('admin/settings', 2)
    E("(()=>{const i=document.querySelector('[name=realtor_fee]'); i.value='50 % комиссии застройщика'; document.querySelector('form.ad-form').submit();})()"); time.sleep(2)
    go('rieltoram/'); ok('настройки → «Риелторам»: вознаграждение подставилось', '50 % комиссии застройщика' in E("document.body.innerText"))
    go('admin/feeds/new', 2)
    E("(()=>{const f=document.querySelector('form.ad-form'); f.name.value='Тестовый фид'; f.url.value='http://127.0.0.1:8093/feed.xml'; f.only_verified.checked=false; f.submit();})()"); time.sleep(2)
    loc = E("location.pathname"); ok('выгрузка создана', loc.startswith('/admin/feeds/') and loc != '/admin/feeds/new', loc)
    E("[...document.querySelectorAll('form')].find(f=>f.querySelector('[name=do][value=run]')).submit()"); time.sleep(4)
    flash = E("document.body.innerText.slice(0,1200)")
    ok('выгрузка: «Загрузить сейчас»', 'добавлено 3' in flash, flash[:200])
    go('kvartiry/'); ok('каталог: квартиры из фида на сайте', E("document.querySelectorAll('.ct-card').length") == n0 + 3, f"{n0} → {E('document.querySelectorAll(\".ct-card\").length')}")
    ok('каталог: ЖК из фида', 'Тестовый парк' in E("document.body.innerText"))
    go('admin/apartments', 2); ok('админка: квартиры открываются', E("document.querySelectorAll('tr[data-href]').length") >= 15)
    errs('админка')
finally:
    b.close()
    open(OUT + '/qa_report.txt', 'w', encoding='utf8').write('\n'.join(RES))
    print('\nИТОГО: OK', sum(r.startswith('OK') for r in RES), 'FAIL', sum(r.startswith('FAIL') for r in RES))
