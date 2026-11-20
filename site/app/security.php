<?php
// Заголовки безопасности для всех ответов и правила паролей.

// $path — путь запроса; $https — запрос пришёл по HTTPS. Возвращает [заголовок => значение].
function pn_security_headers(string $path, bool $https): array {
    $h = [
        'X-Content-Type-Options' => 'nosniff',                                   // браузер не угадывает тип файла (картинка не станет скриптом)
        'Referrer-Policy' => 'strict-origin-when-cross-origin',                   // на чужие сайты уходит только домен, без адреса страницы
        'Permissions-Policy' => 'camera=(), microphone=(), geolocation=(), payment=(), usb=()',
        'X-Frame-Options' => 'SAMEORIGIN',                                        // чужой сайт не встроит наш в рамку (кликджекинг)
    ];
    if ($https) $h['Strict-Transport-Security'] = 'max-age=31536000';             // после первого визита — только HTTPS
    if ($path === '/admin' || str_starts_with($path, '/admin/')) {
        $h['X-Frame-Options'] = 'DENY';
        $h['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            . "font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'";
        $h['Cache-Control'] = 'no-store';                                         // страницы с заявками и телефонами не остаются в кэше
        $h['X-Robots-Tag'] = 'noindex, nofollow';
    } else {
        $h['Content-Security-Policy'] = "frame-ancestors 'self'; base-uri 'self'; object-src 'none'";
    }
    if (str_starts_with($path, '/api/')) $h['Cache-Control'] = 'no-store';
    return $h;
}

// Новый пароль: не короче 10 символов, не совпадает с логином, не из списка самых частых. Пусто — подходит, иначе — что не так.
function pn_password_problem(string $pass, string $login): string {
    if (mb_strlen($pass) < 10) return 'Пароль должен быть не короче 10 символов';
    $p = mb_strtolower($pass);
    if ($p === mb_strtolower($login) || str_contains($p, mb_strtolower($login)) && mb_strlen($login) >= 4) return 'Пароль не должен содержать логин';
    $common = ['1234567890', '0987654321', 'qwertyuiop', 'password12', 'password123', 'admin12345', 'administrator', 'qwerty1234', '1q2w3e4r5t', 'platforma1', 'платформа1'];
    if (in_array($p, $common, true) || preg_match('/^(.)\1+$/u', $pass)) return 'Слишком простой пароль — придумайте другой';
    return '';
}

// Слабый ли текущий пароль (для напоминания в админке): короче 10 символов, равен логину или «admin».
function pn_password_weak(string $pass, string $login): bool {
    return pn_password_problem($pass, $login) !== '' || mb_strtolower($pass) === 'admin';
}
