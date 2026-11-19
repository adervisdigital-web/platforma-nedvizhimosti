<?php /** Ремонт под ключ. Переменные: $r (цены ₽/м²: базовый, комфорт, премиум), $settings */
$lv = [
    ['Базовый', 'Чистовая отделка без лишнего: заехать и жить или сдавать.', ['Выравнивание стен и пола', 'Ламинат, обои под покраску', 'Межкомнатные двери', 'Санузел под ключ: плитка, сантехника', 'Электрика и розетки по проекту']],
    ['Комфорт', 'Самый частый выбор: качественные материалы и продуманные детали.', ['Всё из базового', 'Инженерная доска или кварцвинил', 'Плитка на кухне и в санузле', 'Скрытые инсталляции, тёплый пол', 'Ровные потолки и встроенный свет']],
    ['Премиум', 'Дизайн-проект и материалы премиум-класса.', ['Дизайн-проект и визуализации', 'Премиальные материалы и сантехника', 'Сложные потолки и сценарии света', 'Столярка и встроенная мебель', 'Авторский надзор']],
]; ?>
<section class="sx-hero" style="--sxp:50% 60%"><img class="sx-bg" src="assets/img/ba_after.jpg" alt="" fetchpriority="high" decoding="async"><div class="sx-in">
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <span>Ремонт</span></nav>
<div class="ct-head">
  <h1>Ремонт квартир под ключ<i class="ct-dot" aria-hidden="true"></i></h1>
  <p class="ct-intro">Делаем ремонт своей бригадой — в новостройке и на вторичке, в том числе сразу после покупки квартиры у нас. Смета до начала работ,
    цена фиксируется в договоре, акт на каждый этап, гарантия 5 лет.</p>
</div>
  <ul class="sx-chips"><li>от <b><?= pn_rub((int) $r[0]) ?>/м²</b></li><li>Смета до начала работ</li><li>Акт на каждый этап</li><li>Гарантия <b>5 лет</b></li></ul>
</div></section>

<div class="sv-levels">
<?php foreach ($lv as $k => [$name, $sub, $inc]): ?>
  <section class="sv-lv<?= $k === 1 ? ' hit' : '' ?>"><?php if ($k === 1): ?><span class="sv-badge">Чаще выбирают</span><?php endif; ?>
    <h2><?= $name ?></h2><p class="sv-p">от <b><?= pn_rub((int) $r[$k]) ?>/м²</b></p><p class="sv-sub"><?= $sub ?></p>
    <ul><?php foreach ($inc as $i): ?><li><?= $i ?></li><?php endforeach; ?></ul>
  </section>
<?php endforeach; ?>
</div>
<p class="ob-note">Состав работ примерный — точный перечень и цену фиксируем в смете после замера.</p>

<section class="sv-sec ob-calc" data-ren data-prices="<?= pn_e(json_encode(array_map('intval', array_slice($r, 0, 3)))) ?>"><h2 class="sv-h">Сколько стоит ремонт вашей квартиры</h2>
  <div class="ob-calc-in">
    <div class="ob-calc-f">
      <div class="ob-chips" role="radiogroup" aria-label="Уровень ремонта"><?php foreach ($lv as $k => [$name]): ?>
        <button type="button" role="radio" aria-checked="<?= $k === 1 ? 'true' : 'false' ?>" data-lv="<?= $k ?>"><?= $name ?> <span><?= pn_rub((int) $r[$k]) ?>/м²</span></button><?php endforeach; ?></div>
      <label class="ob-rng">Площадь квартиры <output data-o="area">60 м²</output><input type="range" min="20" max="150" step="1" value="60" data-i="area"></label>
    </div>
    <div class="ob-calc-r" aria-live="polite">
      <span>Ремонт под ключ</span><b data-o="sum"><?= pn_rub((int) $r[1] * 60) ?></b>
      <dl><div><dt>Цена за м²</dt><dd data-o="ppm"><?= pn_rub((int) $r[1]) ?></dd></div><div><dt>Гарантия</dt><dd>5 лет</dd></div><div><dt>Оплата</dt><dd>по этапам</dd></div></dl>
      <a class="pg-btn red" href="./#lead">Получить смету</a>
      <small>Предварительный расчёт. Точную смету составим после замера.</small>
    </div>
  </div>
</section>

<section class="sv-sec"><h2 class="sv-h">До и после</h2>
  <div class="sv-cur" data-cur style="--p:50%">
    <img src="assets/img/ba_after.jpg" alt="Та же квартира после ремонта" loading="lazy">
    <img class="sv-cur-b" src="assets/img/ba_before.jpg" alt="Квартира до ремонта" loading="lazy">
    <span class="sv-cur-t sv-cur-tb">До</span><span class="sv-cur-t sv-cur-ta">После</span>
    <span class="sv-cur-h" aria-hidden="true"><i></i></span>
    <input type="range" min="0" max="100" value="50" aria-label="Шторка: слева — до ремонта, справа — после">
  </div>
  <p class="sv-note">Одна и та же комната: потяните шторку, чтобы сравнить.</p>
</section>

<section class="sv-sec"><h2 class="sv-h">Как работаем</h2>
  <ol class="sv-steps">
    <li><b>Замер</b>Приезжаем, обмеряем квартиру и обсуждаем задачи.</li>
    <li><b>Смета</b>Считаем работы и материалы до начала — без сюрпризов в процессе.</li>
    <li><b>Договор</b>Фиксируем цену, сроки и этапы.</li>
    <li><b>Работы по этапам</b>Принимаете каждый этап по акту и платите только за принятое.</li>
    <li><b>Гарантия 5 лет</b>Отвечаем за работы по договору.</li>
  </ol>
</section>

<section class="sv-band">
  <div><h2>Квартира и ремонт — одним пакетом</h2><p>Подберём квартиру без отделки и сразу посчитаем ремонт: увидите итоговую сумму до покупки.</p></div>
  <a class="pg-btn red" href="kvartiry/novostroyki/">Смотреть новостройки</a>
</section>
<script src="assets/js/page.js" defer></script>
