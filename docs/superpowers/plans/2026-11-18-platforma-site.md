# Рабочий сайт «Платформа недвижимости» — план реализации

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Цель:** превратить прототип `08_Сайт_пример/index.html` (v40) в сайт на PHP + SQLite: админка, приём заявок, страницы объектов. Плюс статическая сборка-витрина для GitHub Pages.

**Архитектура.** Один набор PHP-шаблонов работает в двух режимах:
- **на сервере** — данные из SQLite;
- **в `build.php`** — те же шаблоны рендерятся в статический HTML и JSON в `10_Сайт/`, `DEMO=1`.

Данные попадают на страницу встроенным JSON (`<script id="pn-data" type="application/json">`), его читает `assets/js/data.js`. Поэтому сайт не зависит от режима.

JS прототипа режется на классические `<script>` по разделам в исходном порядке. Верхнеуровневые `const/let/function` остаются общими, логику не переписываем.

**Стек:** PHP 8.3 (pdo_sqlite, gd, mbstring, curl, openssl), SQLite, ванильные JS и CSS. Leaflet 1.9.4 с unpkg — как в прототипе. Python 3 + headless Chrome — только для существующих проверок (`tools/cdp.py`, `test_site.py`, `check_anim.py`).

**Спецификация:** `docs/superpowers/specs/2026-11-18-platforma-site-design.md`

## Общие ограничения

**Стек и окружение:**
- PHP ≥ 8.2, без фреймворков и Composer-зависимостей, без Docker, Node и сборщиков.
- База — SQLite через PDO. DSN задаётся в `site/app/config.php`, переход на MySQL — сменой DSN.

**Данные и безопасность:**
- `site/data/*.sqlite`, `site/uploads/*` (кроме `.gitkeep`), заявки и токены — только в `.gitignore`. В `10_Сайт/` — никаких персональных данных.
- Прототип `08_Сайт_пример/` не меняется.
- Секреты (токен бота, SMTP) хранятся в `settings` в базе. Не в коде и не в JSON сборки.

**Витрина на GitHub:**
- Сборка — в `10_Сайт/`.
- В режиме DEMO: заявки не отправляются, ответ «принято (демо)», `<meta name="robots" content="noindex">`, `robots.txt` = `Disallow: /`.
- Все ссылки и пути в сборке относительные. Сайт открывается по адресу `…/platforma-nedvizhimosti/10_Сайт/`.

**Значения из спецификации:**
- Цены ремонта 20 000 / 45 000 / 80 000 ₽/м².
- Тёплый контур от 75 000 ₽/м².
- Телефон +7 965 500-29-18.
- Часы «на связи до 21:00».
- Лимит 5 заявок в час на IP.
- Форма не быстрее 3 с.
- Вход: пауза 15 минут после 5 неудачных попыток.
- Фото WebP 480/960/2000.

**Работа и проверка:**
- Тексты интерфейса — на русском, тон и формулировки как в v40.
- Поля ввода на мобильных ≥ 16 px.
- Перед «готово» по сайту — чек-лист из `AGENTS.md`: `test_site.py`, `check_anim.py`, `shot_mobile.py`, сравнение скриншотов.
- Коммиты локальные. `git push` — только с разрешения пользователя: публичный репозиторий, автоотправку блокирует система.

## На что смотреть при проверке

1. **Кириллица в адресах.** ЖК «Липовый сквер», дом «Северный Урал 235» → латинский slug: `zhk-lipovyy-skver`, `severnyy-ural-235`. Тест в задаче 6.
2. **Числа из админки с запятой и пробелами** («58,4», «9 450 000») сохраняются числами. Пустая цена — ошибка формы, не 0 ₽. Тест в задаче 10.
3. **Телефон в любом виде.**
   - «8 (965) 500-29-18», «+7 965 500 29 18», «9655002918» → `+79655002918`.
   - Короткий или иностранный номер — отказ с понятной ошибкой.
   - Тест в задаче 12.
4. **Загрузка фото.**
   - Огромное (8000 px, 15 МБ) уменьшается.
   - Повёрнутое по EXIF выправляется.
   - Не картинка (pdf, svg, heic, переименованный exe) отклоняется.
   - Тест в задаче 9.
