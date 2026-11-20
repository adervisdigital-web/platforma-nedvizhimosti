<?php /** Страница проекта дома. Переменные: $h (Repo::house, форма прототипа + price_from/area), $others (другие проекты), $settings */
$warm = (int) ($settings['warm_contour_from'] ?? 0);
$name = $h['line'] . ' ' . $h['n'];
$area = (float) ($h['area'] ?: $h['n']);
$price = $h['price_from'] ?: ($warm ? (int) round($warm * $area) : 0);
$photos = array_map(fn($ph, $k) => [pn_img_attrs('houses/' . $ph, '(max-width: 1000px) 100vw, 62vw'), "Дом «{$name}»" . ($k ? ', фото ' . ($k + 1) : '')], $h['ph'], array_keys($h['ph']));
$plans = array_map(fn($pl) => [pn_img_attrs('houses/' . $pl[1], '(max-width: 1000px) 100vw, 62vw'), $pl[0]], $h['plans']);
$tel = $settings['phone_tel'] ?? '';
$facts = array_filter([['Площадь', pn_area($area)], ['Этажей', (string) $h['fl']], ['Комнаты', $h['rooms']], ['Потолки', $h['ceil']],
    ['Тёплый контур', $warm ? 'от ' . pn_rub($warm) . '/м²' : null]], fn($f) => $f[1] !== null && $f[1] !== ''); ?>
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <a href="doma/">Дома</a> · <span><?= pn_e($name) ?></span></nav>
<div class="ob">
  <div class="ob-main">
    <?= pn_render('obj_gallery', ['photos' => $photos, 'plans' => $plans, 'planTab' => 'Планировки']) ?>

    <section class="ob-facts" aria-label="Коротко о проекте">
      <?php foreach ($facts as [$k, $v]): ?><div><span><?= $k ?></span><b><?= pn_e($v) ?></b></div><?php endforeach; ?>
    </section>

    <section class="ob-sec" id="about"><h2>О проекте</h2>
      <?php if ($h['idea']): ?><blockquote class="ob-idea" style="--c:<?= pn_e($h['c']) ?>"><?= pn_e($h['idea']) ?></blockquote><?php endif; ?>
      <div class="ob-txt"><?php foreach ($h['text'] as $p): ?><p><?= pn_e($p) ?></p><?php endforeach; ?></div>
    </section>

    <?php if ($h['feats']): ?>
    <section class="ob-sec" id="feats"><h2>Особенности</h2>
      <ul class="ob-checks"><?php foreach ($h['feats'] as $f): ?><li><i aria-hidden="true"></i><?= pn_e($f) ?></li><?php endforeach; ?></ul>
    </section>
    <?php endif; ?>

    <?php if ($plans): ?>
    <section class="ob-sec" id="plan"><h2>Планировки</h2>
      <div class="ob-plangrid"><?php foreach ($plans as $k => [$attrs, $cap]): ?>
        <figure><button type="button" class="ob-planbig" data-plan="<?= $k ?>" aria-label="Открыть «<?= pn_e($cap) ?>» крупно"><img <?= $attrs ?> alt="Планировка: <?= pn_e($cap) ?>" loading="lazy"><span>Открыть крупно</span></button><figcaption><?= pn_e($cap) ?></figcaption></figure>
      <?php endforeach; ?></div>
    </section>
    <?php endif; ?>

    <?php if ($price): ?>
    <section class="ob-sec ob-calc" id="inst" data-inst data-price="<?= $price ?>"><h2>Рассрочка 0 %</h2>
      <div class="ob-calc-in">
        <div class="ob-calc-f">
          <p class="ob-lead">Строим своими бригадами по этапам. Без банка и процентов: взнос 30 % сразу, остаток — равными платежами до 5 лет.</p>
          <label class="ob-rng">Первый взнос <output data-o="down"><?= pn_rub((int) round($price * .3)) ?> · 30 %</output><input type="range" min="30" max="90" step="5" value="30" data-i="down" aria-label="Первый взнос, %"></label>
          <label class="ob-rng">Срок <output data-o="term">3 года</output><input type="range" min="1" max="5" step="1" value="3" data-i="term" aria-label="Срок рассрочки, лет"></label>
        </div>
        <div class="ob-calc-r" aria-live="polite">
          <span>Платёж в месяц</span><b data-o="pay"><?= pn_rub((int) round($price * .7 / 36)) ?></b>
          <dl><div><dt>Дом в тёплом контуре</dt><dd>от <?= pn_rub($price) ?></dd></div><div><dt>Остаток в рассрочку</dt><dd data-o="rest"><?= pn_rub((int) round($price * .7)) ?></dd></div><div><dt>Переплата</dt><dd>0 ₽</dd></div></dl>
          <a class="pg-btn red" href="./#house-<?= pn_e($h['id']) ?>" data-lead="quiz" data-title="Смета на дом" data-want="Смета: <?= pn_e($name) ?>" data-ref="doma/<?= pn_e($h['slug']) ?>/" data-calc>Получить смету</a>
          <small>Тёплый контур от <?= pn_rub($warm) ?>/м². Итог зависит от участка, фундамента и комплектации — назовём в смете.</small>
        </div>
      </div>
    </section>
    <?php endif; ?>
  </div>

  <aside class="ob-side">
    <div class="ob-card">
      <p class="pg-tag"><i class="ob-dot" style="--c:<?= pn_e($h['c']) ?>"></i>Линейка «<?= pn_e($h['line']) ?>»</p>
      <h1><?= pn_e($name) ?></h1>
      <p class="pg-where"><?= pn_e($h['motto']) ?></p>
      <?php if ($price): ?><p class="pg-price">от <?= pn_rub($price) ?></p><p class="pg-sub">тёплый контур · <?= pn_area($area) ?></p>
      <a class="ob-mortlink" href="#inst"><span>Рассрочка 0 % до 5 лет</span><b>от <?= pn_rub((int) round($price * .7 / 60)) ?>/мес</b><i aria-hidden="true">→</i></a><?php endif; ?>
      <div class="ob-ok"><i aria-hidden="true"></i><span><b>Строим своими бригадами</b><br>Смета до начала работ. Гарантия 5 лет на фундамент, конструктив и крышу</span></div>
      <div class="pg-act">
        <a class="pg-btn red" href="./#house-<?= pn_e($h['id']) ?>" data-lead="quiz" data-title="Обсудим проект" data-want="Проект дома: <?= pn_e($name) ?>" data-ref="doma/<?= pn_e($h['slug']) ?>/">Обсудить проект</a>
        <a class="pg-btn" href="tel:<?= pn_e($tel) ?>">Позвонить</a>
        <button type="button" class="pg-btn ghost" data-share aria-label="Поделиться ссылкой"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4"/></svg>Поделиться</button>
      </div>
      <p class="ob-mgr">На связи <?= pn_e($settings['hours_from'] ?? '9:00') ?>–<?= pn_e($settings['hours_to'] ?? '21:00') ?> · <a href="tel:<?= pn_e($tel) ?>"><?= pn_e($settings['phone'] ?? '') ?></a></p>
    </div>
  </aside>
</div>

<?php if ($others): ?>
<section class="ob-sim"><h2>Другие проекты</h2>
  <div class="dm-grid dm-oth"><?php foreach (array_slice($others, 0, 4) as $o) echo pn_render('dm_card', ['h' => $o, 'warm' => $warm]); ?></div>
</section>
<?php endif; ?>

<?php if ($price): ?><div class="ob-bar"><div><b>от <?= pn_rub($price) ?></b><span>рассрочка 0 %</span></div><a class="pg-btn red" href="./#house-<?= pn_e($h['id']) ?>" data-lead="quiz" data-title="Обсудим проект" data-want="Проект дома: <?= pn_e($name) ?>" data-ref="doma/<?= pn_e($h['slug']) ?>/">Обсудить</a></div><?php endif; ?>
<script src="assets/js/page.js" defer></script>
