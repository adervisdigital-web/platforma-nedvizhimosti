<?php
// Мини-раннер тестов: pn_t('имя', fn() => ...); проверки pn_eq / pn_ok.
$GLOBALS['PN_T'] = ['pass' => 0, 'fail' => 0, 'msgs' => []];
function pn_t(string $name, callable $fn): void {
    try { $fn(); $GLOBALS['PN_T']['pass']++; }
    catch (Throwable $e) { $GLOBALS['PN_T']['fail']++; $GLOBALS['PN_T']['msgs'][] = "FAIL $name: " . $e->getMessage(); }
}
function pn_eq($a, $b, string $msg = ''): void {
    if ($a !== $b) throw new Exception(($msg ? "$msg: " : '') . 'ожидалось ' . var_export($b, true) . ', получено ' . var_export($a, true));
}
function pn_ok($cond, string $msg = ''): void { if (!$cond) throw new Exception($msg ?: 'условие ложно'); }
// Свежая тестовая база: миграции + стартовые данные. Подменяет DSN конфигурации на временный файл.
function pn_test_db(bool $seed = true): PDO {
    $dir = __DIR__ . '/_tmp'; if (!is_dir($dir)) mkdir($dir, 0777, true);
    $GLOBALS['PN_DB'] = null; gc_collect_cycles();                  // закрыть прошлое соединение, иначе Windows не даст удалить файл
    $f = "$dir/test.sqlite"; foreach ([$f, "$f-wal", "$f-shm"] as $x) if (is_file($x) && !unlink($x)) throw new Exception("не удалить $x");
    $GLOBALS['PN_DSN'] = "sqlite:$f"; $GLOBALS['PN_CONFIG_RESET'] = true; $GLOBALS['PN_ENT_RESET'] = true;
    $db = pn_db(); pn_migrate($db); if ($seed) pn_seed_db($db);
    return $db;
}
