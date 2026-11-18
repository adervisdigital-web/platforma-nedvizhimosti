<?php
require_once __DIR__ . '/../app/bootstrap.php';
pn_t('db-источник = seed для страницы (те же 12 карточек, дома, отзывы)', function () {
    pn_test_db();
    $a = pn_page_data(pn_db_source(), pn_config()); $b = pn_page_data(pn_seed_all(), pn_config());
    pn_eq($a['items'], $b['items'], 'квартиры');
    pn_eq($a['houses'], $b['houses'], 'дома');
    pn_eq(count($a['reviews']), count($b['reviews']), 'отзывы');
    pn_eq($a['progs'], $b['progs'], 'программы ипотеки');
});
pn_t('api/items: снятая с публикации квартира не видна', function () {
    $db = pn_test_db();
    $db->exec("update apartments set published=0 where id=2");
    [$code, $body] = pn_api('items');
    pn_eq($code, 200); $items = json_decode($body, true);
    pn_eq(count($items), 11); pn_ok(!in_array('2-zhk-severnyy-bulvar', array_column($items, 'slug'), true), 'снятая квартира в выдаче');
});
pn_t('api/reviews: демо-отзывы скрыты, когда show_demo_reviews=0', function () {
    $db = pn_test_db();
    pn_eq(count(json_decode(pn_api('reviews')[1], true)), 5);
    $db->exec("update settings set value='0' where key='show_demo_reviews'");
    pn_eq(count(json_decode(pn_api('reviews')[1], true)), 0);
});
pn_t('api/settings: без секретов', function () {
    $db = pn_test_db();
    $db->exec("insert into settings(key,value) values ('tg_token','\"123:abc\"'),('smtp_pass','\"x\"'),('crm_url','\"http://crm\"')");
    $s = json_decode(pn_api('settings')[1], true);
    foreach (array_keys($s) as $k) pn_ok(!preg_match('/^(tg_|smtp_|crm_|salt)/', $k), "секрет в выдаче: $k");
    pn_eq($s['phone'], '+7 965 500-29-18');
});
pn_t('api: неизвестный путь → 404', function () {
    pn_test_db();
    [$code, $body] = pn_api('nope');
    pn_eq($code, 404); pn_eq(json_decode($body, true), ['error' => 'not_found']);
});
