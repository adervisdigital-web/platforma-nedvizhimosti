<?php /** Страница квартиры. Переменные: $a (Repo::apartment), $idx (номер в списке главной — для #obj-N), $pay, $rate, $progs, $ren, $similar, $settings */
$where = $a['complex'] ?? $a['address'];
$per_m = (int) round($a['price'] / max(1, $a['area']));
$title = pn_rooms($a['rooms']) . ', ' . pn_area($a['area']);
$num = fn($v, $u = ' м²') => $v === null || $v === '' ? null : str_replace('.', ',', (string) pn_num($v)) . $u;
$photos = array_map(fn($ph, $k) => [pn_img_attrs($ph, '(max-width: 1000px) 100vw, 62vw'), pn_apt_title($a) . ($k ? ', фото ' . ($k + 1) : '')], $a['photos'], array_keys($a['photos']));
$plans = array_map(fn($pl) => [pn_img_attrs($pl, '(max-width: 1000px) 100vw, 62vw'), 'Планировка · ' . pn_area($a['area'])], $a['plans']);
$tel = $settings['phone_tel'] ?? ''; $phone = $settings['phone'] ?? '';
$progs = array_values(array_filter($progs, fn($p) => isset($p['name'], $p['rate'])));
$facts = array_filter([
    ['Общая', pn_area($a['area'])],
    ['Жилая', $num($a['living_area'])],
    ['Кухня', $num($a['kitchen_area']) ?? ($a['rooms'] === 0 ? 'в комнате' : null)],
    ['Этаж', $a['floor'] . ' из ' . $a['floors']],
    ['Потолки', $num($a['ceiling'], ' м')],
], fn($f) => $f[1] !== null);
$aptRows = array_filter([
    ['Тип', $a['market'] === 'new' ? 'Новостройка' : 'Вторичное жильё'], ['Комнат', $a['rooms'] ? (string) $a['rooms'] : 'студия'],
    ['Общая площадь', pn_area($a['area'])], ['Жилая площадь', $num($a['living_area'])], ['Кухня', $num($a['kitchen_area'])],
    ['Этаж', $a['floor'] . ' из ' . $a['floors']], ['Потолки', $num($a['ceiling'], ' м')], ['Санузел', $a['bathroom']], ['Балкон', $a['balcony']],
    ['Окна', $a['view']], ['Отделка', $a['finish_label'] ?: ($a['finish'] === 'without' ? 'Без отделки' : 'С отделкой')],
], fn($r) => $r[1] !== null && $r[1] !== '');
$houseRows = array_filter([
    ['ЖК', $a['complex']], ['Адрес', $a['address']], ['Район', $a['district']], ['Застройщик', $a['developer']], ['Дом', $a['house_status']],
], fn($r) => $r[1] !== null && $r[1] !== '');
$checks = $a['complex_checks'] ?: ($a['market'] === 'secondary'
    ? ['Право собственности и история перехода прав', 'Нет обременений, арестов и долгов', 'Нет зарегистрированных жильцов, в том числе детей', 'Согласие супруга и нет споров в судах']
    : []); ?>
