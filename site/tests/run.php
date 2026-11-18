<?php
// php site/tests/run.php [фильтр] — запускает site/tests/*_test.php
require __DIR__ . '/lib.php';
$filter = $argv[1] ?? '';
foreach (glob(__DIR__ . '/*_test.php') as $f) {
    if ($filter && !str_contains(basename($f), $filter)) continue;
    require $f;
}
foreach ($GLOBALS['PN_T']['msgs'] as $m) echo $m, "\n";
printf("%d passed, %d failed\n", $GLOBALS['PN_T']['pass'], $GLOBALS['PN_T']['fail']);
exit($GLOBALS['PN_T']['fail'] ? 1 : 0);
