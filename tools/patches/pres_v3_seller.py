"""Презентация: модель «продаём мы — делают проверенные», новая обложка, масштаб на весь экран.
Run из корня репо: py -3 tools/patches/pres_v3_seller.py"""
p = 'tools/p_present.py'
s = open(p, encoding='utf8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


# обложка: консультант с ключами вместо прораба; фиксированная высота (масштаб даёт zoom)
rep('.cover{{height:clamp(640px,52vw,1200px);', '.cover{{height:780px;')
rep('.cover .l svg{{width:clamp(150px,10vw,260px);height:auto}}', '.cover .l svg{{width:150px;height:auto}}')
rep('.cover .r{{background:url(photo/worker.jpg) 50% 22%/cover;', '.cover .r{{background:url(photo/advisor.jpg) 50% 30%/cover;')
rep('aria-label="Прораб в красной каске"', 'aria-label="Консультант Платформы с ключами от квартиры"')

# на весь экран: вся страница масштабируется от базовой ширины 1440 (как изображения на Behance)
rep('<title>Платформа недвижимости — бренд</title>',
    '<title>Платформа недвижимости — бренд</title>\n'
    '<script>function fit(){{var w=innerWidth;document.documentElement.style.zoom=w>1440?w/1440:1}}fit();addEventListener("resize",fit)</script>')

# тексты: продаём мы — делают проверенные партнёры
rep('<span>Бригады, за которые мы ручаемся. Смета и сроки — до начала работ, приёмка каждого этапа.</span>',
    '<span>Ремонт у партнёров, за которых мы ручаемся. Смета и сроки — до начала работ, приёмка каждого этапа.</span>')
rep('<span>Каменные дома по готовым и индивидуальным проектам — от фундамента до ключей, руками проверенных строителей.</span>',
    '<span>Каменные дома от проверенных строителей-партнёров — по готовым и индивидуальным проектам.</span>')
rep("car('helmet', 'каска', 'c4', '50% 62%')", "car('helmet', 'каска инспектора', 'c4', '50% 62%')")
rep("car('vest', 'спецодежда', 'c4b', '62% 60%')", "car('vest', 'жилет инспектора', 'c4b', '62% 60%')")
rep("car('fence', 'ограждение стройки', 'c6', '50% 60%')", "car('fence', 'ограждение объекта партнёра', 'c6', '50% 60%')")
rep("'паспорт объекта'", "'паспорт объекта с отметкой о проверке'")
rep('Кладка стен · приёмка прораба', 'Кладка стен · проверено Платформой')

open(p, 'w', encoding='utf8').write(s)

# носители: забор и паспорт объекта — партнёрский объект, отметка о проверке
m = 'tools/mockups/p_mockups.py'
t = open(m, encoding='utf8').read()
for a, b in [('Здесь строится<br>каменный дом<span style="color:{INK}">.</span>', 'Этот дом<br>проверен<span style="color:{INK}">.</span>'),
             ("('Подрядчик', 'ПЛАТФОРМА НЕДВИЖИМОСТЬ')", "('Подрядчик', '[НАЗВАНИЕ]'), ('Проверено', 'ПЛАТФОРМА НЕДВИЖИМОСТЬ')")]:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
open(m, 'w', encoding='utf8').write(t)
print('ok')
