<?php /** Риелторам — партнёрская программа. Переменные: $s (настройки), $na (квартир на сайте), $nz (ЖК), $nd (проверенных застройщиков), $ren (цены ремонта) */
$ph = fn(string $k, string $p) => trim((string) ($s[$k] ?? '')) !== '' ? pn_e((string) $s[$k]) : '<span class="pt-ph">[' . $p . ']</span>';
$fee = $ph('realtor_fee', 'ВОЗНАГРАЖДЕНИЕ'); $hold = $ph('realtor_hold', 'СРОК ЗАКРЕПЛЕНИЯ'); $pay = $ph('realtor_payout', 'КОГДА ВЫПЛАТА');
$lead = 'data-lead="quiz" data-title="Стать партнёром" data-want="Риелтор: партнёрство с Платформой" data-ref="rieltoram/"'; ?>
<section class="sx-hero" style="--sxp:50% 55%"><img class="sx-bg" src="assets/img/ekb_aerial.jpg" srcset="assets/img/ekb_aerial-1280.jpg 1280w, assets/img/ekb_aerial-1920.jpg 1920w, assets/img/ekb_aerial.jpg 2880w" sizes="100vw" alt="" fetchpriority="high" decoding="async"><div class="sx-in">
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <span>Риелторам</span></nav>
<div class="ct-head">
  <h1>Риелторам<i class="ct-dot" aria-hidden="true"></i></h1>
  <p class="ct-intro">Проводите сделки по новостройкам Екатеринбурга через Платформу: проверенные застройщики в одном окне, клиент закреплён за вами,
    ипотеку и сделку ведём вместе.</p>
</div>
  <ul class="sx-chips"><li>Клиент закреплён за вами</li><li>Вознаграждение — <b><?= $fee ?></b></li><?php if ($na): ?><li><b><?= $na ?></b><span> <?= pn_ru_plural($na, 'квартира', 'квартиры', 'квартир') ?> в каталоге</span></li><?php endif; ?><li>Ипотека в нескольких банках</li></ul>
</div></section>

<section class="sv-sec"><h2 class="sv-h">Что вы получаете</h2>
  <div class="pt-g">
    <article class="pt-c"><h3>Проверенные застройщики в одном окне</h3><p>Квартиры застройщиков, которых мы проверили<?= $nd ? ' (сейчас — ' . $nd . ')' : '' ?>: актуальные цены, планировки и спецпредложения. Каталог обновляется каждый день.</p><a href="kvartiry/">Открыть каталог</a></article>
    <article class="pt-c"><h3>Клиент закреплён за вами</h3><p>Сообщаете менеджеру о клиенте до показа — клиент закрепляется за вами на <?= $hold ?>.</p></article>
    <article class="pt-c red"><h3>Вознаграждение</h3><p><b><?= $fee ?></b>. Выплата — <?= $pay ?>.</p></article>
    <article class="pt-c"><h3>Ипотека</h3><p>Подбираем программу и подаём заявку сразу в несколько банков — Сбер, ВТБ, Альфа-Банк, ДОМ.РФ и другие. Ведём клиента до одобрения.</p><a href="ipoteka/">Ставки и калькулятор</a></article>
    <article class="pt-c"><h3>Бронь и договор</h3><p>Помогаем с бронью и договором долевого участия. Расчёты с застройщиком — через эскроу-счёт.</p></article>
    <article class="pt-c"><h3>Ремонт и дом для клиента</h3><p>Нужен ремонт — делаем своей бригадой, от <?= pn_rub((int) ($ren[0] ?? 20000)) ?> за м². Нужен свой дом — строим по нашим проектам с рассрочкой.</p><a href="remont/">Ремонт</a> <a href="doma/">Дома</a></article>
  </div>
</section>

<section class="sv-sec"><h2 class="sv-h">Как работаем</h2>
  <ol class="sv-steps">
    <li><b>Заявка</b><span>Оставляете заявку — менеджер позвонит и расскажет условия.</span></li>
    <li><b>Договор</b><span>Подписываем партнёрский договор: вознаграждение и сроки — в нём.</span></li>
    <li><b>Закрепление клиента</b><span>Сообщаете о клиенте до показа — он закреплён за вами.</span></li>
    <li><b>Показ и сделка</b><span>Показ, бронь, ипотека и договор — вместе с нашим менеджером.</span></li>
    <li><b>Вознаграждение</b><span>Выплата — <?= $pay ?>.</span></li>
  </ol>
</section>

<section class="sv-sec"><h2 class="sv-h">Вопросы</h2>
  <div class="pt-faq">
    <details><summary>Какие объекты можно предлагать клиентам?</summary><p>Квартиры из нашего каталога — новостройки проверенных застройщиков<?= $na ? ', сейчас ' . $na . ' ' . pn_ru_plural($na, 'квартира', 'квартиры', 'квартир') : '' ?>. Каталог обновляется каждый день.</p></details>
    <details><summary>Сколько я получу и когда?</summary><p>Вознаграждение — <?= $fee ?>. Выплата — <?= $pay ?>. Всё это прописываем в партнёрском договоре.</p></details>
    <details><summary>Что, если клиент потом обратится к вам напрямую?</summary><p>Клиент, о котором вы сообщили до показа, закреплён за вами на <?= $hold ?>.</p></details>
    <details><summary>Что нужно, чтобы начать?</summary><p>Оставьте заявку или позвоните: <a href="tel:+79655002918">+7 965 500-29-18</a>. Менеджер расскажет условия и пришлёт договор.</p></details>
  </div>
</section>

<section class="sv-band">
  <div><h2>Станьте партнёром Платформы</h2><p>Оставьте телефон — расскажем условия и подключим к каталогу проверенных новостроек.</p></div>
  <a class="pg-btn red" href="./#lead" <?= $lead ?>>Стать партнёром</a>
</section>
<script src="assets/js/page.js" defer></script>
