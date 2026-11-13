"""Отладка: какой элемент лежит в точках (x,y) блока сайта. Run из корня репо:
py -3 -X utf8 tools/debug_point.py <id секции> "x1,y1 x2,y2 ..." [ширина]"""
import os, re, subprocess, sys

SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '08_Сайт_пример')
ID, PTS = sys.argv[1], [tuple(map(int, p.split(','))) for p in sys.argv[2].split()]
W = sys.argv[3] if len(sys.argv) > 3 else '1440'
s = open(os.path.join(SITE, 'index.html'), encoding='utf8').read()
HIDE = f'<style>main>section:not(#{ID}),header,footer,.tabbar,.chatfab,.prog{{display:none!important}}</style>'
js = ('<script>setTimeout(()=>{const r=[];for(const [x,y] of ' + str([list(p) for p in PTS]) + '){const e=document.elementFromPoint(x,y);'
      "r.push(x+','+y+': '+(e?e.tagName+'.'+e.className+' bg='+getComputedStyle(e).backgroundColor+' parent='+e.parentElement.className+' size='+e.offsetWidth+'x'+e.offsetHeight:'-'))}"
      "for(const q of ['.devs','.stage','.mbp','.lid','.mbp .vp','.iph','.iph .vp','.base','.shadow']){const e=document.querySelector(q),b=e.getBoundingClientRect(),c=getComputedStyle(e);r.push(q+' '+[b.x,b.y,b.width,b.height].map(Math.round)+' bg='+c.backgroundColor+' rad='+c.borderRadius+' bs='+c.boxShadow.slice(0,40)+' out='+c.outlineStyle)}document.body.setAttribute('data-r',r.join(' | '))},800)</script>")
out = os.path.join(SITE, '_dbg.html')
open(out, 'w', encoding='utf8').write(s.replace('</head>', HIDE + '</head>').replace('</body>', js + '</body>'))
C = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'
d = subprocess.run([C, '--headless=new', '--disable-gpu', '--user-data-dir=' + os.environ['TEMP'] + r'\pn_chrome_test', '--allow-file-access-from-files',
                    '--virtual-time-budget=4000', f'--window-size={W},1000', '--dump-dom', 'file:///' + out.replace('\\', '/')], capture_output=True, encoding='utf8').stdout
os.remove(out)
m = re.search(r'data-r="([^"]*)"', d or '')
print((m.group(1) if m else 'none').replace(' | ', '\n'))
