<section class="sec" id="houses" style="padding-top:0"><div class="w">
  <div class="lhead"><div><div class="br">[ <b>●</b> Дома ]</div><h2 class="t">Свой дом — в рассрочку 0&nbsp;% до&nbsp;5&nbsp;лет<i class="o"></i></h2></div>
    <p style="max-width:480px;color:#4A4741;margin:0">Пять проектов в трёх линейках — Северный, Южный и Средний Урал. Планировку и фасад настроим под вашу семью. Строят наши бригады — из газоблока, кирпича, керамоблока или дерева.</p></div>
  <div class="hfl seg2" id="hfl" role="group" aria-label="Линейка"><button aria-pressed="true" data-l="">Все проекты</button><button aria-pressed="false" data-l="Северный Урал">Северный Урал</button><button aria-pressed="false" data-l="Южный Урал">Южный Урал</button><button aria-pressed="false" data-l="Средний Урал">Средний Урал</button><button aria-pressed="false" data-fl="1">Одноэтажные</button><button aria-pressed="false" data-fl="2">Двухэтажные</button></div>
  <div class="hx" id="hx"></div>
  <div class="calc inst">
    <div class="cin">
      <div><div style="font-size:14px;color:var(--mut);margin-bottom:10px">Проект</div><div class="seg2" id="hproj"></div></div>
      <div class="rng"><label for="ha">Площадь дома <b id="hav"></b></label><input type="range" id="ha" min="100" max="400" step="5" value="235"></div>
      <div class="rng"><label for="ht">Рассрочка <b id="htv"></b></label><input type="range" id="ht" min="1" max="5" step="1" value="3"></div>
      <div><div style="font-size:14px;color:var(--mut);margin-bottom:10px">Как платить остаток</div>
        <div class="seg2" id="hmode"><button aria-pressed="true" data-m="inst">Рассрочка 0 %</button><button aria-pressed="false" data-m="stage">По этапам стройки</button></div></div>
    </div>
    <div class="cout dk" aria-live="polite">
      <div class="note" id="hname"></div>
      <div class="pay" id="hpay">—</div>
      <div class="crow"><span>Стоимость тёплого контура, от</span><b id="hsum">—</b></div>
      <div class="crow"><span>Первый взнос 30 %</span><b id="hpv">—</b></div>
      <div class="crow"><span id="hrestL">Остаток</span><b id="hrest">—</b></div>
      <a class="btn" href="#lead">Обсудить проект</a>
      <div class="note">Расчёт ориентировочный: от <?php try { echo pn_rub((int) (Repo::settingsAll()['warm_contour_from'] ?? 95000)); } catch (Throwable $e) { echo '95 000 ₽'; } ?> за м² тёплого контура, первый взнос 30 %, остальное — равными платежами без процентов. Точную цену назовёт менеджер после выбора проекта и материала.</div>
    </div>
  </div>
</div></section>

