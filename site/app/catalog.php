<?php
// Каталог квартир и SEO-страницы: /kvartiry/ (все), подборки по рынку и комнатам, районы /kvartiry/rayon/<район>/, страницы ЖК /zhk/<жк>/.
// Подборка публикуется, только если в ней есть квартиры (пустые страницы — 404, в sitemap не попадают).

const PN_ROOMS_PAGES = [
    'studii' => [0, 'Студии в Екатеринбурге', 'Студии'],
    '1-komnatnye' => [1, 'Однокомнатные квартиры в Екатеринбурге', '1-комн.'],
    '2-komnatnye' => [2, 'Двухкомнатные квартиры в Екатеринбурге', '2-комн.'],
    '3-komnatnye' => [3, 'Трёхкомнатные квартиры в Екатеринбурге', '3-комн.'],
    '4-komnatnye' => [4, 'Четырёхкомнатные и большие квартиры в Екатеринбурге', '4+ комн.'],
];

function pn_zhk_path(string $slug): string { return 'zhk/' . preg_replace('~^zhk-~', '', $slug) . '/'; }
function pn_mln(int $v): string {
    return $v >= 1000000 ? rtrim(rtrim(number_format($v / 1e6, 2, ',', ' '), '0'), ',') . ' млн ₽' : pn_rub($v);
}
function pn_ru_plural(int $n, string $one, string $few, string $many): string {
    $m = $n % 10; $h = $n % 100;
    return $m === 1 && $h !== 11 ? $one : ($m >= 2 && $m <= 4 && ($h < 12 || $h > 14) ? $few : $many);
}

// Подборки: путь => [h1, короткое имя для навигации, фильтр, группа]. Районы — из опубликованных квартир.
function pn_catalog_pages(): array {
    $p = [
        'kvartiry/' => ['Квартиры в Екатеринбурге', 'Все', fn($a) => true, 'all'],
        'kvartiry/novostroyki/' => ['Новостройки в Екатеринбурге', 'Новостройки', fn($a) => $a['market'] === 'new', 'type'],
        'kvartiry/vtorichka/' => ['Вторичное жильё в Екатеринбурге', 'Вторичка', fn($a) => $a['market'] === 'secondary', 'type'],
    ];
    $p += [
        'kvartiry/gotovye-novostroyki/' => ['Квартиры в сданных новостройках Екатеринбурга', 'Сданные дома', fn($a) => $a['market'] === 'new' && !$a['due'], 'feat'],
        'kvartiry/s-otdelkoy/' => ['Квартиры с отделкой в Екатеринбурге', 'С отделкой', fn($a) => $a['finish'] === 'with', 'feat'],
        'kvartiry/semeynaya-ipoteka/' => ['Квартиры под семейную ипотеку в Екатеринбурге', 'Семейная ипотека', fn($a) => $a['market'] === 'new', 'feat'],
        'kvartiry/skidki/' => ['Скидки и спецпредложения на квартиры', 'Скидки', fn($a) => $a['discount_pct'] > 0 || $a['special'], 'feat'],
    ];
    foreach (PN_ROOMS_PAGES as $slug => [$r, $h1, $short])
        $p["kvartiry/$slug/"] = [$h1, $short, fn($a) => $r === 4 ? $a['rooms'] >= 4 : $a['rooms'] === $r, 'rooms'];
    $ds = array_unique(array_filter(array_column(Repo::apartments(), 'district')));
    sort($ds);
    foreach ($ds as $d) $p['kvartiry/rayon/' . pn_slug($d) . '/'] = ["Квартиры в районе $d", $d, fn($a) => $a['district'] === $d, 'district'];
    return $p;
}

// ЖК с подробностями для страницы ЖК и каталога.
function pn_complexes_full(): array {
    $o = [];
    foreach (pn_db()->query('select c.*, d.name as developer from complexes c left join developers d on d.id = c.developer_id order by c.name')->fetchAll() as $c) {
        $o[$c['name']] = ['name' => $c['name'], 'slug' => $c['slug'], 'path' => pn_zhk_path($c['slug']), 'district' => $c['district'], 'address' => $c['address'],
            'description' => $c['description'] ?? '', 'checks' => json_decode($c['checks'] ?: '[]', true) ?: [], 'photos' => json_decode($c['photos'] ?: '[]', true) ?: [],
            'lat' => $c['lat'] === null ? null : (float) $c['lat'], 'lng' => $c['lng'] === null ? null : (float) $c['lng'], 'developer' => $c['developer']];
    }
    return $o;
}

