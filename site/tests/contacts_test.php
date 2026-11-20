<?php
require_once __DIR__ . '/../app/bootstrap.php';
// Контакты из настроек: Telegram, MAX, адрес офиса в подвале и в разметке для поисковиков.
pn_t('pn_tg_url: ник, ник с @, ссылка, пусто', function () {
    pn_eq(pn_tg_url(['telegram' => 'platfoma96']), 'https://t.me/platfoma96');
    pn_eq(pn_tg_url(['telegram' => ' @platfoma96 ']), 'https://t.me/platfoma96');
    pn_eq(pn_tg_url(['telegram' => 'https://t.me/+abc']), 'https://t.me/+abc');
    pn_eq(pn_tg_url([]), '');
});
pn_t('pn_msgr_link: ссылка, название MAX, без настроек — чат', function () {
    pn_ok(str_contains(pn_msgr_link('tg', '', ['telegram' => 'platfoma96']), 'href="https://t.me/platfoma96" target="_blank" rel="noopener"'), 'tg ссылка');
    pn_ok(str_contains(pn_msgr_link('tg', '', []), 'data-soon="Telegram"'), 'tg без ника');
    $m = pn_msgr_link('max', '', ['max' => 'Платформа недвижимости 96']);
    pn_ok(str_contains($m, 'data-soon="MAX"') && str_contains($m, 'data-find="Платформа недвижимости 96"'), 'max по названию');
    pn_ok(str_contains(pn_msgr_link('max', '', ['max' => 'https://max.ru/x']), 'href="https://max.ru/x"'), 'max ссылка');
    pn_ok(str_contains(pn_msgr_link('max', '', ['max' => '<b>']), 'data-find="&lt;b&gt;"'), 'экранирование');
});
pn_t('seo_org: адрес офиса и Telegram для поисковиков', function () {
    $o = seo_org(['phone' => '+7', 'address' => 'ул. Амундсена, 136', 'telegram' => 'platfoma96', 'domain' => 'p.forma196.ru']);
    pn_eq($o['address']['streetAddress'], 'ул. Амундсена, 136');
    pn_eq($o['address']['addressLocality'], 'Екатеринбург');
    pn_eq($o['sameAs'], ['https://t.me/platfoma96']);
    pn_ok(!isset(seo_org(['phone' => '+7'])['address']), 'без адреса — нет поля');
});