5. **Сборка под подпапкой GitHub Pages.** В `10_Сайт/**/*.html` нет `href="/` и `src="/`. Страницы объектов открываются из подпапок. Тест в задаче 5.

---

## Этап 1. Разборка прототипа и витрина

### Задача 1: Окружение и каркас

**Файлы:**
- Create: `site/app/config.php`, `site/app/bootstrap.php`, `site/tests/run.php`, `site/tests/lib.php`, `site/.gitignore`, `site/README.md`, `site/router.php` (для `php -S`)
- Create dirs: `site/public/assets/{css,js,img}`, `site/app/templates/sections`, `site/data/seed`, `site/uploads` (с `.gitkeep`)

**Интерфейсы:**
- Создаёт:
  - `pn_config(): array` — ключи `dsn`, `demo` (bool), `base_url`, `root`;
  - `pn_t(string $name, callable $fn): void` и `pn_eq($a, $b, string $msg): void` — мини-раннер тестов;
  - `php site/tests/run.php` — запускает все `site/tests/*_test.php`, код выхода ≠ 0 при падении.

- [ ] **Шаг 1.** Спросить пользователя разрешение поставить PHP 8.3 portable (zip с windows.php.net) в `C:\tools\php`, с расширениями pdo_sqlite, gd, mbstring, curl, openssl в `php.ini`. Ожидание: `php -v` → `PHP 8.3.x`, `php -m` содержит `pdo_sqlite gd mbstring curl openssl`.
- [ ] **Шаг 2.** Тест `site/tests/smoke_test.php`: `pn_t('config', fn() => pn_eq(pn_config()['demo'], false, 'по умолчанию не демо'))`. Запуск `php site/tests/run.php` → FAIL (нет config).
- [ ] **Шаг 3.** Реализовать `config.php`, `bootstrap.php` (autoload `app/*.php`, `PN_DEMO` из env или аргумента), раннер. `.gitignore`: `data/*.sqlite`, `uploads/*`, `!uploads/.gitkeep`, `app/local.php`.
- [ ] **Шаг 4.** `php site/tests/run.php` → `1 passed`.
- [ ] **Шаг 5.** Коммит `site: каркас, конфиг, мини-раннер тестов`.

### Задача 2: Стартовые данные из прототипа

**Файлы:**
- Create: `site/tools/extract_seed.py` (через `tools/cdp.py`)
- Out: `site/data/seed/{apartments,complexes,houses,reviews,settings,faq,quick}.json`
- Test: `site/tests/seed_test.php`

**Интерфейсы:**
- Создаёт JSON-файлы seed. Поля — по таблицам из спецификации: `apartments` с `rooms, area, floor, floors, complex, district, price, discount_pct, finish, house_status, due, special, photos[], map_x, map_y`.
- Соответствие полям прототипа: `r→rooms`, `s→area`, `fl→floor`, `fls→floors`, `zk→complex`, `d→district`, `p→price`, `disc→discount_pct`, `fin→finish`, `st→house_status`, `due`, `special`, `img→photos[0]`, `x,y→map_x,map_y`.

- [ ] **Шаг 1.** Тест: в `apartments.json` 12 записей, в `houses.json` 5, у `houses[0]` `slug=='severnyy-ural-235'`, у каждой квартиры есть `price>0` и `photos[0]`, в `settings.json` есть `phone=='+7 965 500-29-18'`, `renovation_prices==[20000,45000,80000]`, `warm_contour_from==75000`.
- [ ] **Шаг 2.** Запуск → FAIL.
- [ ] **Шаг 3.** `extract_seed.py`:
  - открывает прототип в headless Chrome через `cdp.py`;
  - выполняет `JSON.stringify({ITEMS,HOUSES,FAQ:FAQ.map(([r,a])=>[r.source,r.flags,a]),QUICK})`;
  - мапит поля, отзывы и настройки берёт из DOM блока `#rev` и констант.
- [ ] **Шаг 4.** Тест → PASS.
- [ ] **Шаг 5.** Коммит.

### Задача 3: Разборка HTML/CSS/JS на шаблоны

**Файлы:**
- Create: `site/tools/split_proto.py` (одноразовый, повторяемый).
- Out:
  - `site/public/assets/css/site.css` — один файл, весь `<style>`;
  - `site/public/assets/js/{core,header,search,list,map,how,partners,calc,houses,ba,cab,rev,pact,lead,chat,loader}.js`;
  - `site/app/templates/layout.php`;
  - `site/app/templates/sections/{header,search,list,how,partners,calc,houses,ba,cab,rev,pact,lead,footer,dialogs}.php`.
