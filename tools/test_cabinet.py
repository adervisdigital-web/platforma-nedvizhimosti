"""Автотест демо-кабинета (08_Сайт_пример/kabinet.html) в headless Chrome: вход, подпись акта, объекты, камеры, платежи, чат.
Run из корня репо: py -3 -X utf8 tools/test_cabinet.py"""
import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, '08_Сайт_пример', 'kabinet.html')
out = os.path.join(ROOT, '08_Сайт_пример', '_test_cab.html')
s = open(src, encoding='utf8').read()
pre = '<script>try{sessionStorage.clear()}catch(e){};window.__e=[];addEventListener("error",e=>__e.push(e.message+" @"+e.lineno));</script>'
test = r'''<script>setTimeout(()=>{const $=q=>document.querySelector(q),$$=q=>[...document.querySelectorAll(q)];let R=[];try{
const ph=$('#ph');ph.value='9655002918';ph.dispatchEvent(new Event('input'));$('#lform').requestSubmit();R.push('phone='+ph.value+' codeShown='+!$('#fCode').hidden);
$('#code').value='12';$('#lform').requestSubmit();R.push('badCode='+$('#fCode').classList.contains('bad'));
$('#code').value='1234';$('#lform').requestSubmit();R.push('app='+!$('#app').hidden+' title='+$('#tName').textContent+' badge='+($('.snav .bd')||{}).textContent);
$('[data-v=home] [data-sign]').click();R.push('dlg='+$('#dlg').open+' '+$('#dlgT').textContent);$('#sms').value='5555';$('#doSign').click();
R.push('signed: stage='+$('[data-v=home] h3').textContent+' badge='+(($('.snav .bd')||{}).textContent||'нет')+' feed='+$('.feed li').textContent);
$$('[data-go=cams]')[0].click();R.push('view='+$('.view.on').dataset.v);$$('[data-cam]')[1].click();R.push('cam2='+$('.view.on .cn').textContent);$$('[data-day]')[2].click();R.push('arch='+$('.view.on .live').textContent);
$$('.snav [data-go=pay]')[0].click();R.push('pay='+$('.view.on .big').textContent.trim()+' rows='+$$('.sch tr').length);
$$('.snav [data-go=docs]')[0].click();$$('[data-d]')[2].click();R.push('plan dlg='+$('#dlg').open+' '+$('#dlgT').textContent);$('#dlg').close();
$$('.snav [data-go=chat]')[0].click();$('#cin').value='Когда следующий этап?';$('#cf').requestSubmit();R.push('msgs='+$$('.m').length);
$$('[data-obj=reno]')[0].click();R.push('reno='+$('#tName').textContent+' view='+$('.view.on').dataset.v);
}catch(x){R.push('ERR '+x.message)}setTimeout(()=>{R.push('reply='+($$('.m').slice(-1)[0]||{}).textContent);R.push('errors='+__e.join(';'));document.body.setAttribute('data-r',R.join(' || '))},1200)},500)</script>'''
open(out, 'w', encoding='utf8').write(s.replace('<head>', '<head>' + pre).replace('</body>', test + '</body>'))
C = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'
d = subprocess.run([C, '--headless=new', '--disable-gpu', '--user-data-dir=' + os.environ['TEMP'] + r'\pn_chrome_test', '--allow-file-access-from-files',
                    '--virtual-time-budget=6000', '--dump-dom', 'file:///' + out.replace('\\', '/')], capture_output=True, encoding='utf8').stdout
os.remove(out)
m = re.search(r'data-r="([^"]*)"', d or '')
print((m.group(1) if m else 'NO RESULT').replace('&quot;', '"').replace(' || ', '\n'))
