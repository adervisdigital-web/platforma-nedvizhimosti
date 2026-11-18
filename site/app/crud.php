<?php
// Разделы админки на общем механизме: список с поиском, форма, сохранение, удаление, публикация, копия.
function pn_entities(): array {
    static $cache = null;
    if ($cache !== null && empty($GLOBALS['PN_ENT_RESET'])) return $cache;
    $GLOBALS['PN_ENT_RESET'] = false;
    $complexes = fn() => array_column(pn_db()->query('select id, name from complexes order by name')->fetchAll(), 'name', 'id');
    $developers = fn() => array_column(pn_db()->query('select id, name from developers order by name')->fetchAll(), 'name', 'id');
    return $cache = [
        'apartments' => ['title' => 'Квартиры', 'one' => 'квартира', 'table' => 'apartments', 'publish' => true, 'copy' => true,
            'search' => ['a.address', 'c.name', 'a.district'],
            'list_sql' => 'select a.*, c.name as complex from apartments a left join complexes c on c.id = a.complex_id',
            'cols' => ['id' => '№', 'complex' => 'ЖК / адрес', 'rooms' => 'Комн.', 'area' => 'м²', 'price' => 'Цена', 'published' => 'На сайте'],
            'fields' => [
                'market' => ['label' => 'Рынок', 'type' => 'select', 'req' => true, 'opts' => ['new' => 'Новостройка', 'secondary' => 'Вторичка']],
                'complex_id' => ['label' => 'ЖК', 'type' => 'select', 'opts' => $complexes()],
                'address' => ['label' => 'Адрес (для вторички)', 'type' => 'text'],
                'district' => ['label' => 'Район (если не как у ЖК)', 'type' => 'text'],
                'rooms' => ['label' => 'Комнат (0 — студия)', 'type' => 'int', 'req' => true, 'min' => 0, 'max' => 9],
                'area' => ['label' => 'Площадь, м²', 'type' => 'number', 'req' => 'Укажите площадь', 'min' => 5, 'max' => 1000],
                'floor' => ['label' => 'Этаж', 'type' => 'int', 'req' => true, 'min' => -2, 'max' => 120],
                'floors' => ['label' => 'Этажей в доме', 'type' => 'int', 'req' => true, 'min' => 1, 'max' => 120],
                'price' => ['label' => 'Цена, ₽', 'type' => 'number', 'req' => 'Укажите цену', 'min' => 1],
                'discount_pct' => ['label' => 'Скидка, %', 'type' => 'int', 'min' => 0, 'max' => 90],
                'finish' => ['label' => 'Отделка', 'type' => 'select', 'req' => true, 'opts' => ['with' => 'С отделкой', 'without' => 'Без отделки']],
                'finish_label' => ['label' => 'Подпись отделки (необязательно)', 'type' => 'text'],
                'house_status' => ['label' => 'Статус дома', 'type' => 'text', 'req' => true, 'hint' => 'Например: «Дом сдан» или «Сдача — II кв. 2027»'],
                'due' => ['label' => 'Срок сдачи ГГГГММ (0 — сдан)', 'type' => 'int', 'min' => 0, 'max' => 209912],
                'special' => ['label' => 'Спецпредложение', 'type' => 'bool'],
                'description' => ['label' => 'Описание', 'type' => 'textarea', 'wide' => true],
                'photos' => ['label' => 'Фото (первое — обложка)', 'type' => 'photos', 'wide' => true],
                'published' => ['label' => 'Опубликовать на сайте', 'type' => 'bool'],
            ]],
        'complexes' => ['title' => 'ЖК', 'one' => 'ЖК', 'table' => 'complexes', 'search' => ['c.name', 'c.district'],
            'list_sql' => 'select c.*, d.name as developer from complexes c left join developers d on d.id = c.developer_id',
            'cols' => ['name' => 'Название', 'district' => 'Район', 'developer' => 'Застройщик'],
            'used_by' => ['apartments', 'complex_id', 'В этом ЖК есть квартиры — сначала перенесите или удалите их'],
            'fields' => [
                'name' => ['label' => 'Название', 'type' => 'text', 'req' => true],
                'district' => ['label' => 'Район', 'type' => 'text', 'req' => true],
                'developer_id' => ['label' => 'Застройщик', 'type' => 'select', 'opts' => $developers()],
                'address' => ['label' => 'Адрес', 'type' => 'text'],
                'lat' => ['label' => 'Широта', 'type' => 'number'], 'lng' => ['label' => 'Долгота', 'type' => 'number'],
                'checks' => ['label' => 'Что проверили (по строке)', 'type' => 'lines', 'wide' => true],
                'photos' => ['label' => 'Фото', 'type' => 'photos', 'wide' => true],
            ]],
        'developers' => ['title' => 'Застройщики', 'one' => 'застройщик', 'table' => 'developers', 'search' => ['d.name'],
            'list_sql' => 'select d.* from developers d', 'cols' => ['name' => 'Название', 'site' => 'Сайт', 'verified' => 'Проверен'],
            'fields' => [
                'name' => ['label' => 'Название', 'type' => 'text', 'req' => true], 'site' => ['label' => 'Сайт', 'type' => 'text'],
                'verified' => ['label' => 'Проверен', 'type' => 'bool'],
            ]],
        'houses' => ['title' => 'Дома', 'one' => 'проект дома', 'table' => 'houses', 'publish' => true, 'search' => ['h.line', 'h.motto'],
            'list_sql' => 'select h.* from houses h', 'order' => 'sort, id',
            'cols' => ['line' => 'Линейка', 'number' => 'Номер', 'area' => 'м²', 'published' => 'На сайте'],
            'fields' => [
                'line' => ['label' => 'Линейка', 'type' => 'text', 'req' => true, 'hint' => 'Северный Урал / Южный Урал / Средний Урал'],
                'number' => ['label' => 'Номер (обычно = площадь)', 'type' => 'int', 'req' => true, 'min' => 1],
                'area' => ['label' => 'Площадь, м²', 'type' => 'number', 'min' => 10],
                'motto' => ['label' => 'Девиз', 'type' => 'text'], 'color' => ['label' => 'Цвет линейки (#HEX)', 'type' => 'text'],
                'floors' => ['label' => 'Этажей', 'type' => 'int', 'min' => 1, 'max' => 4], 'rooms' => ['label' => 'Комнаты', 'type' => 'text'],
                'ceiling' => ['label' => 'Потолки', 'type' => 'text'], 'price_from' => ['label' => 'Цена от, ₽', 'type' => 'number', 'min' => 1],
                'sort' => ['label' => 'Порядок показа', 'type' => 'int'],
                'features' => ['label' => 'Особенности (по строке)', 'type' => 'lines', 'wide' => true],
                'idea' => ['label' => 'Идея', 'type' => 'textarea', 'wide' => true],
                'text' => ['label' => 'Текст (абзацы через пустую строку)', 'type' => 'paras', 'wide' => true],
                'photos' => ['label' => 'Фото', 'type' => 'photos', 'wide' => true],
                'plans' => ['label' => 'Планировки: «подпись | фото» по строке', 'type' => 'pairs', 'wide' => true,
                    'hint' => 'Фото планировки сначала загрузите в «Фото», затем перенесите его имя сюда и удалите из фото'],
                'published' => ['label' => 'Опубликовать на сайте', 'type' => 'bool'],
            ]],
        'reviews' => ['title' => 'Отзывы', 'one' => 'отзыв', 'table' => 'reviews', 'publish' => true, 'search' => ['r.name', 'r.text'],
            'list_sql' => 'select r.* from reviews r', 'order' => 'sort, id',
            'cols' => ['name' => 'Имя', 'about' => 'О чём', 'is_demo' => 'Демо', 'published' => 'На сайте'],
            'fields' => [
                'name' => ['label' => 'Имя', 'type' => 'text', 'req' => true], 'about' => ['label' => 'Подпись (что купили)', 'type' => 'text'],
                'tag' => ['label' => 'Метка на фото', 'type' => 'select', 'opts' => ['Новостройка' => 'Новостройка', 'Вторичка' => 'Вторичка', 'Ремонт' => 'Ремонт', 'Дом' => 'Дом']],
                'topic' => ['label' => 'Тема', 'type' => 'select', 'opts' => ['apartment' => 'Квартира', 'house' => 'Дом', 'renovation' => 'Ремонт']],
                'rating' => ['label' => 'Оценка', 'type' => 'int', 'min' => 1, 'max' => 5], 'sort' => ['label' => 'Порядок', 'type' => 'int'],
                'text' => ['label' => 'Текст отзыва', 'type' => 'textarea', 'req' => true, 'wide' => true],
                'photo' => ['label' => 'Фото (имя)', 'type' => 'text'],
                'is_demo' => ['label' => 'Демо-отзыв (на боевом сайте скрыт)', 'type' => 'bool'], 'published' => ['label' => 'Показывать', 'type' => 'bool'],
            ]],
    ];
}