- Copy: `08_Сайт_пример/photo/` → `site/public/assets/img/`.

**Интерфейсы:**
- Создаёт `pn_render(string $tpl, array $vars): string` в `app/view.php`. Шаблоны получают `$data` (массивы из seed или БД) и `$cfg`.

- [ ] **Шаг 1.** Тест `split_test.php`:
  - `pn_render('layout', [...seed])` содержит все 11 `id` секций прототипа (`search, list, how, partners, calc, houses, ba, cab, rev, pact, lead`);
  - содержит `<link rel="stylesheet" href="assets/css/site.css">`;
  - содержит 16 тегов `<script src="assets/js/...">` в порядке из списка выше.
- [ ] **Шаг 2.** → FAIL.
- [ ] **Шаг 3.** `split_proto.py`:
  - режет HTML по `<header>`, `<section id=…>`, `<footer>` и диалогам после подвала;
  - режет большой `<script>` по маркерам-комментариям разделов прототипа (`// ---` и `// v`) в исходном порядке;
  - массивы данных заменяет чтением из `PN` (задача 4): `const ITEMS = PN.items();` и т. п.;
  - пути `photo/` → `assets/img/`.
- [ ] **Шаг 4.** → PASS.
- [ ] **Шаг 5.** Коммит.

### Задача 4: Слой данных `data.js` и встраивание данных

**Файлы:**
- Create: `site/public/assets/js/data.js`, `site/app/data_static.php`
- Modify: `site/app/templates/layout.php`

**Интерфейсы:**
- Создаёт:
  - `pn_page_data(array $seedOrDb, array $cfg): array` — что встраивается в страницу;
  - в layout: `<script id="pn-data" type="application/json"><?= json(...) ?></script>`, подключается до всех скриптов.
- JS:
  - `window.PN = {items(), complexes(), houses(), reviews(), settings(), faq(), quick(), demo: bool, api: string}`;
  - `PN.items()` возвращает массив в форме прототипа (`r, s, fl, …`), так что код разделов не меняется;
  - `PN.settings().phone`, `.hours_to = '21:00'`, `.renovation_prices`.

- [ ] **Шаг 1.** Тест (PHP): `pn_page_data(seed)` → `items` длиной 12, первый элемент имеет ключи `r,s,fl,fls,zk,d,t,due,st,fin,p,img,x,y`, `demo` берётся из конфига.
- [ ] **Шаг 2.** → FAIL → реализовать `data_static.php` (seed → форма прототипа) и `data.js` (парсинг `#pn-data`, геттеры, `PN.demo`) → PASS.
- [ ] **Шаг 3.** Проверка в браузере: `php -S localhost:8080 site/router.php`. Страница открывается, в консоли 0 ошибок (через `tools/cdp.py`: `window.__e` пуст).
- [ ] **Шаг 4.** Коммит.

### Задача 5: Сборка `build.php` → `10_Сайт/` и проверка как у v40

**Файлы:**
- Create: `site/build.php`, `site/tests/build_test.php`, `site/tests/visual_compare.py`
- Modify: `tools/test_site.py`, `tools/check_anim.py`, `tools/shot_mobile.py` — добавить необязательный аргумент пути к странице (по умолчанию прототип, как сейчас).

**Интерфейсы:**
- Создаёт `php site/build.php [--out=10_Сайт] [--source=seed|db]`:
  - `index.html`, `kvartiry/<slug>/index.html` и `doma/<slug>/index.html` (после задачи 8);
  - `api/*.json`, `assets/`, `robots.txt`;
  - всегда `DEMO=1`.

- [ ] **Шаг 1.** Тест `build_test.php`:
  - после сборки в `10_Сайт/` есть `index.html`, `robots.txt` с `Disallow: /`, `index.html` содержит `noindex`;
  - ни в одном `.html` нет `href="/` и `src="/`;
  - нет файлов `*.sqlite`.
