<?php
require_once __DIR__ . '/../app/bootstrap.php';
function pn_deliver_fixture(array $settings = []): int {
    $db = pn_test_db();
    $set = $db->prepare('insert into settings(key,value) values (?,?) on conflict(key) do update set value = excluded.value');
    foreach ($settings + ['tg_token' => '123:abc', 'tg_chat_id' => '-100500', 'mail_to' => 'sales@example.ru', 'crm_enabled' => 0] as $k => $v) $set->execute([$k, pn_json_enc($v)]);
    $GLOBALS['PN_HTTP_LOG'] = []; $GLOBALS['PN_MAIL_LOG'] = [];
    $GLOBALS['PN_HTTP'] = function ($m, $url, $h, $body) { $GLOBALS['PN_HTTP_LOG'][] = [$url, $body]; return [$GLOBALS['PN_HTTP_CODE'] ?? 200, '{"ok":true}']; };
    $GLOBALS['PN_MAIL'] = function ($to, $subj, $body) { $GLOBALS['PN_MAIL_LOG'][] = [$to, $subj, $body]; return true; };
    $db->prepare("insert into leads(kind,want,budget,phone,object_ref) values ('quiz','Квартиру','до 9 млн ₽','+79655002918','kvartiry/1-zhk-lipovyy-skver')")->execute();
    return (int) $db->lastInsertId();
}
pn_t('Telegram отвечает 500 → не доставлена, повтор доставляет', function () {
    $id = pn_deliver_fixture(); $GLOBALS['PN_HTTP_CODE'] = 500;
    deliver_lead($id);
    $l = pn_db()->query("select * from leads where id=$id")->fetch();
    pn_eq([(int) $l['delivered_tg'], (int) $l['delivered_mail'], (int) $l['attempts']], [0, 1, 1]);
    pn_ok(str_contains($GLOBALS['PN_HTTP_LOG'][0][1], '+7 (965) 500-29-18'), 'телефон в сообщении');
    pn_ok(str_contains($GLOBALS['PN_HTTP_LOG'][0][1], 'kvartiry/1-zhk-lipovyy-skver'), 'ссылка на объект');
    $GLOBALS['PN_HTTP_CODE'] = 200;
    pn_eq(deliver_pending(), 1);
    pn_eq((int) pn_db()->query("select delivered_tg from leads where id=$id")->fetchColumn(), 1);
    pn_eq(count($GLOBALS['PN_MAIL_LOG']), 1, 'письмо повторно не шлётся');
    pn_eq(deliver_pending(), 0, 'больше нечего повторять');
});
pn_t('CRM выключена — не вызывается; включена — POST с заявкой', function () {
    $id = pn_deliver_fixture(); unset($GLOBALS['PN_HTTP_CODE']);
    deliver_lead($id);
    pn_eq(count(array_filter($GLOBALS['PN_HTTP_LOG'], fn($x) => str_contains($x[0], 'crm.example'))), 0);
    $id = pn_deliver_fixture(['crm_enabled' => 1, 'crm_url' => 'https://crm.example.ru/api/leads']);
    deliver_lead($id);
    $crm = array_values(array_filter($GLOBALS['PN_HTTP_LOG'], fn($x) => str_contains($x[0], 'crm.example')));
    pn_eq(count($crm), 1); pn_eq(json_decode($crm[0][1], true)['phone'], '+79655002918');
    pn_eq((int) pn_db()->query("select delivered_crm from leads where id=$id")->fetchColumn(), 1);
});
pn_t('канал не настроен — заявка не считается «не доставленной»', function () {
    $id = pn_deliver_fixture(['tg_token' => '', 'mail_to' => '']);
    deliver_lead($id);
    pn_eq(lead_undelivered(pn_db()->query("select * from leads where id=$id")->fetch()), false);
});
pn_t('заявки в админке: список, статус, заметка, CSV в UTF-8 с BOM', function () {
    $id = pn_deliver_fixture();
    pn_db()->prepare('insert into users(login,password_hash,role) values (?,?,?)')->execute(['m', password_hash('p', PASSWORD_DEFAULT), 'manager']);
    $_SESSION = []; Auth::login('m', 'p');
    pn_eq(pn_route('GET', '/admin/')[2] === '' ? pn_route('GET', '/admin/')[1]['Location'] : '', '/admin/leads');
    [$c, , $html] = pn_route('GET', '/admin/leads');
    pn_eq($c, 200); pn_ok(str_contains($html, 'tel:+79655002918'), 'кликабельный телефон');
    pn_route('POST', "/admin/leads/$id", ['do' => 'status', 'status' => 'work', 'note' => 'перезвонить в 18:00', '_csrf' => csrf_token()]);
    $l = pn_db()->query("select status, note from leads where id=$id")->fetch();
    pn_eq([$l['status'], $l['note']], ['work', 'перезвонить в 18:00']);
    [$c, $h, $csv] = pn_route('GET', '/admin/leads/csv');
    pn_eq($c, 200); pn_ok(str_starts_with($csv, "\xEF\xBB\xBF"), 'BOM'); pn_ok(str_contains($csv, '+79655002918'), 'телефон в CSV');
    pn_ok(str_contains($h['Content-Type'], 'text/csv'), 'тип CSV');
});