function pn_crud_row(string $table, int $id): ?array {
    $st = pn_db()->prepare("select * from $table where id = ?"); $st->execute([$id]); return $st->fetch() ?: null;
}
// Строка из базы → значения для формы (JSON-поля разворачиваются в текст).
function pn_crud_formvals(array $fields, array $row): array {
    $v = [];
    foreach ($fields as $n => $f) {
        $x = $row[$n] ?? null;
        $dec = is_string($x) && in_array($f['type'], ['lines', 'paras', 'pairs', 'photos'], true) ? (json_decode($x, true) ?? []) : $x;
        $v[$n] = match ($f['type']) {
            'lines' => implode("\n", (array) $dec), 'paras' => implode("\n\n", (array) $dec),
            'pairs' => implode("\n", array_map(fn($p) => implode(' | ', (array) $p), (array) $dec)), 'photos' => (array) $dec,
            'number' => $x === null ? '' : (abs((float) $x) >= 10000 ? number_format((float) $x, 0, ',', ' ') : str_replace('.', ',', (string) pn_num($x))), default => $x ?? '',
        };
    }
    return $v;
}
function pn_crud_dbvals(array $fields, array $data): array {
    $o = [];
    foreach ($data as $n => $v) $o[$n] = in_array($fields[$n]['type'] ?? '', ['lines', 'paras', 'pairs', 'photos'], true) ? pn_json_enc($v) : $v;
    return $o;
}