// Платёж в ипотеку, как на странице квартиры: новостройки — первая программа, вторичка — последняя (рыночная).
function pn_apt_pay(array $a, array $s): int {
    $progs = $s['mortgage_programs'] ?? [];
    $rate = $a['market'] === 'new' ? ($progs[0]['rate'] ?? 6) : (end($progs)['rate'] ?? 20);
    return pn_annuity($a['price'], (float) $rate);
}

function pn_catalog_stats(array $apts): array {
    if (!$apts) return ['n' => 0];
    $p = array_column($apts, 'price'); $ar = array_column($apts, 'area');
    return ['n' => count($apts), 'pmin' => min($p), 'pmax' => max($p), 'amin' => min($ar), 'amax' => max($ar)];
}

function pn_catalog_intro(string $what, array $st, array $zhks): string {
    if (!$st['n']) return 'Сейчас подходящих предложений нет — оставьте заявку, подберём из новых поступлений.';
    $t = sprintf('В продаже %d %s %s: от %s до %s, площадь от %s до %s м².', $st['n'], pn_ru_plural($st['n'], 'предложение', 'предложения', 'предложений'), $what,
        pn_mln($st['pmin']), pn_mln($st['pmax']), str_replace('.', ',', (string) pn_num($st['amin'])), str_replace('.', ',', (string) pn_num($st['amax'])));
    if ($zhks) $t .= ' Жилые комплексы: ' . implode(', ', array_slice($zhks, 0, 6)) . '.';
    return $t . ' Каждый объект проверен до публикации, комиссия для покупателя — 0 ₽.';
}

// Общие данные для навигации по подборкам: [путь => [короткое имя, кол-во]] по группам, районы, ЖК.
function pn_catalog_nav(array $all, array $cx): array {
    $nav = ['type' => [], 'rooms' => [], 'feat' => [], 'district' => []];
    foreach (pn_catalog_pages() as $path => [$h1, $short, $f, $g]) {
        $n = count(array_filter($all, $f));
        if ($n && $g !== 'all') $nav[$g][$path] = [$short, $n];
    }
    $nav['all'] = count($all);
    $z = [];
    foreach ($all as $a) if ($a['complex'] && isset($cx[$a['complex']])) $z[$cx[$a['complex']]['path']] = [$a['complex'], ($z[$cx[$a['complex']]['path']][1] ?? 0) + 1];
    ksort($z); $nav['zhk'] = $z;
    return $nav;
}

// Координаты квартиры для карты: у ЖК — свои, у вторички — центр района.
function pn_apt_geo(array $a, array $cx, array $s): ?array {
    if ($a['complex'] && isset($cx[$a['complex']]) && $cx[$a['complex']]['lat']) return [$cx[$a['complex']]['lat'], $cx[$a['complex']]['lng']];
    return $s['district_geo'][$a['district']] ?? null;
}

function pn_catalog_graph(string $name, string $path, array $apts, array $crumbs, array $s): array {
    $site = pn_site_url($s);
    return [['@type' => 'ItemList', 'name' => $name, 'url' => $site . $path, 'numberOfItems' => count($apts),
        'itemListElement' => array_map(fn($a, $k) => ['@type' => 'ListItem', 'position' => $k + 1, 'url' => $site . "kvartiry/{$a['slug']}/", 'name' => pn_apt_title($a)],
            array_values($apts), array_keys(array_values($apts)))], seo_breadcrumbs($crumbs, $s)];
}

