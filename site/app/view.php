<?php
// Отрисовка шаблонов app/templates/<name>.php. Переменные шаблону — массивом.
function pn_render(string $tpl, array $vars = []): string {
    $__file = __DIR__ . '/templates/' . $tpl . '.php';
    if (!is_file($__file)) throw new RuntimeException("нет шаблона $tpl");
    extract($vars, EXTR_SKIP);
    ob_start();
    include $__file;
    return ob_get_clean();
}
// Порядок кусков главной страницы — как в прототипе (templates/order.json пишет split_proto.py).
function pn_page_order(): array {
    return json_decode(file_get_contents(__DIR__ . '/templates/order.json'), true, 8, JSON_THROW_ON_ERROR);
}
// Переменные главной страницы: порядок кусков и встроенные данные (читает assets/js/data.js).
function pn_page_vars(array $extra = [], ?array $src = null): array {
    $cfg = pn_config();
    return $extra + ['base_tag' => '', 'order' => pn_page_order(), 'demo' => $cfg['demo'],
        'data_json' => pn_data_json(pn_page_data($src ?? pn_seed_all(), $cfg))];
}
