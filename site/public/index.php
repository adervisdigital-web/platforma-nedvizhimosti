<?php
// Фронт-контроллер: все пути сайта, API и (позже) админки.
require __DIR__ . '/../app/bootstrap.php';
$post = $_POST;
if (!$post && str_contains($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) $post = json_decode(file_get_contents('php://input'), true) ?: [];
[$code, $headers, $body] = pn_route($_SERVER['REQUEST_METHOD'] ?? 'GET', $_SERVER['REQUEST_URI'] ?? '/', $post, $_FILES);
http_response_code($code);
foreach ($headers as $k => $v) header("$k: $v");
echo $body;
