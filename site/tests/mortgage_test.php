<?php
// Ипотека с лимитами и семейной по числу детей (2026-11-19).
require_once __DIR__ . '/../app/bootstrap.php';
require_once __DIR__ . '/admin_test.php';
function pn_mort_s(): array {
    return ['mortgage_programs' => [['name' => 'Семейная', 'rate' => 10, 'limit' => 6000000], ['name' => 'IT-ипотека', 'rate' => 6, 'limit' => 9000000], ['name' => 'Рыночная', 'rate' => 18.8]],
        'family_tiers' => [['kids' => 1, 'rate' => 10, 'limit' => 6000000], ['kids' => 2, 'rate' => 8, 'limit' => 8000000], ['kids' => 3, 'rate' => 6, 'limit' => 10000000],
            ['kids' => 4, 'rate' => 4, 'limit' => 10000000], ['kids' => 5, 'rate' => 2, 'limit' => 10000000]]];
}
pn_t('аннуитет: 6 млн, 6 %, 25 лет = 38 658 ₽ (сверено с калькулятором банка)', function () {
    pn_eq((int) round(pn_ann(6000000, 6, 300)), 38658);
});
pn_t('семейная, 1 ребёнок: 9 млн, взнос 20 % → 6 млн по 10 % + 1,2 млн по рыночной', function () {
    $s = pn_mort_s(); $r = pn_mort_pay(9000000, $s['mortgage_programs'][0], $s, 1);
    pn_eq($r['parts'], [[6000000, 10.0], [1200000.0, 18.8]]);
    pn_eq($r['pay'], (int) round(pn_ann(6000000, 10, 360) + pn_ann(1200000, 18.8, 360)));
});
pn_t('семейная, 2 ребёнка: лимит 8 млн — весь кредит 7,2 млн по 8 %; 5+ детей — 2 %', function () {
    $s = pn_mort_s(); $p = $s['mortgage_programs'][0];
    pn_eq(pn_mort_pay(9000000, $p, $s, 2)['parts'], [[7200000.0, 8.0]]);
    pn_eq(pn_prog_terms($p, $s, 7)['rate'], 2.0);
});
pn_t('IT: лимит 9 млн; рыночная — без лимита', function () {
    $s = pn_mort_s();
    pn_eq(count(pn_mort_pay(15000000, $s['mortgage_programs'][1], $s)['parts']), 2);
    pn_eq(count(pn_mort_pay(30000000, $s['mortgage_programs'][2], $s)['parts']), 1);
});
pn_t('админка: программы «название | ставка | лимит, млн», ступени семейной и дата ставок', function () {
    pn_admin_fixture();
    pn_post('/admin/settings', ['do' => 'save', 'phone' => '+7 965 500-29-18', 'renovation_prices' => '20000;45000;80000',
        'mortgage_programs' => "Семейная | 10 | 6\nIT-ипотека | 6 | 9\nРыночная | 18,8", 'family_tiers' => "1 | 10 | 6\n2 | 8 | 8\n3 | 6 | 10", 'rates_date' => '18.11.2026']);
    $s = Repo::settingsAll();
    pn_eq($s['mortgage_programs'][0], ['name' => 'Семейная', 'rate' => 10, 'limit' => 6000000]);
    pn_eq($s['mortgage_programs'][2], ['name' => 'Рыночная', 'rate' => 18.8]);
    pn_eq($s['family_tiers'][1], ['kids' => 2, 'rate' => 8, 'limit' => 8000000]);
    pn_eq($s['rates_date'], '2026-11-18');
});
pn_t('карточка в каталоге: платёж новостройки — по семейной с лимитом, вторички — по рыночной', function () {
    pn_test_db();
    $s = Repo::settingsAll(); $a = Repo::apartments()[0];
    pn_eq(pn_apt_pay($a, $s), pn_mort_pay($a['price'], pn_default_prog($a, $s), $s)['pay']);
});
pn_t('обзор: напоминание, если ставки старше 30 дней', function () {
    pn_admin_fixture();
    pn_db()->prepare("update settings set value = ? where key = 'rates_date'")->execute([json_encode('2026-01-01')]);
    pn_ok(str_contains(pn_route('GET', '/admin/overview')[2], 'Ставки ипотеки актуальны'), 'пункт про ставки');
});