// Служебные поля при сохранении: slug, code, updated_at.
function pn_crud_derive(string $ent, array $d, ?int $id): array {
    $db = pn_db();
    if ($ent === 'apartments') {
        $where = $d['complex_id'] ? (string) $db->query('select name from complexes where id = ' . (int) $d['complex_id'])->fetchColumn() : (string) $d['address'];
        $d['slug_base'] = pn_slug($where);
        $d['updated_at'] = date('Y-m-d H:i:s');
    }
    if ($ent === 'complexes') $d['slug'] = pn_slug((string) $d['name']);
    if ($ent === 'houses') { $d['slug'] = pn_slug($d['line'] . ' ' . $d['number']); if ($id === null) $d['code'] = 'h' . $d['number']; }
    return $d;
}

function pn_crud_save(string $ent, array $data, ?int $id): int {
    $E = pn_entities()[$ent]; $db = pn_db(); $t = $E['table'];
    $vals = pn_crud_dbvals($E['fields'], pn_crud_derive($ent, $data, $id));
    $slugBase = $vals['slug_base'] ?? null; unset($vals['slug_base']);
    if ($ent === 'houses' && $id === null) {           // код дома уникален: h235, h235-2…
        $code = $vals['code']; $k = 2; while ($db->query('select 1 from houses where code = ' . $db->quote($vals['code']))->fetchColumn()) $vals['code'] = $code . '-' . $k++;
    }
    if ($id === null) {
        if ($ent === 'apartments') $vals['slug'] = 'tmp-' . bin2hex(random_bytes(6));
        $cols = array_keys($vals);
        $db->prepare("insert into $t(" . implode(',', $cols) . ') values (' . implode(',', array_fill(0, count($cols), '?')) . ')')->execute(array_values($vals));
        $id = (int) $db->lastInsertId();
        audit('create', $t, $id, $data);
    } else {
        $old = pn_crud_row($t, $id);
        $set = implode(',', array_map(fn($c) => "$c = ?", array_keys($vals)));
        $db->prepare("update $t set $set where id = ?")->execute([...array_values($vals), $id]);
        $diff = []; foreach ($vals as $c => $v) if (($old[$c] ?? null) != $v) $diff[$c] = [$old[$c] ?? null, $v];
        audit('update', $t, $id, $diff);
    }
    if ($slugBase !== null) $db->prepare('update apartments set slug = ? where id = ?')->execute(["$id-$slugBase", $id]);
    return $id;
}

