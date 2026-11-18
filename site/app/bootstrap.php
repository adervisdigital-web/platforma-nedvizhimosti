<?php
// Подключение общего кода. Все модули app/*.php — функции и классы без побочных эффектов.
declare(strict_types=1);
mb_internal_encoding('UTF-8');
date_default_timezone_set('Asia/Yekaterinburg');
foreach (glob(__DIR__ . '/*.php') as $f) {
    if (!in_array(basename($f), ['bootstrap.php', 'local.php', 'cli.php'], true)) require_once $f;
}
foreach (glob(__DIR__ . '/leads/*.php') ?: [] as $f) require_once $f;
