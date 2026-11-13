"""Отладка: выполнить JS-выражение на странице сайта и вывести результат. Run из корня репо:
py -3 -X utf8 tools/debug_js.py "<выражение JS>" [ширина] [query]"""
import os, re, subprocess, sys

SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '08_Сайт_пример')
EXPR = sys.argv[1]
W = sys.argv[2] if len(sys.argv) > 2 else '1440'
Q = sys.argv[3] if len(sys.argv) > 3 else ''
s = open(os.path.join(SITE, 'index.html'), encoding='utf8').read()
js = "<script>setTimeout(()=>{let r;try{r=String(" + EXPR + ")}catch(e){r='ERR '+e.message}document.body.setAttribute('data-r',r)},3000)</script>"
out = os.path.join(SITE, '_d.html')
open(out, 'w', encoding='utf8').write(s.replace('</body>', js + '</body>'))
C = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'
d = subprocess.run([C, '--headless=new', '--disable-gpu', '--user-data-dir=' + os.environ['TEMP'] + r'\pn_chrome_test', '--allow-file-access-from-files',
                    '--virtual-time-budget=6000', f'--window-size={W},900', '--dump-dom', 'file:///' + out.replace('\\', '/') + Q], capture_output=True, encoding='utf8').stdout
os.remove(out)
m = re.search(r'data-r="([^"]*)"', d or '')
print(m.group(1) if m else 'none')
