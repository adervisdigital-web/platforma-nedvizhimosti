<?php
// Статическая витрина для GitHub Pages: те же шаблоны, DEMO=1, относительные пути, без базы и персональных данных.
function pn_rcopy(string $from, string $to): void {
    if (!is_dir($to)) mkdir($to, 0777, true);
    foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($from, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::SELF_FIRST) as $f) {
        $dst = $to . DIRECTORY_SEPARATOR . substr($f->getPathname(), strlen($from) + 1);
        $f->isDir() ? (is_dir($dst) || mkdir($dst, 0777, true)) : copy($f->getPathname(), $dst);
    }
}
function pn_rclear(string $dir): void {
    foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::CHILD_FIRST) as $f)
        $f->isDir() ? rmdir($f->getPathname()) : unlink($f->getPathname());
}
// $source: 'seed' (сейчас) или 'db' (после задачи 7). Возвращает ['pages' => N, 'out' => путь].
function pn_build(string $out, string $source = 'seed'): array {
    if (is_dir($out) && (new FilesystemIterator($out))->valid() && !is_file("$out/.pn-build"))
        throw new RuntimeException("$out не пустая и не похожа на прошлую сборку — не трогаю");
    $prevDemo = $GLOBALS['PN_DEMO'] ?? false;
    $GLOBALS['PN_DEMO'] = true; $GLOBALS['PN_CONFIG_RESET'] = true;
    try {
        if (is_dir($out)) pn_rclear($out); else mkdir($out, 0777, true);
        pn_write_bundle();
        $root = pn_config()['root'];
        $src = $source === 'db' ? pn_db_source() : pn_seed_all();
        $data = pn_page_data($src, pn_config());
        file_put_contents("$out/index.html", pn_render('layout', pn_page_vars([], $src)));
        $pages = 1;
        foreach (pn_build_pages($src) as $rel => $html) {           // страницы объектов — задача 8
            if (!is_dir(dirname("$out/$rel"))) mkdir(dirname("$out/$rel"), 0777, true);
            file_put_contents("$out/$rel", $html); $pages++;
        }
        pn_rcopy("$root/public/assets", "$out/assets");
        copy("$root/public/kabinet.html", "$out/kabinet.html");
        mkdir("$out/api");
        $j = fn($v) => json_encode($v, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
        file_put_contents("$out/api/items.json", $j($data['items']));
        file_put_contents("$out/api/houses.json", $j($data['houses']));
        file_put_contents("$out/api/reviews.json", $j($data['reviews']));
        file_put_contents("$out/api/settings.json", $j($data['settings']));
        file_put_contents("$out/api/complexes.json", $j($src['complexes']));
        file_put_contents("$out/robots.txt", "User-agent: *\nDisallow: /\n");
        file_put_contents("$out/.nojekyll", '');
        file_put_contents("$out/.pn-build", date('c'));
        return ['pages' => $pages, 'out' => $out];
    } finally {
        $GLOBALS['PN_DEMO'] = $prevDemo; $GLOBALS['PN_CONFIG_RESET'] = true;
    }
}
// Страницы объектов (задача 8). Пока пусто.
function pn_build_pages(array $src): array { return []; }
