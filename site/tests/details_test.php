<?php
// Подробные страницы квартиры и дома, планировки, обзор админки (2026-11-18, вторая доработка).
require_once __DIR__ . '/../app/bootstrap.php';
require_once __DIR__ . '/admin_test.php';

pn_t('демо-подробности квартиры: площади, планировка, описание, несколько фото', function () {
    pn_test_db();
    $a = pn_db()->query('select * from apartments where id = 1')->fetch();
    pn_eq((float) $a['kitchen_area'] > 5, true, 'кухня');
    pn_eq(json_decode($a['plans'], true), ['plans/apt-1.svg']);
    pn_ok(mb_strlen((string) $a['description']) > 100, 'описание');
    pn_ok(count(json_decode($a['photos'], true)) >= 3, 'фото');
    pn_ok((float) $a['living_area'] + (float) $a['kitchen_area'] < (float) $a['area'], 'жилая + кухня меньше общей');
});
pn_t('подробности не затирают правки менеджера при повторной загрузке', function () {
    pn_test_db();
    pn_db()->exec("update apartments set description = 'Своё описание', living_area = 30 where id = 1");
    pn_eq(pn_seed_details(pn_db(), true), 0);
    pn_eq(pn_db()->query('select description from apartments where id = 1')->fetchColumn(), 'Своё описание');
});
pn_t('svg-планировка отдаётся как файл, без .jpg', function () {
    pn_eq(pn_img_attrs('plans/apt-1.svg'), 'src="assets/img/plans/apt-1.svg"');
});
pn_t('страница квартиры: галерея, планировка, характеристики, ипотека, похожие', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/kvartiry/1-zhk-lipovyy-skver/');
    pn_eq($c, 200);
    foreach (['data-gal', 'assets/img/plans/apt-1.svg', 'О квартире', 'Кухня', 'Санузел', 'data-mort', 'Похожие квартиры', 'kv_kitchen2'] as $s)
        pn_ok(str_contains($h, $s), "нет «{$s}»");
});
pn_t('квартира без отделки: блок ремонта с ценами из настроек', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/kvartiry/2-zhk-severnyy-bulvar/');
    pn_eq($c, 200); pn_ok(str_contains($h, 'Ремонт под ключ'), 'блок ремонта');
});
pn_t('страница дома: вкладки планировок, рассрочка, другие проекты', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/doma/severnyy-ural-235/');
    pn_eq($c, 200);
    foreach (['data-gal', 'Планировки', 'data-inst', 'Другие проекты', 'n235_p1'] as $s) pn_ok(str_contains($h, $s), "нет «{$s}»");
});
pn_t('админка: поля подробностей в форме квартиры и раздел «Обзор»', function () {
    pn_admin_fixture();
    [$c, , $h] = pn_route('GET', '/admin/apartments/1');
    pn_eq($c, 200); pn_ok(str_contains($h, 'name="kitchen_area"') && str_contains($h, 'name="plans[]"'), 'поля');
    [$c, , $h] = pn_route('GET', '/admin/overview');
    pn_eq($c, 200);
    foreach (['Заявки за 14 дней', 'Перед запуском', 'Журнал действий'] as $s) pn_ok(str_contains($h, $s), "нет «{$s}»");
});
pn_t('сохранение подробностей квартиры из админки', function () {
    pn_admin_fixture();
    pn_post('/admin/apartments/1', pn_apt_post(['kitchen_area' => '12,5', 'living_area' => '30', 'bathroom' => 'раздельный', 'plans' => ['plans/apt-1.svg']]));
    $a = pn_db()->query('select kitchen_area, bathroom, plans from apartments where id = 1')->fetch();
    pn_eq([(float) $a['kitchen_area'], $a['bathroom'], json_decode($a['plans'], true)], [12.5, 'раздельный', ['plans/apt-1.svg']]);
});
