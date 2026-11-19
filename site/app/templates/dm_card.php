<?php /** Карточка проекта дома: страница «Дома» и «Другие проекты» на странице дома. Переменные: $h (Repo::houses), $warm (₽/м² тёплый контур) */
$price = (int) $warm * $h['n']; ?>
  <article class="dm-card" data-l="<?= pn_e($h['line']) ?>" data-fl="<?= $h['fl'] ?>">
    <a class="dm-ph" href="doma/<?= pn_e($h['slug']) ?>/" tabindex="-1" aria-hidden="true"><img <?= pn_img_attrs('houses/' . ($h['ph'][0] ?? ''), '(max-width: 700px) 100vw, 50vw') ?> alt="" loading="lazy"></a>
    <div class="dm-body">
      <p class="dm-line"><i style="--c:<?= pn_e($h['c']) ?>"></i><?= pn_e($h['line']) ?></p>
      <h2><a href="doma/<?= pn_e($h['slug']) ?>/"><?= pn_e($h['line'] . ' ' . $h['n']) ?></a></h2>
      <p class="dm-motto"><?= pn_e($h['motto']) ?></p>
      <ul class="dm-par"><li><b><?= $h['n'] ?> м²</b>площадь</li><li><b><?= $h['fl'] ?></b><?= pn_ru_plural($h['fl'], 'этаж', 'этажа', 'этажей') ?></li><li><b><?= pn_e($h['rooms']) ?></b>комнаты</li></ul>
      <?php if ($price): ?><p class="ct-price"><b>от <?= pn_rub($price) ?></b><span>тёплый контур</span></p>
      <p class="ct-pay">Рассрочка 0 % — от <b><?= pn_rub((int) round($price * .7 / 60)) ?>/мес</b></p><?php endif; ?>
    </div>
  </article>
