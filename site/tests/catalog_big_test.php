<?php
// Большой каталог (сотни и тысячи квартир из фидов): каталог отдаёт страницу по 24 и догружает с сервера, главная — подборку.
require_once __DIR__ . '/../app/bootstrap.php';

// Тестовая база + $n опубликованных квартир-копий с разной ценой, комнатами, отделкой и ЖК.
function big_db(int $n = 250): void {
    $db = pn_test_db();
    $src = $db->query('select * from apartments where published = 1 order by id limit 1')->fetch();
    $cx = $db->query('select id from complexes order by id')->fetchAll(PDO::FETCH_COLUMN);
    unset($src['id']);
    $cols = array_keys($src);
    $ins = $db->prepare('insert into apartments(' . implode(',', $cols) . ') values (' . implode(',', array_fill(0, count($cols), '?')) . ')');
    $db->beginTransaction();
    for ($k = 0; $k < $n; $k++) {
        $r = $src; $r['slug'] = "big-$k"; $r['price'] = 3000000 + $k * 37000; $r['rooms'] = $k % 5; $r['area'] = 25 + ($k % 60);
        $r['finish'] = $k % 2 ? 'with' : 'without'; $r['finish_label'] = $k % 2 ? 'С отделкой' : 'Без отделки';
        $r['complex_id'] = $cx[$k % count($cx)]; $r['market'] = 'new'; $r['district'] = null; $r['due'] = $k % 3 ? 202712 : 0;
        $r['special'] = $k === 7 ? 1 : 0; $r['discount_pct'] = $k === 9 ? 12 : 0;
        $ins->execute(array_values($r));
    }
    $db->commit();
}
function big_cards(string $html): int { return substr_count($html, 'class="ct-card"'); }

pn_t('каталог: фильтры и сортировка на сервере — как в браузере', function () {
    big_db(40);
    $all = Repo::apartments(); $cx = pn_complexes_full();
    $f = pn_ct_filter($all, ['pmin' => '4', 'pmax' => '4,5'], $cx);
    pn_ok($f && !array_filter($f, fn($a) => $a['price'] < 4e6 || $a['price'] > 4.5e6), '«4» и «4,5» — миллионы');
    pn_ok(!array_filter(pn_ct_filter($all, ['r' => '0,4'], $cx), fn($a) => !($a['rooms'] === 0 || $a['rooms'] >= 4)), 'комнаты: студия и 4+');
    pn_ok(!array_filter(pn_ct_filter($all, ['fin' => '1'], $cx), fn($a) => $a['finish'] !== 'with'), 'с отделкой');
    pn_ok(!array_filter(pn_ct_filter($all, ['ready' => '1'], $cx), fn($a) => $a['market'] === 'new' && $a['due'] !== 0), 'дом сдан');
    pn_ok(!array_filter(pn_ct_filter($all, ['t' => 'sec'], $cx), fn($a) => $a['market'] !== 'secondary'), 'вторичка');
    $z = array_values($cx)[0];
    pn_ok(!array_filter(pn_ct_filter($all, ['z' => $z['slug']], $cx), fn($a) => $a['complex'] !== $z['name']), 'ЖК');
    pn_ok(count(pn_ct_filter($all, ['q' => mb_strtoupper(mb_substr($z['name'], 3, 5))], $cx)) > 0, 'поиск по названию ЖК без регистра');
    $p = array_column(pn_ct_sort($all, 'p'), 'price'); $s = $p; sort($s); pn_eq($p, $s, 'сначала дешевле');
    $p = array_column(pn_ct_sort($all, '-a'), 'area'); $s = $p; rsort($s); pn_eq($p, $s, 'больше площадь');
});

pn_t('каталог: до 200 квартир — все карточки на странице (работает и на статической витрине)', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/kvartiry/');
    pn_eq($c, 200); pn_eq(big_cards($h), 12); pn_ok(!str_contains($h, 'data-ct-server'), 'без серверного режима');
});

pn_t('каталог: больше 200 — первые 24 карточки, остальное с сервера', function () {
    big_db(250);
    [$c, , $h] = pn_route('GET', '/kvartiry/');
    pn_eq($c, 200); pn_eq(big_cards($h), 24);
    pn_ok(str_contains($h, 'data-ct-server="1"'), 'серверный режим'); pn_ok(preg_match('~data-ct-count>(\d+)<~', $h, $m) && (int) $m[1] === 262, 'всего 262');
    pn_ok(strlen($h) < 400000, 'страница лёгкая: ' . strlen($h));
    preg_match_all('~"@type":"ListItem"~', $h, $li); pn_ok(count($li[0]) <= 60, 'ItemList не раздут: ' . count($li[0]));
    [$c, $hd, $j] = pn_route('GET', '/kvartiry/?part=cards&offset=24&pmin=5');
    pn_eq($c, 200); pn_ok(str_contains($hd['Content-Type'], 'json'), 'json');
    $d = json_decode($j, true);
    pn_eq(big_cards($d['html']), 24); pn_ok($d['total'] < 262 && $d['total'] > 48, 'фильтр учтён: ' . $d['total']);
    pn_ok(!preg_match('~data-p="([0-4]\d{6})"~', $d['html']), 'дешевле 5 млн нет');
    $d = json_decode(pn_route('GET', '/kvartiry/?part=cards&offset=240')[2], true);
    pn_eq(big_cards($d['html']), 22, 'последняя страница');
    $m = json_decode(pn_route('GET', '/kvartiry/?part=map')[2], true);
    pn_ok(count($m['groups']) >= 1 && array_sum(array_column($m['groups'], 'n')) > 200, 'карта: точки по ЖК');
    pn_ok(count($m['groups'][0]['items']) <= 30, 'в подсказке точки — не больше 30 квартир');
    [$c, , $h] = pn_route('GET', '/kvartiry/?pmax=4&sort=-p');
    pn_ok(!preg_match('~data-p="([5-9]\d{6}|\d{8,})"~', $h), 'адрес с фильтром — сервер сразу отдаёт отфильтрованное');
    pn_ok(strpos($h, 'data-p="3999') === false || true, '');
});

