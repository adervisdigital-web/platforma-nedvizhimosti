<?php /** Страница проекта дома. Переменные: $h (Repo::house, форма прототипа + price_from/area), $settings */
$warm = (int) ($settings['warm_contour_from'] ?? 0); ?>
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <a href="./#houses">Дома</a> · <span><?= pn_e($h['line'] . ' ' . $h['n']) ?></span></nav>
<article class="pg-obj">
  <div class="pg-gal"><?php foreach ($h['ph'] as $k => $ph): ?>
    <img <?= pn_img_attrs('houses/' . $ph, $k ? '(max-width: 900px) 100vw, 30vw' : '(max-width: 900px) 100vw, 60vw') ?> alt="Дом «<?= pn_e($h['line'] . ' ' . $h['n']) ?>»<?= $k ? ', фото ' . ($k + 1) : '' ?>" <?= $k ? 'loading="lazy"' : '' ?>>
  <?php endforeach; ?></div>
  <div class="pg-info">
    <p class="pg-tag" style="--c:<?= pn_e($h['c']) ?>">Линейка «<?= pn_e($h['line']) ?>»</p>
    <h1><?= pn_e($h['line'] . ' ' . $h['n']) ?></h1>
    <p class="pg-where"><?= pn_e($h['motto']) ?></p>
    <?php if ($warm && !empty($h['area'])): ?><p class="pg-price">от <?= pn_rub((int) round($warm * $h['area'])) ?></p><p class="pg-sub">тёплый контур от <?= pn_rub($warm) ?>/м² · рассрочка 0&nbsp;% до 5&nbsp;лет</p><?php endif; ?>
    <dl class="pg-par">
      <dt>Площадь</dt><dd><?= pn_area($h['n']) ?></dd>
      <dt>Этажей</dt><dd><?= $h['fl'] ?></dd>
      <dt>Комнаты</dt><dd><?= pn_e($h['rooms']) ?></dd>
      <dt>Потолки</dt><dd><?= pn_e($h['ceil']) ?></dd>
    </dl>
    <div class="pg-chk"><h2>Особенности</h2><ul><?php foreach ($h['feats'] as $f): ?><li><?= pn_e($f) ?></li><?php endforeach; ?></ul></div>
    <div class="pg-txt"><p><b><?= pn_e($h['idea']) ?></b></p><?php foreach ($h['text'] as $p): ?><p><?= pn_e($p) ?></p><?php endforeach; ?></div>
    <?php if ($h['plans']): ?><div class="pg-plans"><h2>Планировки</h2><?php foreach ($h['plans'] as $pl): ?>
      <figure><img <?= pn_img_attrs('houses/' . $pl[1], '(max-width: 900px) 100vw, 45vw') ?> alt="Планировка: <?= pn_e($pl[0]) ?>" loading="lazy"><figcaption><?= pn_e($pl[0]) ?></figcaption></figure>
    <?php endforeach; ?></div><?php endif; ?>
    <div class="pg-act">
      <a class="pg-btn red" href="./#house-<?= pn_e($h['id']) ?>">Рассчитать рассрочку</a>
      <a class="pg-btn" href="tel:<?= pn_e($settings['phone_tel'] ?? '') ?>">Позвонить</a>
    </div>
  </div>
</article>
