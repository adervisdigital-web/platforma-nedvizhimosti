<?php
// Фото. Имя без папки ('kv_living2', 'houses/n235_1') — файл прототипа в assets/img/*.jpg.
// Загруженные из админки — 'u/<id>' с WebP 480/960/2000 в uploads/ (задача 9).
function pn_img_attrs(string $name, string $sizes = '100vw'): string {
    return 'src="assets/img/' . pn_e($name) . '.jpg"';
}