- [ ] **Шаг 2.** → FAIL → реализовать → PASS.
- [ ] **Шаг 3.** Формы в DEMO. В `lead.js` / `chat.js` / обратном звонке при `PN.demo` — поведение прототипа плюс подпись «демо», без запроса к API. Без DEMO — `fetch(PN.api + 'lead', …)`, подключается в задаче 12.
- [ ] **Шаг 4.** Проверки как у v40:
  - `py -3 -X utf8 tools/test_site.py 10_Сайт/index.html` → `errors=` пусто и те же строки результатов, что у прототипа;
  - `py -3 -X utf8 tools/check_anim.py <папка> 10_Сайт/index.html` — все анимации отрабатывают;
  - `py -3 site/tests/visual_compare.py` — скриншоты v40 и сборки на 1440/1920/390 с `?shot`, отличие ≤ 0,5 % пикселей. Иначе — лист расхождений для просмотра глазами.
- [ ] **Шаг 5.** Коммит. Показать пользователю ссылку на локальную сборку. Push — после его разрешения.

## Этап 2. База, API, страницы объектов

### Задача 6: Схема, миграции, seed, slug

**Файлы:**
- Create: `site/app/db.php`, `site/app/migrations/001_init.sql`, `site/app/slug.php`, `site/app/cli.php`
- Test: `site/tests/db_test.php`, `site/tests/slug_test.php`

**Интерфейсы:**
- Создаёт:
  - `pn_db(): PDO` (WAL, foreign_keys=ON, ERRMODE_EXCEPTION);
  - `pn_migrate(PDO): int` — число применённых миграций, таблица `migrations`;
  - `pn_slug(string): string` — транслитерация ГОСТ-подобная, нижний регистр, дефисы;
  - CLI: `php site/app/cli.php migrate|seed|user:add <login> <role>`.
- Таблицы и поля — ровно как в спецификации (`developers, complexes, apartments, houses, reviews, leads, settings, users, audit`). Ограничения:
  - `apartments.complex_id` — FK ON DELETE RESTRICT;
  - `slug` — UNIQUE;
  - `leads.status` CHECK IN (`'new','work','closed'`);
  - `users.role` CHECK IN (`'admin','manager'`).

- [ ] **Шаг 1.** Тесты:
  - `pn_slug('ЖК Липовый сквер')==='zhk-lipovyy-skver'`;
  - `pn_slug('Северный Урал 235')==='severnyy-ural-235'`;
  - `pn_slug('Ёлки, «Щука»!')==='yolki-shchuka'`;
  - на временной БД `migrate` → 1, повтор → 0;
  - `seed` даёт 12 квартир, 5 домов;
  - удалить ЖК с квартирами → `PDOException`.
- [ ] **Шаг 2.** → FAIL → реализовать → PASS.
- [ ] **Шаг 3.** Коммит.

### Задача 7: Репозитории и JSON API

**Файлы:**
- Create: `site/app/repo.php`, `site/public/api/index.php`
- Modify: `site/app/data_static.php` → `site/app/data.php` (единый источник: seed или БД)
- Test: `site/tests/api_test.php`

**Интерфейсы:**
- Создаёт:
  - `Repo::apartments(bool $onlyPublished=true): array`;
  - `Repo::apartment(string $slug): ?array`;
  - `Repo::complexes(): array`, `Repo::houses(): array`, `Repo::house(string $slug): ?array`;
  - `Repo::reviews(): array` — учитывает `settings.show_demo_reviews`;
  - `Repo::settings(): array` — без секретных ключей `tg_token`, `smtp_*`, `crm_*`;
  - `pn_page_data()` теперь берёт из `Repo`.
- API: `GET api/items`, `api/complexes`, `api/houses`, `api/reviews`, `api/settings` → JSON UTF-8. Неизвестный путь → 404 JSON `{"error":"not_found"}`.

- [ ] **Шаг 1.** Тесты:
  - снятая с публикации квартира не попадает в `api/items`;
  - при `show_demo_reviews=0` демо-отзывы скрыты;
  - в `api/settings` нет ключей, начинающихся с `tg_`, `smtp_`, `crm_`;
  - `build.php --source=db` выдаёт те же 12 карточек, что и из seed.
- [ ] **Шаг 2.** → FAIL → реализовать → PASS.
- [ ] **Шаг 3.** Коммит.

### Задача 8: Страницы квартир и домов, SEO

