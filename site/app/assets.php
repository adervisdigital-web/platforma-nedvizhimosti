<?php
// JS-исходники site/src/js/NN-*.js склеиваются в один public/assets/js/app.js в порядке order.json:
// в прототипе функции вызываются раньше объявления (hoisting внутри одного скрипта).
function pn_bundle_js(): string {
    $dir = pn_config()['root'] . '/src/js';
    $order = json_decode(file_get_contents("$dir/order.json"), true, 8, JSON_THROW_ON_ERROR);
    return implode('', array_map(fn($f) => file_get_contents("$dir/$f"), $order));
}
function pn_write_bundle(): string {
    $out = pn_config()['root'] . '/public/assets/js/app.js';
    file_put_contents($out, pn_bundle_js());
    return $out;
}
