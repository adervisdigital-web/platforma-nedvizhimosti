<?php
require_once __DIR__ . '/../app/bootstrap.php';
function pn_auth_fixture(): void {
    $db = pn_test_db();
    $ins = $db->prepare('insert into users(login,password_hash,role) values (?,?,?)');
    $ins->execute(['boss', password_hash('Верный-пароль-1', PASSWORD_DEFAULT), 'admin']);
    $ins->execute(['mgr', password_hash('пароль-менеджера', PASSWORD_DEFAULT), 'manager']);
    $_SESSION = []; unset($GLOBALS['PN_NOW']);
}
pn_t('вход: верный пароль', function () {
    pn_auth_fixture();
    pn_eq(Auth::login('boss', 'Верный-пароль-1'), true);
    pn_eq(Auth::user()['login'], 'boss');
});
pn_t('5 неверных попыток → блокировка на 15 минут даже с верным паролем', function () {
    pn_auth_fixture();
    $GLOBALS['PN_NOW'] = 1_000_000;
    for ($i = 0; $i < 5; $i++) pn_eq(Auth::login('boss', 'не тот'), false);
    pn_eq(Auth::login('boss', 'Верный-пароль-1'), false, 'сразу после 5 ошибок');
    pn_eq(Auth::lastError(), 'Слишком много попыток, попробуйте через 15 минут');
    $GLOBALS['PN_NOW'] += 14 * 60; pn_eq(Auth::login('boss', 'Верный-пароль-1'), false, 'через 14 минут');
    $GLOBALS['PN_NOW'] += 2 * 60;  pn_eq(Auth::login('boss', 'Верный-пароль-1'), true, 'через 16 минут');
});
pn_t('/admin/ без входа → 302 на вход', function () {
    pn_auth_fixture();
    [$code, $h] = pn_route('GET', '/admin/');
    pn_eq($code, 302); pn_eq($h['Location'], '/admin/login');
});
pn_t('POST без CSRF-токена → 403', function () {
    pn_auth_fixture();
    pn_eq(pn_route('POST', '/admin/login', ['login' => 'boss', 'password' => 'Верный-пароль-1'])[0], 403);
    $tok = csrf_token();
    pn_eq(pn_route('POST', '/admin/login', ['login' => 'boss', 'password' => 'Верный-пароль-1', '_csrf' => $tok])[0], 302, 'с токеном — вход и переход');
});
pn_t('менеджер не видит раздел пользователей', function () {
    pn_auth_fixture();
    Auth::login('mgr', 'пароль-менеджера');
    pn_eq(pn_route('GET', '/admin/users')[0], 403);
    Auth::logout(); Auth::login('boss', 'Верный-пароль-1');
    pn_eq(pn_route('GET', '/admin/users')[0], 200);
});
pn_t('журнал действий', function () {
    pn_auth_fixture(); Auth::login('boss', 'Верный-пароль-1');
    audit('update', 'apartments', 1, ['price' => [1, 2]]);
    $r = pn_db()->query('select * from audit order by id desc limit 1')->fetch();
    pn_eq([$r['action'], $r['entity'], (int) $r['entity_id']], ['update', 'apartments', 1]);
    pn_ok((int) $r['user_id'] > 0, 'кто изменил');
});
