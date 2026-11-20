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
            'cols' => ['photo' => '', 'id' => '№', 'complex' => 'ЖК / адрес', 'rooms' => 'Комн.', 'area' => 'м²', 'price' => 'Цена', 'published' => 'На сайте'],
            'fields' => [
                'market' => ['sec' => 'Где', 'label' => 'Рынок', 'type' => 'select', 'req' => true, 'opts' => ['new' => 'Новостройка', 'secondary' => 'Вторичка']],
                'complex_id' => ['label' => 'ЖК', 'type' => 'select', 'opts' => $complexes()],
                'address' => ['label' => 'Адрес (для вторички)', 'type' => 'text'],
                'district' => ['label' => 'Район (если не как у ЖК)', 'type' => 'text'],
                'rooms' => ['sec' => 'Квартира', 'label' => 'Комнат (0 — студия)', 'type' => 'int', 'req' => true, 'min' => 0, 'max' => 9],
                'area' => ['label' => 'Площадь, м²', 'type' => 'number', 'req' => 'Укажите площадь', 'min' => 5, 'max' => 1000],
                'living_area' => ['label' => 'Жилая, м²', 'type' => 'number', 'min' => 1, 'max' => 1000],
                'kitchen_area' => ['label' => 'Кухня, м²', 'type' => 'number', 'min' => 1, 'max' => 200, 'hint' => 'Пусто — у студии кухня в комнате'],
                'floor' => ['label' => 'Этаж', 'type' => 'int', 'req' => true, 'min' => -2, 'max' => 120],
                'floors' => ['label' => 'Этажей в доме', 'type' => 'int', 'req' => true, 'min' => 1, 'max' => 120],
                'ceiling' => ['label' => 'Потолки, м', 'type' => 'number', 'min' => 2, 'max' => 6],
                'bathroom' => ['label' => 'Санузел', 'type' => 'select', 'opts' => ['совмещённый' => 'Совмещённый', 'раздельный' => 'Раздельный', 'два санузла' => 'Два санузла']],
                'balcony' => ['label' => 'Балкон', 'type' => 'select', 'opts' => ['нет' => 'Нет', 'балкон' => 'Балкон', 'лоджия' => 'Лоджия', 'два балкона' => 'Два балкона', 'терраса' => 'Терраса']],
                'view' => ['label' => 'Окна выходят', 'type' => 'text', 'hint' => 'Например: «во двор», «на парк», «на две стороны»'],
                'price' => ['sec' => 'Цена и отделка', 'label' => 'Цена, ₽', 'type' => 'number', 'req' => 'Укажите цену', 'min' => 1],
                'discount_pct' => ['label' => 'Скидка, %', 'type' => 'int', 'min' => 0, 'max' => 90],
                'finish' => ['label' => 'Отделка', 'type' => 'select', 'req' => true, 'opts' => ['with' => 'С отделкой', 'without' => 'Без отделки']],
                'finish_label' => ['label' => 'Подпись отделки (необязательно)', 'type' => 'text'],
                'house_status' => ['sec' => 'Дом', 'label' => 'Статус дома', 'type' => 'text', 'req' => true, 'hint' => 'Например: «Дом сдан» или «Сдача — II кв. 2027»'],
                'due' => ['label' => 'Срок сдачи ГГГГММ (0 — сдан)', 'type' => 'int', 'min' => 0, 'max' => 209912],
                'special' => ['label' => 'Спецпредложение', 'type' => 'bool'],
                'description' => ['sec' => 'Описание и фото', 'label' => 'Описание', 'type' => 'textarea', 'wide' => true],
                'photos' => ['label' => 'Фото (первое — обложка)', 'type' => 'photos', 'wide' => true],
                'plans' => ['sec' => 'Планировка', 'label' => 'Картинка планировки от застройщика или из объявления', 'type' => 'photos', 'wide' => true],
                'published' => ['label' => 'Опубликовать на сайте', 'type' => 'bool'],
            ]],
        'complexes' => ['title' => 'ЖК', 'one' => 'ЖК', 'table' => 'complexes', 'search' => ['c.name', 'c.district'],
            'list_sql' => 'select c.*, d.name as developer from complexes c left join developers d on d.id = c.developer_id',
            'cols' => ['photo' => '', 'name' => 'Название', 'district' => 'Район', 'developer' => 'Застройщик'],
            'used_by' => ['apartments', 'complex_id', 'В этом ЖК есть квартиры — сначала перенесите или удалите их'],
            'fields' => [
                'name' => ['sec' => 'ЖК', 'label' => 'Название', 'type' => 'text', 'req' => true],
                'district' => ['label' => 'Район', 'type' => 'text', 'req' => true],
                'developer_id' => ['label' => 'Застройщик', 'type' => 'select', 'opts' => $developers()],
                'address' => ['label' => 'Адрес', 'type' => 'text'],
                'lat' => ['sec' => 'Точка на карте', 'hint' => 'Правый клик на Яндекс.Картах → «Что здесь?» → первое число', 'label' => 'Широта', 'type' => 'number'], 'lng' => ['label' => 'Долгота', 'type' => 'number'],
                'description' => ['sec' => 'Страница ЖК', 'label' => 'Описание (абзацы через пустую строку)', 'type' => 'textarea', 'wide' => true],
                'checks' => ['label' => 'Что проверили (по строке)', 'type' => 'lines', 'wide' => true],
                'photos' => ['label' => 'Фото', 'type' => 'photos', 'wide' => true],
            ]],
        'developers' => ['title' => 'Застройщики', 'one' => 'застройщик', 'table' => 'developers', 'search' => ['d.name'],
            'list_sql' => 'select d.* from developers d', 'cols' => ['name' => 'Название', 'site' => 'Сайт', 'verified' => 'Проверен'],
            'fields' => [
                'name' => ['label' => 'Название', 'type' => 'text', 'req' => true], 'site' => ['label' => 'Сайт', 'type' => 'text'],
                'verified' => ['label' => 'Проверен', 'type' => 'bool'],
            ]],
        'feeds' => ['title' => 'Выгрузки', 'one' => 'выгрузка', 'table' => 'feeds', 'search' => ['f.name', 'f.url'], 'actions' => ['run' => 'Загрузить сейчас'],
            'list_sql' => "select f.*, (select count(*) from apartments a where a.feed_id = f.id and a.feed_state = 'active') as n_active,
                (select count(*) from apartments a where a.feed_id = f.id and a.feed_state = 'active' and a.published = 1) as n_pub from feeds f",
            'cols' => ['name' => 'Название', 'n_active' => 'В фиде', 'n_pub' => 'На сайте', 'last_status' => 'Последняя загрузка'],
            'intro' => 'XML-фиды в формате Яндекс.Недвижимости: от застройщиков-партнёров (попросите у их менеджера ссылку «для сайта агентства») или «База.ПРО» Н-маркет. '
                . 'Сайт сам забирает каждый фид раз в сутки: новые квартиры добавляет, цены обновляет, проданные снимает. Описание, спецпредложение, скидку и фото, которые вы поменяли сами, загрузка не трогает.',
            'fields' => [
                'name' => ['sec' => 'Выгрузка', 'label' => 'Название', 'type' => 'text', 'req' => true, 'hint' => 'Например: «Брусника» или «Н-маркет, Екатеринбург»'],
                'url' => ['label' => 'Ссылка на XML-фид', 'type' => 'url', 'req' => true, 'wide' => true, 'hint' => 'Формат Яндекс.Недвижимости (realty-feed)'],
                'developer_id' => ['label' => 'Застройщик (если это фид одного застройщика)', 'type' => 'select', 'opts' => $developers(),
                    'hint' => 'Пусто — застройщик берётся из описания квартир в фиде'],
                'only_verified' => ['sec' => 'Показ на сайте', 'label' => 'Показывать только квартиры проверенных застройщиков', 'type' => 'bool',
                    'hint' => 'Отметка «Проверен» — в разделе «Застройщики». Остальные квартиры загружаются, но скрыты'],
                'enabled' => ['label' => 'Загружать каждый день', 'type' => 'bool', 'hint' => 'Если выключить, квартиры этой выгрузки снимаются с сайта'],
            ]],
        'houses' => ['title' => 'Дома', 'one' => 'проект дома', 'table' => 'houses', 'publish' => true, 'search' => ['h.line', 'h.motto'],
            'list_sql' => 'select h.* from houses h', 'order' => 'sort, id',
            'cols' => ['photo' => '', 'line' => 'Линейка', 'number' => 'Номер', 'area' => 'м²', 'published' => 'На сайте'],
            'fields' => [
                'line' => ['sec' => 'Проект', 'label' => 'Линейка', 'type' => 'text', 'req' => true, 'hint' => 'Северный Урал / Южный Урал / Средний Урал'],
                'number' => ['label' => 'Номер (обычно = площадь)', 'type' => 'int', 'req' => true, 'min' => 1],
                'area' => ['label' => 'Площадь, м²', 'type' => 'number', 'min' => 10],
                'motto' => ['label' => 'Девиз', 'type' => 'text'], 'color' => ['label' => 'Цвет линейки (#HEX)', 'type' => 'text'],
                'floors' => ['sec' => 'Характеристики и цена', 'label' => 'Этажей', 'type' => 'int', 'min' => 1, 'max' => 4], 'rooms' => ['label' => 'Комнаты', 'type' => 'text'],
                'ceiling' => ['label' => 'Потолки', 'type' => 'text'], 'price_from' => ['label' => 'Цена от, ₽', 'type' => 'number', 'min' => 1],
                'sort' => ['label' => 'Порядок показа', 'type' => 'int'],
                'features' => ['sec' => 'Тексты', 'label' => 'Особенности (по строке)', 'type' => 'lines', 'wide' => true],
                'idea' => ['label' => 'Идея', 'type' => 'textarea', 'wide' => true],
                'text' => ['label' => 'Текст (абзацы через пустую строку)', 'type' => 'paras', 'wide' => true],
                'photos' => ['sec' => 'Фото и планировки', 'label' => 'Фото', 'type' => 'photos', 'wide' => true],
                'plans' => ['label' => 'Планировки: «подпись | фото» по строке', 'type' => 'pairs', 'wide' => true,
                    'hint' => 'Фото планировки сначала загрузите в «Фото», затем перенесите его имя сюда и удалите из фото'],
                'published' => ['label' => 'Опубликовать на сайте', 'type' => 'bool'],
            ]],
        'reviews' => ['title' => 'Отзывы', 'one' => 'отзыв', 'table' => 'reviews', 'publish' => true, 'search' => ['r.name', 'r.text'],
            'list_sql' => 'select r.* from reviews r', 'order' => 'sort, id',
            'cols' => ['name' => 'Имя', 'about' => 'О чём', 'is_demo' => 'Демо', 'published' => 'На сайте'],
            'fields' => [
                'name' => ['sec' => 'Автор', 'label' => 'Имя', 'type' => 'text', 'req' => true], 'about' => ['label' => 'Подпись (что купили)', 'type' => 'text'],
                'tag' => ['label' => 'Метка на фото', 'type' => 'select', 'opts' => ['Новостройка' => 'Новостройка', 'Вторичка' => 'Вторичка', 'Ремонт' => 'Ремонт', 'Дом' => 'Дом']],
                'topic' => ['label' => 'Тема', 'type' => 'select', 'opts' => ['apartment' => 'Квартира', 'house' => 'Дом', 'renovation' => 'Ремонт']],
                'rating' => ['label' => 'Оценка', 'type' => 'int', 'min' => 1, 'max' => 5], 'sort' => ['label' => 'Порядок', 'type' => 'int'],
                'text' => ['sec' => 'Отзыв', 'label' => 'Текст отзыва', 'type' => 'textarea', 'req' => true, 'wide' => true],
                'photo' => ['label' => 'Фото (имя)', 'type' => 'text'],
                'is_demo' => ['sec' => 'Показ', 'label' => 'Демо-отзыв (на боевом сайте скрыт)', 'type' => 'bool'], 'published' => ['label' => 'Показывать', 'type' => 'bool'],
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
    $old = $old ?? null;
    if ($slugBase !== null && ($old['source'] ?? 'manual') !== 'feed') $db->prepare('update apartments set slug = ? where id = ?')->execute(["$id-$slugBase", $id]);
    if ($ent === 'apartments' && ($old['source'] ?? '') === 'feed') {          // менеджер правил квартиру из фида: его публикация и фото важнее загрузки
        $own = ($old['photos'] ?? '[]') !== ($vals['photos'] ?? '[]') || ($old['plans'] ?? '[]') !== ($vals['plans'] ?? '[]');
        $man = (int) ($old['published'] ?? 0) !== (int) ($vals['published'] ?? 0);
        if ($own || $man) $db->prepare('update apartments set feed_own_media = max(feed_own_media, ?), feed_manual = max(feed_manual, ?) where id = ?')->execute([(int) $own, (int) $man, $id]);
    }
    if (in_array($ent, ['developers', 'feeds'], true)) pn_feed_visibility();
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
        if ($ent === 'apartments' && ($row['source'] ?? '') === 'feed') $db->prepare('update apartments set feed_manual = 1 where id = ?')->execute([$id]);
        return pn_redirect("$base/$id", $do === 'publish' ? 'Опубликовано на сайте' : 'Снято с сайта');
    }
    if ($method === 'POST' && $id && $ent === 'feeds' && $do === 'run') {
        $s = pn_feed_import($id); $img = pn_feed_images(150, 60); audit('run', 'feeds', $id, $s);
        $st = pn_db()->prepare('select last_status from feeds where id = ?'); $st->execute([$id]);
        return pn_redirect("$base/$id", $st->fetchColumn() . ($img['left'] ? ". Картинки: скачано {$img['ok']}, остальные ({$img['left']}) докачаются по расписанию" : ''));
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
        if (!$row && $ent === 'feeds') { $vals['only_verified'] = 1; $vals['enabled'] = 1; }
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
        'phone' => ['sec' => 'Контакты', 'label' => 'Телефон на сайте', 'type' => 'text', 'req' => true], 'hours_from' => ['label' => 'На связи с', 'type' => 'text'],
        'hours_to' => ['label' => 'На связи до', 'type' => 'text'], 'legal' => ['label' => 'Юрлицо (подвал)', 'type' => 'text'],
        'domain' => ['label' => 'Домен', 'type' => 'text'], 'address' => ['label' => 'Адрес офиса (без города)', 'type' => 'text', 'hint' => 'Например: ул. Амундсена, 136 — в подвале, меню связи и для поисковиков'],
        'telegram' => ['label' => 'Telegram: ник или ссылка', 'type' => 'text', 'hint' => 'platfoma96 или https://t.me/…; пусто — кнопка ведёт в чат на сайте'],
        'max' => ['label' => 'MAX: ссылка или название канала', 'type' => 'text', 'hint' => 'Ссылка — кнопка откроет MAX; только название — подскажем, что искать'], 'warm_contour_from' => ['sec' => 'Цены и ипотека', 'label' => 'Тёплый контур от, ₽/м²', 'type' => 'int', 'min' => 1],
        'renovation_prices' => ['label' => 'Ремонт: базовый; комфорт; премиум, ₽/м²', 'type' => 'text'],
        'mortgage_programs' => ['label' => 'Ипотека: «название | ставка, % | лимит, млн ₽» по строке', 'type' => 'pairs', 'wide' => true,
            'hint' => 'Лимит — сумма кредита по льготной ставке; сверх неё калькулятор считает по рыночной. У рыночной лимит не нужен. У семейной ставка и лимит берутся по числу детей — ниже.'],
        'family_tiers' => ['label' => 'Семейная по числу детей: «детей | ставка, % | лимит, млн ₽»', 'type' => 'pairs', 'wide' => true,
            'hint' => 'Последняя строка действует и для большего числа детей (5 → «5 и больше»).'],
        'rates_date' => ['label' => 'Ставки актуальны на (ДД.ММ.ГГГГ)', 'type' => 'text', 'hint' => 'Показывается под калькуляторами. Обновляйте раз в месяц и после решений ЦБ.'],
        'tg_token' => ['sec' => 'Заявки в Telegram', 'label' => 'Токен бота', 'type' => 'secret', 'hint' => 'Выдаёт BotFather в Telegram при создании бота'], 'tg_chat_id' => ['label' => 'Чат менеджеров (chat_id)', 'type' => 'text', 'hint' => 'Добавьте бота в группу менеджеров; chat_id группы начинается с «-»'],
        'mail_to' => ['sec' => 'Заявки на почту', 'label' => 'Почта для заявок', 'type' => 'text'], 'smtp_host' => ['label' => 'SMTP-сервер (пусто — mail())', 'type' => 'text'],
        'smtp_port' => ['label' => 'SMTP-порт', 'type' => 'int'], 'smtp_user' => ['label' => 'SMTP-логин', 'type' => 'text'],
        'smtp_pass' => ['label' => 'SMTP-пароль', 'type' => 'secret'], 'smtp_from' => ['label' => 'Отправитель писем', 'type' => 'text'],
        'crm_enabled' => ['sec' => 'CRM', 'label' => 'Отправлять заявки в CRM', 'type' => 'bool'], 'crm_url' => ['label' => 'Адрес API CRM', 'type' => 'text'],
        'crm_token' => ['label' => 'Ключ API CRM', 'type' => 'secret'],
        'demo_data' => ['sec' => 'Демо', 'label' => 'Пометка «демо-данные» на сайте', 'type' => 'bool'], 'show_demo_reviews' => ['label' => 'Показывать демо-отзывы', 'type' => 'bool'],
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
        $d['mortgage_programs'] = array_map(fn($p) => ['name' => $p[0], 'rate' => pn_num(forms_number($p[1]))]
            + (isset($p[2]) && forms_number($p[2]) ? ['limit' => (int) round(forms_number($p[2]) * 1000000)] : []), $progs);
        $tiers = array_values(array_filter((array) ($d['family_tiers'] ?? []), fn($p) => trim((string) $p[0]) !== ''));
        if (array_filter($tiers, fn($p) => !ctype_digit(trim((string) $p[0])) || (forms_number($p[1] ?? '') ?? 0) <= 0 || (forms_number($p[2] ?? '') ?? 0) <= 0))
            $errors['family_tiers'] = 'По строке: «детей | ставка | лимит в млн», например «1 | 10 | 6»';
        $d['family_tiers'] = array_map(fn($p) => ['kids' => (int) $p[0], 'rate' => pn_num(forms_number($p[1] ?? '')), 'limit' => (int) round((forms_number($p[2] ?? '') ?? 0) * 1000000)], $tiers);
        $rd = trim((string) ($d['rates_date'] ?? ''));
        if ($rd !== '' && !preg_match('~^(\d\d)\.(\d\d)\.(\d{4})$~', $rd, $mm)) $errors['rates_date'] = 'Дата в виде 18.11.2026';
        $d['rates_date'] = $rd === '' ? null : (isset($mm) && $mm ? "$mm[3]-$mm[2]-$mm[1]" : $rd);
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
        $k === 'mortgage_programs' => implode("\n", array_map(fn($p) => $p['name'] . ' | ' . str_replace('.', ',', (string) $p['rate'])
            . (!empty($p['limit']) ? ' | ' . str_replace('.', ',', (string) ($p['limit'] / 1000000)) : ''), (array) ($cur[$k] ?? []))),
        $k === 'family_tiers' => implode("\n", array_map(fn($p) => $p['kids'] . ' | ' . str_replace('.', ',', (string) $p['rate']) . ' | '
            . str_replace('.', ',', (string) ($p['limit'] / 1000000)), (array) ($cur[$k] ?? []))),
        $k === 'rates_date' => pn_rates_date_ru($cur),
        $f['type'] === 'secret' => '', default => $cur[$k] ?? '',
    };
    return pn_admin_page('Настройки', 'admin/form', ['active' => 'settings', 'E' => ['fields' => $F, 'one' => 'настройки'], 'ent' => 'settings', 'id' => null,
        'row' => null, 'vals' => $vals, 'errors' => $errors, 'secret_set' => array_map(fn($f) => true, array_filter($cur, fn($v, $k) => ($F[$k]['type'] ?? '') === 'secret' && $v !== '' && $v !== null, ARRAY_FILTER_USE_BOTH))]);
}
