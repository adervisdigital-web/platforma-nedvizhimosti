"""Автотест интерактива сайта в headless Chrome: клики по поиску, фильтрам, сортировке, сравнению, телефону.
Run из корня репо: py -3 tools/test_site.py"""
import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, '08_Сайт_пример', 'index.html')
out = os.path.join(ROOT, '08_Сайт_пример', '_test.html')
s = open(src, encoding='utf8').read()
pre = '<script>try{localStorage.clear()}catch(e){};window.__e=[];addEventListener("error",e=>__e.push(e.message+" @"+e.lineno));</script>'
test = r'''<script>setTimeout(()=>{const $=q=>document.querySelector(q),$$=q=>[...document.querySelectorAll(q)];let R=[];try{
$$('.ib.cmp')[0].click();$$('.ib.cmp')[2].click();$$('.ib.fav')[1].click();
$$('.tabs button')[1].click();R.push('go(sec,1-2)='+$('#goN').textContent);$('#sf').requestSubmit();
R.push('cnt='+$('#cnt').textContent+' flt='+$('#fltT').textContent+' cards='+$$('.card').length);
$('#fltX').click();R.push('reset cards='+$$('.card').length+' more='+$('#moreBtn').textContent);
$$('.seg.sort button')[1].click();R.push('cheapest='+$('.card .price').textContent);
$$('.seg.view button')[1].click();R.push('sortStill='+$('.seg.sort [aria-pressed=true]').textContent);
$('#cmpBtn').click();R.push('dlg='+$('#dlg').open+' tr='+$$('.ctab tr').length);$('#dlg').close();
const lp=$('#lp');lp.value='89655002918';lp.dispatchEvent(new Event('input'));R.push('tel='+lp.value);
$$('.cat')[1].click();R.push('cat done='+$$('.card').length+' '+$('#fltT').textContent);
$$('button.mort')[0].click();R.push('calc='+$('#cpv').textContent);
if($('#qvFav')===null){$$('.card .qv')[0].click();R.push('quick='+$('#dlg').open+' '+$('#dlgT').textContent+' checks='+$$('.qvc span').length);$('#qvFav').click();$('#dlg').close();R.push('range--p='+$('#cp').style.getPropertyValue('--p'));}
if($('#hx')){R.push('houses='+$$('.hc').length);$$('#hfl button')[5].click();R.push('2fl='+$$('.hc:not([hidden])').length);$$('#hfl button')[0].click();
$$('[data-open]')[0].click();R.push('hdlg='+$('#dlg').open+' '+$('#dlgT').textContent+' thumbs='+$$('.hth button').length);$$('#plTabs button')[1].click();R.push('plan='+$('#plImg').getAttribute('src'));
$('#hvCalc').click();R.push('calc='+$('#hname').textContent+' area='+$('#ha').value+' pay='+$('#hpay').textContent);}
R.push('cmpCnt='+$('#cmpCnt').textContent+' fav='+$('#favCnt').textContent+' cats='+$$('[data-c]').map(e=>e.textContent).join('/'));
}catch(x){R.push('ERR '+x.message)}R.push('errors='+__e.join(';'));document.body.setAttribute('data-r',R.join(' || '))},600)</script>'''
open(out, 'w', encoding='utf8').write(s.replace('<head>', '<head>' + pre).replace('</body>', test + '</body>'))
C = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'
d = subprocess.run([C, '--headless=new', '--disable-gpu', '--user-data-dir=' + os.environ['TEMP'] + r'\pn_chrome_test', '--allow-file-access-from-files',
                    '--virtual-time-budget=5000', '--dump-dom', 'file:///' + out.replace('\\', '/')], capture_output=True, encoding='utf8').stdout
os.remove(out)
m = re.search(r'data-r="([^"]*)"', d or '')
print((m.group(1) if m else 'NO RESULT').replace('&quot;', '"').replace(' || ', '\n'))
