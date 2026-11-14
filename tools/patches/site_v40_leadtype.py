"""Сайт v40 — заявка: «На» не висит в конце строки (неразрывный пробел после коротких слов в подписи), точки меньше и тише;
на телефоне точки не заходят под текст — поле только в нижней части блока (за формой), мелкое и с мягким градиентом.
Run из корня репо после v39: py -3 tools/patches/site_v40_leadtype.py"""
import re
P = '08_Сайт_пример/'
s = open(P + 'index.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


# типографика: короткие слова (предлоги, союзы) привязаны к следующему слову
i = s.index('<section class="lead" id="lead">'); j = s.index('</p>', i)
seg = s[i:j]
seg2 = re.sub(r'(?<=[\s>(«])(На|на|в|и|с|к|у|о|а|по|за|от|до|из|не|мы|Мы|Или|или)\s', lambda m: m.group(1) + ' ', seg)
s = s[:i] + seg2 + s[j:]

rep('const step = W < 800 ? 24 : 28, mob = W < 800; pts = [];', 'const step = W < 800 ? 18 : 24, mob = W < 800; pts = [];')
rep('const g = mob ? ss(-.2, 1.2, (y / H) * .6 + (x / W) * .4) * .7 : ss(.32, .82, x / W);',
    'const g = mob ? ss(.5, .95, y / H) * (.55 + .45 * ss(0, 1, x / W)) : ss(.34, .86, x / W);')
rep('const a = Math.min(.95, .1 + .3 * g + w * .4 + .55 * k), rad = 1.4 + 3.4 * g + 3.2 * k;',
    'const a = Math.min(.9, .06 + .34 * g + w * .3 + .5 * k), rad = (W < 800 ? .6 + 1.6 * g : .9 + 2.5 * g) + 2.6 * k;')
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok', seg2.count(' ') - seg.count(' '))
