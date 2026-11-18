<?php
require_once __DIR__ . '/../app/bootstrap.php';
$GLOBALS['PN_DEMO'] = false; $GLOBALS['PN_CONFIG_RESET'] = true;
pn_t('страница квартиры: заголовок, Offer в рублях', function () {
    pn_test_db();
    [$code, , $html] = pn_route('GET', '/kvartiry/1-zhk-lipovyy-skver/');
    pn_eq($code, 200);
    preg_match('~<title>(.*?)</title>~u', $html, $m);
    foreach (['2-комн.', '58,4 м²', 'Липовый сквер'] as $w) pn_ok(str_contains($m[1] ?? '', $w), "в title нет «{$w}»: " . ($m[1] ?? ''));
    pn_ok(str_contains($html, '"@type":"Offer"') && str_contains($html, '"priceCurrency":"RUB"'), 'нет Offer/RUB');
    pn_ok(str_contains($html, '<base href="../../">'), 'относительная база для подпапки');
    pn_ok(!preg_match('~(href|src)="/(?!/)~', $html), 'абсолютные пути');
});
pn_t('страница дома и 404', function () {
    pn_test_db();
    pn_eq(pn_route('GET', '/doma/severnyy-ural-235/')[0], 200);
    pn_eq(pn_route('GET', '/kvartiry/999-net-takoy/')[0], 404);
    pn_eq(pn_route('GET', '/doma/net-takogo/')[0], 404);
    [$code, $hdr] = pn_route('GET', '/kvartiry/1-zhk-lipovyy-skver');
    pn_eq($code, 301); pn_eq($hdr['Location'] ?? '', '/kvartiry/1-zhk-lipovyy-skver/');
});
pn_t('снятая с публикации квартира — 404', function () {
    $db = pn_test_db(); $db->exec('update apartments set published=0 where id=1');
    pn_eq(pn_route('GET', '/kvartiry/1-zhk-lipovyy-skver/')[0], 404);
});
pn_t('главная: SEO из шаблона, без og:image прототипа', function () {
    pn_test_db();
    [$code, , $html] = pn_route('GET', '/');
    pn_eq($code, 200);
    pn_ok(str_contains($html, '"@type":"RealEstateAgent"'), 'JSON-LD организации');
    pn_ok(!str_contains($html, '08_%D0%A1'), 'ссылка на прототип в og:image');
    pn_ok(!str_contains($html, 'noindex'), 'боевой режим без noindex');
});
pn_t('sitemap: главная + 12 квартир + 5 домов; robots', function () {
    pn_test_db();
    [$code, , $xml] = pn_route('GET', '/sitemap.xml');
    pn_eq($code, 200); pn_eq(substr_count($xml, '<loc>'), 18);
    pn_ok(str_contains(pn_route('GET', '/robots.txt')[2], 'Sitemap:'), 'robots со ссылкой на карту');
});
pn_t('демо: noindex и Disallow', function () {
    pn_test_db();
    $GLOBALS['PN_DEMO'] = true; $GLOBALS['PN_CONFIG_RESET'] = true;
    try {
        pn_ok(str_contains(pn_route('GET', '/kvartiry/1-zhk-lipovyy-skver/')[2], '<meta name="robots" content="noindex">'), 'noindex на странице квартиры');
        pn_eq(trim(pn_route('GET', '/robots.txt')[2]), "User-agent: *\nDisallow: /");
    } finally { $GLOBALS['PN_DEMO'] = false; $GLOBALS['PN_CONFIG_RESET'] = true; }
});
pn_t('сборка: страницы объектов в подпапках', function () {
    pn_test_db();
    $out = __DIR__ . '/_tmp/build_db';
    $r = pn_build($out, 'db');
    pn_eq($r['pages'], 1 + 12 + 5);
    pn_ok(is_file("$out/kvartiry/1-zhk-lipovyy-skver/index.html") && is_file("$out/doma/severnyy-ural-235/index.html"), 'файлы страниц');
});
