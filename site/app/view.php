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
// Переменные главной страницы: порядок кусков, SEO и встроенные данные (читает assets/js/data.js).
function pn_page_vars(array $extra = [], ?array $src = null): array {
    $cfg = pn_config();
    $src ??= pn_source();
    return $extra + ['base_tag' => $cfg['demo'] ? '<meta name="robots" content="noindex">' : '', 'order' => pn_page_order(), 'demo' => $cfg['demo'],
        'seo_head' => seo_meta(seo_main($src['settings']), $src['settings']), 'jsonld' => seo_jsonld([], $src['settings']),
        'data_json' => pn_data_json(pn_page_data($src, $cfg))];
}

// Настройки сайта для общих кусков (шапка, подвал, чат): один запрос на страницу; без базы — пусто.
function pn_site_settings(): array {
    static $s = null;
    if ($s === null) { try { $s = Repo::settingsAll(); } catch (Throwable $e) { $s = []; } }
    return $s;
}
// Ссылка на Telegram из настройки «telegram»: ник (с @ или без) или полная ссылка.
function pn_tg_url(array $s): string {
    $v = trim((string) ($s['telegram'] ?? ''));
    if ($v === '') return '';
    if (preg_match('~^https?://~i', $v)) return $v;
    return 'https://t.me/' . rawurlencode(ltrim($v, '@'));
}
// Кнопка мессенджера: есть ссылка — открывает его; есть только название (MAX) — подсказка, как найти; нет ничего — чат на сайте.
function pn_msgr_link(string $kind, string $cls = '', ?array $s = null): string {
    $s ??= pn_site_settings(); $c = $cls !== '' ? ' class="' . pn_e($cls) . '"' : '';
    if ($kind === 'tg') {
        $u = pn_tg_url($s);
        return $u !== '' ? '<a' . $c . ' href="' . pn_e($u) . '" target="_blank" rel="noopener">Telegram</a>' : '<a' . $c . ' href="#" data-soon="Telegram">Telegram</a>';
    }
    $v = trim((string) ($s['max'] ?? ''));
    if (preg_match('~^https?://~i', $v)) return '<a' . $c . ' href="' . pn_e($v) . '" target="_blank" rel="noopener">MAX</a>';
    return '<a' . $c . ' href="#" data-soon="MAX"' . ($v !== '' ? ' data-find="' . pn_e($v) . '"' : '') . '>MAX</a>';
}
