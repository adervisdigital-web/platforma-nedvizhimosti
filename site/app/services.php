<?php
// Страницы услуг для карточек главной: /doma/ (проекты домов), /remont/ (ремонт под ключ), /ipoteka/ (программы и калькулятор).

// Пояснения к известным программам ипотеки; для новых названий — общий текст.
function pn_mort_note(string $name): string {
    $n = mb_strtolower($name);
    return match (true) {
        str_contains($n, 'семейн') => pn_family_note(),
        str_contains($n, 'it') => 'Для сотрудников аккредитованных IT-компаний — нужна справка с работы.',
        str_contains($n, 'рыноч') => 'Любая квартира, в том числе вторичка. Ставку часто удаётся снизить за счёт застройщика или банка.',
        default => 'Условия уточним в банке под вашу ситуацию.',
    };
}

function pn_page_houses(): string {
    $s = Repo::settingsAll(); $hs = Repo::houses();
    $warm = (int) ($s['warm_contour_from'] ?? 0);
    $min = $hs && $warm ? min(array_map(fn($h) => $warm * $h['n'], $hs)) : 0;
    $seo = ['title' => 'Проекты каменных домов в Екатеринбурге — строительство в рассрочку 0 % | Платформа недвижимости',
        'description' => count($hs) . ' проектов каменных домов от ' . ($min ? pn_mln($min) : '') . ': тёплый контур от ' . pn_rub($warm) . '/м², свои бригады, рассрочка без процентов до 5 лет, гарантия 5 лет.',
        'path' => 'doma/', 'image' => 'assets/img/houses/' . ($hs[0]['ph'][0] ?? '') . '.jpg'];
    $crumbs = [['Главная', ''], ['Дома', 'doma/']];
    $site = pn_site_url($s);
    $graph = [['@type' => 'ItemList', 'name' => 'Проекты домов', 'itemListElement' => array_map(fn($h, $k) => ['@type' => 'ListItem', 'position' => $k + 1,
        'url' => $site . "doma/{$h['slug']}/", 'name' => $h['line'] . ' ' . $h['n']], $hs, array_keys($hs))], seo_breadcrumbs($crumbs, $s)];
    return pn_subpage(200, 'doma', ['hs' => $hs, 'warm' => $warm, 'min' => $min], $seo, $graph, 1);
}

function pn_page_remont(): string {
    $s = Repo::settingsAll(); $r = $s['renovation_prices'] ?? [20000, 45000, 80000];
    $seo = ['title' => 'Ремонт квартир под ключ в Екатеринбурге — от ' . pn_rub((int) $r[0]) . '/м² | Платформа недвижимости',
        'description' => 'Ремонт квартир под ключ своей бригадой: базовый от ' . pn_rub((int) $r[0]) . '/м², комфорт от ' . pn_rub((int) $r[1]) . '/м², премиум от ' . pn_rub((int) $r[2])
            . '/м². Смета до начала работ, цена в договоре, акт на каждый этап, гарантия 5 лет.',
        'path' => 'remont/', 'image' => 'assets/img/ba_after.jpg'];
    $crumbs = [['Главная', ''], ['Ремонт', 'remont/']];
    $graph = [['@type' => 'Service', 'name' => 'Ремонт квартир под ключ', 'areaServed' => 'Екатеринбург', 'provider' => seo_org($s),
        'offers' => ['@type' => 'AggregateOffer', 'priceCurrency' => 'RUB', 'lowPrice' => (int) $r[0], 'highPrice' => (int) $r[2], 'unitText' => 'м²']], seo_breadcrumbs($crumbs, $s)];
    return pn_subpage(200, 'remont', ['r' => $r], $seo, $graph, 1);
}

function pn_page_ipoteka(): string {
    $s = Repo::settingsAll();
    $progs = array_values(array_filter($s['mortgage_programs'] ?? [], fn($p) => isset($p['name'], $p['rate'])));
    $minRate = $progs ? min(array_column($progs, 'rate')) : null;
    $seo = ['title' => 'Ипотека на квартиру в Екатеринбурге' . ($minRate !== null ? ' от ' . str_replace('.', ',', (string) $minRate) . ' %' : '') . ' — калькулятор и подбор программы | Платформа недвижимости',
        'description' => 'Рассчитайте ипотеку: ' . implode(', ', array_map(fn($p) => $p['name'] . ' ' . str_replace('.', ',', (string) $p['rate']) . ' %', $progs))
            . '. Подаём заявку сразу в несколько банков: Сбер, ВТБ, Альфа-Банк, ДОМ.РФ и другие.',
        'path' => 'ipoteka/', 'image' => 'assets/img/kv_living2.jpg'];
    $crumbs = [['Главная', ''], ['Ипотека', 'ipoteka/']];
    return pn_subpage(200, 'ipoteka', ['progs' => $progs, 'apts' => Repo::apartments()], $seo, [seo_breadcrumbs($crumbs, $s)], 1);
}

function pn_family_note(): string {
    $t = Repo::settingsAll()['family_tiers'] ?? [];
    if (!$t) return 'Для семей с детьми, на новостройки. Условия подтвердит банк — проверим, подходите ли вы.';
    $f = fn($x) => str_replace('.', ',', (string) $x);
    return 'Новостройки. Ставка и лимит по числу детей: ' . implode(', ', array_map(fn($x) => ($x['kids'] >= 5 ? '5+' : $x['kids']) . ' — ' . $f($x['rate']) . ' % до ' . $f($x['limit'] / 1e6) . ' млн', $t))
        . '. Сверх лимита — по рыночной ставке.';
}
