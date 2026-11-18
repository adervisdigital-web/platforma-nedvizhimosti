<?php /** Карточка квартиры в каталоге. Переменные: $a (Repo::apartments), $i (порядок), $cx (pn_complexes_full), $s (настройки) */
$z = $a['complex'] && isset($cx[$a['complex']]) ? $cx[$a['complex']] : null;
$geo = pn_apt_geo($a, $cx, $s);
$ready = $a['market'] === 'secondary' || (int) $a['due'] === 0;
$ppm = (int) round($a['price'] / max(1, $a['area']));
$pay = pn_apt_pay($a, $s); ?>
<article class="ct-card" data-i="<?= $i ?>" data-p="<?= $a['price'] ?>" data-a="<?= pn_num($a['area']) ?>" data-r="<?= $a['rooms'] ?>" data-m="<?= $a['market'] === 'new' ? 'new' : 'sec' ?>"
  data-d="<?= pn_e(pn_slug((string) $a['district'])) ?>" data-z="<?= pn_e($z ? $z['slug'] : '') ?>" data-f="<?= $a['finish'] === 'with' ? 1 : 0 ?>" data-ready="<?= $ready ? 1 : 0 ?>" data-ppm="<?= $ppm ?>"
  <?= $geo ? 'data-lat="' . $geo[0] . '" data-lng="' . $geo[1] . '"' : '' ?>>
  <a class="ct-ph" href="kvartiry/<?= pn_e($a['slug']) ?>/" tabindex="-1" aria-hidden="true"><img <?= pn_img_attrs($a['photos'][0] ?? 'kv_empty', '(max-width: 700px) 100vw, (max-width: 1400px) 50vw, 33vw') ?> alt="" loading="lazy">
    <span class="ct-tags"><span><?= $a['market'] === 'new' ? 'Новостройка' : 'Вторичка' ?></span><?php if ($a['discount_pct']): ?><span class="red">−<?= $a['discount_pct'] ?> %</span><?php endif; ?><?php if ($a['special']): ?><span class="dark">Спецпредложение</span><?php endif; ?></span></a>
  <div class="ct-body">
    <h3><a href="kvartiry/<?= pn_e($a['slug']) ?>/"><?= pn_e(pn_rooms($a['rooms'])) ?>, <?= pn_area($a['area']) ?></a></h3>
    <p class="ct-where"><?php if ($z): ?><a href="<?= pn_e($z['path']) ?>"><?= pn_e($z['name']) ?></a><?php else: ?><?= pn_e((string) $a['address']) ?><?php endif; ?> · <?= pn_e((string) $a['district']) ?></p>
    <p class="ct-meta"><?= $a['floor'] ?>/<?= $a['floors'] ?> эт. · <?= pn_e($a['finish_label'] ?: ($a['finish'] === 'with' ? 'С отделкой' : 'Без отделки')) ?> · <?= pn_e(explode(' · ', (string) $a['house_status'])[0]) ?></p>
    <p class="ct-price"><b><?= pn_rub($a['price']) ?></b><span><?= pn_rub($ppm) ?>/м²</span></p>
    <p class="ct-pay">В ипотеку от <b><?= pn_rub($pay) ?>/мес</b></p>
  </div>
</article>
