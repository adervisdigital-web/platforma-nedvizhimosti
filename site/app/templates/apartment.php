<?php /** Страница квартиры. Переменные: $a (Repo::apartment), $idx (номер в списке главной — для #obj-N), $pay (платёж в ипотеку, ₽/мес), $rate, $settings */
$where = $a['complex'] ?? $a['address'];
$per_m = (int) round($a['price'] / max(1, $a['area'])); ?>
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <a href="./#list">Квартиры</a> · <span><?= pn_e($where) ?></span></nav>
<article class="pg-obj">
  <div class="pg-gal"><?php foreach ($a['photos'] as $k => $ph): ?>
    <img <?= pn_img_attrs($ph, $k ? '(max-width: 900px) 100vw, 30vw' : '(max-width: 900px) 100vw, 60vw') ?> alt="<?= pn_e(pn_apt_title($a)) ?><?= $k ? ', фото ' . ($k + 1) : '' ?>" <?= $k ? 'loading="lazy"' : '' ?>>
  <?php endforeach; ?></div>
  <div class="pg-info">
    <p class="pg-tag"><?= $a['market'] === 'new' ? 'Новостройка' : 'Вторичка' ?><?= $a['special'] ? ' · спецпредложение' : '' ?></p>
    <h1><?= pn_e(pn_rooms($a['rooms'])) ?>, <?= pn_area($a['area']) ?></h1>
    <p class="pg-where"><?= pn_e($where) ?> · <?= pn_e($a['district']) ?> · <?= $a['floor'] ?>/<?= $a['floors'] ?> этаж</p>
    <p class="pg-price"><?= pn_rub($a['price']) ?><?php if ($a['discount_pct']): ?> <span>−<?= $a['discount_pct'] ?> %</span><?php endif; ?></p>
    <p class="pg-sub"><?= pn_rub($per_m) ?>/м² · в ипотеку от <b><?= pn_rub($pay) ?>/мес</b> (ставка <?= $rate ?>&nbsp;%, взнос 20&nbsp;%, 30&nbsp;лет)</p>
    <dl class="pg-par">
      <dt>Статус дома</dt><dd><?= pn_e($a['house_status']) ?></dd>
      <dt>Отделка</dt><dd><?= pn_e($a['finish_label']) ?></dd>
      <dt>Этаж</dt><dd><?= $a['floor'] ?> из <?= $a['floors'] ?></dd>
      <dt>Район</dt><dd><?= pn_e($a['district']) ?></dd>
    </dl>
    <?php if ($a['complex_checks']): ?>
    <div class="pg-chk"><h2>Что мы проверили</h2><ul><?php foreach ($a['complex_checks'] as $c): ?><li><?= pn_e($c) ?></li><?php endforeach; ?></ul></div>
    <?php endif; ?>
    <?php if (!empty($a['description'])): ?><div class="pg-txt"><?= nl2br(pn_e($a['description'])) ?></div><?php endif; ?>
    <div class="pg-act">
      <a class="pg-btn red" href="./#obj-<?= $idx ?>">Записаться на просмотр</a>
      <a class="pg-btn" href="tel:<?= pn_e($settings['phone_tel'] ?? '') ?>">Позвонить</a>
    </div>
  </div>
</article>
