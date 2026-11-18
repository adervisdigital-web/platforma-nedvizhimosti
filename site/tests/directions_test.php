<?php
// Блок «Квартира. Дом. Ремонт.» на главной: ссылки, живые цифры, до/после, путь клиента, застройщики (2026-11-18).
require_once __DIR__ . '/../app/bootstrap.php';
function pn_partners_html(): string {
    $h = pn_route('GET', '/')[2];
    preg_match('~<section class="sec" id="partners">.*?</section>~s', $h, $m);
    return $m[0] ?? '';
}

pn_t('карточки ведут на страницы и показывают цифры из базы', function () {
    pn_test_db();
    $h = pn_partners_html();
    foreach (['href="kvartiry/"', 'href="doma/"', 'href="remont/"', '12 квартир', 'от 4,39 млн ₽', '5 проектов', 'от 20 000 ₽'] as $s) pn_ok(str_contains($h, $s), "нет «{$s}»");
    pn_db()->exec('update apartments set published = 0 where id in (1, 2)');
    pn_ok(str_contains(pn_partners_html(), '10 квартир'), 'цифра меняется вместе с базой');
});
pn_t('ремонт: до и после из одной пары фото', function () {
    pn_test_db();
    $h = pn_partners_html();
    pn_ok(str_contains($h, 'ba_before.jpg') && str_contains($h, 'ba_after.jpg'), 'пара фото');
});
pn_t('путь клиента: шаги-ссылки и «Один менеджер на всё» открывает заявку с пакетом', function () {
    pn_test_db();
    $h = pn_partners_html();
    foreach (['class="stp" href="kvartiry/"', 'class="stp" href="ipoteka/"', 'class="stp" href="remont/"', 'href="#lead" data-pack'] as $s) pn_ok(str_contains($h, $s), "нет «{$s}»");
});
pn_t('застройщики: без квартир — названия текстом; с квартирами — ссылка на их страницу', function () {
    pn_test_db();
    $h = pn_partners_html();
    pn_ok(str_contains($h, '<span>Брусника</span>'), 'запасной список текстом');
    pn_ok(!str_contains($h, 'zastroyshchiki/'), 'ссылок нет');
    $db = pn_db();
    $db->exec("insert into developers(name, verified) values ('Тест Девелопмент', 1)");
    $db->exec('update complexes set developer_id = ' . (int) $db->lastInsertId() . " where slug = 'zhk-lipovyy-skver'");
    $h = pn_partners_html();
    pn_ok(str_contains($h, 'href="zastroyshchiki/test-development/"'), 'ссылка на застройщика');
    [$c, , $p] = pn_route('GET', '/zastroyshchiki/test-development/');
    pn_eq($c, 200); pn_eq(substr_count($p, 'class="ct-card"'), 2); pn_ok(str_contains($p, 'Квартиры от застройщика Тест Девелопмент'), 'h1');
    pn_eq(pn_route('GET', '/zastroyshchiki/net-takogo/')[0], 404);
});
