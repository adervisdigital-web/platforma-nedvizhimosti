<?php
// Данные для страницы. Сейчас — из data/seed/*.json; в задаче 7 тот же pn_page_data() получает данные из БД.
function pn_seed(string $name): array {
    return json_decode(file_get_contents(pn_config()['root'] . "/data/seed/$name.json"), true, 512, JSON_THROW_ON_ERROR);
}
function pn_seed_all(): array {
    $o = [];
    foreach (['apartments', 'complexes', 'houses', 'reviews', 'settings', 'faq', 'quick'] as $n) $o[$n] = pn_seed($n);
    return $o;
}
// Квартира из базы/seed → объект в форме прототипа v40 (r, s, fl, …), чтобы код разделов не менялся.
function pn_item_proto(array $a): array {
    $it = ['img' => $a['photos'][0] ?? '', 'r' => (int) $a['rooms'], 's' => (float) $a['area'], 'fl' => (int) $a['floor'], 'fls' => (int) $a['floors'],
        'zk' => $a['complex'] ?? $a['address'] ?? '', 'd' => $a['district'] ?? '', 't' => $a['market'] === 'new' ? 'new' : 'sec',
        'due' => (int) ($a['due'] ?? 0), 'st' => $a['house_status'] ?? '', 'fin' => $a['finish_label'] ?? ($a['finish'] === 'without' ? 'Без отделки' : 'С отделкой'),
        'p' => (int) $a['price'], 'x' => $a['map_x'] ?? null, 'y' => $a['map_y'] ?? null, 'slug' => $a['slug'] ?? ''];
    if (!empty($a['discount_pct'])) $it['disc'] = (int) $a['discount_pct'];
    if (!empty($a['special'])) $it['special'] = 1;
    return $it;
}
// Публичные настройки: без секретов (токены, SMTP, CRM).
function pn_public_settings(array $s): array {
    return array_filter($s, fn($k) => !preg_match('/^(tg_|smtp_|crm_|salt)/', (string) $k), ARRAY_FILTER_USE_KEY);
}
function pn_page_data(array $src, array $cfg): array {
    $s = $src['settings'];
    return [
        'items'    => array_map('pn_item_proto', array_values(array_filter($src['apartments'], fn($a) => !empty($a['published'])))),
        'houses'   => $src['houses'],
        'reviews'  => $src['reviews'],
        'faq'      => $src['faq'],
        'quick'    => $src['quick'],
        'progs'    => array_map(fn($p) => [$p['name'], $p['rate']], $s['mortgage_programs'] ?? []),
        'geo'      => $s['district_geo'] ?? new stdClass,
        'settings' => pn_public_settings($s),
        'demo'     => (bool) $cfg['demo'],
        'api'      => 'api/',
    ];
}
function pn_data_json(array $data): string {
    return json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP | JSON_THROW_ON_ERROR);
}