<?php $zp = $a['complex_slug'] ? pn_zhk_path($a['complex_slug']) : null; ?>
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <a href="kvartiry/">Квартиры</a> · <?= $zp ? '<a href="' . pn_e($zp) . '">' . pn_e($where) . '</a> · ' : '' ?><span><?= pn_e(pn_rooms($a['rooms'])) ?>, <?= pn_area($a['area']) ?></span></nav>
<div class="ob">
  <div class="ob-main">
    <?= pn_render('obj_gallery', ['photos' => $photos, 'plans' => $plans]) ?>

    <section class="ob-facts" aria-label="Коротко о квартире">
      <?php foreach ($facts as [$k, $v]): ?><div><span><?= $k ?></span><b><?= pn_e($v) ?></b></div><?php endforeach; ?>
    </section>

    <?php if (!empty($a['description'])): ?>
    <section class="ob-sec" id="about"><h2>О квартире</h2>
      <div class="ob-txt"><?php foreach (preg_split('~\R{2,}~', trim($a['description'])) as $p): ?><p><?= nl2br(pn_e($p)) ?></p><?php endforeach; ?></div>
    </section>
    <?php endif; ?>

    <?php if ($plans): ?>
    <section class="ob-sec" id="plan"><h2>Планировка</h2>
      <div class="ob-planrow">
        <button type="button" class="ob-planbig" data-plan="0" aria-label="Открыть планировку крупно"><img <?= $plans[0][0] ?> alt="Планировка квартиры" loading="lazy"><span>Открыть крупно</span></button>
        <dl class="ob-pl-dl"><?php foreach (array_filter([['Общая', pn_area($a['area'])], ['Жилая', $num($a['living_area'])], ['Кухня', $num($a['kitchen_area'])], ['Санузел', $a['bathroom']], ['Балкон', $a['balcony']], ['Окна', $a['view']]], fn($r) => $r[1]) as [$k, $v]): ?>
          <div><dt><?= $k ?></dt><dd><?= pn_e($v) ?></dd></div><?php endforeach; ?></dl>
      </div>
    </section>
    <?php endif; ?>

    <section class="ob-sec" id="params"><h2>Характеристики</h2>
      <div class="ob-cols">
        <div><h3>Квартира</h3><dl class="ob-dl"><?php foreach ($aptRows as [$k, $v]): ?><div><dt><?= $k ?></dt><dd><?= pn_e($v) ?></dd></div><?php endforeach; ?></dl></div>
        <div><h3>Дом</h3><dl class="ob-dl"><?php foreach ($houseRows as [$k, $v]): ?><div><dt><?= $k ?></dt><dd><?= $k === 'ЖК' && $zp ? '<a href="' . pn_e($zp) . '">' . pn_e($v) . '</a>' : pn_e($v) ?></dd></div><?php endforeach; ?></dl>
          <?php if ($zp): ?><a class="ob-more" href="<?= pn_e($zp) ?>">Все квартиры в <?= pn_e($a['complex']) ?> →</a><?php endif; ?>
          <a class="ob-more" href="kvartiry/rayon/<?= pn_e(pn_slug((string) $a['district'])) ?>/">Квартиры в районе <?= pn_e($a['district']) ?> →</a></div>
      </div>
    </section>

    <?php if ($checks): ?>
    <section class="ob-sec" id="checks"><h2>Что мы проверили</h2>
      <ul class="ob-checks"><?php foreach ($checks as $c): ?><li><i aria-hidden="true"></i><?= pn_e($c) ?></li><?php endforeach; ?></ul>
      <p class="ob-note">Проверяем до того, как показать объект на сайте. Документы покажем на просмотре.</p>
    </section>
    <?php endif; ?>

    <?php if ($progs): ?>
    <section class="ob-sec ob-calc" id="mort" data-mort data-price="<?= $a['price'] ?>" data-progs="<?= pn_e(json_encode($progs, JSON_UNESCAPED_UNICODE)) ?>"><h2>Ипотека</h2>
      <div class="ob-calc-in">
        <div class="ob-calc-f">
          <div class="ob-chips" role="radiogroup" aria-label="Программа"><?php foreach ($progs as $k => $p): ?>
            <button type="button" role="radio" aria-checked="<?= (float) $p['rate'] === (float) $rate ? 'true' : 'false' ?>" data-rate="<?= pn_e((string) $p['rate']) ?>"><?= pn_e($p['name']) ?> <span><?= str_replace('.', ',', (string) $p['rate']) ?> %</span></button><?php endforeach; ?></div>
          <label class="ob-rng">Первоначальный взнос <output data-o="down"><?= pn_rub((int) round($a['price'] * .2)) ?> · 20 %</output>
            <input type="range" min="10" max="90" step="5" value="20" data-i="down"></label>
          <label class="ob-rng">Срок <output data-o="term">30 лет</output><input type="range" min="5" max="30" step="1" value="30" data-i="term"></label>
        </div>
        <div class="ob-calc-r" aria-live="polite">
          <span>Ежемесячный платёж</span><b data-o="pay"><?= pn_rub($pay) ?></b>
          <dl><div><dt>Сумма кредита</dt><dd data-o="loan"><?= pn_rub((int) round($a['price'] * .8)) ?></dd></div>
            <div><dt>Переплата</dt><dd data-o="over">—</dd></div><div><dt>Рекомендуемый доход</dt><dd data-o="inc"><?= pn_rub($pay * 2) ?></dd></div></dl>
          <a class="pg-btn red" href="./#calc">Подобрать программу</a>
          <small>Расчёт предварительный. Точную ставку банк назовёт после заявки — поможем подать сразу в несколько банков.</small>
        </div>
      </div>
    </section>
    <?php endif; ?>

    <?php if ($a['finish'] === 'without' && count($ren) >= 3): ?>
    <section class="ob-sec" id="ren"><h2>Ремонт под ключ</h2>
      <p class="ob-lead">Квартира без отделки. Сделаем ремонт своей бригадой по смете — цена фиксируется в договоре, гарантия 5 лет.</p>
      <div class="ob-ren"><?php foreach (['Базовый', 'Комфорт', 'Премиум'] as $k => $n): $sum = (int) round($ren[$k] * $a['area']); ?>
        <div class="<?= $k === 1 ? 'hit' : '' ?>"><span><?= $n ?></span><b><?= pn_rub($sum) ?></b><small><?= pn_rub((int) $ren[$k]) ?>/м² · вместе с квартирой <?= pn_rub($a['price'] + $sum) ?></small></div>
      <?php endforeach; ?></div>
    </section>
    <?php endif; ?>

    <?php if ($a['lat'] && $a['lng']): ?>
    <section class="ob-sec" id="map"><h2>На карте</h2>
      <div class="ob-map" data-map data-lat="<?= $a['lat'] ?>" data-lng="<?= $a['lng'] ?>" data-title="<?= pn_e($where) ?>" role="img" aria-label="Карта: <?= pn_e($where) ?>, <?= pn_e($a['district']) ?>"></div>
      <p class="ob-note"><?= pn_e($where) ?> · <?= pn_e($a['district']) ?>. Точный адрес — при записи на просмотр.</p>
    </section>
    <?php endif; ?>
  </div>

  <aside class="ob-side">
    <div class="ob-card">
      <p class="pg-tag"><?= $a['market'] === 'new' ? 'Новостройка' : 'Вторичка' ?><?= $a['special'] ? ' · <em>спецпредложение</em>' : '' ?></p>
      <h1><?= pn_e($title) ?></h1>
      <p class="pg-where"><?= pn_e($where) ?> · <?= pn_e($a['district']) ?> · <?= $a['floor'] ?>/<?= $a['floors'] ?> этаж</p>
      <p class="pg-price"><?= pn_rub($a['price']) ?><?php if ($a['discount_pct']): ?> <span>−<?= $a['discount_pct'] ?> %</span><?php endif; ?></p>
      <p class="pg-sub"><?= pn_rub($per_m) ?>/м²</p>
      <a class="ob-mortlink" href="#mort"><span>В ипотеку от</span><b><?= pn_rub($pay) ?>/мес</b><i aria-hidden="true">→</i></a>
      <div class="ob-ok"><i aria-hidden="true"></i><span><b>Проверено Платформой</b><br>0 ₽ комиссии для покупателя</span></div>
      <div class="pg-act">
        <a class="pg-btn red" href="./#obj-<?= $idx ?>">Записаться на просмотр</a>
        <a class="pg-btn" href="tel:<?= pn_e($tel) ?>">Позвонить</a>
        <button type="button" class="pg-btn ghost" data-share aria-label="Поделиться ссылкой"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4"/></svg>Поделиться</button>
      </div>
      <p class="ob-mgr">На связи <?= pn_e($settings['hours_from'] ?? '9:00') ?>–<?= pn_e($settings['hours_to'] ?? '21:00') ?> · <a href="tel:<?= pn_e($tel) ?>"><?= pn_e($phone) ?></a></p>
    </div>
  </aside>
</div>

<?php if ($similar): ?>
<section class="ob-sim"><h2>Похожие квартиры</h2>
  <div class="ob-simg"><?php foreach ($similar as $s): ?>
    <a class="ob-simc" href="kvartiry/<?= pn_e($s['slug']) ?>/"><img <?= pn_img_attrs($s['photos'][0] ?? 'kv_empty', '(max-width: 900px) 100vw, 33vw') ?> alt="" loading="lazy">
      <span class="ob-simt"><?= pn_e(pn_rooms($s['rooms'])) ?>, <?= pn_area($s['area']) ?></span><span class="ob-simw"><?= pn_e($s['complex'] ?? $s['address']) ?> · <?= pn_e($s['district']) ?></span><b><?= pn_rub($s['price']) ?></b></a>
  <?php endforeach; ?></div>
</section>
<?php endif; ?>

<div class="ob-bar"><div><b><?= pn_rub($a['price']) ?></b><span>от <?= pn_rub($pay) ?>/мес</span></div><a class="pg-btn red" href="./#obj-<?= $idx ?>">Записаться</a></div>
<script src="assets/js/page.js" defer></script>
