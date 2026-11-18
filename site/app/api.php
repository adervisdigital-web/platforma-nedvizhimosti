<?php
// JSON API для чтения: items, complexes, houses, reviews, settings. Возвращает [код, тело]. Приём заявок (POST lead) — задача 12.
function pn_api(string $path): array {
    $j = fn($v) => json_encode($v, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR);
    $path = trim($path, '/');
    $src = fn() => pn_db_source();
    switch ($path) {
        case 'items':     return [200, $j(pn_page_data($src(), pn_config())['items'])];
        case 'complexes': return [200, $j(Repo::complexes())];
        case 'houses':    return [200, $j(Repo::houses())];
        case 'reviews':   return [200, $j(pn_visible_reviews(Repo::reviews(), Repo::settingsAll()))];
        case 'settings':  return [200, $j(Repo::settings())];
    }
    return [404, $j(['error' => 'not_found'])];
}
