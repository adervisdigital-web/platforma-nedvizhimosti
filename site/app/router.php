<?php
// Маршруты сайта. Возвращает [код, заголовки, тело]. Пути — от корня сайта.
function pn_html_response(int $code, string $html): array { return [$code, ['Content-Type' => 'text/html; charset=utf-8'], $html]; }

// Подстраница в каркасе page.php. $depth — сколько папок до корня (для <base>).
function pn_subpage(int $code, string $tpl, array $vars, array $seo, array $graph, int $depth): string {
    $s = Repo::settingsAll();
    $cfg = pn_config();
    $base = $depth ? str_repeat('../', $depth) : './';
    $head = seo_meta($seo, $s) . "\n" . '<link rel="stylesheet" href="assets/css/page.css">';
    return pn_render('page', ['base_tag' => ($cfg['demo'] ? '<meta name="robots" content="noindex">' : '') . '<base href="' . $base . '">',
        'seo_head' => $head, 'jsonld' => seo_jsonld($graph, $s), 'settings' => pn_public_settings($s),
        'content' => pn_render($tpl, $vars + ['settings' => pn_public_settings($s)])]);
}

// Ежемесячный платёж как в калькуляторе прототипа: кредит 80 %, 30 лет.
function pn_annuity(int $price, float $rate): int {
    $L = $price * .8; $m = $rate / 1200;
    if ($m <= 0) return (int) round($L / 360);                                    // без процентов
    return (int) round($L * $m / (1 - pow(1 + $m, -360)));
}

function pn_page_apartment(string $slug): ?string {
    $a = Repo::apartment($slug);
    if (!$a) return null;
    $s = Repo::settingsAll();
    $progs = $s['mortgage_programs'] ?? [];
    $rate = $a['market'] === 'new' ? ($progs[0]['rate'] ?? 6) : (end($progs)['rate'] ?? 20);
    $idx = array_search($a['slug'], array_column(Repo::apartments(), 'slug'), true);
    $title = pn_apt_title($a);
    $where = $a['complex'] ?? $a['address'];
    $seo = ['title' => "$title — купить в Екатеринбурге | Платформа недвижимости",
        'description' => sprintf('%s %s, %d/%d этаж, %s (%s). Цена %s, %s. Проверено Платформой недвижимости, 0 ₽ комиссии.',
            pn_rooms($a['rooms']), pn_area($a['area']), $a['floor'], $a['floors'], $where, $a['district'], pn_rub($a['price']), mb_strtolower($a['house_status'])),
        'path' => "kvartiry/{$a['slug']}/", 'image' => 'assets/img/' . ($a['photos'][0] ?? 'ekb_dusk') . '.jpg', 'type' => 'product'];
    $site = pn_site_url($s);
    $graph = [['@type' => 'Product', 'name' => $title, 'image' => $site . $seo['image'], 'description' => $seo['description'],
        'offers' => ['@type' => 'Offer', 'price' => $a['price'], 'priceCurrency' => 'RUB', 'availability' => 'https://schema.org/InStock', 'url' => $site . $seo['path']]],
        seo_breadcrumbs([['Главная', ''], ['Квартиры', '#list'], [$where, $seo['path']]], $s)];
    return pn_subpage(200, 'apartment', ['a' => $a, 'idx' => $idx === false ? 0 : $idx, 'pay' => pn_annuity($a['price'], (float) $rate), 'rate' => $rate],
        $seo, $graph, 2);
}

