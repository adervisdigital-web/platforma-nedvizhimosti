<?php
// Тесты по замечаниям финальной проверки.
require_once __DIR__ . '/../app/bootstrap.php';
pn_t('R1: портрет 12 Мп с EXIF=6 при memory_limit 128M сохраняется', function () {
    $out = __DIR__ . '/_tmp/r1'; @mkdir($out, 0777, true);
    $script = $out . '/run.php';
    file_put_contents($script, '<?php require ' . var_export(__DIR__ . '/../app/bootstrap.php', true) . '; $GLOBALS["PN_UPLOADS"] = ' . var_export($out, true) . ';'
        . ' $r = pn_image_store(' . var_export(__DIR__ . '/fixtures/phone12mp_exif6.jpg', true) . ', "p.jpg"); [$w, $h] = getimagesize(pn_uploads_dir() . "/" . $r["w2000"]); echo "OK {$w}x{$h}";');
    $res = shell_exec('"' . PHP_BINARY . '" -d memory_limit=128M -d display_errors=1 "' . $script . '" 2>&1');
    pn_ok(str_starts_with(trim((string) $res), 'OK '), 'результат: ' . trim((string) $res));
    [$w, $h] = array_map('intval', explode('x', substr(trim($res), 3)));
    pn_ok($h > $w && $h === 2000, "портрет с длинной стороной 2000, получено {$w}x{$h}");
});
pn_t('R2: ставка 0 не роняет расчёт; пустая ставка в настройках — ошибка формы', function () {
    pn_eq(pn_annuity(3_600_000, 0.0), 8000, 'без процентов: 80 % / 360');
    pn_test_db();
    pn_db()->prepare('insert into users(login,password_hash,role) values (?,?,?)')->execute(['a', password_hash('p', PASSWORD_DEFAULT), 'admin']);
    $_SESSION = []; Auth::login('a', 'p');
    [$c, , $html] = pn_route('POST', '/admin/settings', ['do' => 'save', 'phone' => '+7 965 500-29-18', 'renovation_prices' => '20000;45000;80000',
        'mortgage_programs' => "Семейная\nIT | 12", '_csrf' => csrf_token()]);
    pn_eq($c, 200); pn_ok(str_contains($html, 'ставку'), 'сообщение про ставку');
    pn_eq(Repo::settingsAll()['mortgage_programs'][0]['rate'], pn_seed('settings')['mortgage_programs'][0]['rate'], 'настройки не испорчены');
});
pn_t('R3: наружу уходят только публичные настройки (allow-list)', function () {
    $db = pn_test_db();
    $db->exec("insert into settings(key,value) values ('mail_to','\"boss@corp.ru\"'),('future_secret','\"x\"')");
    $s = json_decode(pn_api('settings')[1], true);
    pn_ok(!isset($s['mail_to']) && !isset($s['future_secret']), 'утекло: ' . implode(',', array_keys($s)));
    pn_ok(!str_contains(pn_render('layout', pn_page_vars()), 'boss@corp.ru'), 'почта в данных страницы');
    pn_eq($s['phone'], '+7 965 500-29-18');
});
pn_t('R5: формулы в CSV обезврежены', function () {
    $db = pn_test_db();
    $db->prepare("insert into leads(kind,name,phone,note) values ('quiz',?, '+79655002918', ?)")->execute(['=HYPERLINK("http://x","y")', '+cmd']);
    $db->prepare('insert into users(login,password_hash,role) values (?,?,?)')->execute(['m', password_hash('p', PASSWORD_DEFAULT), 'manager']);
    $_SESSION = []; Auth::login('m', 'p');
    $csv = pn_route('GET', '/admin/leads/csv')[2];
    pn_ok(str_contains($csv, "'=HYPERLINK") && !preg_match('/;"?=HYPERLINK/', $csv), 'формула не обезврежена');
    pn_ok(str_contains($csv, "'+cmd"), 'плюс в начале');
    pn_ok(str_contains($csv, '+79655002918'), 'телефон остался числом-строкой');
});
pn_t('R6: POST больше лимита сервера — понятное сообщение, не «форма устарела»', function () {
    pn_test_db();
    $_SERVER['CONTENT_LENGTH'] = '60000000';
    try { [$c, , $b] = pn_route('POST', '/admin/apartments/1', []); } finally { unset($_SERVER['CONTENT_LENGTH']); }
    pn_eq($c, 413); pn_ok(str_contains($b, 'МБ'), 'сообщение с лимитом: ' . $b);
});
pn_t('R8: повтор доставки при входе ограничен по времени', function () {
    pn_test_db();
    for ($i = 0; $i < 5; $i++) pn_db()->exec("insert into leads(kind,phone) values ('callback','+79655002918')");
    $GLOBALS['PN_HTTP'] = function () { usleep(400_000); return [500, '']; };
    pn_db()->exec("insert into settings(key,value) values ('tg_token','\"1:a\"'),('tg_chat_id','\"1\"')");
    $t = microtime(true); deliver_pending(20, 1.0); $dt = microtime(true) - $t;
    unset($GLOBALS['PN_HTTP']);
    pn_ok($dt < 2.0, sprintf('заняло %.1f с', $dt));
});
