<?php
require_once __DIR__ . '/../app/bootstrap.php';
pn_t('slug: кириллица → латиница', function () {
    pn_eq(pn_slug('ЖК Липовый сквер'), 'zhk-lipovyy-skver');
    pn_eq(pn_slug('Северный Урал 235'), 'severnyy-ural-235');
    pn_eq(pn_slug('Ёлки, «Щука»!'), 'yolki-shchuka');
    pn_eq(pn_slug('  '), 'n-a');
});
pn_t('migrate: один раз', function () {
    $db = pn_test_db(false);
    pn_eq(pn_migrate($db), 0, 'повторный прогон');
    pn_ok((int) $db->query("select count(*) from migrations")->fetchColumn() >= 1, 'записана миграция');
});
pn_t('seed: 12 квартир, 5 домов, ЖК связаны', function () {
    $db = pn_test_db();
    pn_eq((int) $db->query('select count(*) from apartments')->fetchColumn(), 12);
    pn_eq((int) $db->query('select count(*) from houses')->fetchColumn(), 5);
    pn_eq((int) $db->query("select count(*) from apartments where market='new' and complex_id is null")->fetchColumn(), 0, 'новостройки привязаны к ЖК');
    pn_eq($db->query("select slug from apartments where id=1")->fetchColumn(), '1-zhk-lipovyy-skver');
});
pn_t('нельзя удалить ЖК, у которого есть квартиры', function () {
    $db = pn_test_db();
    $err = null; try { $db->exec("delete from complexes where slug='zhk-lipovyy-skver'"); } catch (PDOException $e) { $err = $e; }
    pn_ok($err instanceof PDOException, 'удаление должно упасть');
});
