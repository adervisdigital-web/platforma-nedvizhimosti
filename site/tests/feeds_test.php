<?php
require_once __DIR__ . '/../app/bootstrap.php';
// Загрузка квартир из XML-фидов (формат Яндекс.Недвижимости): разбор, добавление, обновление, снятие проданных, показ только проверенных, картинки.
const PN_FEED_FIX = __DIR__ . '/fixtures/feed_ekb.xml';

// Подмена скачивания: фид — из файла-фикстуры (или переданного XML), картинки — маленький PNG; считает обращения.
function feed_fake_fetch(?string $xml = null, array $broken = []): void {
    $GLOBALS['PN_FETCH_LOG'] = [];
    $GLOBALS['PN_FETCH'] = function (string $url, string $dest) use ($xml, $broken) {
        $GLOBALS['PN_FETCH_LOG'][] = $url;
        foreach ($broken as $b) if (str_contains($url, $b)) throw new RuntimeException("HTTP 404 $url");
        if (str_starts_with($url, 'https://feed.test/')) { file_put_contents($dest, $xml ?? file_get_contents(PN_FEED_FIX)); return; }
        $im = imagecreatetruecolor(40, 30); imagefill($im, 0, 0, imagecolorallocate($im, 200, 120, 90)); imagepng($im, $dest); imagedestroy($im);
    };
}
function feed_test_setup(array $feed = []): int {
    $db = pn_test_db(); $GLOBALS['PN_UPLOADS'] = __DIR__ . '/_tmp/uploads';
    feed_fake_fetch();
    $db->prepare('insert into developers(name, verified) values (?, 1)')->execute(['Брусника']);
    $f = $feed + ['name' => 'Тестовый фид', 'url' => 'https://feed.test/ekb.xml', 'only_verified' => 1, 'developer_id' => null];
    $db->prepare('insert into feeds(name, url, only_verified, developer_id) values (?,?,?,?)')->execute([$f['name'], $f['url'], $f['only_verified'], $f['developer_id']]);
    return (int) $db->lastInsertId();
}
function feed_apt(string $ext): ?array {
    $st = pn_db()->prepare("select a.*, c.name as complex, d.name as developer, d.verified from apartments a left join complexes c on c.id = a.complex_id
        left join developers d on d.id = c.developer_id where a.source = 'feed' and a.external_id like ?");
    $st->execute(["%:$ext"]); return $st->fetch() ?: null;
}

pn_t('фид: разбор квартир, пропуск домов, аренды и объявлений без цены', function () {
    $r = pn_feed_offers(PN_FEED_FIX);
    pn_eq(count($r['offers']), 3); pn_eq($r['skipped'], 3);
    $o = $r['offers'][0];
    pn_eq($o['ext'], '101'); pn_eq($o['rooms'], 2); pn_eq($o['area'], 58.4); pn_eq($o['living_area'], 32.1); pn_eq($o['kitchen_area'], 12.5);
    pn_eq($o['floor'], 5); pn_eq($o['floors'], 17); pn_eq($o['price'], 7500000); pn_eq($o['ceiling'], 2.8);
    pn_eq($o['finish'], 'with'); pn_eq($o['finish_label'], 'Чистовая отделка');
    pn_eq($o['house_status'], 'Сдача — II кв. 2027'); pn_eq($o['due'], 202706);
    pn_eq($o['district'], 'Академический'); pn_eq($o['complex'], 'Тестовый парк'); pn_eq($o['complex_ext'], 'nm:5001');
    pn_eq($o['developer'], 'Брусника'); pn_eq($o['bathroom'], 'раздельный'); pn_eq($o['balcony'], 'лоджия');
    pn_eq($o['lat'], 56.7901); pn_eq($o['market'], 'new');
    pn_eq(array_column($o['media'], 0), ['plan', 'floorplan', 'housemain', 'houseuncategorized']);
    pn_eq($o['media'][0][1], 'nm:PLAN-101', 'ключ картинки Н-маркет — по pid, без меняющегося hash');
    $s = $r['offers'][1];
    pn_eq($s['rooms'], 0, 'студия'); pn_eq($s['finish'], 'without'); pn_eq($s['house_status'], 'Дом сдан'); pn_eq($s['due'], 0);
    $n = $r['offers'][2];
    pn_eq($n['complex'], 'Новый квартал', 'ЖК и кавычки снимаются'); pn_eq($n['district'], 'Уралмаш'); pn_eq($n['developer'], 'Новострой-Урал');
    pn_eq($n['finish'], 'without'); pn_eq($n['finish_label'], 'Подготовка под чистовую отделку'); pn_eq($n['complex_ext'], 'name:новый квартал');
});

pn_t('фид: первая загрузка — квартиры, ЖК и застройщики; на сайте только проверенные', function () {
    $fid = feed_test_setup();
    $st = pn_feed_import($fid);
    pn_eq([$st['added'], $st['updated'], $st['gone'], $st['skipped']], [3, 0, 0, 3]);
    $a = feed_apt('101');
    pn_eq($a['external_id'], "$fid:101"); pn_eq((int) $a['feed_id'], $fid); pn_eq($a['feed_state'], 'active');
    pn_eq($a['complex'], 'ЖК Тестовый парк'); pn_eq($a['developer'], 'Брусника'); pn_eq((int) $a['published'], 1);
    pn_ok(preg_match('/^\d+-zhk-testovyy-park$/', $a['slug']) === 1, 'slug: ' . $a['slug']);
    pn_eq((int) $a['price'], 7500000); pn_eq($a['description'], 'Квартира 2 ккв в комплексе Тестовый парк. Застройщик: Брусника. Рядом парк.');
    $n = feed_apt('103');
    pn_eq($n['developer'], 'Новострой-Урал'); pn_eq((int) $n['verified'], 0); pn_eq((int) $n['published'], 0, 'непроверенный застройщик — скрыта');
    pn_eq((int) pn_db()->query("select count(*) from complexes where name = 'ЖК Тестовый парк'")->fetchColumn(), 1, 'один ЖК на две квартиры');
    $f = pn_db()->query("select * from feeds where id = $fid")->fetch();
    pn_ok($f['last_ok_at'] !== null, 'время успешной загрузки'); pn_ok(str_contains($f['last_status'], 'добавлено 3'), $f['last_status']);
    pn_ok(Repo::apartment($a['slug']) !== null, 'страница квартиры открывается');
});

pn_t('фид: повторная загрузка обновляет цену, проданные снимает, ручные правки не трогает', function () {
    $fid = feed_test_setup(); pn_feed_import($fid);
    $a = feed_apt('101');
    pn_db()->prepare('update apartments set description = ?, special = 1, discount_pct = 7, view = ? where id = ?')->execute(['Наш текст', 'на парк', $a['id']]);
    $xml = file_get_contents(PN_FEED_FIX);
    $xml = str_replace('<value>7500000</value>', '<value>7300000</value>', $xml);
    $xml = preg_replace('~<offer internal-id="102">.*?</offer>~s', '', $xml);
    feed_fake_fetch($xml);
    $st = pn_feed_import($fid);
    pn_eq([$st['added'], $st['updated'], $st['gone']], [0, 2, 1]);
    $a = feed_apt('101');
    pn_eq((int) $a['price'], 7300000); pn_eq($a['description'], 'Наш текст'); pn_eq((int) $a['special'], 1); pn_eq((int) $a['discount_pct'], 7); pn_eq($a['view'], 'на парк');
    $s = feed_apt('102');
    pn_eq($s['feed_state'], 'gone'); pn_eq((int) $s['published'], 0, 'пропала из фида — снята с сайта');
    feed_fake_fetch();
    pn_feed_import($fid);
    $s = feed_apt('102');
    pn_eq([$s['feed_state'], (int) $s['published']], ['active', 1], 'вернулась в фид — снова на сайте');
});

pn_t('фид: ошибка скачивания или пустой фид — ничего не снимаем', function () {
    $fid = feed_test_setup(); pn_feed_import($fid);
    feed_fake_fetch('<realty-feed xmlns="http://webmaster.yandex.ru/schemas/feed/realty/2010-06"></realty-feed>');
    $st = pn_feed_import($fid);
    pn_ok(!empty($st['error']), 'ошибка в результате');
    pn_eq((int) feed_apt('101')['published'], 1);
    feed_fake_fetch('это не xml <<<');
    $st = pn_feed_import($fid); pn_ok(!empty($st['error']));
    feed_fake_fetch(null, ['feed.test']);
    $st = pn_feed_import($fid); pn_ok(str_contains($st['error'], '404'), $st['error']);
    $f = pn_db()->query("select * from feeds where id = $fid")->fetch();
    pn_ok(str_starts_with($f['last_status'], 'Ошибка'), $f['last_status']);
    pn_eq((int) pn_db()->query("select count(*) from apartments where source = 'feed' and published = 1")->fetchColumn(), 2);
});

pn_t('фид: резкое падение числа квартир — не снимаем, предупреждаем', function () {
    $fid = feed_test_setup(); pn_feed_import($fid);
    $xml = preg_replace('~<offer internal-id="10[23]">.*?</offer>~s', '', file_get_contents(PN_FEED_FIX));
    feed_fake_fetch($xml);
    $st = pn_feed_import($fid);
    pn_eq($st['gone'], 0); pn_ok($st['hide_skipped'], 'снятие пропущено');
    pn_eq(feed_apt('102')['feed_state'], 'active');
    pn_ok(str_contains(pn_db()->query("select last_status from feeds where id = $fid")->fetchColumn(), 'не сняты'), 'предупреждение в статусе');
});

pn_t('фид: отметка «Проверен» у застройщика сразу открывает его квартиры', function () {
    $fid = feed_test_setup(); pn_feed_import($fid);
    pn_db()->exec("update developers set verified = 1 where name = 'Новострой-Урал'");
    pn_feed_visibility();
    pn_eq((int) feed_apt('103')['published'], 1);
    pn_db()->exec("update developers set verified = 0 where name = 'Брусника'");
    pn_feed_visibility();
    pn_eq((int) feed_apt('101')['published'], 0);
});

pn_t('фид: фид без отбора показывает всё; ручная публикация менеджера сильнее загрузки', function () {
    $fid = feed_test_setup(['only_verified' => 0]); pn_feed_import($fid);
    pn_eq((int) feed_apt('103')['published'], 1);
    $id = (int) feed_apt('101')['id'];
    pn_db()->prepare('update apartments set published = 0, feed_manual = 1 where id = ?')->execute([$id]);
    pn_feed_import($fid);
    pn_eq((int) feed_apt('101')['published'], 0, 'менеджер снял — остаётся снятой');
});

pn_t('фид: застройщик фида задаётся вручную, если это фид одного застройщика', function () {
    $db = pn_test_db(); $GLOBALS['PN_UPLOADS'] = __DIR__ . '/_tmp/uploads'; feed_fake_fetch();
    $db->exec("insert into developers(name, verified) values ('Атлас', 1)"); $did = (int) $db->lastInsertId();
    $db->prepare('insert into feeds(name, url, developer_id) values (?,?,?)')->execute(['Атлас', 'https://feed.test/a.xml', $did]);
    pn_feed_import((int) $db->lastInsertId());
    pn_eq(feed_apt('103')['developer'], 'Атлас'); pn_eq((int) feed_apt('103')['published'], 1);
});

pn_t('фид: картинки скачиваются к нам один раз, планировки и фото ЖК заполняются', function () {
    $fid = feed_test_setup(); pn_feed_import($fid);
    feed_fake_fetch(null, ['PLAN-102']);
    $r = pn_feed_images(50, 30);
    pn_eq($r['err'], 1);
    $log = $GLOBALS['PN_FETCH_LOG'];
    pn_eq(count(array_filter($log, fn($u) => str_contains($u, 'HOUSE-MAIN'))), 1, 'общая картинка — один раз');
    pn_ok(!array_filter($log, fn($u) => str_contains($u, 'PLAN-103')), 'скрытые квартиры картинки не тянут');
    $a = feed_apt('101');
    $plans = json_decode($a['plans'], true); $photos = json_decode($a['photos'], true);
    pn_eq(count($plans), 2); pn_ok(str_starts_with($plans[0], 'u/'), 'планировка — загруженная WebP');
    pn_ok(is_file($GLOBALS['PN_UPLOADS'] . '/' . substr($plans[0], 2) . '-960.webp'), 'файл на месте');
    pn_eq(count($photos), 2, 'фото квартиры — фото ЖК');
    $c = pn_db()->query("select photos from complexes where name = 'ЖК Тестовый парк'")->fetchColumn();
    pn_eq(count(json_decode($c, true)), 2, 'фото ЖК');
    pn_eq(json_decode(feed_apt('102')['plans'], true), [], 'битая планировка — пусто');
    pn_eq((int) pn_db()->query("select tries from feed_images where key = 'nm:PLAN-102'")->fetchColumn(), 1);
    $before = count($GLOBALS['PN_FETCH_LOG']);
    pn_feed_images(50, 30);
    pn_eq(count($GLOBALS['PN_FETCH_LOG']) - $before, 1, 'повтор — только для битой');
});

pn_t('фид: фото, которые менеджер поменял сам, загрузка не трогает', function () {
    $fid = feed_test_setup(); pn_feed_import($fid);
    $id = (int) feed_apt('101')['id'];
    pn_db()->prepare('update apartments set photos = ?, feed_own_media = 1 where id = ?')->execute(['["kv_living2"]', $id]);
    pn_feed_images(50, 30);
    pn_eq(json_decode(feed_apt('101')['photos'], true), ['kv_living2']);
});

pn_t('фид: запуск по расписанию — только включённые и не чаще раза в 20 часов', function () {
    $fid = feed_test_setup();
    pn_db()->exec("insert into feeds(name, url, enabled) values ('Выключен', 'https://feed.test/off.xml', 0)");
    $r = pn_feeds_run();
    pn_eq(array_keys($r['feeds']), [$fid]);
    $r = pn_feeds_run();
    pn_eq($r['feeds'], [], 'второй запуск сразу — пропуск');
    $r = pn_feeds_run(true);
    pn_eq(array_keys($r['feeds']), [$fid], 'принудительно');
});

pn_t('фид: раздел админки «Выгрузки» и кнопка «Загрузить сейчас»', function () {
    $fid = feed_test_setup();
    pn_ok(isset(pn_admin_sections()['feeds']), 'раздел есть');
    $GLOBALS['PN_ENT_RESET'] = true;
    $r = pn_crud('feeds', 'POST', (string) $fid, ['do' => 'run'], [], ['id' => 1, 'login' => 't', 'role' => 'admin']);
    pn_eq($r[0], 302);
    pn_eq((int) pn_db()->query("select count(*) from apartments where source = 'feed'")->fetchColumn(), 3);
    $r = forms_parse(pn_entities()['feeds']['fields'], ['name' => 'X', 'url' => 'file:///etc/passwd'], [], []);
    pn_ok(isset($r['errors']['url']), 'только http(s)');
});

pn_t('фид: действия менеджера в админке — «Снять с сайта» и «Проверен» у застройщика', function () {
    $fid = feed_test_setup(); pn_feed_import($fid);
    $u = ['id' => 1, 'login' => 't', 'role' => 'admin']; $GLOBALS['PN_ENT_RESET'] = true;
    $a = feed_apt('101');
    pn_crud('apartments', 'POST', (string) $a['id'], ['do' => 'unpublish'], [], $u);
    pn_eq((int) feed_apt('101')['feed_manual'], 1);
    pn_feed_import($fid);
    pn_eq((int) feed_apt('101')['published'], 0, 'загрузка не возвращает снятую менеджером');
    $did = (int) pn_db()->query("select id from developers where name = 'Новострой-Урал'")->fetchColumn();
    pn_crud('developers', 'POST', (string) $did, ['do' => 'save', 'name' => 'Новострой-Урал', 'verified' => '1'], [], $u);
    pn_eq((int) feed_apt('103')['published'], 1, 'отметка «Проверен» в админке сразу показывает квартиры');
});

pn_t('фид: «квартиры» с явно неверной площадью или ценой за м² пропускаются', function () {
    $mk = fn($area, $price) => '<realty-feed xmlns="http://webmaster.yandex.ru/schemas/feed/realty/2010-06"><offer internal-id="9"><type>продажа</type><category>квартира</category>'
        . "<price><value>$price</value></price><area><value>$area</value></area><rooms>1</rooms><floor>1</floor><floors-total>1</floors-total></offer></realty-feed>";
    $f = tempnam(sys_get_temp_dir(), 'fx');
    foreach ([[1757, 50000000, 0], [5, 900000, 0], [40, 400000, 0], [40, 5000000, 1], [450, 90000000, 1]] as [$a, $p, $ok]) {
        file_put_contents($f, $mk($a, $p));
        pn_eq(count(pn_feed_offers($f)['offers']), $ok, "$a м², $p ₽");
    }
    unlink($f);
});
