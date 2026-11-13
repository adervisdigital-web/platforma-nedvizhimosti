"""HTML-страницы со знаками (чёрный на белом) для загрузки в изобразительный поиск. Run из корня репо."""
import os, sys
sys.path.insert(0, 'tools')
import p_mark_variants2 as V2
import p_mark_variants3 as V3
import p_mark_variants4 as V4
V = V2.V

T = os.path.join(os.environ['TEMP'], 'pn_be')
for k in (sys.argv[1:] or ['now', 'leg', 'base', 'line', 'frame']):
    s = V.svg(k, 420, '#000', '#000')
    with open(os.path.join(T, f'mk_{k}.html'), 'w', encoding='utf8') as f:
        f.write('<!doctype html><html><body style="margin:0;background:#fff;width:600px;height:600px;'
                f'display:flex;align-items:center;justify-content:center">{s}</body></html>')
print('ok')
