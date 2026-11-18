<?php
// Конфигурация. Локальные переопределения (не в git) — app/local.php, возвращает массив.
function pn_config(): array {
    static $c = null;
    if ($c !== null && empty($GLOBALS['PN_CONFIG_RESET'])) return $c;
    $GLOBALS['PN_CONFIG_RESET'] = false;
    $root = dirname(__DIR__);
    $c = [
        'root'     => $root,
        'dsn'      => 'sqlite:' . $root . '/data/site.sqlite',
        'demo'     => filter_var(getenv('PN_DEMO') ?: ($GLOBALS['PN_DEMO'] ?? false), FILTER_VALIDATE_BOOL),
        'base_url' => getenv('PN_BASE_URL') ?: '',
        'source'   => getenv('PN_SOURCE') ?: 'db',
    ];
    if (is_file(__DIR__ . '/local.php')) $c = array_replace($c, (array) require __DIR__ . '/local.php');
    return $c;
}
