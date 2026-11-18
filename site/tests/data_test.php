<?php
require_once __DIR__ . '/../app/bootstrap.php';
pn_t('page_data: квартиры в форме прототипа', function () {
    $d = pn_page_data(pn_seed_all(), pn_config());
    pn_eq(count($d['items']), 12);
    $keys = array_keys($d['items'][0]);
    foreach (['r', 's', 'fl', 'fls', 'zk', 'd', 't', 'due', 'st', 'fin', 'p', 'img', 'x', 'y'] as $k) pn_ok(in_array($k, $keys, true), "нет ключа $k");
    pn_eq($d['items'][0]['t'], 'new'); pn_eq($d['items'][3]['t'], 'sec', 'вторичка');
    pn_eq($d['demo'], pn_config()['demo']);
    pn_eq(count($d['houses']), 5); pn_eq($d['progs'][0], ['Семейная', pn_seed('settings')['mortgage_programs'][0]['rate']]);
});
pn_t('page_data: в разметке нет закрывающего </script> внутри данных', function () {
    $h = pn_render('layout', pn_page_vars());
    pn_ok(str_contains($h, '<script id="pn-data" type="application/json">'), 'нет блока данных');
    $json = explode('</script>', explode('<script id="pn-data" type="application/json">', $h)[1])[0];
    pn_eq(json_decode($json, true)['settings']['phone'], '+7 965 500-29-18');
});
