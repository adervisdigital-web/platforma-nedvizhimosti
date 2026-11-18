"""Формы на живом сервере (не демо): «принято» показывается только после ответа сервера; маска не делает из иностранного номера +7.
Run: сервер `php -S 127.0.0.1:8080 -t site/public site/router.php`, затем py -3 -X utf8 site/tests/js_lead_check.py → «ИТОГ: ok» или список ошибок."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'tools'))
from cdp import Browser
b = Browser()
b.call('Page.addScriptToEvaluateOnNewDocument', source='window.__e=[];addEventListener("error",e=>__e.push(e.message));'
       # сервер «отказывает» с 429 — подменяем fetch для api/lead
       'const _f=window.fetch;window.fetch=(u,o)=>String(u).includes("api/lead")?Promise.resolve(new Response(JSON.stringify({ok:false,error:"rate",message:"Слишком много заявок подряд — позвоните нам"}),{status:429})):_f(u,o);')
b.open('http://127.0.0.1:8080/?shot', wait=4)
r = json.loads(b.ev("""(async()=>{const $=q=>document.querySelector(q), out={};
 $('#qNext').click(); $('#qNext').click();
 const lp=$('#lp'); lp.value='89655002918'; lp.dispatchEvent(new Event('input')); $('#lc').checked=true;
 $('#leadForm').requestSubmit(); await new Promise(r=>setTimeout(r,2200));
 out.quizSentAfter429 = $('#leadForm').classList.contains('sent'); out.toast = ($('#toast')||{}).textContent;
 lp.value='+49 151 23456789'; lp.dispatchEvent(new Event('input')); out.foreignMasked = lp.value;
 $('#leadForm').requestSubmit(); out.foreignBad = lp.closest('.f').classList.contains('bad');
 out.err = window.__e; return JSON.stringify(out);})()"""))
b.close()
print(r)
bad = []
if r['quizSentAfter429']: bad.append('после отказа сервера форма показала «принято»')
if 'Слишком много' not in (r['toast'] or ''): bad.append('нет сообщения об отказе: ' + str(r['toast']))
if r['foreignMasked'].startswith('+7'): bad.append('маска превратила иностранный номер в ' + r['foreignMasked'])
if not r['foreignBad']: bad.append('иностранный номер не помечен ошибкой')
if r['err']: bad.append('ошибки JS: ' + '; '.join(r['err']))
print('ИТОГ:', 'ok' if not bad else 'ОШИБКИ — ' + ' | '.join(bad))
