<?php /** Галерея объекта: вкладки «Фото / Планировки», большой кадр, миниатюры, просмотр на весь экран (assets/js/page.js).
 * Переменные: $photos — [[attrs, alt]], $plans — [[attrs, подпись]], $planTab — подпись вкладки планировок. */
$planTab = $planTab ?? 'Планировка'; ?>
<section class="ob-gal" data-gal aria-label="Фото и планировки">
  <div class="ob-tabs" role="tablist">
    <button type="button" role="tab" aria-selected="true" data-tab="ph">Фото <span><?= count($photos) ?></span></button>
    <?php if ($plans): ?><button type="button" role="tab" aria-selected="false" data-tab="pl"><?= pn_e($planTab) ?><?= count($plans) > 1 ? ' <span>' . count($plans) . '</span>' : '' ?></button><?php endif; ?>
  </div>
  <div class="ob-pane" data-pane="ph">
    <div class="ob-stage">
      <?php foreach ($photos as $k => [$attrs, $alt]): ?>
      <button type="button" class="ob-slide<?= $k ? '' : ' is-cur' ?>" data-i="<?= $k ?>" aria-label="Открыть фото <?= $k + 1 ?> крупно"><img <?= $attrs ?> alt="<?= pn_e($alt) ?>"<?= $k ? ' loading="lazy"' : ' fetchpriority="high"' ?>></button>
      <?php endforeach; ?>
      <?php if (count($photos) > 1): ?>
      <button type="button" class="ob-nav prev" data-step="-1" aria-label="Предыдущее фото"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
      <button type="button" class="ob-nav next" data-step="1" aria-label="Следующее фото"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
      <span class="ob-count"><b>1</b> / <?= count($photos) ?></span>
      <?php endif; ?>
      <span class="ob-zoom" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></span>
    </div>
    <?php if (count($photos) > 1): ?><div class="ob-thumbs"><?php foreach ($photos as $k => [$attrs, $alt]): ?>
      <button type="button" class="<?= $k ? '' : 'is-cur' ?>" data-go="<?= $k ?>" aria-label="Фото <?= $k + 1 ?>"><img <?= $attrs ?> alt="" loading="lazy"></button><?php endforeach; ?></div><?php endif; ?>
  </div>
  <?php if ($plans): ?>
  <div class="ob-pane" data-pane="pl" hidden>
    <?php if (count($plans) > 1): ?><div class="ob-floors" role="tablist"><?php foreach ($plans as $k => [$attrs, $cap]): ?>
      <button type="button" class="<?= $k ? '' : 'is-cur' ?>" data-fl="<?= $k ?>"><?= pn_e($cap) ?></button><?php endforeach; ?></div><?php endif; ?>
    <?php foreach ($plans as $k => [$attrs, $cap]): ?>
    <figure class="ob-plan" data-flp="<?= $k ?>"<?= $k ? ' hidden' : '' ?>><button type="button" class="ob-planbtn" data-plan="<?= $k ?>" aria-label="Открыть планировку крупно"><img <?= $attrs ?> alt="Планировка: <?= pn_e($cap) ?>" loading="lazy"></button><figcaption><?= pn_e($cap) ?></figcaption></figure>
    <?php endforeach; ?>
  </div>
  <?php endif; ?>
</section>
