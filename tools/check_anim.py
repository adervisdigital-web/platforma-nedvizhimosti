"""Проверка анимаций сайта в реальном времени на трёх ширинах (1440, 1920, телефон 390).
Run из корня репо: py -3 -X utf8 tools/check_anim.py <папка для кадров>  → печатает отчёт, сохраняет ключевые кадры."""
import os, sys, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import Browser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file:///' + os.path.join(ROOT, '08_Сайт_пример', 'index.html').replace('\\', '/')
OUT = sys.argv[1]
R = []


def log(*a):
    s = ' '.join(str(x) for x in a); R.append(s); print(s, flush=True)


def go(b, sel, block='center'):
    b.ev(f"document.documentElement.style.scrollBehavior='auto';(document.querySelector('{sel}')).scrollIntoView({{block:'{block}'}})")


def run(name, w, h, mobile):
    b = Browser()
    try:
        b.viewport(w, h, mobile)
        b.ev("try{sessionStorage.clear();localStorage.clear()}catch(e){}")
        b.open(URL)
        t0 = time.time(); b.shot(f'{OUT}/{name}_ldr0.png')
        time.sleep(.9); b.shot(f'{OUT}/{name}_ldr1.png')
        log(f'[{name}] заставка 0.9с:', b.ev("(()=>{const l=document.getElementById('ldr');return l.className+' bar='+document.getElementById('ldrBar').style.width+' dot='+getComputedStyle(document.querySelector('.ldr-dot')).opacity})()"))
        time.sleep(2.2)
        log(f'[{name}] после заставки {time.time()-t0:.1f}с:', b.ev("document.documentElement.className+' | ldr='+document.getElementById('ldr').className"))
        time.sleep(1.2); b.shot(f'{OUT}/{name}_hero.png')
        log(f'[{name}] первый экран:', b.ev("(()=>{const q=s=>getComputedStyle(document.querySelector(s));return 'h1 op='+q('.hero h1').opacity+' dot='+q('.hero h1 i.o').transform+' sbox op='+q('.sbox').opacity+' chipv='+(document.querySelector('#chipv')?q('#chipv').opacity:'-')})()"))
        log(f'[{name}] карточка ЖК:', b.ev("document.getElementById('cvName').textContent+' | ok='+document.querySelectorAll('#cvList li.ok').length+' '+document.getElementById('cvSt').textContent"))
        # меню при прокрутке
        b.ev("scrollTo(0,1200)"); time.sleep(.8)
        log(f'[{name}] меню при прокрутке:', b.ev("document.querySelector('header').className+' prog='+getComputedStyle(document.getElementById('prog')).getPropertyValue('--s')"))
        if not mobile:
            b.ev("scrollTo(0,0)"); time.sleep(.5)
            a = b.ev("(()=>{const r=document.querySelectorAll('nav.main a')[2].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
            b.mouse(*a); time.sleep(.7)
            log(f'[{name}] точка под меню:', b.ev("getComputedStyle(document.querySelector('nav.main')).getPropertyValue('--nx')+' op='+getComputedStyle(document.querySelector('nav.main .nd')).opacity"))
        # подборки
        go(b, '.cats'); time.sleep(3.5)
        log(f'[{name}] поле точек «Самые выгодные»:', b.ev("'off='+document.querySelectorAll('.cfield i.off').length+' win='+document.querySelectorAll('.cfield i.win').length"))
        if not mobile:
            c = b.ev("(()=>{const r=document.querySelectorAll('.cat')[2].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
            b.mouse(*c); time.sleep(.7)
            log(f'[{name}] наведение на подборку:', b.ev("getComputedStyle(document.querySelectorAll('.cat')[2]).transform"))
            b.shot(f'{OUT}/{name}_cats.png')
        # отбор: сканер и цифры
        go(b, '#scan'); time.sleep(4.5); b.shot(f'{OUT}/{name}_scan.png')
        log(f'[{name}] сканер:', b.ev("'off='+document.querySelectorAll('#sfield i.off').length+' act='+((document.querySelector('#clist li.act')||{}).textContent||'-')+' out='+document.getElementById('sOut').textContent"))
        go(b, '.stats2'); time.sleep(3.2); b.shot(f'{OUT}/{name}_stats.png')
        log(f'[{name}] цифры:', b.ev("[...document.querySelectorAll('.odo')].map(o=>[...o.querySelectorAll('.col')].map(c=>getComputedStyle(c).transform.split(',')[5]).join('|')).join(' ; ')+' dots='+document.querySelectorAll('.sd i.on').length"))
        # путь клиента
        go(b, '.way'); time.sleep(3)
        log(f'[{name}] путь клиента:', b.ev("'lit='+document.querySelectorAll('.way .stp.lit').length+' fill='+document.querySelectorAll('.way .ln.fill').length"))
        # ремонт
        go(b, '#baBox'); vals = []
        for _ in range(8):
            time.sleep(.35); vals.append(b.ev("Math.round(+document.getElementById('baR').value)"))
        b.shot(f'{OUT}/{name}_ba.png')
        log(f'[{name}] шторка до/после (сама):', vals, b.ev("'clip='+document.querySelector('#baBox .after').style.clipPath+' step='+((document.querySelector('#bSteps li.cur b')||{}).textContent)"))
        # кабинет
        go(b, '#devs'); time.sleep(2)
        if not mobile:
            d = b.ev("(()=>{const r=document.getElementById('devs').getBoundingClientRect();return [r.x+r.width*.8,r.y+r.height*.2]})()")
            b.mouse(*d); time.sleep(.5)
            log(f'[{name}] наклон устройств:', b.ev("document.getElementById('devs').style.getPropertyValue('--ry')+' '+document.getElementById('devs').style.getPropertyValue('--rx')"))
        b.shot(f'{OUT}/{name}_devs.png')
        log(f'[{name}] экраны устройств:', b.ev("[...document.querySelectorAll('.dvx iframe')].map(f=>{try{return f.contentDocument.getElementById('tName').textContent}catch(e){return 'нет доступа'}}).join(' | ')"))
        # договор
        go(b, '#desk'); time.sleep(4.5); b.shot(f'{OUT}/{name}_desk.png')
        log(f'[{name}] договор:', b.ev("(()=>{const d=document.getElementById('desk');return d.className+' ok='+d.querySelectorAll('.cl li.ok').length+' flap='+(d.querySelector('.flap')?getComputedStyle(d.querySelector('.flap')).transform:'-')+' paper='+getComputedStyle(d.querySelector('.paper')).transform+' sig='+getComputedStyle(d.querySelector('.sig')).strokeDashoffset+' seal='+getComputedStyle(d.querySelector('.seal')).opacity})()"))
        # подвал
        go(b, '.fbig'); time.sleep(1.5)
        log(f'[{name}] точка в «Ставим точку.»:', b.ev("getComputedStyle(document.querySelector('.fbig i.o')).transform+' prog end='+document.getElementById('prog').className"))
        b.shot(f'{OUT}/{name}_foot.png')
        log(f'[{name}] ошибки JS:', b.ev("window.__errs||'нет перехватчика'"))
    finally:
        b.close()


for name, w, h, m in (('d1440', 1440, 900, False), ('d1920', 1920, 1080, False), ('m390', 390, 844, True)):
    run(name, w, h, m)
open(os.path.join(OUT, 'anim_report.txt'), 'w', encoding='utf8').write('\n'.join(R))
