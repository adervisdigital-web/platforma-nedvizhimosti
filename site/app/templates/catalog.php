<?php /** Каталог и подборки. Переменные: $h1, $path, $group, $apts, $st, $crumbs, $intro, $nav, $cx, $s */
$opt = function (array $vals) { $vals = array_values(array_unique(array_filter($vals))); sort($vals); return $vals; };
$dists = $group === 'district' ? [] : $opt(array_column($apts, 'district'));
$zs = $opt(array_column($apts, 'complex'));
$pill = fn(string $p, string $t, int $n) => '<a href="' . pn_e($p) . '"' . ($p === $path ? ' aria-current="page"' : '') . '>' . pn_e($t) . ' <span>' . $n . '</span></a>'; ?>
<section class="sx-hero" style="--sxp:50% 55%"><img class="sx-bg" src="assets/img/ekb_aerial.jpg" srcset="assets/img/ekb_aerial-1280.jpg 1280w, assets/img/ekb_aerial-1920.jpg 1920w, assets/img/ekb_aerial.jpg 2880w" sizes="100vw" alt="" fetchpriority="high" decoding="async"><div class="sx-in">
<nav class="pg-bc" aria-label="Навигация"><?php foreach ($crumbs as $k => [$t, $u]): ?><?= $k ? ' · ' : '' ?><?= $k === count($crumbs) - 1 ? '<span>' . pn_e($t) . '</span>' : '<a href="' . ($u === '' ? './' : pn_e($u)) . '">' . pn_e($t) . '</a>' ?><?php endforeach; ?></nav>
<div class="ct-head">
  <h1><?= pn_e($h1) ?><i class="ct-dot" aria-hidden="true"></i></h1>
  <p class="ct-intro"><?= pn_e($intro) ?></p>
</div>
  <ul class="sx-chips"><li><b><?= count($apts) ?></b> <?= pn_ru_plural(count($apts), "квартира", "квартиры", "квартир") ?></li><?php if ($apts): ?><li>от <b><?= pn_mln((int) min(array_column($apts, "price"))) ?></b></li><?php endif; ?><li><b>0 ₽</b> комиссии</li><li>Только проверенные застройщики</li></ul>
</div></section>

<nav class="ct-pills" aria-label="Подборки">
  <?= $pill('kvartiry/', 'Все', $nav['all']) ?>
  <?php foreach ($nav['type'] as $p => [$t, $n]) echo $pill($p, $t, $n); ?>
  <span class="ct-sep" aria-hidden="true"></span>
  <?php foreach ($nav['rooms'] as $p => [$t, $n]) echo $pill($p, $t, $n); ?>
  <?php if ($nav['feat']): ?><span class="ct-sep" aria-hidden="true"></span><?php foreach ($nav['feat'] as $p => [$t, $n]) echo $pill($p, $t, $n); ?><?php endif; ?>
</nav>
<?php if ($path === 'kvartiry/semeynaya-ipoteka/'):
    $fam = array_values(array_filter($s['mortgage_programs'] ?? [], fn($p) => mb_stripos((string) ($p['name'] ?? ''), 'семейн') !== false))[0] ?? null; ?>
<section class="ct-fam" aria-label="Семейная ипотека">
  <?php $tiers = $s['family_tiers'] ?? []; $rr = array_column($tiers, 'rate'); $ll = array_column($tiers, 'limit'); ?>
  <div><span>Ставка</span><b><?= $rr ? str_replace('.', ',', (string) min($rr)) . '–' . str_replace('.', ',', (string) max($rr)) . ' %' : ($fam ? str_replace('.', ',', (string) $fam['rate']) . ' %' : 'льготная') ?></b></div>
  <div><span>Лимит</span><b><?= $ll ? str_replace('.', ',', (string) (min($ll) / 1e6)) . '–' . str_replace('.', ',', (string) (max($ll) / 1e6)) . ' млн' : 'по банку' ?></b></div>
  <div><span>Взнос</span><b>от 20 %</b></div>
  <div class="ct-fam-t"><p><?= pn_e(pn_family_note()) ?> Менеджер проверит, подходите ли вы, и подаст заявку сразу в несколько банков.</p><a href="ipoteka/">Все программы и калькулятор →</a></div>
</section>
<?php endif; ?>

