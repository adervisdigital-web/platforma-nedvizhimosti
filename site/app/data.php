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
    $it = ['id' => isset($a['id']) ? (int) $a['id'] : null, 'img' => $a['photos'][0] ?? '', 'r' => (int) $a['rooms'], 's' => pn_num($a['area']), 'fl' => (int) $a['floor'], 'fls' => (int) $a['floors'],
        'zk' => $a['complex'] ?? $a['address'] ?? '', 'd' => $a['district'] ?? '', 't' => $a['market'] === 'new' ? 'new' : 'sec',
        'due' => (int) ($a['due'] ?? 0), 'st' => $a['house_status'] ?? '', 'fin' => $a['finish'] === 'without' ? 'Без отделки' : ($a['finish_label'] ?: 'С отделкой'),
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
const PN_MAIN_CAP = 60;   // на главной — подборка; весь список — в каталоге
// Подборка главной при большом каталоге: спецпредложения и скидки, затем лучшая цена за м² — по кругу из разных ЖК и комнатности.
function pn_main_pick(array $apts, int $cap = PN_MAIN_CAP): array {
    if (count($apts) <= $cap) return $apts;
    usort($apts, fn($a, $b) => [(int) $b['special'], (int) $b['discount_pct'], $a['price'] / max(1, $a['area'])] <=> [(int) $a['special'], (int) $a['discount_pct'], $b['price'] / max(1, $b['area'])]);
    $buckets = [];
    foreach ($apts as $a) $buckets[($a['complex'] ?? $a['address'] ?? '') . '|' . min(4, (int) $a['rooms'])][] = $a;
    $pick = [];
    while (count($pick) < $cap && $buckets) foreach ($buckets as $k => &$b) { if (count($pick) >= $cap) break; $pick[] = array_shift($b); if (!$b) unset($buckets[$k]); }
    unset($b);
    usort($pick, fn($a, $b) => $a['id'] <=> $b['id']);
    return $pick;
}
// Индекс всех квартир для счётчиков главной (поиск, районы, ЖК, плитки): [тип, комнат, цена, с отделкой, срок, район №, ЖК №, скидка, спец].
function pn_main_all(array $apts): array {
    $d = []; $z = []; $rows = [];
    foreach ($apts as $a) {
        $dk = (string) ($a['district'] ?? ''); $zk = (string) ($a['complex'] ?? $a['address'] ?? '');
        $d[$dk] ??= count($d); $z[$zk] ??= count($z);
        $rows[] = [$a['market'] === 'new' ? 'new' : 'sec', (int) $a['rooms'], (int) $a['price'], $a['finish'] === 'with' ? 1 : 0, (int) ($a['due'] ?? 0),
            $d[$dk], $z[$zk], (int) ($a['discount_pct'] ?? 0), (int) ($a['special'] ?? 0)];
    }
    return ['d' => array_keys($d), 'z' => array_keys($z), 'rows' => $rows];
}
function pn_page_data(array $src, array $cfg): array {
    $s = $src['settings'];
    $pub = array_values(array_filter($src['apartments'], fn($a) => !empty($a['published'])));
    return [
        'items'    => array_map('pn_item_proto', pn_main_pick($pub)),
        'total'    => count($pub),
        'capped'   => count($pub) > PN_MAIN_CAP,
        'all'      => count($pub) > PN_MAIN_CAP ? pn_main_all($pub) : null,
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