function pn_crud(string $ent, string $method, string $sub, array $post, array $files, array $u): array {
    $E = pn_entities()[$ent]; $t = $E['table']; $db = pn_db(); $base = "/admin/$ent";
    $id = ctype_digit($sub) ? (int) $sub : null;
    if ($sub !== '' && $sub !== 'new' && $id === null) throw new PnHttp(404, [], 'Нет такой записи');
    $row = $id ? pn_crud_row($t, $id) : null;
    if ($id && !$row) throw new PnHttp(404, [], 'Запись не найдена — возможно, её уже удалили');
    $do = $post['do'] ?? '';
    if ($method === 'POST' && $id && in_array($do, ['publish', 'unpublish'], true) && !empty($E['publish'])) {
        $db->prepare("update $t set published = ? where id = ?")->execute([$do === 'publish' ? 1 : 0, $id]); audit($do, $t, $id);
        return pn_redirect("$base/$id", $do === 'publish' ? 'Опубликовано на сайте' : 'Снято с сайта');
    }
    if ($method === 'POST' && $id && $do === 'copy' && !empty($E['copy'])) {
        $data = $row; unset($data['id'], $data['created_at']); $data['published'] = 0; $data['slug'] = 'tmp-' . bin2hex(random_bytes(6)); $data['source'] = 'manual'; $data['external_id'] = null;
        $cols = array_keys($data);
        $db->prepare("insert into $t(" . implode(',', $cols) . ') values (' . implode(',', array_fill(0, count($cols), '?')) . ')')->execute(array_values($data));
        $nid = (int) $db->lastInsertId();
        $db->prepare("update $t set slug = ? where id = ?")->execute([$nid . substr($row['slug'], strlen((string) $id)), $nid]);
        audit('copy', $t, $nid, ['from' => $id]);
        return pn_redirect("$base/$nid", 'Копия создана — она не опубликована, проверьте и опубликуйте');
    }
    if ($method === 'POST' && $id && $do === 'delete') {
        if (!empty($E['used_by'])) {
            [$tb, $col, $msg] = $E['used_by'];
            $st = $db->prepare("select count(*) from $tb where $col = ?"); $st->execute([$id]);
            if ((int) $st->fetchColumn() > 0) return pn_redirect("$base/$id", $msg);
        }
        $db->prepare("delete from $t where id = ?")->execute([$id]); audit('delete', $t, $id, $row);
        return pn_redirect($base, 'Удалено');
    }
    if ($method === 'POST' && ($do === 'save' || $do === '')) {
        $r = $ent === 'apartments' ? forms_apartment($post, $files) : forms_parse($E['fields'], $post, $files, $row ?? []);
        if (!$r['errors']) {
            try { $nid = pn_crud_save($ent, $r['data'], $id); return pn_redirect("$base/$nid", 'Сохранено'); }
            catch (PDOException $e) { $r['errors']['_'] = str_contains($e->getMessage(), 'UNIQUE') ? 'Такая запись уже есть (совпадает название)' : 'Не удалось сохранить: ' . $e->getMessage(); }
        }
        $vals = pn_crud_formvals($E['fields'], pn_crud_dbvals($E['fields'], $r['data']) + ($row ?? []));
        return pn_admin_page(($id ? 'Изменить: ' : 'Новый: ') . $E['one'], 'admin/form', ['active' => $ent, 'E' => $E, 'ent' => $ent, 'id' => $id, 'row' => $row,
            'vals' => $vals, 'errors' => $r['errors']]);
    }
    if ($sub === 'new' || $id) {
        $vals = $row ? pn_crud_formvals($E['fields'], $row) : array_map(fn($f) => $f['type'] === 'photos' ? [] : '', $E['fields']);
        if (!$row && $ent === 'complexes') $vals['checks'] = "Разрешение на строительство\nПроектная декларация, эскроу\nПрошлые дома сданы в срок\nНет банкротных дел";
        if (!$row && isset($E['fields']['published'])) $vals['published'] = 0;
        return pn_admin_page($row ? 'Изменить: ' . $E['one'] : 'Новый: ' . $E['one'], 'admin/form', ['active' => $ent, 'E' => $E, 'ent' => $ent, 'id' => $id,
            'row' => $row, 'vals' => $vals, 'errors' => []]);
    }
    // список
    $q = trim((string) ($_GET['q'] ?? '')); $alias = explode(' ', trim(substr($E['list_sql'], strpos($E['list_sql'], ' from ') + 6)))[1] ?? '';
    $sql = $E['list_sql']; $args = [];
    if ($q !== '') { $sql .= ' where (' . implode(' or ', array_map(fn($c) => "$c like ?", $E['search'])) . ')'; $args = array_fill(0, count($E['search']), "%$q%"); }
    $sql .= ' order by ' . ($E['order'] ?? "$alias.id desc");
    $st = $db->prepare($sql); $st->execute($args);
    return pn_admin_page($E['title'], 'admin/list', ['active' => $ent, 'E' => $E, 'ent' => $ent, 'rows' => $st->fetchAll(), 'q' => $q]);
}

