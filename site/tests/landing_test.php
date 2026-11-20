<?php
// Страницы для карточек главной: подборки (готовые, с отделкой, семейная ипотека, скидки), /doma/, /remont/, /ipoteka/ (2026-11-18).
require_once __DIR__ . '/../app/bootstrap.php';

pn_t('новые подборки: готовые новостройки, с отделкой, семейная ипотека, скидки', function () {
    pn_test_db();
    $all = Repo::apartments(); $cnt = fn($f) => count(array_filter($all, $f));
    foreach ([['/kvartiry/gotovye-novostroyki/', fn($a) => $a['market'] === 'new' && !$a['due'], 'сданных'],
              ['/kvartiry/s-otdelkoy/', fn($a) => $a['finish'] === 'with', 'отделкой'],
              ['/kvartiry/semeynaya-ipoteka/', fn($a) => $a['market'] === 'new', 'семейную ипотеку'],
              ['/kvartiry/skidki/', fn($a) => $a['discount_pct'] > 0 || $a['special'], 'Скидки']] as [$p, $f, $t]) {
        [$c, , $h] = pn_route('GET', $p);
        pn_eq($c, 200, $p); pn_eq(substr_count($h, 'class="ct-card"'), $cnt($f), $p); pn_ok(str_contains($h, $t), "$p: «{$t}»");
    }
    pn_ok(str_contains(pn_route('GET', '/kvartiry/semeynaya-ipoteka/')[2], 'ct-fam'), 'блок условий семейной ипотеки');
});
pn_t('/doma/: все проекты, фильтр по линейке, рассрочка', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/doma/');
    pn_eq($c, 200); pn_eq(substr_count($h, 'class="dm-card"'), count(Repo::houses()));
    pn_ok(str_contains($h, 'data-line') && str_contains($h, 'Рассрочка'), 'фильтр и рассрочка');
});
pn_t('/remont/: три уровня с ценами из настроек и калькулятор', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/remont/');
    pn_eq($c, 200);
    foreach (['20 000 ₽/м²', '45 000 ₽/м²', '80 000 ₽/м²', 'data-ren', 'Замер <b>бесплатно</b>', 'около 6 месяцев'] as $s) pn_ok(str_contains($h, $s), "нет «{$s}»");
    pn_ok(!str_contains($h, 'этап, гарантия 5 лет') && !str_contains($h, 'Гарантия <b>5 лет') && !str_contains($h, '<dt>Гарантия</dt>'), 'срок гарантии на ремонт заказчик не подтвердил');
});
pn_t('/ipoteka/: программы из настроек, калькулятор с ценой, банки', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/ipoteka/');
    pn_eq($c, 200);
    foreach (['Семейная', 'IT-ипотека', 'data-mort', 'data-i="price"', 'ДОМ.РФ', 'kvartiry/semeynaya-ipoteka/'] as $s) pn_ok(str_contains($h, $s), "нет «{$s}»");
});
pn_t('карточки главной ведут на страницы, а не фильтруют список', function () {
    pn_test_db();
    $h = pn_route('GET', '/')[2];
    foreach (['kvartiry/skidki/', 'kvartiry/gotovye-novostroyki/', 'kvartiry/s-otdelkoy/', 'kvartiry/semeynaya-ipoteka/', 'kvartiry/vtorichka/', 'href="doma/"', 'href="remont/"', 'href="ipoteka/"'] as $s)
        pn_ok(str_contains($h, $s), "нет ссылки $s");
    pn_ok(!preg_match('~class="cat[^"]*"[^>]*data-f=~', $h), 'data-f остался у карточки');
});
pn_t('sitemap и сборка: дома, ремонт, ипотека, новые подборки', function () {
    pn_test_db();
    $x = pn_sitemap();
    foreach (['doma/</loc>', 'remont/</loc>', 'ipoteka/</loc>', 'kvartiry/skidki/'] as $s) pn_ok(str_contains($x, $s), "sitemap: нет $s");
    $p = pn_build_pages([]);
    foreach (['doma/index.html', 'remont/index.html', 'ipoteka/index.html', 'kvartiry/semeynaya-ipoteka/index.html'] as $k) pn_ok(isset($p[$k]), "сборка: нет $k");
});
