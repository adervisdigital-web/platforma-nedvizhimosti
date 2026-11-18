<?php /** Проекты домов. Переменные: $hs (Repo::houses), $warm (₽/м² тёплый контур), $min, $settings */
$lines = array_values(array_unique(array_column($hs, 'line')));
$fls = array_values(array_unique(array_column($hs, 'fl'))); sort($fls); ?>
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <span>Дома</span></nav>
<div class="ct-head">
  <h1>Каменные дома по нашим проектам<i class="ct-dot" aria-hidden="true"></i></h1>
  <p class="ct-intro"><?= count($hs) ?> <?= pn_ru_plural(count($hs), 'проект', 'проекта', 'проектов') ?> от <?= pn_rub($min) ?> в тёплом контуре. Строим своими бригадами, смета — до начала работ,
    рассрочка без процентов до 5 лет и гарантия 5 лет. Планировку и фасад настроим под вашу семью.</p>
</div>

<div class="ct-pills dm-f" role="group" aria-label="Фильтр проектов">
  <button type="button" data-line="" aria-pressed="true">Все <span><?= count($hs) ?></span></button>
  <?php foreach ($lines as $l): ?><button type="button" data-line="<?= pn_e($l) ?>" aria-pressed="false"><?= pn_e($l) ?> <span><?= count(array_filter($hs, fn($h) => $h['line'] === $l)) ?></span></button><?php endforeach; ?>
  <span class="ct-sep" aria-hidden="true"></span>
  <?php foreach ($fls as $f): ?><button type="button" data-fl="<?= $f ?>" aria-pressed="false"><?= $f ?> <?= pn_ru_plural($f, 'этаж', 'этажа', 'этажей') ?></button><?php endforeach; ?>
</div>

<div class="dm-grid">
<?php foreach ($hs as $h): $price = $warm * $h['n']; ?>
  <article class="dm-card" data-l="<?= pn_e($h['line']) ?>" data-fl="<?= $h['fl'] ?>">
    <a class="dm-ph" href="doma/<?= pn_e($h['slug']) ?>/" tabindex="-1" aria-hidden="true"><img <?= pn_img_attrs('houses/' . ($h['ph'][0] ?? ''), '(max-width: 700px) 100vw, 50vw') ?> alt="" loading="lazy"></a>
    <div class="dm-body">
      <p class="dm-line"><i style="--c:<?= pn_e($h['c']) ?>"></i><?= pn_e($h['line']) ?></p>
      <h2><a href="doma/<?= pn_e($h['slug']) ?>/"><?= pn_e($h['line'] . ' ' . $h['n']) ?></a></h2>
      <p class="dm-motto"><?= pn_e($h['motto']) ?></p>
      <ul class="dm-par"><li><b><?= $h['n'] ?> м²</b>площадь</li><li><b><?= $h['fl'] ?></b><?= pn_ru_plural($h['fl'], 'этаж', 'этажа', 'этажей') ?></li><li><b><?= pn_e($h['rooms']) ?></b>комнаты</li></ul>
      <?php if ($warm): ?><p class="ct-price"><b>от <?= pn_rub($price) ?></b><span>тёплый контур</span></p>
      <p class="ct-pay">Рассрочка 0 % — от <b><?= pn_rub((int) round($price * .7 / 60)) ?>/мес</b></p><?php endif; ?>
    </div>
  </article>
<?php endforeach; ?>
</div>
<div class="ct-empty" data-dm-empty hidden><p>Таких проектов пока нет — построим по индивидуальному.</p></div>

<section class="sv-sec"><h2 class="sv-h">Как строим</h2>
  <ol class="sv-steps">
    <li><b>Выбор проекта</b>Подбираем проект и участок, адаптируем планировку и фасад под семью.</li>
    <li><b>Смета и договор</b>Считаем смету до начала работ — цена фиксируется в договоре.</li>
    <li><b>Стройка по этапам</b>Фундамент, коробка, кровля, окна — акт на каждый этап.</li>
    <li><b>Тёплый контур</b>Дом закрыт и утеплён: можно заходить с отделкой — своей или нашей.</li>
    <li><b>Гарантия 5 лет</b>Отвечаем за конструкцию и работы по договору.</li>
  </ol>
</section>

<section class="sv-band">
  <div><h2>Рассрочка 0 % до 5 лет</h2><p>Без банка и процентов: первый взнос от 30 %, остаток — равными платежами. Тёплый контур от <?= pn_rub($warm) ?>/м²; точную цену назовём в смете — она зависит от участка, фундамента и материала стен.</p></div>
  <a class="pg-btn red" href="./#houses">Рассчитать рассрочку</a>
</section>
<script src="assets/js/catalog.js" defer></script>
