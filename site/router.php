<?php
// Локальный сервер: php -S localhost:8080 -t site/public site/router.php  (корень — site/public)
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$file = __DIR__ . '/public' . $path;
if ($path !== '/' && is_file($file)) return false;      // статика отдаётся как есть
chdir(__DIR__ . '/public');
require __DIR__ . '/public/index.php';
