<?php
require_once __DIR__ . '/../app/bootstrap.php';
// Страницы «Риелторам» и «Застройщикам» (2026-11-21): позиционирование «отдел продаж на аутсорсинге», заявка-партнёрство, условия из настроек.

pn_t('«Риелторам»: страница, заявка «Стать партнёром», пометки вместо незаданных условий', function () {
    pn_test_db();
    [$c, , $h] = pn_route('GET', '/rieltoram/');
    pn_eq($c, 200);
    pn_ok(str_contains($h, '<h1>Риелторам'), 'h1');
    pn_ok(str_contains($h, 'data-want="Риелтор: партнёрство с Платформой"'), 'заявка');
    foreach (['[ВОЗНАГРАЖДЕНИЕ]', '[СРОК ЗАКРЕПЛЕНИЯ]', '[КОГДА ВЫПЛАТА]'] as $p) pn_ok(str_contains($h, $p), "пометка $p");
    pn_ok(str_contains($h, 'rel="canonical"') && str_contains($h, 'rieltoram/'), 'canonical');
    pn_eq(pn_route('GET', '/rieltoram')[0], 301);
});
pn_t('«Риелторам»: условия из админки заменяют пометки', function () {
    $db = pn_test_db();
    $set = $db->prepare('insert or replace into settings(key, value) values (?, ?)');
    $set->execute(['realtor_fee', pn_json_enc('50 % комиссии застройщика')]);
    $set->execute(['realtor_hold', pn_json_enc('90 дней')]);
    $set->execute(['realtor_payout', pn_json_enc('после оплаты застройщика')]);
    [, , $h] = pn_route('GET', '/rieltoram/');
    pn_ok(str_contains($h, '50 % комиссии застройщика') && str_contains($h, '90 дней') && str_contains($h, 'после оплаты застройщика'), 'условия');
    pn_ok(!str_contains($h, '[ВОЗНАГРАЖДЕНИЕ]'), 'без пометки');
    pn_ok(isset(pn_settings_fields()['realtor_fee'], pn_settings_fields()['realtor_hold'], pn_settings_fields()['realtor_payout'], pn_settings_fields()['dev_terms']), 'поля в настройках');
});
pn_t('«Застройщикам»: отдел продаж на аутсорсинге, модель оплаты из настроек', function () {
    $db = pn_test_db();
    [$c, , $h] = pn_route('GET', '/zastroyshchikam/');
    pn_eq($c, 200);
    pn_ok(str_contains($h, 'Отдел продаж на аутсорсинге'), 'h1'); pn_ok(str_contains($h, '[МОДЕЛЬ ОПЛАТЫ]'), 'пометка');
    pn_ok(str_contains($h, 'data-want="Застройщик: отдел продаж на аутсорсинге"'), 'заявка');
    $db->prepare('insert or replace into settings(key, value) values (?, ?)')->execute(['dev_terms', pn_json_enc('только за проданные квартиры')]);
    pn_ok(str_contains(pn_route('GET', '/zastroyshchikam/')[2], 'только за проданные квартиры'), 'условия');
});
pn_t('ссылки «Риелторам» и «Застройщикам»: главная, подвал, меню телефона, карта сайта', function () {
    pn_test_db();
    [, , $h] = pn_route('GET', '/');
    pn_ok(substr_count($h, 'href="rieltoram/"') >= 3, 'главная: блок, подвал, меню — ' . substr_count($h, 'href="rieltoram/"'));
    pn_ok(substr_count($h, 'href="zastroyshchikam/"') >= 3, 'застройщикам');
    [, , $p] = pn_route('GET', '/remont/');
    pn_ok(str_contains($p, 'href="rieltoram/"'), 'подстраница');
    $sm = pn_sitemap();
    pn_ok(str_contains($sm, 'rieltoram/') && str_contains($sm, 'zastroyshchikam/'), 'sitemap');
    pn_ok(in_array('rieltoram/', pn_catalog_paths(), true), 'сборка витрины');
});