<?php if ($apts): ?>
<button type="button" class="ct-ftog" data-ct-ftog aria-expanded="false" aria-controls="ctFilters"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M3 5h14M6 10h8M8.5 15h3"/></svg>Фильтры<span class="ct-fn" data-ct-fn hidden></span></button>
<form class="ct-filters" id="ctFilters" data-ct-form aria-label="Фильтры" onsubmit="return false">
  <label class="ct-f"><span>Цена, ₽</span><span class="ct-2"><input name="pmin" inputmode="numeric" placeholder="от <?= pn_e(pn_mln($st['pmin'])) ?>" aria-label="Цена от"><input name="pmax" inputmode="numeric" placeholder="до <?= pn_e(pn_mln($st['pmax'])) ?>" aria-label="Цена до"></span></label>
  <label class="ct-f"><span>Площадь от, м²</span><input name="amin" inputmode="decimal" placeholder="<?= pn_e(str_replace('.', ',', (string) pn_num($st['amin']))) ?>"></label>
  <?php if (count($dists) > 1): ?><label class="ct-f"><span>Район</span><select name="d"><option value="">Любой</option><?php foreach ($dists as $d): ?><option value="<?= pn_e(pn_slug($d)) ?>"><?= pn_e($d) ?></option><?php endforeach; ?></select></label><?php endif; ?>
  <?php if (count($zs) > 1): ?><label class="ct-f"><span>ЖК</span><select name="z"><option value="">Любой</option><?php foreach ($zs as $z): ?><option value="<?= pn_e($cx[$z]['slug'] ?? pn_slug($z)) ?>"><?= pn_e($z) ?></option><?php endforeach; ?></select></label><?php endif; ?>
  <div class="ct-checks">
    <label class="ct-chk"><input type="checkbox" name="fin" value="1"> С отделкой</label>
    <label class="ct-chk"><input type="checkbox" name="ready" value="1"> Дом сдан</label>
  </div>
</form>

<div class="ct-bar">
  <p class="ct-count" aria-live="polite">Найдено: <b data-ct-count><?= $st['n'] ?></b></p>
  <button type="button" class="ct-reset" data-ct-reset hidden>Сбросить фильтры</button>
  <div class="ct-bar-r">
    <label class="ct-sort"><span class="ct-vh">Сортировка</span><select name="sort" data-ct-sort>
      <option value="">По умолчанию</option><option value="p">Сначала дешевле</option><option value="-p">Сначала дороже</option><option value="ppm">Дешевле за м²</option><option value="-a">Больше площадь</option></select></label>
    <div class="ct-view" role="group" aria-label="Вид"><button type="button" data-view="list" aria-pressed="true">Список</button><button type="button" data-view="map" aria-pressed="false">На карте</button></div>
  </div>
</div>

<div class="ct-grid" data-ct-list>
  <?php foreach ($apts as $i => $a) echo pn_render('ct_card', ['a' => $a, 'i' => $i, 'cx' => $cx, 's' => $s]); ?>
</div>
<div class="ct-map" data-ct-map hidden role="region" aria-label="Квартиры на карте"></div>
<div class="ct-empty" data-ct-empty hidden><p>По этим условиям ничего не нашлось.</p><button type="button" class="pg-btn" data-ct-reset>Сбросить фильтры</button></div>
<div class="ct-more" data-ct-more-wrap hidden><button type="button" class="pg-btn" data-ct-more>Показать ещё</button></div>
<?php endif; ?>

<section class="ct-cta">
  <div><h2>Не нашли подходящую?</h2><p>Расскажите, что ищете — подберём из проверенных предложений, в том числе тех, что ещё не на сайте.</p></div>
  <a class="pg-btn red" href="./#lead" data-lead="quiz" data-title="Подберём квартиру" data-want="Подбор квартиры: <?= pn_e($h1) ?>" data-ref="<?= pn_e($path) ?>" data-filters>Подобрать квартиру</a>
</section>

<section class="ct-links">
  <?php if ($nav['district']): ?><div><h2>Квартиры по районам</h2><nav class="ct-linkl"><?php foreach ($nav['district'] as $p => [$t, $n]): ?><a href="<?= pn_e($p) ?>"<?= $p === $path ? ' aria-current="page"' : '' ?>><?= pn_e($t) ?> <span><?= $n ?></span></a><?php endforeach; ?></nav></div><?php endif; ?>
  <?php if ($nav['dev']): ?><div><h2>Застройщики</h2><nav class="ct-linkl"><?php foreach ($nav['dev'] as $p => [$t, $n]): ?><a href="<?= pn_e($p) ?>"<?= $p === $path ? ' aria-current="page"' : '' ?>><?= pn_e($t) ?> <span><?= $n ?></span></a><?php endforeach; ?></nav></div><?php endif; ?>
  <?php if ($nav['zhk']): ?><div><h2>Жилые комплексы</h2><nav class="ct-linkl"><?php foreach ($nav['zhk'] as $p => [$t, $n]): ?><a href="<?= pn_e($p) ?>"><?= pn_e($t) ?> <span><?= $n ?></span></a><?php endforeach; ?></nav></div><?php endif; ?>
</section>
<script src="assets/js/catalog.js" defer></script>