function pn_page_catalog(string $path, string $query = ''): ?string {
    $pages = pn_catalog_pages();
    if (!isset($pages[$path])) return null;
    [$h1, $short, $f, $group] = $pages[$path];
    $all = Repo::apartments();
    $apts = array_values(array_filter($all, $f));
    if (!$apts && $path !== 'kvartiry/') return null;
    $s = Repo::settingsAll(); $cx = pn_complexes_full();
    $st = pn_catalog_stats($apts);
    $zhks = array_values(array_unique(array_filter(array_column($apts, 'complex'))));
    $what = match ($group) { 'all' => 'в Екатеринбурге', 'type' => $path === 'kvartiry/novostroyki/' ? 'в новостройках' : 'на вторичном рынке',
        'rooms' => '— ' . mb_strtolower(str_replace(' в Екатеринбурге', '', $h1)),
        'feat' => ['kvartiry/gotovye-novostroyki/' => 'в сданных новостройках', 'kvartiry/s-otdelkoy/' => 'с отделкой или ремонтом',
            'kvartiry/semeynaya-ipoteka/' => 'в новостройках — подходят под семейную ипотеку', 'kvartiry/skidki/' => 'со скидкой или на спецусловиях'][$path], default => "в районе $short" };
    $title = $h1 . ($group === 'district' ? ', Екатеринбург' : '') . ($st['n'] ? " — {$st['n']} " . pn_ru_plural($st['n'], 'предложение', 'предложения', 'предложений') . ' от ' . pn_mln($st['pmin']) : '')
        . ' | Платформа недвижимости';
    $desc = $st['n'] ? "$h1: {$st['n']} " . pn_ru_plural($st['n'], 'проверенное предложение', 'проверенных предложения', 'проверенных предложений')
        . ' от ' . pn_mln($st['pmin']) . ' до ' . pn_mln($st['pmax']) . '. Новостройки и вторичка, 0 ₽ комиссии, помощь с ипотекой.' : "$h1 — подбор проверенных квартир, 0 ₽ комиссии.";
    $crumbs = [['Главная', ''], ['Квартиры', 'kvartiry/']];
    if ($path !== 'kvartiry/') $crumbs[] = [$short === 'Все' ? $h1 : ($group === 'district' ? "Район $short" : $short), $path];
    $seo = ['title' => $title, 'description' => $desc, 'path' => $path, 'image' => 'assets/img/' . ($apts[0]['photos'][0] ?? 'ekb_dusk') . '.jpg'];
    $depth = substr_count($path, '/');
    return pn_subpage(200, 'catalog', ['h1' => $h1, 'path' => $path, 'group' => $group, 'apts' => $apts, 'st' => $st, 'crumbs' => $crumbs,
        'intro' => pn_catalog_intro($what, $st, $zhks), 'nav' => pn_catalog_nav($all, $cx), 'cx' => $cx, 's' => $s],
        $seo, pn_catalog_graph($h1, $path, $apts, $crumbs, $s), $depth, $query !== '');
}

function pn_page_zhk(string $slug, string $query = ''): ?string {
    $cx = pn_complexes_full(); $z = null;
    foreach ($cx as $c) if ($c['path'] === "zhk/$slug/") $z = $c;
    if (!$z) return null;
    $all = Repo::apartments();
    $apts = array_values(array_filter($all, fn($a) => $a['complex'] === $z['name']));
    if (!$apts) return null;
    $s = Repo::settingsAll(); $st = pn_catalog_stats($apts);
    $title = "{$z['name']}, {$z['district']} — квартиры от " . pn_mln($st['pmin']) . ' | Платформа недвижимости';
    $desc = "{$z['name']} в Екатеринбурге ({$z['district']}): {$st['n']} " . pn_ru_plural($st['n'], 'квартира', 'квартиры', 'квартир') . ' в продаже от ' . pn_mln($st['pmin'])
        . '. Застройщик проверен Платформой недвижимости, 0 ₽ комиссии.';
    $crumbs = [['Главная', ''], ['Квартиры', 'kvartiry/'], [$z['name'], $z['path']]];
    $others = array_filter(pn_catalog_nav($all, $cx)['zhk'], fn($k) => $k !== $z['path'], ARRAY_FILTER_USE_KEY);
    $seo = ['title' => $title, 'description' => $desc, 'path' => $z['path'], 'image' => 'assets/img/' . ($z['photos'][0] ?? $apts[0]['photos'][0] ?? 'zhk') . '.jpg'];
    $graph = pn_catalog_graph($z['name'], $z['path'], $apts, $crumbs, $s);
    $graph[] = ['@type' => 'ApartmentComplex', 'name' => $z['name'], 'address' => ['@type' => 'PostalAddress', 'addressLocality' => 'Екатеринбург', 'streetAddress' => (string) $z['address']],
        'geo' => $z['lat'] ? ['@type' => 'GeoCoordinates', 'latitude' => $z['lat'], 'longitude' => $z['lng']] : null];
    return pn_subpage(200, 'zhk', ['z' => $z, 'apts' => $apts, 'st' => $st, 'crumbs' => $crumbs, 'others' => $others, 'cx' => $cx, 's' => $s],
        $seo, $graph, 2, $query !== '');
}

// Все адреса каталога для sitemap и сборки витрины.
function pn_catalog_paths(): array {
    $all = Repo::apartments(); $o = ['doma/', 'remont/', 'ipoteka/'];   // страницы услуг — app/services.php
    foreach (pn_catalog_pages() as $path => [, , $f]) if ($path === 'kvartiry/' || array_filter($all, $f)) $o[] = $path;
    $names = array_unique(array_filter(array_column($all, 'complex')));
    foreach (pn_complexes_full() as $c) if (in_array($c['name'], $names, true)) $o[] = $c['path'];
    return $o;
}
