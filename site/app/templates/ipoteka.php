<?php /** Ипотека. Переменные: $progs [['name', 'rate']], $apts (Repo::apartments), $settings */
$price0 = 7000000;
$rate0 = $progs[0]['rate'] ?? 6;
$banks = ['Сбер', 'ВТБ', 'Альфа-Банк', 'ДОМ.РФ', 'Россельхозбанк', 'УБРиР']; ?>
<section class="sx-hero" style="--sxp:50% 45%"><img class="sx-bg" src="assets/img/ekb_city.jpg" srcset="assets/img/ekb_city-1280.jpg 1280w, assets/img/ekb_city-1920.jpg 1920w, assets/img/ekb_city.jpg 2880w" sizes="100vw" alt="" fetchpriority="high" decoding="async"><div class="sx-in">
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <span>Ипотека</span></nav>
<div class="ct-head">
  <h1>Ипотека на квартиру в Екатеринбурге<i class="ct-dot" aria-hidden="true"></i></h1>
  <p class="ct-intro">Посчитайте платёж и выберите программу. Мы подаём заявку сразу в несколько банков и показываем, где платёж ниже, — бесплатно для покупателя.</p>
</div>
  <ul class="sx-chips"><?php if ($progs): ?><li>от <b><?= str_replace(".", ",", (string) min(array_column($progs, "rate"))) ?> %</b></li><?php endif; ?><li>Заявка сразу в несколько банков</li><li>Бесплатно для покупателя</li></ul>
</div></section>

<?php if ($progs): ?>
<?php $mcfg = pn_mort_cfg(Repo::settingsAll()); $sel = 0; $rdate = pn_rates_date_ru(Repo::settingsAll()); ?>
<section class="ob-calc" data-mort data-price="<?= $price0 ?>" data-mcfg="<?= pn_e(json_encode($mcfg, JSON_UNESCAPED_UNICODE)) ?>" aria-label="Ипотечный калькулятор">
  <div class="ob-calc-in">
    <div class="ob-calc-f">
      <label class="ob-rng sv-price">Стоимость квартиры <input type="text" inputmode="numeric" value="<?= number_format($price0, 0, ',', ' ') ?>" data-i="price" aria-label="Стоимость квартиры, ₽"></label>
      <div class="ob-chips" role="radiogroup" aria-label="Программа"><?php foreach ($mcfg['progs'] as $k => $p): ?>
            <button type="button" role="radio" aria-checked="<?= $k === $sel ? 'true' : 'false' ?>" data-pi="<?= $k ?>"><?= pn_e($p['name']) ?> <span><?= str_replace('.', ',', (string) $p['rate']) ?> %</span></button><?php endforeach; ?></div>
          <?php if ($mcfg['tiers']): ?><div class="ob-kids" data-kids role="group" aria-label="Детей в семье"<?= empty($mcfg['progs'][$sel]['family']) ? ' hidden' : '' ?>><span>Детей</span><?php foreach ([1, 2, 3, 4, 5] as $k): ?>
            <button type="button" data-k="<?= $k ?>" aria-pressed="<?= $k === 1 ? 'true' : 'false' ?>"><?= $k === 5 ? '5+' : $k ?></button><?php endforeach; ?></div><?php endif; ?>
      <label class="ob-rng">Первоначальный взнос <output data-o="down"><?= pn_rub((int) ($price0 * .2)) ?> · 20 %</output><input type="range" min="10" max="90" step="5" value="20" data-i="down" aria-label="Первоначальный взнос, %"></label>
      <label class="ob-rng">Срок <output data-o="term">30 лет</output><input type="range" min="5" max="30" step="1" value="30" data-i="term" aria-label="Срок ипотеки, лет"></label>
    </div>
    <div class="ob-calc-r" aria-live="polite">
      <span>Ежемесячный платёж</span><b data-o="pay"><?= pn_rub(pn_mort_pay($price0, $mcfg['progs'][0] ?? ['name' => '', 'rate' => $rate0], Repo::settingsAll())['pay']) ?></b>
      <dl><div><dt>Сумма кредита</dt><dd data-o="loan"><?= pn_rub((int) ($price0 * .8)) ?></dd></div><div><dt>Переплата</dt><dd data-o="over">—</dd></div><div><dt>Рекомендуемый доход</dt><dd data-o="inc">—</dd></div></dl>
      <a class="pg-btn red" href="./#lead">Подобрать программу</a>
      <small data-o="parts"></small>
      <small><?= $rdate ? 'Ставки на ' . $rdate . '. ' : '' ?>Расчёт предварительный. Точную ставку банк назовёт после заявки.</small>
    </div>
  </div>
</section>

<section class="sv-sec"><h2 class="sv-h">Программы</h2>
  <div class="sv-progs"><?php foreach ($progs as $p): ?>
    <div><span class="sv-rate"><?= str_replace('.', ',', (string) $p['rate']) ?> %</span><h3><?= pn_e($p['name']) ?></h3><p><?= pn_e(pn_mort_note((string) $p['name'])) ?></p>
      <?php if (mb_stripos((string) $p['name'], 'семейн') !== false): ?><a href="kvartiry/semeynaya-ipoteka/">Квартиры под программу →</a><?php endif; ?></div>
  <?php endforeach; ?></div>
  <p class="ob-note"><?= $rdate ? 'Ставки на ' . $rdate . ', ' : '' ?>ориентировочно. Лимит — сумма кредита по льготной ставке; сверх него банк выдаёт по рыночной. Условия программ меняются — проверим актуальные на день заявки.</p>
</section>
<?php endif; ?>

<section class="sv-sec"><h2 class="sv-h">Банки-партнёры</h2>
  <div class="ct-linkl sv-banks"><?php foreach ($banks as $b): ?><span><?= $b ?></span><?php endforeach; ?></div>
</section>

<section class="sv-sec"><h2 class="sv-h">Как получить ипотеку с нами</h2>
  <ol class="sv-steps">
    <li><b>Заявка</b>Оставляете телефон — уточним доход, взнос и состав семьи.</li>
    <li><b>Несколько банков</b>Подаём одну анкету сразу в несколько банков.</li>
    <li><b>Одобрение</b>Сравниваем предложения и выбираем, где платёж ниже.</li>
    <li><b>Квартира</b>Подбираем проверенную квартиру под одобренную сумму.</li>
    <li><b>Сделка</b>Сопровождаем до ключей, комиссия для покупателя — 0 ₽.</li>
  </ol>
</section>

<section class="sv-band">
  <div><h2>Подберите квартиру под платёж</h2><p>В каталоге у каждой квартиры указан платёж в ипотеку — <?= count($apts) ?> проверенных предложений.</p></div>
  <a class="pg-btn red" href="kvartiry/">Открыть каталог</a>
</section>
<script src="assets/js/page.js" defer></script>
