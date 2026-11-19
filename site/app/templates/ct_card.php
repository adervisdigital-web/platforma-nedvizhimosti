<?php /** Карточка квартиры в каталоге. Переменные: $a (Repo::apartments), $i (порядок), $cx (pn_complexes_full), $s (настройки) */
$z = $a['complex'] && isset($cx[$a['complex']]) ? $cx[$a['complex']] : null;
$geo = pn_apt_geo($a, $cx, $s);
$ready = $a['market'] === 'secondary' || (int) $a['due'] === 0;
$ppm = (int) round($a['price'] / max(1, $a['area']));
$pay = pn_apt_pay($a, $s);
$prog = pn_default_prog($a, $s); $rate = pn_prog_terms($prog, $s)['rate'];
$gid = pn_apt_gid($a['slug']);
$tag = $a['special'] ? 'Спецпредложение' : ($a['discount_pct'] ? 'Ниже рынка на ' . $a['discount_pct'] . ' %' : '');
$noFin = $a['finish'] !== 'with'; $ren = (int) (($s['renovation_prices'] ?? [20000])[0] ?? 20000); ?>
<article class="ct-card" data-i="<?= $i ?>" data-p="<?= $a['price'] ?>" data-a="<?= pn_num($a['area']) ?>" data-r="<?= $a['rooms'] ?>" data-m="<?= $a['market'] === 'new' ? 'new' : 'sec' ?>"
  data-d="<?= pn_e(pn_slug((string) $a['district'])) ?>" data-z="<?= pn_e($z ? $z['slug'] : '') ?>" data-f="<?= $a['finish'] === 'with' ? 1 : 0 ?>" data-ready="<?= $ready ? 1 : 0 ?>" data-ppm="<?= $ppm ?>"
  <?= $geo ? 'data-lat="' . $geo[0] . '" data-lng="' . $geo[1] . '"' : '' ?>>
  <a class="ct-ph" href="kvartiry/<?= pn_e($a['slug']) ?>/" tabindex="-1" aria-hidden="true"><img <?= pn_img_attrs($a['photos'][0] ?? 'kv_empty', '(max-width: 700px) 100vw, (max-width: 1400px) 50vw, 33vw') ?> alt="" loading="lazy">
    <span class="ct-tags"><?php if ($tag): ?><span class="red"><?= pn_e($tag) ?></span><?php endif; ?></span></a>
  <div class="ct-acts"><button type="button" class="ib cmp" data-cmp="<?= $gid ?>" aria-pressed="false" aria-label="Сравнить"><svg class="ico"><use href="#cmp"/></svg></button><button type="button" class="ib fav" data-fav="<?= $gid ?>" aria-pressed="false" aria-label="В избранное"><svg class="ico"><use href="#heart"/></svg></button></div>
  <div class="ct-body">
    <h3><a href="kvartiry/<?= pn_e($a['slug']) ?>/"><?= pn_e(pn_rooms($a['rooms'])) ?>, <?= pn_area($a['area']) ?></a></h3>
    <p class="ct-where"><?php if ($z): ?><a href="<?= pn_e($z['path']) ?>"><?= pn_e($z['name']) ?></a><?php else: ?><?= pn_e((string) $a['address']) ?><?php endif; ?> · <?= pn_e((string) $a['district']) ?></p>
    <p class="ct-ok"><i></i><?= $a['market'] === 'new' ? 'Застройщик проверен' : 'Сделка проверена юристом' ?></p>
    <p class="ct-meta"><?= $a['floor'] ?>/<?= $a['floors'] ?> эт. · <?= pn_e($a['finish_label'] ?: ($a['finish'] === 'with' ? 'С отделкой' : 'Без отделки')) ?> · <?= pn_e(explode(' · ', (string) $a['house_status'])[0]) ?></p>
    <?php if ($noFin): ?><a class="ct-ren" href="remont/">+ наш ремонт под ключ — от <?= pn_mln((int) round($a['area'] * $ren)) ?></a><?php endif; ?>
    <p class="ct-tg"><span><?= $a['market'] === 'new' ? 'Новостройка' : 'Вторичка' ?></span><span><?= $a['market'] === 'new' ? 'Семейная ипотека' : 'Чистая сделка' ?></span></p>
    <div class="ct-foot">
      <p class="ct-price"><b><?= pn_rub($a['price']) ?></b><span><?= pn_rub($ppm) ?> за м²</span></p>
      <p class="ct-pay"><span>В ипотеку</span><b>от <?= pn_rub($pay) ?>/мес</b><small><?= pn_e(mb_strtolower((string) $prog['name'])) ?> <?= str_replace('.', ',', (string) $rate) ?> % · взнос 20 %</small></p>
    </div>
  </div>
</article>
