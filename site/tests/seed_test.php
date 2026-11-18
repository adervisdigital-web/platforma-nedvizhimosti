<?php
$seed = fn(string $n) => json_decode(file_get_contents(__DIR__ . "/../data/seed/$n.json"), true, 512, JSON_THROW_ON_ERROR);
pn_t('seed: 12 квартир с ценой и фото', function () use ($seed) {
    $a = $seed('apartments'); pn_eq(count($a), 12);
    foreach ($a as $x) { pn_ok($x['price'] > 0, 'цена'); pn_ok(!empty($x['photos'][0]), 'фото'); pn_ok(in_array($x['market'], ['new', 'secondary'], true), 'market'); }
});
pn_t('seed: 5 домов, первый — Северный Урал 235', function () use ($seed) {
    $h = $seed('houses'); pn_eq(count($h), 5); pn_eq($h[0]['slug'], 'severnyy-ural-235');
});
pn_t('seed: настройки из спецификации', function () use ($seed) {
    $s = $seed('settings');
    pn_eq($s['phone'], '+7 965 500-29-18'); pn_eq($s['renovation_prices'], [20000, 45000, 80000]); pn_eq($s['warm_contour_from'], 75000);
});
pn_t('seed: ЖК и отзывы', function () use ($seed) {
    pn_ok(count($seed('complexes')) >= 3, 'ЖК'); $r = $seed('reviews'); pn_ok(count($r) >= 3, 'отзывы'); pn_eq($r[0]['is_demo'], 1);
});
