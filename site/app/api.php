<?php
// JSON API для чтения: items, complexes, houses, reviews, settings. Возвращает [код, тело]. Приём заявок (POST lead) — задача 12.
function pn_api(string $path, string $method = 'GET', array $post = []): array {
    $j = fn($v) => json_encode($v, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR);
    $path = trim($path, '/');
    $src = fn() => pn_db_source();
    if ($path === 'lead') {
        if ($method !== 'POST') return [405, $j(['error' => 'method'])];
        $r = lead_accept($post, pn_ip(), pn_now());
        return [$r['ok'] ? 200 : ($r['error'] === 'rate' ? 429 : 400), $j($r)];
    }
    parse_str((string) ($GLOBALS['PN_QUERY'] ?? ''), $q);
    switch ($path) {
        case 'items':
            if (isset($q['ids'])) {                                       // избранное, сравнение, «Вы смотрели» — квартиры не из подборки главной
                $want = array_slice(array_map('intval', array_filter(explode(',', (string) $q['ids']), 'ctype_digit')), 0, 50);
                return [200, $j(array_values(array_map('pn_item_proto', array_filter(Repo::apartments(), fn($a) => in_array($a['id'], $want, true)))))];
            }
            return [200, $j(array_map('pn_item_proto', Repo::apartments()))];
        case 'count':                                                     // поиск первого экрана при большом каталоге
            return [200, $j(['n' => count(pn_ct_filter(Repo::apartments(), array_map(fn($v) => is_array($v) ? '' : (string) $v, $q), pn_complexes_full()))])];
        case 'complexes': return [200, $j(Repo::complexes())];
        case 'houses':    return [200, $j(Repo::houses())];
        case 'reviews':   return [200, $j(pn_visible_reviews(Repo::reviews(), Repo::settingsAll()))];
        case 'settings':  return [200, $j(Repo::settings())];
    }
    return [404, $j(['error' => 'not_found'])];
}
