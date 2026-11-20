<?php
require_once __DIR__ . '/../app/bootstrap.php';
require_once __DIR__ . '/auth_test.php';

pn_t('заголовки: сайт — nosniff, рамка только своя; админка — CSP, DENY, no-store, noindex; HTTPS — HSTS', function () {
    $s = pn_security_headers('/kvartiry/', false);
    pn_eq([$s['X-Content-Type-Options'], $s['X-Frame-Options']], ['nosniff', 'SAMEORIGIN']);
    pn_ok(!isset($s['Strict-Transport-Security']), 'без HTTPS HSTS не ставим');
    pn_ok(str_contains($s['Content-Security-Policy'], "frame-ancestors 'self'"), 'csp сайта');
    $a = pn_security_headers('/admin/leads', true);
    pn_eq([$a['X-Frame-Options'], $a['Cache-Control'], $a['X-Robots-Tag']], ['DENY', 'no-store', 'noindex, nofollow']);
    pn_ok(str_contains($a['Content-Security-Policy'], "script-src 'self'") && str_contains($a['Content-Security-Policy'], "frame-ancestors 'none'"), 'csp админки');
    pn_ok(isset($a['Strict-Transport-Security']), 'hsts');
    pn_eq(pn_security_headers('/api/lead', false)['Cache-Control'], 'no-store');
});
pn_t('правила пароля: длина, логин внутри, частые пароли', function () {
    pn_eq(pn_password_problem('короткий', 'boss'), 'Пароль должен быть не короче 10 символов');
    pn_eq(pn_password_problem('my-boss-password', 'boss'), 'Пароль не должен содержать логин');
    pn_eq(pn_password_problem('1234567890', 'boss'), 'Слишком простой пароль — придумайте другой');
    pn_eq(pn_password_problem('ааааааааааа', 'boss'), 'Слишком простой пароль — придумайте другой');
    pn_eq(pn_password_problem('окно-берёза-кран-48', 'boss'), '');
    pn_ok(pn_password_weak('admin', 'admin') && pn_password_weak('boss', 'boss'), 'admin/логин — слабые');
});
pn_t('сессия: 2 часа без действий или 12 часов после входа — выход', function () {
    pn_auth_fixture(); $GLOBALS['PN_NOW'] = 2_000_000;
    pn_eq(Auth::login('boss', 'Верный-пароль-1'), true);
    $GLOBALS['PN_NOW'] += 3600; pn_ok(Auth::user() !== null, 'через час — в системе');
    $GLOBALS['PN_NOW'] += 2 * 3600 + 1; pn_eq(Auth::user(), null, 'после 2 ч бездействия — вышли');
    pn_eq(Auth::login('boss', 'Верный-пароль-1'), true);
    for ($i = 0; $i < 8; $i++) { $GLOBALS['PN_NOW'] += 5400; pn_ok(Auth::user() !== null, "активен, {$i}"); }   // каждые 1,5 ч — 12 ч в системе
    $GLOBALS['PN_NOW'] += 5400;
    pn_eq(Auth::user(), null, 'больше 12 ч после входа — вышли даже при активности');
    unset($GLOBALS['PN_NOW']);
});
pn_t('выход: по ссылке (GET) не выходит, по кнопке (POST с токеном) — выходит', function () {
    pn_auth_fixture(); Auth::login('mgr', 'пароль-менеджера');
    [$c] = pn_route('GET', '/admin/logout'); pn_eq($c, 302); pn_ok(Auth::user() !== null, 'GET не разлогинил');
    [$c, $h] = pn_route('POST', '/admin/logout', ['_csrf' => csrf_token()]); pn_eq([$c, $h['Location']], [302, '/admin/login']);
    pn_eq(Auth::user(), null);
});
pn_t('смена своего пароля: проверка текущего, совпадение, правила; после — входит с новым', function () {
    pn_auth_fixture(); Auth::login('mgr', 'пароль-менеджера'); $t = csrf_token();
    [, , $b] = pn_route('POST', '/admin/password', ['_csrf' => $t, 'old' => 'не тот', 'new' => 'окно-берёза-кран-48', 'new2' => 'окно-берёза-кран-48']);
    pn_ok(str_contains($b, 'Текущий пароль указан неверно'), 'неверный текущий');
    [, , $b] = pn_route('POST', '/admin/password', ['_csrf' => $t, 'old' => 'пароль-менеджера', 'new' => 'короткий', 'new2' => 'короткий']);
    pn_ok(str_contains($b, 'не короче 10 символов'), 'короткий');
    [$c] = pn_route('POST', '/admin/password', ['_csrf' => $t, 'old' => 'пароль-менеджера', 'new' => 'окно-берёза-кран-48', 'new2' => 'окно-берёза-кран-48']);
    pn_eq($c, 302);
    Auth::logout(); pn_eq(Auth::login('mgr', 'пароль-менеджера'), false, 'старый не подходит');
    pn_eq(Auth::login('mgr', 'окно-берёза-кран-48'), true, 'новый подходит');
    pn_eq($_SESSION['weak'], false);
});
pn_t('вход со слабым паролем — напоминание в админке', function () {
    pn_test_db(); $_SESSION = [];
    pn_db()->prepare('insert into users(login,password_hash,role) values (?,?,?)')->execute(['admin', password_hash('admin', PASSWORD_DEFAULT), 'admin']);
    pn_eq(Auth::login('admin', 'admin'), true); pn_eq($_SESSION['weak'], true);
    [, , $b] = pn_route('GET', '/admin/leads'); pn_ok(str_contains($b, 'Пароль ненадёжный'), 'баннер');
});