function pn_page_house(string $slug): ?string {
    $h = Repo::house($slug);
    if (!$h) return null;
    $s = Repo::settingsAll();
    $name = $h['line'] . ' ' . $h['n'];
    $seo = ['title' => "Проект дома «{$name}» — {$h['n']} м², строительство в рассрочку | Платформа недвижимости",
        'description' => "Каменный дом «{$name}»: {$h['n']} м², {$h['fl']} эт., {$h['rooms']}. {$h['motto']}. Свои бригады, рассрочка 0 % до 5 лет, гарантия 5 лет.",
        'path' => "doma/{$h['slug']}/", 'image' => 'assets/img/houses/' . ($h['ph'][0] ?? '') . '.jpg', 'type' => 'product'];
    $graph = [['@type' => 'Product', 'name' => "Проект дома «{$name}»", 'image' => pn_site_url($s) . $seo['image'], 'description' => $seo['description']],
        seo_breadcrumbs([['Главная', ''], ['Дома', '#houses'], [$name, $seo['path']]], $s)];
    return pn_subpage(200, 'house', ['h' => $h], $seo, $graph, 2);
}

function pn_sitemap(): string {
    $s = Repo::settingsAll(); $site = pn_site_url($s);
    $urls = [$site];
    foreach (Repo::apartments() as $a) $urls[] = $site . "kvartiry/{$a['slug']}/";
    foreach (Repo::houses() as $h) $urls[] = $site . "doma/{$h['slug']}/";
    return '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        . implode('', array_map(fn($u) => '<url><loc>' . pn_e($u) . '</loc></url>', $urls)) . "</urlset>\n";
}

function pn_route(string $method, string $path, array $post = [], array $files = []): array {
    try { return pn_route_inner($method, $path, $post, $files); }
    catch (PnHttp $e) {
        if ($e->status >= 300 && $e->status < 400) return [$e->status, $e->headers, ''];
        return [$e->status, ['Content-Type' => 'text/plain; charset=utf-8'], $e->getMessage()];
    }
}
function pn_route_inner(string $method, string $path, array $post, array $files): array {
    $path = '/' . ltrim(rawurldecode(parse_url($path, PHP_URL_PATH) ?: '/'), '/');
    if ($path === '/admin' || str_starts_with($path, '/admin/')) return pn_admin_route($method, $path, $post, $files);
    $demo = pn_config()['demo'];
    if ($path === '/' || $path === '/index.html') return pn_html_response(200, pn_render('layout', pn_page_vars()));
    if ($path === '/robots.txt') {
        $body = $demo ? "User-agent: *\nDisallow: /\n" : "User-agent: *\nDisallow: /admin/\nDisallow: /api/\nSitemap: " . pn_site_url(Repo::settingsAll()) . "sitemap.xml\n";
        return [200, ['Content-Type' => 'text/plain; charset=utf-8'], $body];
    }
    if ($path === '/sitemap.xml' && !$demo) return [200, ['Content-Type' => 'application/xml; charset=utf-8'], pn_sitemap()];
    if (str_starts_with($path, '/api/')) {
        [$code, $body] = pn_api(substr($path, 5), $method, $post);
        return [$code, ['Content-Type' => 'application/json; charset=utf-8'], $body];
    }
    if (preg_match('~^/(kvartiry|doma)/([a-z0-9-]+)$~', $path)) return [301, ['Location' => "$path/"], ''];
    if (preg_match('~^/kvartiry/([a-z0-9-]+)/$~', $path, $m) && ($h = pn_page_apartment($m[1])) !== null) return pn_html_response(200, $h);
    if (preg_match('~^/doma/([a-z0-9-]+)/$~', $path, $m) && ($h = pn_page_house($m[1])) !== null) return pn_html_response(200, $h);
    if ($path === '/privacy/' || $path === '/privacy')
        return pn_html_response(200, pn_subpage(200, 'privacy', [], ['title' => 'Политика обработки персональных данных | Платформа недвижимости',
            'description' => 'Политика обработки персональных данных «Платформы недвижимости».', 'path' => 'privacy/'], [], 1));
    $depth = max(0, substr_count(trim($path, '/'), '/') + (str_ends_with($path, '/') ? 1 : 0));
    return pn_html_response(404, pn_subpage(404, '404', [], ['title' => 'Страница не найдена | Платформа недвижимости', 'description' => 'Такой страницы нет.',
        'path' => ''], [], $depth));
}
