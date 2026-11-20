<?php /** «Квартира. Дом. Ремонт.»: карточки ведут на страницы, цифры — из базы (меняются вместе с админкой), ремонт — до/после.
 * Застройщики: если у застройщика в базе есть квартиры — ссылка на его страницу; пока таких нет — список партнёров текстом. */
try {
    $apts = Repo::apartments(); $hs = Repo::houses(); $set = Repo::settingsAll();
    $cx = pn_complexes_full();
    $devLinks = array_filter(pn_catalog_pages(), fn($v) => $v[3] === 'dev');
} catch (Throwable $e) { $apts = []; $hs = []; $set = []; $cx = []; $devLinks = []; }
$na = count($apts); $pmin = $apts ? min(array_column($apts, 'price')) : 0;
$nz = count(array_unique(array_filter(array_column($apts, 'complex'))));
$nh = count($hs); $warm = (int) ($set['warm_contour_from'] ?? 0);
$hmin = $hs && $warm ? $warm * min(array_column($hs, 'n')) : 0;
$areas = array_column($hs, 'n'); $lines = array_values(array_unique(array_column($hs, 'line')));
$ren = $set['renovation_prices'] ?? [20000, 45000, 80000];
$num = fn($n, $a, $b, $c) => $n . ' ' . pn_ru_plural($n, $a, $b, $c); ?>
<section class="sec" id="partners"><div class="w">
  <div class="br">[ <b>●</b> Что мы делаем ]</div>
  <h2 class="t"><span class="nw">Квартира<i class="o"></i></span> <span class="nw">Дом<i class="o"></i></span> <span class="nw">Ремонт<i class="o"></i></span></h2>
  <div class="pgrid">
    <div class="pc"><div class="ph"><img src="assets/img/zhk.jpg" alt="Новый жилой комплекс в сумерках" loading="lazy"><span>Продаём</span></div><div class="b"><h3>Квартиры<i class="o"></i></h3>
      <p>Новостройки от проверенных застройщиков — со спецпредложениями напрямую от них. Вторичка — после проверки юриста. Комиссии для покупателя нет.</p>
      <?php if ($na): ?><div class="br2"><span class="nw">[ <?= $num($na, 'квартира', 'квартиры', 'квартир') ?> ]</span> <span class="nw">[ от <?= pn_mln($pmin) ?> ]</span><?= $nz ? ' <span class="nw">[ ' . $num($nz, 'жилой комплекс', 'жилых комплекса', 'жилых комплексов') . ' ]</span>' : '' ?></div><?php endif; ?>
      <div class="devs"><?php if ($devLinks): foreach ($devLinks as $p => [, $short]): ?><a href="<?= pn_e($p) ?>"><?= pn_e($short) ?></a><?php endforeach; else: ?><span>Брусника</span><span>Атомстройкомплекс</span><span>УГМК</span><span>Прогресс</span><span>Атлас</span><?php endif; ?></div>
      <a class="lk" href="kvartiry/">Смотреть квартиры</a></div></div>
    <div class="pc"><div class="ph"><img src="assets/img/houses/n235_1.jpg" alt="Дом «Северный Урал 235» среди сосен" loading="lazy"><span>Строим</span></div><div class="b"><h3>Дома<i class="o"></i></h3>
      <p><?php if ($nh): ?><?= ucfirst($num($nh, 'проект', 'проекта', 'проектов')) ?> в линейках <?= pn_e(preg_replace('~, ([^,]+)$~u', ' и $1', implode(', ', array_map(fn($l) => preg_replace('~ Урал$~u', '', $l), $lines)))) ?> Урал — от <?= min($areas) ?> до <?= max($areas) ?> м²<?= $hmin ? ', от ' . pn_mln($hmin) . ' в тёплом контуре' : '' ?>.<?php else: ?>Каменные дома по нашим проектам.<?php endif; ?>
        Строят наши бригады. Взнос 30 %, остальное — равными платежами до 5 лет без процентов.</p>
      <div class="br2"><span class="nw">[ газоблок ]</span> <span class="nw">[ кирпич ]</span> <span class="nw">[ керамоблок ]</span> <span class="nw">[ дерево ]</span> <span class="nw">[ гарантия 5 лет ]</span></div><a class="lk" href="doma/">Выбрать проект</a></div></div>
    <div class="pc"><div class="ph pba" data-pba><img src="assets/img/ba_before.jpg" alt="Квартира до ремонта" loading="lazy"><img class="pba-a" src="assets/img/ba_after.jpg" alt="Та же квартира после нашего ремонта" loading="lazy"><span>Делаем сами</span><em class="pba-l" aria-hidden="true"><b>до</b><b>после</b></em></div><div class="b"><h3>Ремонт<i class="o"></i></h3>
      <p>Работа и материалы — от <?= pn_rub((int) $ren[0]) ?> за м²: базовый, комфорт или премиум. Смета и предварительный договор до начала, акт на каждый этап.</p>
      <div class="br2"><span class="nw">[ смета ]</span> <span class="nw">[ договор ]</span> <span class="nw">[ акты этапов ]</span> <span class="nw">[ замер бесплатно ]</span></div><a class="lk" href="remont/">Посчитать ремонт</a></div></div>
  </div>
  <div class="way"><a class="stp" href="kvartiry/"><i></i>Подобрали квартиру</a><span class="ln"></span><a class="stp" href="ipoteka/"><i></i>Провели сделку</a><span class="ln"></span><a class="stp" href="remont/"><i></i>Сделали ремонт</a><span class="ln"></span><span class="stp"><i></i>Вы получили ключи</span><a class="btn red" href="#lead" data-pack>Один менеджер на всё</a></div>
</div></section>
