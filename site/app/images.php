<?php
// Фото. Имя без «u/» ('kv_living2', 'houses/n235_1') — файл прототипа assets/img/<имя>.jpg.
// Загруженные из админки — 'u/<ГГГГММ>/<id>': WebP 480/960/2000 в public/uploads/<ГГГГММ>/<id>-<w>.webp.
const PN_IMG_WIDTHS = [480, 960, 2000];
const PN_IMG_MAX_BYTES = 25 * 1024 * 1024;

function pn_uploads_dir(): string { return $GLOBALS['PN_UPLOADS'] ?? pn_config()['root'] . '/public/uploads'; }

// Сохраняет загруженный файл: проверка типа по содержимому, поворот по EXIF, пересохранение через GD (метаданные удаляются).
// Возвращает ['id' => 'u/ГГГГММ/xxxx', 'w480' => 'ГГГГММ/xxxx-480.webp', 'w960' => …, 'w2000' => …] (пути — от uploads/).
function pn_image_store(string $tmpPath, string $origName): array {
    $bad = 'Можно загружать только JPG, PNG или WebP';
    if (!is_file($tmpPath)) throw new InvalidArgumentException('Файл не загрузился, попробуйте ещё раз');
    if (filesize($tmpPath) > PN_IMG_MAX_BYTES) throw new InvalidArgumentException('Файл больше 25 МБ — уменьшите его и загрузите снова');
    $mime = (new finfo(FILEINFO_MIME_TYPE))->file($tmpPath);
    if (!in_array($mime, ['image/jpeg', 'image/png', 'image/webp'], true)) throw new InvalidArgumentException($bad);
    $info = @getimagesize($tmpPath);
    if (!$info || $info[0] < 1 || $info[1] < 1) throw new InvalidArgumentException($bad);
    if ($info[0] * $info[1] > 60_000_000) throw new InvalidArgumentException('Слишком большое фото (больше 60 Мп) — уменьшите его до 8000 px по длинной стороне');
    $need = (int) ($info[0] * $info[1] * 5.5) + 64 * 1024 * 1024;                 // GD: ~4–5 байт на пиксель + запас
    if (pn_bytes(ini_get('memory_limit')) < $need) @ini_set('memory_limit', (string) $need);
    $im = match ($mime) { 'image/jpeg' => @imagecreatefromjpeg($tmpPath), 'image/png' => @imagecreatefrompng($tmpPath), 'image/webp' => @imagecreatefromwebp($tmpPath) };
    if (!$im) throw new InvalidArgumentException($bad);
    $max = max(PN_IMG_WIDTHS);
    if (max(imagesx($im), imagesy($im)) > $max) {                                    // сначала уменьшаем — поворот большого кадра съедает вдвое больше памяти
        $k = $max / max(imagesx($im), imagesy($im));
        $small = imagescale($im, (int) round(imagesx($im) * $k), (int) round(imagesy($im) * $k), IMG_BICUBIC);
        imagedestroy($im); $im = $small;
    }
    if ($mime === 'image/jpeg' && function_exists('exif_read_data')) $im = pn_exif_fix($im, (int) (@exif_read_data($tmpPath)['Orientation'] ?? 1));
    $dir = date('Ym'); $id = bin2hex(random_bytes(6));
    $abs = pn_uploads_dir() . "/$dir";
    if (!is_dir($abs) && !mkdir($abs, 0775, true)) throw new RuntimeException('Не удалось создать папку для фото — проверьте права на uploads/');
    $out = ['id' => "u/$dir/$id"];
    $w0 = imagesx($im); $h0 = imagesy($im);
    foreach (PN_IMG_WIDTHS as $w) {
        $tw = min($w, $w0); $th = (int) round($h0 * $tw / $w0);
        $dst = $tw === $w0 ? $im : imagescale($im, $tw, $th, IMG_BICUBIC);
        imagewebp($dst, "$abs/$id-$w.webp", 82);
        if ($dst !== $im) imagedestroy($dst);
        $out["w$w"] = "$dir/$id-$w.webp";
    }
    imagedestroy($im);
    return $out;
}

function pn_exif_fix(GdImage $im, int $o): GdImage {
    if ($o === 2 || $o === 4 || $o === 5 || $o === 7) imageflip($im, IMG_FLIP_HORIZONTAL);
    $deg = match ($o) { 3, 4 => 180, 5, 6 => -90, 7, 8 => 90, default => 0 };
    if (!$deg) return $im;
    $r = imagerotate($im, $deg, 0); imagedestroy($im); return $r;
}

function pn_bytes(string $v): int {
    $v = trim($v); if ($v === '-1') return PHP_INT_MAX;
    $n = (int) $v; $u = strtolower(substr($v, -1));
    return $u === 'g' ? $n << 30 : ($u === 'm' ? $n << 20 : ($u === 'k' ? $n << 10 : $n));
}

function pn_srcset(array $img): string {
    return implode(', ', array_map(fn($w) => 'uploads/' . $img["w$w"] . " {$w}w", PN_IMG_WIDTHS));
}

// Атрибуты <img>: для загруженных — src (960) + srcset + sizes; для фото прототипа — src на JPG.
function pn_img_attrs(string $name, string $sizes = '100vw'): string {
    if (preg_match('~^(?:[a-z]+/)?u/(\d{6}/[0-9a-f]+)$~', $name, $m)) {
        $img = []; foreach (PN_IMG_WIDTHS as $w) $img["w$w"] = "{$m[1]}-$w.webp";
        return 'src="uploads/' . pn_e($img['w960']) . '" srcset="' . pn_e(pn_srcset($img)) . '" sizes="' . pn_e($sizes) . '"';
    }
    if (preg_match('~^[a-z0-9/_-]+\.svg$~', $name)) return 'src="assets/img/' . pn_e($name) . '"';   // схемы планировок из seed
    return 'src="assets/img/' . pn_e($name) . '.jpg"';
}
