<?php
// Телефон в любом виде → +7XXXXXXXXXX. Только российские номера: после +7 — 10 цифр, первая 3, 4, 8 или 9 (города, мобильные).
function phone_norm(string $raw): ?string {
    $d = preg_replace('/\D+/', '', $raw);
    if (strlen($d) === 11 && ($d[0] === '7' || $d[0] === '8')) $d = substr($d, 1);
    if (strlen($d) !== 10 || !in_array($d[0], ['3', '4', '8', '9'], true)) return null;
    return '+7' . $d;
}
function phone_pretty(string $n): string {
    return preg_replace('/^\+7(\d{3})(\d{3})(\d{2})(\d{2})$/', '+7 ($1) $2-$3-$4', $n);
}
