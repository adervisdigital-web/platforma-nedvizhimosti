<?php
// Данные для страницы: один pn_page_data() для двух источников — data/seed/*.json и базы (pn_db_source() в repo.php).
function pn_seed(string $name): array {
    return json_decode(file_get_contents(pn_config()['root'] . "/data/seed/$name.json"), true, 512, JSON_THROW_ON_ERROR);
}
function pn_seed_all(): array {
    $o = [];
    foreach (['apartments', 'complexes', 'houses', 'reviews', 'settings', 'faq', 'quick'] as $n) $o[$n] = pn_seed($n);
    return $o;
}
// Источник по умолчанию: база, если в ней есть квартиры; иначе seed (витрина, первый запуск).
function pn_source(): array {
    if (pn_config()['source'] === 'db') {
        try {
            $db = pn_db();
            if ((int) $db->query('select count(*) from apartments')->fetchColumn() > 0) return pn_db_source();
        } catch (Throwable $e) { /* нет базы — показываем seed */ }
    }
    return pn_seed_all();
}
// Число без лишнего «.0»: 120.0 → 120, 58.4 → 58.4 (как в данных прототипа).
function pn_num($v) {
    if ($v === null || $v === '') return null;
    return (float) $v == (int) $v ? (int) $v : (float) $v;
}
// Квартира из базы/seed → объект в форме прототипа v40 (r, s, fl, …), чтобы код разделов не менялся.
function pn_item_proto(array $a): array {
    $it = ['img' => $a['photos'][0] ?? '', 'r' => (int) $a['rooms'], 's' => pn_num($a['area']), 'fl' => (int) $a['floor'], 'fls' => (int) $a['floors'],
        'zk' => $a['complex'] ?? $a['address'] ?? '', 'd' => $a['district'] ?? '', 't' => $a['market'] === 'new' ? 'new' : 'sec',
        'due' => (int) ($a['due'] ?? 0), 'st' => $a['house_status'] ?? '', 'fin' => $a['finish_label'] ?? ($a['finish'] === 'without' ? 'Без отделки' : 'С отделкой'),
        'p' => (int) $a['price'], 'x' => pn_num($a['map_x'] ?? null), 'y' => pn_num($a['map_y'] ?? null), 'slug' => $a['slug'] ?? ''];
    if (!empty($a['discount_pct'])) $it['disc'] = (int) $a['discount_pct'];
    if (!empty($a['special'])) $it['special'] = 1;
    return $it;
}
// Публичные настройки: без секретов (токены, SMTP, CRM, соль) и без служебных списков.
const PN_PUBLIC_SETTINGS = ['phone', 'phone_tel', 'hours_from', 'hours_to', 'renovation_prices', 'warm_contour_from', 'mortgage_programs', 'family_tiers', 'rates_date', 'district_geo',
    'legal', 'domain', 'demo_data', 'show_demo_reviews'];
function pn_public_settings(array $s): array {
    return array_intersect_key($s, array_flip(PN_PUBLIC_SETTINGS));            // только разрешённое: новые ключи (почта, токены) наружу не попадут
}
function pn_visible_reviews(array $reviews, array $settings): array {
    $demo = !empty($settings['show_demo_reviews']);
    return array_values(array_filter($reviews, fn($r) => !empty($r['published']) && ($demo || empty($r['is_demo']))));
}
function pn_page_data(array $src, array $cfg): array {
    $s = $src['settings'];
    return [
        'items'    => array_map('pn_item_proto', array_values(array_filter($src['apartments'], fn($a) => !empty($a['published'])))),
        'houses'   => $src['houses'],
        'reviews'  => pn_visible_reviews($src['reviews'], $s),
        'faq'      => $src['faq'],
        'quick'    => $src['quick'],
        'progs'    => array_map(fn($p) => [$p['name'], $p['rate']], $s['mortgage_programs'] ?? []),
        'mort'     => pn_mort_cfg($s),
        'geo'      => $s['district_geo'] ?? new stdClass,
        'settings' => pn_public_settings($s),
        'demo'     => (bool) $cfg['demo'],
        'api'      => 'api/',
    ];
}
function pn_data_json(array $data): string {
    return json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP | JSON_THROW_ON_ERROR);
}
