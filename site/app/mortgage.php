<?php
// Ипотека по правилам из админки. Программы: [{name, rate, limit?}] — limit (₽) — лимит льготной части; сверх лимита — рыночная ставка
// (так банки выдают «комбинированную» ипотеку). Семейная: ставка и лимит зависят от числа детей — family_tiers [{kids, rate, limit}].
// Тот же расчёт — в assets/js/data.js (PN.mort) и assets/js/page.js; при изменении править все три.

function pn_ann(float $L, float $rate, int $months): float {
    if ($L <= 0) return 0.0;
    $m = $rate / 1200;
    return $m > 0 ? $L * $m / (1 - pow(1 + $m, -$months)) : $L / $months;
}
function pn_is_family(array $p): bool { return mb_stripos((string) ($p['name'] ?? ''), 'семейн') !== false; }
function pn_market_rate(array $s): float {
    $progs = $s['mortgage_programs'] ?? [];
    foreach ($progs as $p) if (mb_stripos((string) $p['name'], 'рыноч') !== false) return (float) $p['rate'];
    return $progs ? (float) max(array_column($progs, 'rate')) : 20.0;
}
// Ставка и лимит программы с учётом детей (для семейной).
function pn_prog_terms(array $p, array $s, int $kids = 1): array {
    if (pn_is_family($p) && !empty($s['family_tiers'])) {
        $t = null;
        foreach ($s['family_tiers'] as $x) if ((int) $x['kids'] <= max(1, $kids) && (!$t || (int) $x['kids'] > (int) $t['kids'])) $t = $x;
        if ($t) return ['rate' => (float) $t['rate'], 'limit' => isset($t['limit']) ? (int) $t['limit'] : null];
    }
    return ['rate' => (float) $p['rate'], 'limit' => isset($p['limit']) && $p['limit'] ? (int) $p['limit'] : null];
}
// Платёж: ['pay', 'loan', 'over', 'parts' => [[сумма, ставка], ...]]
function pn_mort_pay(int $price, array $p, array $s, int $kids = 1, float $downPct = 20, int $years = 30): array {
    $L = $price * (1 - $downPct / 100); $n = $years * 12;
    $t = pn_prog_terms($p, $s, $kids);
    $parts = $t['limit'] !== null && $L > $t['limit'] ? [[$t['limit'], $t['rate']], [$L - $t['limit'], pn_market_rate($s)]] : [[$L, $t['rate']]];
    $pay = array_sum(array_map(fn($x) => pn_ann($x[0], $x[1], $n), $parts));
    return ['pay' => (int) round($pay), 'loan' => (int) round($L), 'over' => (int) round($pay * $n - $L), 'parts' => $parts];
}
// Программа «по умолчанию» для объявления: новостройка — семейная (1 ребёнок), вторичка — рыночная.
function pn_default_prog(array $a, array $s): array {
    $progs = $s['mortgage_programs'] ?? [];
    if ($a['market'] === 'new') foreach ($progs as $p) if (pn_is_family($p)) return $p;
    foreach ($progs as $p) if (mb_stripos((string) $p['name'], 'рыноч') !== false) return $p;
    return $progs ? end($progs) : ['name' => 'Рыночная', 'rate' => 20];
}
// Публичная конфигурация для JS калькуляторов.
function pn_mort_cfg(array $s): array {
    return ['progs' => array_values(array_map(fn($p) => ['name' => $p['name'], 'rate' => (float) $p['rate'], 'limit' => isset($p['limit']) && $p['limit'] ? (int) $p['limit'] : null,
        'family' => pn_is_family($p)], $s['mortgage_programs'] ?? [])), 'tiers' => $s['family_tiers'] ?? [], 'market' => pn_market_rate($s), 'date' => $s['rates_date'] ?? null];
}
function pn_rates_date_ru(array $s): string {
    $d = $s['rates_date'] ?? ''; return preg_match('~^(\d{4})-(\d\d)-(\d\d)$~', $d, $m) ? "$m[3].$m[2].$m[1]" : '';
}
