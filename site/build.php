<?php
// php site/build.php [--out=путь] [--source=seed|db] — статическая витрина (DEMO) для GitHub Pages, по умолчанию в 10_Сайт/ в корне репо.
require __DIR__ . '/app/bootstrap.php';
$opt = getopt('', ['out:', 'source:']);
$r = pn_build($opt['out'] ?? dirname(__DIR__) . '/10_Сайт', $opt['source'] ?? 'seed');
echo "собрано: {$r['pages']} стр. → {$r['out']}\n";
