<?php
require_once __DIR__ . '/../app/bootstrap.php';
pn_t('layout: все секции прототипа, стиль и один app.js', function () {
    $html = pn_render('layout', pn_page_vars());
    foreach (['search', 'list', 'how', 'partners', 'calc', 'houses', 'ba', 'cab', 'rev', 'pact', 'lead'] as $id)
        pn_ok(str_contains($html, "id=\"$id\""), "нет секции $id");
    pn_ok(str_contains($html, 'href="assets/css/site.css"'), 'нет site.css');
    pn_eq(substr_count($html, 'src="assets/js/app.js"'), 1, 'app.js подключён один раз');
    pn_ok(!preg_match('~(src|href)="photo/~', $html), 'остались относительные пути photo/');
    pn_ok(!str_contains($html, '<style>'), 'остался встроенный стиль');
});
pn_t('bundle: app.js = склейка src/js по порядку', function () {
    $dir = pn_config()['root'] . '/src/js';
    $order = json_decode(file_get_contents("$dir/order.json"), true);
    pn_ok(count($order) > 10, 'файлов JS');
    $want = implode('', array_map(fn($f) => file_get_contents("$dir/$f"), $order));
    pn_eq(pn_bundle_js(), $want);
    pn_ok(str_contains($want, 'const ITEMS = PN.items()'), 'данные через PN');
});
