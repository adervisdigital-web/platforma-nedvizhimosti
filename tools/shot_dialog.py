"""Скриншоты окна сравнения (ноутбук 1440×900 и телефон 390×844). Run из корня репо: py -3 tools/shot_dialog.py <папка_вывода>"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, '08_Сайт_пример')
OUT = sys.argv[1]
s = open(os.path.join(SITE, 'index.html'), encoding='utf8').read()
t = s.replace('<head>', '<head><script>try{localStorage.clear()}catch(e){}</script>').replace(
    '</body>', "<script>setTimeout(()=>{$$('.ib.cmp')[0].click();$$('.ib.cmp')[1].click();$$('.ib.cmp')[3].click();"
    + {'quick': "quick(ITEMS[1]);", 'house': "houseView(HOUSES[0]);"}.get(sys.argv[2] if len(sys.argv) > 2 else '', "showCmp();") + "},300)</script></body>")
pages = {'_dlg.html': t, '_dlgm.html': '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0}iframe{border:0;width:390px;height:844px}</style></head><body><iframe src="_dlg.html"></iframe></body></html>'}
for n, c in pages.items():
    open(os.path.join(SITE, n), 'w', encoding='utf8').write(c)
C = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'
for n, size, png in (('_dlg.html', '1440,900', 'dlg.png'), ('_dlgm.html', '600,844', 'dlgm.png')):
    subprocess.run([C, '--headless=new', '--disable-gpu', '--user-data-dir=' + os.environ['TEMP'] + r'\pn_chrome_test', '--hide-scrollbars',
                    '--allow-file-access-from-files', '--virtual-time-budget=5000', f'--window-size={size}', '--screenshot=' + os.path.join(OUT, png),
                    'file:///' + os.path.join(SITE, n).replace('\\', '/')], capture_output=True)
for n in pages:
    os.remove(os.path.join(SITE, n))
print('ok')
