<?php
// Фронт-контроллер: все пути сайта, API и админки.
require __DIR__ . '/../app/bootstrap.php';
header_remove('X-Powered-By');                                                  // не сообщаем версию PHP
if (!is_file(__DIR__ . '/assets/js/app.js')) pn_write_bundle();   // app.js не хранится в git — собираем при первом запуске
$post = $_POST;
if (!$post && str_contains($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
    $raw = (string) file_get_contents('php://input', false, null, 0, 65537);     // заявка — пара сотен байт; больше 64 КБ не читаем
    if (strlen($raw) > 65536) { http_response_code(413); header('Content-Type: application/json; charset=utf-8'); echo '{"ok":false,"error":"too_large"}'; exit; }
    $post = json_decode($raw, true) ?: [];
}
$reqPath = '/' . ltrim(rawurldecode(parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/'), '/');
$https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
[$code, $headers, $body] = pn_route($_SERVER['REQUEST_METHOD'] ?? 'GET', $_SERVER['REQUEST_URI'] ?? '/', $post, $_FILES);
http_response_code($code);
foreach (array_replace(pn_security_headers($reqPath, $https), $headers) as $k => $v) header("$k: $v");   // заголовки маршрута важнее общих
echo $body;