**Файлы:**
- Create:
  - `site/app/router.php`, `site/public/index.php` (фронт-контроллер), `site/public/.htaccess` (rewrite на index.php);
  - `site/app/templates/{apartment,house,privacy,404}.php`, `site/app/seo.php`.
- Modify: `site/router.php` (dev), `site/build.php` (рендер страниц объектов, `sitemap.xml` только для не-DEMO).
- Test: `site/tests/pages_test.php`

**Интерфейсы:**
- Маршруты: `/`, `/kvartiry/{id}-{slug}/`, `/doma/{slug}/`, `/privacy/`, `/sitemap.xml`, `/robots.txt`, `/api/*`, `/admin/*`.
- `seo_meta(array $page): string`: title, description, canonical, OG.
- `seo_jsonld(array $page): string`: Organization, Product + Offer (цена, RUB), BreadcrumbList.
- Страница квартиры: фото с `srcset`, параметры, «что проверили» по ЖК, платёж в ипотеку (как в быстром просмотре), кнопки «Позвонить» и «Записаться на просмотр».
- Быстрый просмотр на главной получает ссылку «Открыть страницу».

- [ ] **Шаг 1.** Тесты:
  - `/kvartiry/1-zhk-lipovyy-skver/` → 200, `<title>` содержит «2-комн.», «58,4 м²» и «Липовый сквер», есть `"@type":"Offer"` с `"priceCurrency":"RUB"`;
  - `/doma/severnyy-ural-235/` → 200;
  - несуществующий slug → 404;
  - в DEMO в `<head>` есть `noindex`, без DEMO — `sitemap.xml` содержит 12 + 5 + 1 адресов.
- [ ] **Шаг 2.** → FAIL → реализовать → PASS.
- [ ] **Шаг 3.** Пересобрать `10_Сайт/`, повторить проверки задачи 5. Страницы объектов открываются из подпапок, ссылки относительные.
- [ ] **Шаг 4.** Коммит.

### Задача 9: Фото — WebP трёх размеров

**Файлы:**
- Create: `site/app/images.php`
- Test: `site/tests/images_test.php` (фикстуры в `site/tests/fixtures/`: большой jpg 8000×6000, jpg с EXIF orientation=6, pdf, svg, текст с расширением .jpg)

**Интерфейсы:**
- Создаёт:
  - `pn_image_store(string $tmpPath, string $origName): array` → `['id'=>..., 'w480'=>..., 'w960'=>..., 'w2000'=>...]`. Пути относительно `uploads/`, при ошибке — `InvalidArgumentException` с русским текстом;
  - `pn_srcset(array $img): string`.
- Правила:
  - принимаем только jpeg/png/webp по `finfo`;
  - EXIF-поворот;
  - пересохраняем через GD (метаданные удаляются);
  - max 2000 по длинной стороне;
  - входной файл до 25 МБ.
- `cli.php seed` прогоняет фото прототипа через `pn_image_store`.

- [ ] **Шаг 1.** Тесты:
  - 8000×6000 → `w2000` шириной 2000;
  - EXIF=6 → результат портретный;
  - pdf/svg/«фальшивый jpg» → исключение «Можно загружать только JPG, PNG или WebP»;
  - `pn_srcset` содержит `480w, 960w, 2000w`.
- [ ] **Шаг 2.** → FAIL → реализовать → PASS.
- [ ] **Шаг 3.** Шаблоны карточек и страниц переходят на `srcset` + `loading="lazy"`.
- [ ] **Шаг 4.** Коммит.

## Этап 3. Админка

### Задача 10: Вход, роли, CSRF, журнал

**Файлы:**
- Create: `site/app/auth.php`, `site/app/csrf.php`, `site/app/audit.php`, `site/admin/{index,login,logout}.php`, `site/app/templates/admin/{layout,login}.php`, `site/public/assets/css/admin.css`
- Test: `site/tests/auth_test.php`

**Интерфейсы:**
- Создаёт:
  - `Auth::login(string $login, string $pass): bool`;
  - `Auth::user(): ?array`, `Auth::require(string $role='manager'): void` — без входа 302 на `/admin/login`, при недостатке роли 403;
  - `csrf_field(): string`, `csrf_check(): void` — 403 при неверном токене;
  - `audit(string $action, string $entity, int $id, array $diff): void`.
