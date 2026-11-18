<?php
require_once __DIR__ . '/../app/bootstrap.php';
function pn_admin_fixture(): void {
    pn_test_db();
    pn_db()->prepare('insert into users(login,password_hash,role) values (?,?,?)')->execute(['boss', password_hash('p', PASSWORD_DEFAULT), 'admin']);
    $_SESSION = []; Auth::login('boss', 'p');
    $GLOBALS['PN_UPLOADS'] = __DIR__ . '/_tmp/uploads';
}
function pn_post(string $path, array $post, array $files = []): array { return pn_route('POST', $path, $post + ['_csrf' => csrf_token()], $files); }
function pn_apt_post(array $over = []): array {
    $cx = (int) pn_db()->query("select id from complexes where slug='zhk-kvarts'")->fetchColumn();
    return $over + ['do' => 'save', 'market' => 'new', 'rooms' => '2', 'area' => '61,5', 'floor' => '5', 'floors' => '16', 'complex_id' => (string) $cx,
        'district' => '', 'price' => '9 450 000', 'discount_pct' => '', 'finish' => 'with', 'house_status' => 'Дом сдан', 'due' => '', 'photos' => ['kv_living2'],
        'description' => 'Светлая двушка', 'published' => '1'];
}
pn_t('числа из формы: запятая и пробелы', function () {
    pn_eq(forms_number('58,4'), 58.4);
    pn_eq(forms_number('9 450 000'), 9450000.0);
    pn_eq(forms_number(' 9 450 000 ₽ '), 9450000.0);
    pn_eq(forms_number(''), null);
    pn_eq(forms_number('abc'), null);
});
pn_t('квартира без цены — ошибка «Укажите цену», в базу не попадает', function () {
    pn_admin_fixture();
    $r = forms_apartment(pn_apt_post(['price' => '']));
    pn_eq($r['errors']['price'] ?? null, 'Укажите цену');
    $before = (int) pn_db()->query('select count(*) from apartments')->fetchColumn();
    [$code, , $html] = pn_post('/admin/apartments/new', pn_apt_post(['price' => '']));
    pn_eq($code, 200); pn_ok(str_contains($html, 'Укажите цену'), 'ошибка на форме');
    pn_eq((int) pn_db()->query('select count(*) from apartments')->fetchColumn(), $before);
});
pn_t('новостройка без ЖК и публикация без фото — ошибки', function () {
    pn_admin_fixture();
    pn_eq(forms_apartment(pn_apt_post(['complex_id' => '']))['errors']['complex_id'] ?? null, 'Выберите ЖК');
    pn_eq(forms_apartment(pn_apt_post(['photos' => []]))['errors']['photos'] ?? null, 'Чтобы опубликовать, добавьте хотя бы одно фото');
    pn_eq(forms_apartment(pn_apt_post(['floor' => '17']))['errors']['floor'] ?? null, 'Этаж больше, чем этажей в доме');
});
pn_t('квартира из админки появляется в API и на своей странице', function () {
    pn_admin_fixture();
    [$code, $h] = pn_post('/admin/apartments/new', pn_apt_post());
    pn_eq($code, 302);
    $id = (int) pn_db()->query('select max(id) from apartments')->fetchColumn();
    $a = pn_db()->query("select * from apartments where id = $id")->fetch();
    pn_eq([(float) $a['area'], (int) $a['price']], [61.5, 9450000]);
    pn_eq($a['slug'], "$id-zhk-kvarts");
    pn_ok(in_array("$id-zhk-kvarts", array_column(json_decode(pn_api('items')[1], true), 'slug'), true), 'в api/items');
    pn_eq(pn_route('GET', "/kvartiry/$id-zhk-kvarts/")[0], 200);
    pn_ok((int) pn_db()->query("select count(*) from audit where entity='apartments' and entity_id=$id")->fetchColumn() >= 1, 'запись в журнале');
});
pn_t('копия квартиры — неопубликованная, со своим адресом', function () {
    pn_admin_fixture();
    [$code] = pn_post('/admin/apartments/1', ['do' => 'copy']);
    pn_eq($code, 302);
    $c = pn_db()->query('select * from apartments order by id desc limit 1')->fetch();
    pn_eq((int) $c['published'], 0); pn_ok($c['slug'] !== '1-zhk-lipovyy-skver', 'новый slug');
});
pn_t('снять с публикации → пропадает с сайта; журнал пишет изменение', function () {
    pn_admin_fixture();
    pn_post('/admin/apartments/1', ['do' => 'unpublish']);
    pn_eq(pn_route('GET', '/kvartiry/1-zhk-lipovyy-skver/')[0], 404);
    pn_eq(pn_db()->query("select action from audit where entity='apartments' and entity_id=1 order by id desc")->fetchColumn(), 'unpublish');
});
pn_t('загрузка фото в форме квартиры', function () {
    pn_admin_fixture();
    $tmp = __DIR__ . '/_tmp/up.png'; copy(__DIR__ . '/fixtures/small.png', $tmp);
    $files = ['upload' => ['name' => ['small.png'], 'tmp_name' => [$tmp], 'error' => [UPLOAD_ERR_OK], 'size' => [filesize($tmp)], 'type' => ['image/png']]];
    pn_post('/admin/apartments/1', pn_apt_post(['photos' => ['kv_living2']]), $files);
    $ph = json_decode(pn_db()->query('select photos from apartments where id=1')->fetchColumn(), true);
    pn_eq(count($ph), 2); pn_ok(str_starts_with($ph[1], 'u/'), 'загруженное фото в конце списка');
});
pn_t('ЖК с квартирами не удаляется — понятное сообщение', function () {
    pn_admin_fixture();
    $cx = (int) pn_db()->query("select id from complexes where slug='zhk-kvarts'")->fetchColumn();
    [$code, $h] = pn_post("/admin/complexes/$cx", ['do' => 'delete']);
    pn_eq($code, 302);
    pn_ok((bool) pn_db()->query("select 1 from complexes where id=$cx")->fetchColumn(), 'ЖК на месте');
    pn_ok(str_contains((string) ($_SESSION['flash'] ?? ''), 'есть квартиры'), 'сообщение: ' . ($_SESSION['flash'] ?? ''));
});
pn_t('настройки: секрет не затирается пустым полем, цены ремонта — числами', function () {
    pn_admin_fixture();
    pn_post('/admin/settings', ['do' => 'save', 'phone' => '+7 965 500-29-18', 'tg_token' => '123:abc', 'renovation_prices' => '20 000; 45000; 80 000']);
    pn_post('/admin/settings', ['do' => 'save', 'phone' => '+7 965 500-29-18', 'tg_token' => '', 'renovation_prices' => '20000;45000;80000']);
    $s = Repo::settingsAll();
    pn_eq($s['tg_token'], '123:abc'); pn_eq($s['renovation_prices'], [20000, 45000, 80000]); pn_eq($s['phone_tel'], '+79655002918');
});
pn_t('страницы разделов открываются', function () {
    pn_admin_fixture();
    foreach (['apartments', 'apartments/new', 'apartments/1', 'complexes', 'developers', 'houses', 'houses/1', 'reviews', 'settings', 'users'] as $p)
        pn_eq(pn_route('GET', "/admin/$p")[0], 200, $p);
});
