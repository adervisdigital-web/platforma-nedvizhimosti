<section class="sec" id="calc" style="padding-top:0"><div class="w">
  <div class="br">[ <b>●</b> Ипотека ]</div>
  <h2 class="t">Посчитайте платёж — без звёздочек<i class="o"></i></h2>
  <div class="banks">Работаем с банками: <span>Сбер</span><span>ВТБ</span><span>Альфа-Банк</span><span>ДОМ.РФ</span><span>Россельхозбанк</span><span>УБРИР</span> — и получаем для клиентов индивидуальные ставки.</div>
  <div class="calc">
    <div class="cin">
      <div class="rng"><label for="cp">Стоимость квартиры <b id="cpv"></b></label><input type="range" id="cp" min="2000000" max="20000000" step="100000" value="7500000"></div>
      <div class="rng"><label for="cd">Первый взнос <b id="cdv"></b></label><input type="range" id="cd" min="10" max="90" step="1" value="20"></div>
      <div class="rng"><label for="ct">Срок <b id="ctv"></b></label><input type="range" id="ct" min="5" max="30" step="1" value="25"></div>
      <div><div style="font-size:14px;color:var(--mut);margin-bottom:10px">Программа (ставки — пример, точные подберём под вас)</div>
        <div class="rates" id="rates"><?php   // программы и ставки — из админки (Настройки → Ипотека)
  try { $progs = array_values(array_filter(Repo::settingsAll()['mortgage_programs'] ?? [], fn($p) => isset($p['name'], $p['rate']))); } catch (Throwable $e) { $progs = []; }
  if (!$progs) $progs = [['name' => 'Семейная', 'rate' => 6], ['name' => 'Рыночная', 'rate' => 20]];
  foreach ($progs as $k => $p): ?><button aria-pressed="<?= $k ? 'false' : 'true' ?>" data-p="<?= $k ?>" data-r="<?= pn_e((string) $p['rate']) ?>"><?= pn_e($p['name']) ?><small><?= str_replace('.', ',', (string) $p['rate']) ?> %</small></button><?php endforeach; ?></div></div>
      <div class="kids" id="kids" role="group" aria-label="Детей в семье"><span>Детей в семье</span><?php foreach ([1, 2, 3, 4, 5] as $k): ?><button type="button" data-k="<?= $k ?>" aria-pressed="<?= $k === 1 ? 'true' : 'false' ?>"><?= $k === 5 ? '5+' : $k ?></button><?php endforeach; ?>
        <small>с 1 октября 2026 ставка и лимит семейной ипотеки зависят от числа детей</small></div>
    </div>
    <div class="cout" aria-live="polite">
      <div class="note">Ежемесячный платёж</div>
      <div class="pay" id="pay">—</div>
      <div class="cbar" aria-hidden="true"><i id="cbL"></i><i id="cbO"></i></div><div class="cleg"><span><i></i>Кредит <b id="cbLv"></b></span><span><i></i>Переплата <b id="cbOv"></b></span></div>
      <div class="crow"><span>Сумма кредита</span><b id="loan">—</b></div>
      <div class="crow"><span>Переплата за весь срок</span><b id="over">—</b></div>
      <div class="crow"><span>Нужный доход, от</span><b id="inc">—</b></div>
      <div class="cprog" id="cprog" role="group" aria-label="Сравнение программ"></div>
      <div class="note cparts" id="cparts"></div>
      <a class="btn" href="#lead" data-lead="quiz" data-title="Подберём ипотеку" data-want="Ипотека: подобрать программу" data-ref="#calc" data-calc>Подобрать программу</a>
      <div class="note"><?php try { $rd = pn_rates_date_ru(Repo::settingsAll()); } catch (Throwable $e) { $rd = ''; } ?><?= $rd ? 'Ставки на ' . $rd . '. ' : '' ?>Расчёт ориентировочный: аннуитетный платёж. Итоговые условия зависят от банка и программы.</div>
    </div>
  </div>
</div></section>