- Сессия: HttpOnly, SameSite=Lax, Secure при HTTPS.
- Блокировка: 5 неудачных попыток для логина или IP → 15 минут, сообщение «Слишком много попыток, попробуйте через 15 минут».

- [ ] **Шаг 1.** Тесты:
  - верный пароль → true;
  - 5 неверных → 6-я попытка с верным паролем false до истечения 15 минут (часы подменяются через `pn_now()`);
  - POST без CSRF → 403;
  - `/admin/` без входа → 302;
  - manager на `/admin/users` → 403.
- [ ] **Шаг 2.** → FAIL → реализовать → PASS.
- [ ] **Шаг 3.** Коммит.

### Задача 11: Разделы админки

**Файлы:**
- Create:
  - `site/admin/{apartments,complexes,developers,houses,reviews,settings,users}.php`;
  - `site/app/forms.php` (разбор и проверка полей);
  - `site/app/templates/admin/{list,form}.php`;
  - `site/public/assets/js/admin.js` — фото перетаскиванием, сортировка фото.
- Test: `site/tests/admin_test.php`

**Интерфейсы:**
- Создаёт:
  - `forms_number(string $raw): ?float` — «58,4» → 58.4, «9 450 000» → 9450000, «» → null;
  - `forms_apartment(array $post): array{data: array, errors: array}`.
- Обязательные поля квартиры: комнаты, площадь, этаж, этажей, ЖК, цена > 0, хотя бы одно фото для публикации.
- Квартиры: список с поиском и фильтром (ЖК, комнаты, опубликована), форма, «опубликовать / снять», «копировать» (копия неопубликованная, slug с `-2`).
- ЖК: 4 пункта проверки.
- Дома: особенности, тексты, фото, планировки по этажам.
- Настройки: телефон, часы, реквизиты, ставки, цены ремонта, тёплый контур, `tg_token`, `tg_chat_id`, почта, SMTP, `crm_enabled`, `crm_url`, флаги `demo_data` и `show_demo_reviews`.
- Пользователи — только admin.
- Каждое изменение пишется в `audit`.

- [ ] **Шаг 1.** Тесты:
  - `forms_number('58,4')===58.4`, `forms_number('9 450 000')===9450000.0`, `forms_number('')===null`;
  - квартира без цены → ошибка «Укажите цену»;
  - сохранённая через форму квартира появляется в `api/items`, её страница отвечает 200;
  - «копировать» → копия с `published=0`;
  - изменение пишет строку в `audit`.
- [ ] **Шаг 2.** → FAIL → реализовать → PASS.
- [ ] **Шаг 3.** Глазами: админка на 1440 и 390 px (`tools/shot_block.py`-подобный снимок), поля ≥ 16 px на телефоне.
- [ ] **Шаг 4.** Коммит.

## Этап 4. Заявки

### Задача 12: Приём заявки

**Файлы:**
- Create: `site/app/leads/accept.php`, `site/app/phone.php`, маршрут `POST api/lead`
- Modify: `lead.js`, `chat.js`, `header.js` (обратный звонок), `list.js` / `houses.js` (запись на просмотр) — без DEMO отправлять `fetch(PN.api+'lead', {method:'POST', body: JSON})`.
- Test: `site/tests/lead_test.php`

**Интерфейсы:**
- Создаёт:
  - `phone_norm(string): ?string`;
  - `lead_accept(array $in, string $ip, int $now): array{ok: bool, id?: int, error?: string}`.
- Поля входа: `kind` (`quiz|callback|viewing|chat`), `want`, `budget`, `area`, `name`, `phone`, `object_ref`, `slot`, `consent`, `hp` (ловушка), `t0` (время открытия формы).
- Сохранение — до любой отправки. `ip_hash = sha256(ip . settings.salt)`.
- Ответ: `{"ok":true,"message":"Заявка принята, перезвоним до 21:00"}`. Для `viewing` ещё `ics` — текст файла, как в прототипе.

- [ ] **Шаг 1.** Тесты:
  - `phone_norm('8 (965) 500-29-18')==='+79655002918'`, `phone_norm('+7 965 500 29 18')==='+79655002918'`, `phone_norm('9655002918')==='+79655002918'`;
  - `phone_norm('12345')===null`, `phone_norm('+44 20 7946 0958')===null`;
  - без `consent` → `error=='consent'`;
  - `hp` не пусто → `ok=false`, в базе пусто;
  - `now - t0 < 3` → отказ;
  - 6-я заявка за час с одного IP → `error=='rate'`;
  - валидная → строка в `leads` со `status='new'`, `delivered_tg=0`.
