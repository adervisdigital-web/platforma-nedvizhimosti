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
    $prevDemo = $GLOBALS['PN_DEMO'] ?? false; $prevDsn = $GLOBALS['PN_DSN'] ?? null; $prevDb = $GLOBALS['PN_DB'] ?? null;
    $GLOBALS['PN_DEMO'] = true; $GLOBALS['PN_CONFIG_RESET'] = true;
    try {
        if (is_dir($out)) pn_rclear($out); else mkdir($out, 0777, true);
        pn_write_bundle();
        $root = pn_config()['root'];
        if ($source === 'seed') pn_build_seed_db();                 // страницы объектов строятся из базы — для seed поднимаем временную
        $src = pn_db_source();
        $data = pn_page_data($src, pn_config());
        file_put_contents("$out/index.html", pn_render('layout', pn_page_vars([], $src)));
        $pages = 1;   // + страницы квартир и домов; политика не считается
        foreach (pn_build_pages($src) as $rel => $html) {           // страницы объектов — задача 8
            if (!is_dir(dirname("$out/$rel"))) mkdir(dirname("$out/$rel"), 0777, true);
            file_put_contents("$out/$rel", $html);
            if (!str_starts_with($rel, 'privacy/')) $pages++;
        }
        pn_rcopy("$root/public/assets", "$out/assets");
        copy("$root/public/kabinet.html", "$out/kabinet.html");
        if (is_dir("$root/public/uploads")) pn_rcopy("$root/public/uploads", "$out/uploads");   // фото из админки (только картинки WebP)
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
        if ($source === 'seed') { $GLOBALS['PN_DB'] = $prevDb; if ($prevDsn === null) unset($GLOBALS['PN_DSN']); else $GLOBALS['PN_DSN'] = $prevDsn; }
    }
}
// Временная база из data/seed — чтобы витрина собиралась без рабочей базы.
function pn_build_seed_db(): void {
    $f = sys_get_temp_dir() . '/pn_build_seed.sqlite';
    $GLOBALS['PN_DB'] = null; gc_collect_cycles();
    foreach ([$f, "$f-wal", "$f-shm"] as $x) if (is_file($x)) unlink($x);
    $GLOBALS['PN_DSN'] = "sqlite:$f"; $GLOBALS['PN_CONFIG_RESET'] = true;
    pn_migrate(pn_db()); pn_seed_db(pn_db());
}
// Страницы объектов и политика: путь файла → HTML.
function pn_build_pages(array $src): array {
    $o = [];
    foreach (Repo::apartments() as $a) $o["kvartiry/{$a['slug']}/index.html"] = pn_page_apartment($a['slug']);
    foreach (Repo::houses() as $h) $o["doma/{$h['slug']}/index.html"] = pn_page_house($h['slug']);
    foreach (pn_catalog_paths() as $p) $o[$p . 'index.html'] = pn_route('GET', '/' . $p)[2];   // каталог, подборки, ЖК
    $o['privacy/index.html'] = pn_route('GET', '/privacy/')[2];
    return $o;
}
