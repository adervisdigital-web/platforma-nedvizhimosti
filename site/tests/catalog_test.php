<?php
// Каталог квартир, SEO-страницы подборок и ЖК (2026-11-18).
require_once __DIR__ . '/../app/bootstrap.php';
function pn_cards(string $html): int { return substr_count($html, 'class="ct-card"'); }

pn_t('каталог /kvartiry/: все опубликованные квартиры, заголовок, канонический адрес', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/kvartiry/');
    pn_eq($c, 200); pn_eq(pn_cards($h), 12);
    pn_ok(str_contains($h, '<h1>Квартиры в Екатеринбурге'), 'h1');
    pn_ok(str_contains($h, 'kvartiry/"><meta') || preg_match('~rel="canonical" href="[^"]*kvartiry/"~', $h), 'canonical');
    pn_ok(str_contains($h, '"@type":"ItemList"'), 'ItemList');
});
pn_t('подборки: студии, новостройки, вторичка, 4-комнатные — только свои квартиры', function () {
    pn_test_db();
    $all = Repo::apartments();
    $cnt = fn($f) => count(array_filter($all, $f));
    foreach ([['/kvartiry/studii/', fn($a) => $a['rooms'] === 0, 'Студии'], ['/kvartiry/novostroyki/', fn($a) => $a['market'] === 'new', 'Новостройки'],
              ['/kvartiry/vtorichka/', fn($a) => $a['market'] === 'secondary', 'Вторичка'], ['/kvartiry/4-komnatnye/', fn($a) => $a['rooms'] >= 4, 'Четырёхкомнатные']] as [$p, $f, $t]) {
        [$c, , $h] = pn_route('GET', $p);
        pn_eq($c, 200, $p); pn_eq(pn_cards($h), $cnt($f), $p); pn_ok(str_contains($h, $t), "$p: «{$t}»");
    }
});
pn_t('район: страница есть, у несуществующего района — 404', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/kvartiry/rayon/uralmash/');
    pn_eq($c, 200); pn_ok(pn_cards($h) >= 1, 'квартиры Уралмаша'); pn_ok(str_contains($h, 'Уралмаш'), 'название района');
    pn_eq(pn_route('GET', '/kvartiry/rayon/net-takogo/')[0], 404);
});
pn_t('пустая подборка не публикуется (404), страница квартиры не перекрыта подборкой', function () {
    pn_test_db();
    pn_db()->exec('update apartments set published = 0 where rooms >= 4');
    pn_eq(pn_route('GET', '/kvartiry/4-komnatnye/')[0], 404);
    pn_eq(pn_route('GET', '/kvartiry/1-zhk-lipovyy-skver/')[0], 200);
});
pn_t('страница ЖК: описание, проверки, квартиры, ссылка со страницы квартиры', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/zhk/lipovyy-skver/');
    pn_eq($c, 200);
    pn_ok(str_contains($h, 'Академическом'), 'описание'); pn_ok(str_contains($h, 'Разрешение на строительство'), 'проверки');
    pn_eq(pn_cards($h), 2);
    pn_eq(pn_route('GET', '/zhk/net-takogo/')[0], 404);
    pn_ok(str_contains(pn_route('GET', '/kvartiry/1-zhk-lipovyy-skver/')[2], 'href="zhk/lipovyy-skver/"'), 'ссылка на ЖК со страницы квартиры');
});
pn_t('фильтр в адресе — noindex, без фильтра — индексируется', function () {
    pn_test_db();
    pn_ok(str_contains(pn_route('GET', '/kvartiry/?pmax=6000000')[2], 'noindex'), 'с фильтром');
    pn_ok(!str_contains(pn_route('GET', '/kvartiry/')[2], 'noindex'), 'без фильтра');
});
pn_t('sitemap: подборки и ЖК', function () {
    pn_test_db();
    $x = pn_sitemap();
    foreach (['kvartiry/</loc>', 'kvartiry/studii/', 'kvartiry/rayon/uralmash/', 'zhk/lipovyy-skver/'] as $s) pn_ok(str_contains($x, $s), "нет $s");
});
pn_t('сборка витрины: страницы каталога и ЖК', function () {
    pn_test_db();
    $p = pn_build_pages([]);
    foreach (['kvartiry/index.html', 'kvartiry/studii/index.html', 'kvartiry/rayon/uralmash/index.html', 'zhk/lipovyy-skver/index.html'] as $k)
        pn_ok(isset($p[$k]), "нет $k");
});
