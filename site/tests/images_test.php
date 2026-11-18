<?php
require_once __DIR__ . '/../app/bootstrap.php';
ini_set('memory_limit', '1024M');
$GLOBALS['PN_UPLOADS'] = __DIR__ . '/_tmp/uploads';
$fx = fn($n) => __DIR__ . "/fixtures/$n";
pn_t('фото 8000×6000 → WebP 480/960/2000', function () {
    $f = __DIR__ . '/_tmp/big.jpg';
    if (!is_file($f)) { $im = imagecreatetruecolor(8000, 6000); imagefill($im, 0, 0, imagecolorallocate($im, 120, 140, 160)); imagejpeg($im, $f, 60); imagedestroy($im); }
    $r = pn_image_store($f, 'Огромное фото.JPG');
    pn_ok(str_starts_with($r['id'], 'u/'), 'id с u/');
    foreach ([480, 960, 2000] as $w) pn_eq(getimagesize(pn_uploads_dir() . '/' . $r["w$w"])[0], $w, "ширина $w");
});
pn_t('EXIF-поворот: альбомный кадр с orientation=6 становится портретным', function () use ($fx) {
    $r = pn_image_store($fx('exif6.jpg'), 'exif6.jpg');
    [$w, $h] = getimagesize(pn_uploads_dir() . '/' . $r['w480']);
    pn_ok($h > $w, "ожидался портрет, получено {$w}×{$h}");
});
pn_t('маленькое фото не растягивается, PNG принимается', function () use ($fx) {
    $r = pn_image_store($fx('small.png'), 'small.png');
    pn_eq(getimagesize(pn_uploads_dir() . '/' . $r['w2000'])[0], 300);
});
pn_t('pdf, svg, «фальшивый jpg» — отказ с понятным текстом', function () use ($fx) {
    foreach (['doc.pdf', 'pic.svg', 'fake.jpg'] as $n) {
        $err = null; try { pn_image_store($fx($n), $n); } catch (InvalidArgumentException $e) { $err = $e->getMessage(); }
        pn_eq($err, 'Можно загружать только JPG, PNG или WebP', $n);
    }
});
pn_t('srcset и атрибуты картинки', function () {
    pn_eq(pn_srcset(['w480' => '202611/a-480.webp', 'w960' => '202611/a-960.webp', 'w2000' => '202611/a-2000.webp']),
        'uploads/202611/a-480.webp 480w, uploads/202611/a-960.webp 960w, uploads/202611/a-2000.webp 2000w');
    pn_ok(str_contains(pn_img_attrs('u/202611/a'), 'srcset="uploads/202611/a-480.webp 480w'), 'srcset для загруженного');
    pn_eq(pn_img_attrs('kv_living2'), 'src="assets/img/kv_living2.jpg"');
    pn_ok(str_contains(pn_img_attrs('houses/u/202611/b'), 'uploads/202611/b-960.webp'), 'загруженное фото дома');
});
