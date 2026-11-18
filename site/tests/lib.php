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
