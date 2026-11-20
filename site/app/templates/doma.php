<?php /** Проекты домов. Переменные: $hs (Repo::houses), $warm (₽/м² тёплый контур), $min, $settings */
$lines = array_values(array_unique(array_column($hs, 'line')));
$fls = array_values(array_unique(array_column($hs, 'fl'))); sort($fls); ?>
<section class="sx-hero" style="--sxp:50% 72%"><img class="sx-bg" src="assets/img/houses/y195_1.jpg" srcset="assets/img/houses/y195_1-1280.jpg 1280w, assets/img/houses/y195_1.jpg 1600w" sizes="100vw" alt="" fetchpriority="high" decoding="async"><div class="sx-in">
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <span>Дома</span></nav>
<div class="ct-head">
  <h1>Каменные дома по нашим проектам<i class="ct-dot" aria-hidden="true"></i></h1>
  <p class="ct-intro"><?= count($hs) ?> <?= pn_ru_plural(count($hs), 'проект', 'проекта', 'проектов') ?> от <?= pn_rub($min) ?> в тёплом контуре. Строим своими бригадами, смета — до начала работ,
    взнос 30 %, остаток — равными платежами без процентов до 5 лет. Гарантия 5 лет на фундамент, конструктив и крышу. Планировку и фасад настроим под вашу семью.</p>
</div>
  <ul class="sx-chips"><li><b><?= count($hs) ?></b> <?= pn_ru_plural(count($hs), "проект", "проекта", "проектов") ?></li><?php if ($warm): ?><li>от <b><?= pn_rub($warm) ?>/м²</b> тёплый контур</li><?php endif; ?><li>Рассрочка <b>0 %</b> до 5 лет</li><li>Строят наши бригады</li></ul>
</div></section>

<div class="ct-pills dm-f" role="group" aria-label="Фильтр проектов">
  <button type="button" data-line="" aria-pressed="true">Все <span><?= count($hs) ?></span></button>
  <?php foreach ($lines as $l): ?><button type="button" data-line="<?= pn_e($l) ?>" aria-pressed="false"><?= pn_e($l) ?> <span><?= count(array_filter($hs, fn($h) => $h['line'] === $l)) ?></span></button><?php endforeach; ?>
  <span class="ct-sep" aria-hidden="true"></span>
  <?php foreach ($fls as $f): ?><button type="button" data-fl="<?= $f ?>" aria-pressed="false"><?= $f ?> <?= pn_ru_plural($f, 'этаж', 'этажа', 'этажей') ?></button><?php endforeach; ?>
</div>

<div class="dm-grid">
<?php foreach ($hs as $h) echo pn_render('dm_card', ['h' => $h, 'warm' => $warm]); ?>
</div>
<div class="ct-empty" data-dm-empty hidden><p>Таких проектов пока нет — построим по индивидуальному.</p></div>

<section class="sv-sec"><h2 class="sv-h">Как строим</h2>
  <ol class="sv-steps">
    <li><b>Выбор проекта</b>Подбираем проект и участок, адаптируем планировку и фасад под семью.</li>
    <li><b>Смета и договор</b>Считаем смету до начала работ — цена фиксируется в договоре.</li>
    <li><b>Стройка по этапам</b>Фундамент, коробка, кровля, окна — акт на каждый этап.</li>
    <li><b>Тёплый контур</b>Дом закрыт и утеплён: можно заходить с отделкой — своей или нашей.</li>
    <li><b>Гарантия 5 лет</b>На фундамент, конструктив дома и крышу — по договору.</li>
  </ol>
</section>

<section class="sv-band">
  <div><h2>Рассрочка 0 % до 5 лет</h2><p>Без банка и процентов: первый взнос 30 % сразу, остаток — равными платежами. Тёплый контур от <?= pn_rub($warm) ?>/м²; точную цену назовём в смете — она зависит от участка, фундамента и материала стен.</p></div>
  <a class="pg-btn red" href="./#houses" data-lead="quiz" data-title="Дом в рассрочку" data-want="Дом в рассрочку 0 %: подобрать проект и посчитать платёж" data-ref="doma/">Рассчитать рассрочку</a>
</section>
<script src="assets/js/catalog.js" defer></script>
