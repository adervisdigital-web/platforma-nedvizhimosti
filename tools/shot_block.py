"""Скриншот одного блока сайта (прокрутка к #id + необязательный JS). Run из корня репо:
py -3 tools/shot_block.py <id> <папка_вывода> [js]  → <id>.png (1440×1000), <id>_w.png (1920×1080), <id>_m.png (телефон 390)"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, '08_Сайт_пример')
ID, OUT = sys.argv[1], sys.argv[2]
JS = sys.argv[3] if len(sys.argv) > 3 else ''
s = open(os.path.join(SITE, 'index.html'), encoding='utf8').read()
HIDE = f'<style>main>section:not(#{ID}),header,footer,.tabbar,.chatfab,.prog{{display:none!important}}</style>'
t = s.replace('</head>', HIDE + '</head>').replace('</body>', f'<script>setTimeout(()=>{{{JS}}},500)</script></body>')
pages = {'_blk.html': t, '_blkm.html': '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0}iframe{border:0;width:390px;height:1700px}</style></head><body><iframe src="_blk.html"></iframe></body></html>'}
for n, c in pages.items():
    open(os.path.join(SITE, n), 'w', encoding='utf8').write(c)
C = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'
for n, size, png in (('_blk.html', '1440,1000', ID + '.png'), ('_blk.html', '1920,1080', ID + '_w.png'), ('_blkm.html', '600,1700', ID + '_m.png')):
    subprocess.run([C, '--headless=new', '--disable-gpu', '--user-data-dir=' + os.environ['TEMP'] + r'\pn_chrome_test', '--hide-scrollbars',
                    '--allow-file-access-from-files', '--virtual-time-budget=5000', f'--window-size={size}', '--screenshot=' + os.path.join(OUT, png),
                    'file:///' + os.path.join(SITE, n).replace('\\', '/')], capture_output=True)
for n in pages:
    os.remove(os.path.join(SITE, n))
print('ok')
