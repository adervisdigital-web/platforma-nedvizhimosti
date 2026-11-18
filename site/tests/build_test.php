<?php
require_once __DIR__ . '/../app/bootstrap.php';
pn_t('build: витрина для GitHub Pages', function () {
    $out = __DIR__ . '/_tmp/build';
    $r = pn_build($out);
    pn_ok($r['pages'] >= 1, 'страниц');
    pn_ok(is_file("$out/index.html"), 'index.html');
    pn_eq(trim(file_get_contents("$out/robots.txt")), "User-agent: *\nDisallow: /");
    $idx = file_get_contents("$out/index.html");
    pn_ok(str_contains($idx, '<meta name="robots" content="noindex">'), 'noindex');
    pn_ok(str_contains($idx, '"demo":true'), 'demo в данных');
    pn_ok(is_file("$out/assets/js/app.js") && is_file("$out/assets/js/data.js") && is_file("$out/assets/css/site.css"), 'ассеты');
    pn_ok(is_file("$out/api/items.json"), 'api/items.json');
    $bad = [];
    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($out, FilesystemIterator::SKIP_DOTS));
    foreach ($it as $f) {
        if (str_ends_with($f, '.sqlite')) $bad[] = "база: $f";
        if (str_ends_with($f, '.html') && preg_match('~(href|src)="/(?!/)~', file_get_contents($f))) $bad[] = "абсолютный путь: $f";
    }
    pn_eq($bad, []);
});
