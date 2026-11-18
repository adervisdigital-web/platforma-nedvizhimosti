<?php
// Фронт-контроллер: все пути сайта, API и (позже) админки.
require __DIR__ . '/../app/bootstrap.php';
[$code, $headers, $body] = pn_route($_SERVER['REQUEST_METHOD'] ?? 'GET', $_SERVER['REQUEST_URI'] ?? '/');
http_response_code($code);
foreach ($headers as $k => $v) header("$k: $v");
echo $body;