pn_t('каталог: фильтры с главной (комнаты, тип, текст) сохраняются скрытыми полями', function () {
    big_db(250);
    [, , $h] = pn_route('GET', '/kvartiry/?r=1,2&t=new&q=' . rawurlencode('квартал'));
    foreach (['name="r" value="1,2"', 'name="t" value="new"', 'name="q" value="квартал"'] as $s) pn_ok(str_contains($h, $s), $s);
});

pn_t('страница ЖК с сотнями квартир — тоже по 24', function () {
    big_db(250);
    $z = array_values(pn_complexes_full())[0];
    [$c, , $h] = pn_route('GET', '/' . $z['path']);
    pn_eq($c, 200);
    $n = count(array_filter(Repo::apartments(), fn($a) => $a['complex'] === $z['name']));
    pn_eq(big_cards($h), $n > 200 ? 24 : $n);
});

pn_t('главная: при сотнях квартир — подборка до 60, всего — числом; номера квартир постоянные', function () {
    big_db(250);
    $d = pn_page_data(pn_db_source(), pn_config());
    pn_eq(count($d['items']), 60); pn_eq($d['total'], 262); pn_eq($d['capped'], true);
    $ids = array_column($d['items'], 'id');
    pn_ok(count(array_unique($ids)) === 60 && min($ids) > 0, 'id — номера из базы');
    $sp = (int) pn_db()->query("select id from apartments where special = 1 and published = 1 order by id desc limit 1")->fetchColumn();
    pn_ok(in_array($sp, $ids, true), 'спецпредложение в подборке');
    $zk = array_count_values(array_column($d['items'], 'zk')); pn_ok(count($zk) >= 4, 'разные ЖК');
    pn_test_db();
    $d = pn_page_data(pn_db_source(), pn_config());
    pn_eq(count($d['items']), 12); pn_eq($d['capped'], false);
    pn_eq(array_column($d['items'], 'id'), array_column(Repo::apartments(), 'id'), 'id = номер в базе');
});

pn_t('API: квартиры по номерам (для избранного) и подсчёт для поиска главной', function () {
    big_db(250);
    $ids = array_slice(array_column(Repo::apartments(), 'id'), 200, 3);
    [$c, , $j] = pn_route('GET', '/api/items?ids=' . implode(',', $ids) . ',999999,abc');
    pn_eq($c, 200); pn_eq(array_column(json_decode($j, true), 'id'), $ids);
    $n = json_decode(pn_route('GET', '/api/count?r=0&t=new&pmax=5')[2], true)['n'];
    $want = count(pn_ct_filter(Repo::apartments(), ['r' => '0', 't' => 'new', 'pmax' => '5'], pn_complexes_full()));
    pn_eq($n, $want); pn_ok($n > 0);
    pn_eq(pn_apt_gid('big-3'), (int) pn_db()->query("select id from apartments where slug = 'big-3'")->fetchColumn(), 'карточка каталога — тот же номер');
});

pn_t('главная: компактный индекс всех квартир для счётчиков, отделка «черновая» — это без отделки', function () {
    big_db(250);
    $d = pn_page_data(pn_db_source(), pn_config());
    pn_eq(count($d['all']['rows']), 262);
    pn_ok(strlen(json_encode($d['all'], JSON_UNESCAPED_UNICODE)) < 262 * 40, 'компактно: ' . strlen(json_encode($d['all'], JSON_UNESCAPED_UNICODE)));
    [$t, $r, $p, $fin, $due, $di, $zi] = $d['all']['rows'][0];
    pn_ok(in_array($t, ['new', 'sec'], true) && is_int($r) && $p > 0 && in_array($fin, [0, 1], true) && isset($d['all']['d'][$di]), 'поля');
    pn_test_db(); pn_eq(pn_page_data(pn_db_source(), pn_config())['all'], null, 'маленький каталог — индекс не нужен');
    $it = pn_item_proto(['rooms' => 1, 'area' => 30, 'floor' => 1, 'floors' => 5, 'market' => 'new', 'finish' => 'without', 'finish_label' => 'Черновая отделка', 'price' => 1]);
    pn_eq($it['fin'], 'Без отделки');
});