// Настройки: ключ → значение JSON в таблице settings.
function pn_settings_fields(): array {
    return [
        'phone' => ['label' => 'Телефон на сайте', 'type' => 'text', 'req' => true], 'hours_from' => ['label' => 'На связи с', 'type' => 'text'],
        'hours_to' => ['label' => 'На связи до', 'type' => 'text'], 'legal' => ['label' => 'Юрлицо (подвал)', 'type' => 'text'],
        'domain' => ['label' => 'Домен', 'type' => 'text'], 'warm_contour_from' => ['label' => 'Тёплый контур от, ₽/м²', 'type' => 'int', 'min' => 1],
        'renovation_prices' => ['label' => 'Ремонт: базовый; комфорт; премиум, ₽/м²', 'type' => 'text'],
        'mortgage_programs' => ['label' => 'Ипотека: «название | ставка» по строке', 'type' => 'pairs', 'wide' => true],
        'tg_token' => ['label' => 'Telegram: токен бота', 'type' => 'secret'], 'tg_chat_id' => ['label' => 'Telegram: чат менеджеров (chat_id)', 'type' => 'text'],
        'mail_to' => ['label' => 'Почта для заявок', 'type' => 'text'], 'smtp_host' => ['label' => 'SMTP-сервер (пусто — mail())', 'type' => 'text'],
        'smtp_port' => ['label' => 'SMTP-порт', 'type' => 'int'], 'smtp_user' => ['label' => 'SMTP-логин', 'type' => 'text'],
        'smtp_pass' => ['label' => 'SMTP-пароль', 'type' => 'secret'], 'smtp_from' => ['label' => 'Отправитель писем', 'type' => 'text'],
        'crm_enabled' => ['label' => 'Отправлять заявки в CRM', 'type' => 'bool'], 'crm_url' => ['label' => 'Адрес API CRM', 'type' => 'text'],
        'crm_token' => ['label' => 'Ключ API CRM', 'type' => 'secret'],
        'demo_data' => ['label' => 'Пометка «демо-данные» на сайте', 'type' => 'bool'], 'show_demo_reviews' => ['label' => 'Показывать демо-отзывы', 'type' => 'bool'],
    ];
}
function pn_admin_settings(string $method, string $sub, array $post, array $files, array $u): array {
    $F = pn_settings_fields(); $cur = Repo::settingsAll();
    $errors = [];
    if ($method === 'POST') {
        $r = forms_parse($F, $post, [], $cur); $d = $r['data']; $errors = $r['errors'];
        $nums = array_map(fn($x) => (int) forms_number($x), preg_split('/[;,\/]/u', (string) $d['renovation_prices']));
        if (count($nums) !== 3 || min($nums) <= 0) $errors['renovation_prices'] = 'Три цены через точку с запятой: 20000; 45000; 80000'; else $d['renovation_prices'] = $nums;
        $progs = array_values(array_filter($d['mortgage_programs'], fn($p) => $p[0] !== ''));
        if (!$progs || array_filter($progs, fn($p) => (forms_number($p[1]) ?? 0) <= 0 || forms_number($p[1]) > 50))
            $errors['mortgage_programs'] = 'Укажите ставку для каждой программы: «Семейная | 6» (больше 0 и не больше 50 %)';
        $d['mortgage_programs'] = array_map(fn($p) => ['name' => $p[0], 'rate' => pn_num(forms_number($p[1]))], $progs);
        $d['phone_tel'] = '+7' . substr(preg_replace('/\D/', '', $d['phone']), -10);
        if (!$errors) {
            $ins = pn_db()->prepare('insert into settings(key, value) values (?, ?) on conflict(key) do update set value = excluded.value');
            $diff = [];
            foreach ($d as $k => $v) { if (($cur[$k] ?? null) != $v) $diff[$k] = str_contains($k, 'token') || str_contains($k, 'pass') ? '***' : $v; $ins->execute([$k, pn_json_enc($v)]); }
            audit('update', 'settings', null, $diff);
            return pn_redirect('/admin/settings', 'Настройки сохранены');
        }
        $cur = $d + $cur;
    }
    $vals = [];
    foreach ($F as $k => $f) $vals[$k] = match (true) {
        $k === 'renovation_prices' => is_array($cur[$k] ?? null) ? implode('; ', $cur[$k]) : (string) ($cur[$k] ?? ''),
        $k === 'mortgage_programs' => implode("\n", array_map(fn($p) => $p['name'] . ' | ' . $p['rate'], (array) ($cur[$k] ?? []))),
        $f['type'] === 'secret' => '', default => $cur[$k] ?? '',
    };
    return pn_admin_page('Настройки', 'admin/form', ['active' => 'settings', 'E' => ['fields' => $F, 'one' => 'настройки'], 'ent' => 'settings', 'id' => null,
        'row' => null, 'vals' => $vals, 'errors' => $errors, 'secret_set' => array_map(fn($f) => true, array_filter($cur, fn($v, $k) => ($F[$k]['type'] ?? '') === 'secret' && $v !== '' && $v !== null, ARRAY_FILTER_USE_BOTH))]);
}
