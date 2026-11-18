<?php
// SEO: мета-теги, Open Graph, JSON-LD, форматирование чисел для заголовков.
function pn_e(?string $s): string { return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

// Абсолютный адрес сайта: из конфига или https://<домен из настроек>/.
function pn_site_url(array $settings = []): string {
    $b = pn_config()['base_url'];
    if ($b) return rtrim($b, '/') . '/';
    return 'https://' . ($settings['domain'] ?? 'p.forma196.ru') . '/';
}
function pn_area(float|int $v): string { return str_replace('.', ',', (string) pn_num($v)) . ' м²'; }
function pn_rub(int $v): string { return number_format($v, 0, ',', ' ') . ' ₽'; }
function pn_rooms(int $r): string { return $r ? "$r-комн. квартира" : 'Студия'; }
function pn_apt_title(array $a): string {
    return pn_rooms($a['rooms']) . ' · ' . pn_area($a['area']) . ' · ' . ($a['complex'] ?? $a['address']);
}

// $p: title, description, path (от корня, без /), image (путь от корня), type
function seo_meta(array $p, array $settings): string {
    $site = pn_site_url($settings);
    $url = $site . ($p['path'] ?? '');
    $img = isset($p['image']) ? $site . $p['image'] : $site . 'assets/img/ekb_dusk.jpg';
    return '<title>' . pn_e($p['title']) . "</title>\n"
        . '<meta name="description" content="' . pn_e($p['description']) . "\">\n"
        . '<meta name="theme-color" content="#F4F2EE">' . "\n"
        . '<link rel="canonical" href="' . pn_e($url) . "\">\n"
        . '<meta property="og:type" content="' . pn_e($p['type'] ?? 'website') . '"><meta property="og:title" content="' . pn_e($p['title']) . "\">\n"
        . '<meta property="og:description" content="' . pn_e($p['description']) . '"><meta property="og:url" content="' . pn_e($url) . '"><meta property="og:image" content="' . pn_e($img) . '">';
}

function seo_org(array $settings): array {
    return ['@type' => 'RealEstateAgent', 'name' => 'Платформа недвижимости', 'telephone' => $settings['phone'] ?? '', 'areaServed' => 'Екатеринбург',
        'url' => pn_site_url($settings)];
}
// $graph: список объектов schema.org (без @context). Организация добавляется всегда.
function seo_jsonld(array $graph, array $settings): string {
    $data = ['@context' => 'https://schema.org', '@graph' => array_merge([seo_org($settings)], $graph)];
    return '<script type="application/ld+json">' . json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) . '</script>';
}
function seo_breadcrumbs(array $items, array $settings): array {
    $site = pn_site_url($settings);
    return ['@type' => 'BreadcrumbList', 'itemListElement' => array_map(fn($k, $it) => ['@type' => 'ListItem', 'position' => $k + 1, 'name' => $it[0],
        'item' => $site . $it[1]], array_keys($items), $items)];
}
function seo_main(array $settings): array {
    return ['title' => 'Платформа недвижимости — квартиры, дома и ремонт в Екатеринбурге',
        'description' => 'Квартиры от проверенных застройщиков Екатеринбурга без комиссии, свой ремонт с гарантией 5 лет и дома в рассрочку до 5 лет.',
        'path' => '', 'type' => 'website'];
}
