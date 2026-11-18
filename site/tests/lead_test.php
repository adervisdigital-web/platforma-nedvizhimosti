<?php
require_once __DIR__ . '/../app/bootstrap.php';
$ok = fn(array $o = []) => $o + ['kind' => 'quiz', 'want' => 'Квартиру', 'budget' => 'до 9 млн ₽', 'area' => '1, 2 комн.', 'name' => 'Анна',
    'phone' => '+7 (965) 500-29-18', 'consent' => '1', 'hp' => '', 't0' => 1_000_000 - 30];
pn_t('телефон: разные записи → +7XXXXXXXXXX', function () {
    pn_eq(phone_norm('8 (965) 500-29-18'), '+79655002918');
    pn_eq(phone_norm('+7 965 500 29 18'), '+79655002918');
    pn_eq(phone_norm('9655002918'), '+79655002918');
    pn_eq(phone_norm('+7 (343) 222-33-44'), '+73432223344', 'городской Екатеринбург');
    pn_eq(phone_norm('12345'), null);
    pn_eq(phone_norm('+44 20 7946 0958'), null, 'иностранный');
    pn_eq(phone_norm('+7 (123) 456-78-90'), null, 'несуществующий код');
});
pn_t('валидная заявка сохраняется первой, со статусом new', function () use ($ok) {
    pn_test_db();
    $r = lead_accept($ok(), '10.0.0.1', 1_000_000);
    pn_eq($r['ok'], true); pn_eq($r['message'], 'Заявка принята, перезвоним до 21:00');
    $l = pn_db()->query('select * from leads where id = ' . (int) $r['id'])->fetch();
    pn_eq([$l['status'], $l['phone'], (int) $l['delivered_tg']], ['new', '+79655002918', 2], 'Telegram в тестовой базе не настроен → 2');
    pn_ok($l['ip_hash'] !== '10.0.0.1' && strlen($l['ip_hash']) === 64, 'IP хранится хэшем');
});
pn_t('без согласия, ловушка, слишком быстро, плохой телефон — отказ без записи', function () use ($ok) {
    pn_test_db();
    pn_eq(lead_accept($ok(['consent' => '']), '1.1.1.1', 1_000_000)['error'], 'consent');
    pn_eq(lead_accept($ok(['hp' => 'http://spam']), '1.1.1.1', 1_000_000)['ok'], false);
    pn_eq(lead_accept($ok(['t0' => 1_000_000 - 1]), '1.1.1.1', 1_000_000)['error'], 'too_fast');
    pn_eq(lead_accept($ok(['phone' => '123']), '1.1.1.1', 1_000_000)['error'], 'phone');
    pn_eq(lead_accept($ok(['kind' => 'hack']), '1.1.1.1', 1_000_000)['error'], 'kind');
    pn_eq((int) pn_db()->query('select count(*) from leads')->fetchColumn(), 0);
});
pn_t('6-я заявка за час с одного IP — rate; через час снова можно', function () use ($ok) {
    pn_test_db();
    for ($i = 0; $i < 5; $i++) pn_eq(lead_accept($ok(), '2.2.2.2', 1_000_000 + $i)['ok'], true);
    pn_eq(lead_accept($ok(), '2.2.2.2', 1_000_000 + 10)['error'], 'rate');
    pn_eq(lead_accept($ok(), '3.3.3.3', 1_000_000 + 10)['ok'], true, 'другой IP');
    pn_eq(lead_accept($ok(['t0' => 1_000_000 + 3700]), '2.2.2.2', 1_000_000 + 3700 + 30)['ok'], true, 'через час');
});
pn_t('запись на просмотр: слот и файл календаря', function () use ($ok) {
    pn_test_db();
    $r = lead_accept($ok(['kind' => 'viewing', 'object_ref' => 'kvartiry/1-zhk-lipovyy-skver', 'slot' => '2026-11-19 10:00']), '4.4.4.4', 1_000_000);
    pn_ok($r['ok'] && str_contains($r['ics'] ?? '', 'DTSTART:20261119T050000Z'), 'ics: ' . ($r['ics'] ?? '—'));
});
pn_t('API: POST /api/lead → 200/400/429 и JSON', function () use ($ok) {
    pn_test_db(); $GLOBALS['PN_NOW'] = 1_000_000; $_SERVER['REMOTE_ADDR'] = '5.5.5.5';
    try {
        [$c, , $b] = pn_route('POST', '/api/lead', $ok()); pn_eq($c, 200); pn_eq(json_decode($b, true)['ok'], true);
        pn_eq(pn_route('POST', '/api/lead', $ok(['phone' => '1']))[0], 400);
        for ($i = 0; $i < 4; $i++) pn_route('POST', '/api/lead', $ok());
        [$c, , $b] = pn_route('POST', '/api/lead', $ok()); pn_eq($c, 429); pn_ok(str_contains(json_decode($b, true)['message'], '+7 965 500-29-18'), 'телефон в отказе');
        pn_eq(pn_route('GET', '/api/lead')[0], 405);
    } finally { unset($GLOBALS['PN_NOW'], $_SERVER['REMOTE_ADDR']); }
});
