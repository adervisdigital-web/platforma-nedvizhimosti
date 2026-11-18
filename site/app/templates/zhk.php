<?php /** Страница ЖК. Переменные: $z (pn_complexes_full), $apts, $st, $crumbs, $others [путь => [имя, кол-во]], $cx, $s, $settings */
$photos = array_map(fn($ph, $k) => [pn_img_attrs($ph, '(max-width: 1000px) 100vw, 62vw'), $z['name'] . ($k ? ', фото ' . ($k + 1) : '')],
    $z['photos'] ?: [$apts[0]['photos'][0] ?? 'zhk'], array_keys($z['photos'] ?: [0]));
$tel = $settings['phone_tel'] ?? '';
$rooms = array_count_values(array_map(fn($a) => $a['rooms'] >= 4 ? 4 : $a['rooms'], $apts)); ksort($rooms);
$statuses = array_values(array_unique(array_map(fn($a) => explode(' · ', (string) $a['house_status'])[0], $apts))); ?>
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <a href="kvartiry/">Квартиры</a> · <span><?= pn_e($z['name']) ?></span></nav>
<div class="ob">
  <div class="ob-main">
    <?= pn_render('obj_gallery', ['photos' => $photos, 'plans' => []]) ?>

    <section class="ob-facts" aria-label="Коротко о ЖК">
      <div><span>Квартир в продаже</span><b><?= $st['n'] ?></b></div>
      <div><span>Цены</span><b>от <?= pn_e(pn_mln($st['pmin'])) ?></b></div>
      <div><span>Площади</span><b><?= str_replace('.', ',', (string) pn_num($st['amin'])) ?>–<?= str_replace('.', ',', (string) pn_num($st['amax'])) ?> м²</b></div>
      <div><span>Дом</span><b><?= pn_e(implode(', ', $statuses)) ?></b></div>
    </section>

    <?php if ($z['description']): ?>
    <section class="ob-sec" id="about"><h2>О комплексе</h2>
      <div class="ob-txt"><?php foreach (preg_split('~\R{2,}~', trim($z['description'])) as $p): ?><p><?= nl2br(pn_e($p)) ?></p><?php endforeach; ?></div>
    </section>
    <?php endif; ?>

    <?php if ($z['checks']): ?>
    <section class="ob-sec" id="checks"><h2>Что мы проверили</h2>
      <ul class="ob-checks"><?php foreach ($z['checks'] as $c): ?><li><i aria-hidden="true"></i><?= pn_e($c) ?></li><?php endforeach; ?></ul>
      <p class="ob-note">Проверяем застройщика и документы до того, как показать квартиры на сайте.</p>
    </section>
    <?php endif; ?>

    <section class="ob-sec" id="flats"><h2>Квартиры в продаже</h2>
      <div class="ct-bar ct-bar-z">
        <p class="ct-count">Найдено: <b data-ct-count><?= $st['n'] ?></b></p>
        <div class="ct-bar-r"><label class="ct-sort"><span class="ct-vh">Сортировка</span><select name="sort" data-ct-sort>
          <option value="">По умолчанию</option><option value="p">Сначала дешевле</option><option value="-p">Сначала дороже</option><option value="ppm">Дешевле за м²</option><option value="-a">Больше площадь</option></select></label></div>
      </div>
      <div class="ct-grid ct-grid-z" data-ct-list><?php foreach ($apts as $i => $a) echo pn_render('ct_card', ['a' => $a, 'i' => $i, 'cx' => $cx, 's' => $s]); ?></div>
      <div class="ct-more" data-ct-more-wrap hidden><button type="button" class="pg-btn" data-ct-more>Показать ещё</button></div>
    </section>

    <?php if ($z['lat'] && $z['lng']): ?>
    <section class="ob-sec" id="map"><h2>На карте</h2>
      <div class="ob-map" data-map data-lat="<?= $z['lat'] ?>" data-lng="<?= $z['lng'] ?>" data-title="<?= pn_e($z['name']) ?>" role="img" aria-label="Карта: <?= pn_e($z['name']) ?>"></div>
      <?php if ($z['address']): ?><p class="ob-note"><?= pn_e($z['address']) ?></p><?php endif; ?>
    </section>
    <?php endif; ?>
  </div>

  <aside class="ob-side">
    <div class="ob-card">
      <p class="pg-tag">Жилой комплекс · <?= pn_e($z['district']) ?></p>
      <h1><?= pn_e($z['name']) ?></h1>
      <p class="pg-where"><?= pn_e($z['address'] ?: $z['district']) ?><?= $z['developer'] ? ' · застройщик ' . pn_e($z['developer']) : '' ?></p>
      <p class="pg-price">от <?= pn_rub($st['pmin']) ?></p>
      <p class="pg-sub"><?= $st['n'] ?> <?= pn_ru_plural($st['n'], 'квартира', 'квартиры', 'квартир') ?> в продаже</p>
      <div class="ct-rooms"><?php foreach ($rooms as $r => $n): ?><span><?= $r === 0 ? 'Студии' : ($r === 4 ? '4+ комн.' : "$r-комн.") ?> <b><?= $n ?></b></span><?php endforeach; ?></div>
      <div class="ob-ok"><i aria-hidden="true"></i><span><b>Застройщик проверен Платформой</b><br>0 ₽ комиссии для покупателя</span></div>
      <div class="pg-act">
        <a class="pg-btn red" href="#flats">Смотреть квартиры</a>
        <a class="pg-btn" href="tel:<?= pn_e($tel) ?>">Позвонить</a>
        <button type="button" class="pg-btn ghost" data-share aria-label="Поделиться ссылкой"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4"/></svg>Поделиться</button>
      </div>
      <p class="ob-mgr">На связи <?= pn_e($settings['hours_from'] ?? '9:00') ?>–<?= pn_e($settings['hours_to'] ?? '21:00') ?> · <a href="tel:<?= pn_e($tel) ?>"><?= pn_e($settings['phone'] ?? '') ?></a></p>
    </div>
  </aside>
</div>

<?php if ($others): ?>
<section class="ct-links"><div><h2>Другие жилые комплексы</h2><nav class="ct-linkl"><?php foreach ($others as $p => [$t, $n]): ?><a href="<?= pn_e($p) ?>"><?= pn_e($t) ?> <span><?= $n ?></span></a><?php endforeach; ?></nav></div>
  <div><h2>Каталог</h2><nav class="ct-linkl"><a href="kvartiry/">Все квартиры</a><a href="kvartiry/novostroyki/">Новостройки</a><a href="kvartiry/rayon/<?= pn_e(pn_slug($z['district'])) ?>/">Квартиры в районе <?= pn_e($z['district']) ?></a></nav></div></section>
<?php endif; ?>
<div class="ob-bar"><div><b>от <?= pn_rub($st['pmin']) ?></b><span><?= $st['n'] ?> <?= pn_ru_plural($st['n'], 'квартира', 'квартиры', 'квартир') ?></span></div><a class="pg-btn red" href="#flats">Квартиры</a></div>
<script src="assets/js/page.js" defer></script>
<script src="assets/js/catalog.js" defer></script>
