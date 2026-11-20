<?php /** Застройщикам — отдел продаж на аутсорсинге. Переменные: $s (настройки), $na (квартир на сайте), $nd (проверенных застройщиков) */
$terms = trim((string) ($s['dev_terms'] ?? '')) !== '' ? pn_e((string) $s['dev_terms']) : '<span class="pt-ph">[МОДЕЛЬ ОПЛАТЫ]</span>';
$hours = pn_e(($s['hours_from'] ?? '9:00') . '–' . ($s['hours_to'] ?? '21:00'));
$lead = 'data-lead="quiz" data-title="Обсудим сотрудничество" data-want="Застройщик: отдел продаж на аутсорсинге" data-ref="zastroyshchikam/"'; ?>
<section class="sx-hero" style="--sxp:30% 60%"><img class="sx-bg" src="assets/img/ekb_dusk.jpg" srcset="assets/img/ekb_dusk-1280.jpg 1280w, assets/img/ekb_dusk-1920.jpg 1920w, assets/img/ekb_dusk.jpg 2880w" sizes="100vw" alt="" fetchpriority="high" decoding="async"><div class="sx-in">
<nav class="pg-bc" aria-label="Навигация"><a href="./">Главная</a> · <span>Застройщикам</span></nav>
<div class="ct-head">
  <h1>Отдел продаж на аутсорсинге<i class="ct-dot" aria-hidden="true"></i></h1>
  <p class="ct-intro">Продаём квартиры проверенных застройщиков Екатеринбурга: свои менеджеры, сайт-каталог, ипотека в нескольких банках
    и риелторы-партнёры. Вы строите — мы продаём.</p>
</div>
  <ul class="sx-chips"><li><b>5 лет</b><span> на рынке</span></li><li><b>1 985</b><span> сделок с квартирами</span></li><li>Оплата — <b><?= $terms ?></b></li></ul>
</div></section>

<section class="sv-sec"><h2 class="sv-h">Что берём на себя</h2>
  <div class="pt-g">
    <article class="pt-c"><h3>Покупатели</h3><p>Ваши квартиры — в нашем каталоге с ценами, планировками и спецпредложениями. Отметка «Застройщик проверен» на каждой карточке.</p><a href="kvartiry/">Как выглядит каталог</a></article>
    <article class="pt-c"><h3>Звонки и показы</h3><p>Менеджеры на связи ежедневно <?= $hours ?>: отвечают на вопросы, записывают на просмотр и приводят покупателя в офис продаж.</p></article>
    <article class="pt-c"><h3>Ипотека</h3><p>Подбираем программу — семейную, IT, рыночную — и подаём заявку сразу в несколько банков.</p><a href="ipoteka/">Ипотека на сайте</a></article>
    <article class="pt-c"><h3>Сделка</h3><p>Бронь, договор долевого участия, расчёты через эскроу-счёт. Покупатель не платит нам комиссию.</p></article>
    <article class="pt-c"><h3>Риелторы-партнёры</h3><p>Риелторы Екатеринбурга проводят сделки по вашим объектам через Платформу — с закреплением клиента и понятным вознаграждением.</p><a href="rieltoram/">Условия для риелторов</a></article>
    <article class="pt-c red"><h3>Ремонт для покупателя</h3><p>Квартиры без отделки продаём вместе с нашим ремонтом под ключ — покупателю проще решиться.</p><a href="remont/">Ремонт</a></article>
  </div>
</section>

<section class="sv-sec"><h2 class="sv-h">Как подключиться</h2>
  <ol class="sv-steps">
    <li><b>Знакомство</b><span>Встречаемся, обсуждаем объекты и условия: <?= $terms ?>.</span></li>
    <li><b>Проверка</b><span>Разрешение на строительство, проектная декларация и эскроу, сроки прошлых домов, банкротные дела.</span></li>
    <li><b>Договор</b><span>Фиксируем условия, объём и порядок работы.</span></li>
    <li><b>Выгрузка</b><span>Вы даёте ссылку на XML-фид — тот же, что для Яндекс Недвижимости. Квартиры сами появляются на сайте и обновляются каждый день.</span></li>
    <li><b>Продажи</b><span>Ведём покупателей от звонка до сделки.</span></li>
  </ol>
</section>

<section class="sv-band">
  <div><h2>Обсудим ваши объекты</h2><p>Оставьте телефон — руководитель Платформы свяжется с вами и расскажет, как мы работаем.</p></div>
  <a class="pg-btn red" href="./#lead" <?= $lead ?>>Обсудить сотрудничество</a>
</section>
<script src="assets/js/page.js" defer></script>