- [ ] **Шаг 2.** → FAIL → реализовать → PASS.
- [ ] **Шаг 3.** Коммит.

### Задача 13: Доставка — Telegram, почта, CRM, повтор; заявки в админке

**Файлы:**
- Create:
  - `site/app/leads/{deliver,telegram,mail,crm}.php`;
  - `site/admin/leads.php` (первый экран админки);
  - `site/app/templates/admin/leads.php`.
- Test: `site/tests/deliver_test.php` (HTTP-клиент и почта подменяются через `pn_http()` / `pn_mail()`)

**Интерфейсы:**
- Создаёт:
  - `interface LeadChannel { public function send(array $lead): bool; }`;
  - `TelegramChannel`, `MailChannel` (`mail()` или SMTP по настройкам), `CrmChannel` (по умолчанию выключен, `send` → true, если `crm_enabled=0`);
  - `deliver_lead(int $id): array` — по каналам, ставит флаги `delivered_*` и `attempts++`;
  - `deliver_pending(int $limit=20): int`.
- Где вызывается:
  - `lead_accept` сразу после сохранения;
  - `deliver_pending` — при входе менеджера в админку и в `php cli.php leads:retry` (для cron).
- Текст в Telegram: «Новая заявка · {kind} · {want} · {budget} · {phone} · {ссылка на объект}».
- Заявки в админке:
  - новые сверху, кликабельный `tel:`;
  - статус, заметка, фильтр;
  - CSV в UTF-8 с BOM, разделитель `;`;
  - метка «не доставлена», если какой-то канал не отправил.

- [ ] **Шаг 1.** Тесты:
  - Telegram отвечает 500 → `delivered_tg=0`, `attempts=1`, `deliver_pending` повторяет, после успеха `delivered_tg=1`;
  - `crm_enabled=0` → CRM не вызывается;
  - CSV открывается как UTF-8 (первые байты — BOM) и содержит телефон.
- [ ] **Шаг 2.** → FAIL → реализовать → PASS.
- [ ] **Шаг 3.** Ручная проверка на тестовом боте пользователя. Токен и chat_id даёт пользователь, хранятся только в базе.
- [ ] **Шаг 4.** Коммит.

## Этап 5. Финиш

### Задача 14: Полная проверка, политика, переезд

**Файлы:**
- Create: `docs/ПЕРЕЕЗД_REG_RU.md`, `site/app/templates/privacy.php` (заглушка: «Текст политики будет добавлен», ссылка из всех форм)
- Modify: `AGENTS.md` (журнал решений, команды запуска и сборки), `index.html` проекта (карточка «Рабочий сайт» → `10_Сайт/`)

**`docs/ПЕРЕЕЗД_REG_RU.md` включает:**
- тариф: PHP ≥ 8.2 с pdo_sqlite, gd, mbstring, curl;
- загрузку `site/` и корень сайта = `site/public`;
- права на запись для `site/data` и `site/uploads`;
- HTTPS (Let's Encrypt в панели Reg.ru);
- cron `*/10 * * * * php site/app/cli.php leads:retry`;
- `cli.php migrate && seed`, `cli.php user:add`;
- бота и почту в настройках;
- снятие DEMO;
- проверку по списку.

- [ ] **Шаг 1.** `php site/tests/run.php` → всё зелёное.
- [ ] **Шаг 2.** Пересобрать `10_Сайт/`.
- [ ] **Шаг 3.** Чек-лист из `AGENTS.md`: `test_site.py`, `check_anim.py` на 1440/1920/390, `shot_mobile.py`, `visual_compare.py`. Результаты — в отчёт, с честным списком того, что не удалось проверить.
- [ ] **Шаг 4.** Поиск по `10_Сайт/`: нет `+7 9…` кроме телефона компании, нет `tg_token`, `.sqlite`, `uploads/` с клиентскими файлами.
- [ ] **Шаг 5.** Коммит.
- [ ] **Шаг 6.** Спросить пользователя разрешение на `git push`. После push — проверить живую страницу `…/platforma-nedvizhimosti/10_Сайт/`.
