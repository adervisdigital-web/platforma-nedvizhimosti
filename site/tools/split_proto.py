"""Разборка прототипа 08_Сайт_пример/index.html (v40) на шаблоны PHP, CSS и JS. Повторяемо.
Run из корня репо: py -3 -X utf8 site/tools/split_proto.py
Пишет: site/public/assets/css/site.css, site/public/assets/js/NN-<тема>.js, site/app/templates/{head,top,header,overlays,footer}.php,
site/app/templates/sections/<id>.php, site/app/templates/scripts.json; копирует фото и kabinet.html.
Самопроверка: склейка кусков == исходник с известными заменами (photo/ → assets/img/, данные → PN.*)."""
import json, os, re, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, '08_Сайт_пример'); S = os.path.join(ROOT, 'site')
T = os.path.join(S, 'app', 'templates'); PUB = os.path.join(S, 'public')
src = open(os.path.join(P, 'index.html'), encoding='utf8').read()
TR = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя', ['a', 'b', 'v', 'g', 'd', 'e', 'yo', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']))
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', ''.join(TR.get(c, c) for c in s.lower())).strip('-')[:40]
img = lambda s: s.replace('photo/', 'assets/img/')


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf8', newline='\n').write(text)


def literal_end(code, i):
    """i — индекс '[' или '{'. Возвращает индекс после парной скобки (строки, шаблоны и регэкспы учтены)."""
    depth, n, prev = 0, len(code), ''
    while i < n:
        c = code[i]
        if c in '\'"`':
            q = c; i += 1
            while code[i] != q: i += 2 if code[i] == '\\' else 1
        elif c == '/' and prev in '[,(:':
            i += 1; cls = False
            while cls or code[i] != '/':
                if code[i] == '\\': i += 1
                elif code[i] == '[': cls = True
                elif code[i] == ']': cls = False
                i += 1
            while code[i + 1].isalpha(): i += 1
        elif c in '[{': depth += 1
        elif c in ']}':
            depth -= 1
            if depth == 0: return i + 1
        if not c.isspace(): prev = c
        i += 1
    raise ValueError('скобка не закрыта')


# --- head: стиль → файл, остальное в шаблон
head, body = src[:src.find('<body>')], src[src.find('<body>'):]
css = re.search(r'<style>(.*?)</style>', head, re.S).group(1)
write(os.path.join(PUB, 'assets', 'css', 'site.css'), css.replace('url(photo/', 'url(../img/').replace("url('photo/", "url('../img/").replace('url("photo/', 'url("../img/'))
head_t = head.replace(f'<style>{css}</style>', '<link rel="stylesheet" href="assets/css/site.css">')
head_t = head_t.replace('href="photo/', 'href="assets/img/').replace('<meta charset="utf-8">', '<meta charset="utf-8"><?= $base_tag ?? "" ?>', 1)
write(os.path.join(T, 'head.php'), head_t)

# --- body: верхнеуровневые элементы (строки с '<' в 1-й колонке)
starts = [m.start() for m in re.finditer(r'^<(?!/)[a-z]+', body, re.M)]
pieces = [body[a:b] for a, b in zip(starts, starts[1:] + [len(body)])]
tag = lambda p: re.match(r'<([a-z]+)([^>]*)', p).group(1, 2)
groups, order = {}, []
def add(name, text):
    if name not in groups: groups[name] = ''; order.append(name)
    groups[name] += text
for p in pieces:
    t, attrs = tag(p)
    m = re.search(r'id="([^"]+)"', attrs)
    if t == 'body' or (t in ('div', 'svg') and not groups.get('header')) or (t == 'script' and not groups.get('header')): add('top', p)
    elif t == 'header': add('header', p)
    elif t == 'main': add('main_open', p)
    elif t == 'section': add('sections/' + (m.group(1) if m else re.search(r'class="([a-z]+)', attrs).group(1)), p)
    elif t == 'footer': add('footer', p)
    elif t == 'script' and 'src=' in attrs: add('libs', p)
    elif t == 'script': add('app_script', p)
    else: add('overlays', p)
app = groups.pop('app_script'); order.remove('app_script')
assert app.startswith('<script>') and app.rstrip().endswith('</html>'), 'хвост с приложением не найден'
code = app[len('<script>'):app.rfind('</script>')]
tail = app[app.rfind('</script>') + len('</script>'):]

# --- данные прототипа → слой PN (задача 4)
REPL = {'ITEMS': 'PN.items()', 'HOUSES': 'PN.houses()', 'FAQ': 'PN.faq()', 'QUICK': 'PN.quick()', 'PROGS': 'PN.progs()', 'GEO': 'PN.geo()'}
for name, expr in REPL.items():
    m = re.search(rf'const {name} = ', code); a = m.end(); b = literal_end(code, a)
    code = code[:a] + expr + code[b:]

# --- JS: по комментариям-заголовкам, в исходном порядке
marks = [m.start() for m in re.finditer(r'^// [^\n]+', code, re.M) if not code[m.start():m.end()].startswith('// v')]   # только в 1-й колонке: внутри IIFE не режем
cut = [0] + [m for m in marks if m > 0] + [len(code)]
files = []
for k, (a, b) in enumerate(zip(cut, cut[1:])):
    chunk = code[a:b]
    if not chunk.strip(): continue
    first = re.match(r'// ([^\n]+)', chunk)
    name = f'{len(files):02d}-' + (slug(first.group(1)) if first and a > 0 else 'core') + '.js'
    write(os.path.join(S, 'src', 'js', name), img(chunk))
    files.append(name)
write(os.path.join(S, 'src', 'js', 'order.json'), json.dumps(files, ensure_ascii=False, indent=1))
assert ''.join(open(os.path.join(S, 'src', 'js', f), encoding='utf8').read() for f in files) == img(code), 'склейка JS не равна коду'

# --- шаблоны
for name in order:
    text = img(groups[name]).replace('href="photo/', 'href="assets/img/')
    if name == 'libs': continue
    write(os.path.join(T, name + '.php'), text)
write(os.path.join(T, 'libs.php'), groups['libs'])
write(os.path.join(T, 'tail.php'), tail)
write(os.path.join(T, 'order.json'), json.dumps([n for n in order if n != 'libs'], ensure_ascii=False))

# --- фото и демо-кабинет
js_dir = os.path.join(S, 'src', 'js')
for f in os.listdir(js_dir) if os.path.isdir(js_dir) else []:
    if f.endswith('.js') and f not in files: os.remove(os.path.join(js_dir, f))
dst = os.path.join(PUB, 'assets', 'img')
if os.path.isdir(dst): shutil.rmtree(dst)
shutil.copytree(os.path.join(P, 'photo'), dst)
write(os.path.join(PUB, 'kabinet.html'), open(os.path.join(P, 'kabinet.html'), encoding='utf8').read())

# --- самопроверка: обратная склейка == исходник с известными заменами
rebuilt = head + ''.join(groups[n] for n in order if n != 'libs') + groups['libs'] + app
assert rebuilt == src, 'склейка кусков не совпала с исходником'
print('шаблонов', len(order), '| js-файлов', len(files), '| css', len(css), 'символов')
