<?php
// php site/app/cli.php migrate | seed | seed:details | user:add <логин> <admin|manager> | feeds:run [--force] | bundle | leads:retry
require __DIR__ . '/bootstrap.php';
$cmd = $argv[1] ?? '';
$db = fn() => pn_db();
switch ($cmd) {
    case 'migrate':
        echo 'применено миграций: ', pn_migrate($db()), "\n";
        break;
    case 'seed':
        pn_migrate($db());
        if ((int) $db()->query('select count(*) from apartments')->fetchColumn() > 0) exit("в базе уже есть квартиры — seed не нужен\n");
        pn_seed_db($db());
        echo "стартовые данные загружены\n";
        break;
    case 'seed:details':
        pn_migrate($db());
        echo 'дополнено квартир: ', pn_seed_details($db(), true), "
";
        echo 'дополнено ЖК: ', pn_seed_complex_details($db()), "
";
        break;
    case 'user:add':
        [$login, $role] = [$argv[2] ?? '', $argv[3] ?? 'manager'];
        if ($login === '' || !in_array($role, ['admin', 'manager'], true)) exit("использование: user:add <логин> <admin|manager>\n");
        $pass = rtrim(strtr(base64_encode(random_bytes(12)), '+/', 'kx'), '=');
        $db()->prepare('insert into users(login,password_hash,role) values (?,?,?)')->execute([$login, password_hash($pass, PASSWORD_DEFAULT), $role]);
        echo "пользователь $login ($role), пароль: $pass — передайте лично и смените после входа\n";
        break;
    case 'feeds:run':                                   // cron раз в час: фиды — раз в сутки, картинки — докачиваются
        pn_migrate($db());
        $r = pn_feeds_run(in_array('--force', $argv, true));
        foreach ($r['feeds'] as $id => $s) echo "выгрузка $id: ", $s['error'] ? 'ошибка — ' . $s['error'] : "в фиде {$s['total']}, добавлено {$s['added']}, обновлено {$s['updated']}, снято {$s['gone']}", "\n";
        echo "картинки: скачано {$r['images']['ok']}, ошибок {$r['images']['err']}, осталось {$r['images']['left']}, отложено (сервер не отвечает) {$r['images']['skipped']}\n";
        break;
    case 'bundle':
        echo 'собран ', pn_write_bundle(), "\n";
        break;
    case 'leads:retry':
        echo 'доставлено повторно: ', function_exists('deliver_pending') ? deliver_pending() : 0, "\n";
        break;
    default:
        exit("команды: migrate | seed | seed:details | user:add <логин> <admin|manager> | feeds:run [--force] | bundle | leads:retry\n");
}
