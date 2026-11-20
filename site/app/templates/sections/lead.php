<section class="lead" id="lead"><canvas class="ldots" id="ldots" aria-hidden="true"></canvas><div class="w lgrid">
  <div><h2 class="t">Расскажите, что ищете. Мы&nbsp;уже знаем, кому можно <span class="nw">доверять<i class="o n"></i></span></h2><p>Подберём варианты среди проверенных предложений и перезвоним. Или позвоните сами: <a href="tel:+79655002918" style="font-weight:700;border-bottom:2px solid #fff">+7 965 500-29-18</a>. На вопросы отвечаем круглосуточно — в чате, Telegram и MAX.</p>
    <div class="msg"><a href="#" data-chat>Чат на сайте</a><?= pn_msgr_link('tg') ?><?= pn_msgr_link('max') ?></div></div>
  <form class="form quiz" id="leadForm" novalidate>
    <div class="qh"><span id="qStep">Шаг 1 из 3</span><span class="qd" aria-hidden="true"><i class="on"></i><i></i><i></i></span></div>
    <fieldset class="on" data-s="1"><legend>Что ищете?</legend>
      <div class="ch" role="group" aria-label="Что ищете"><button type="button" aria-pressed="true" data-q="flat">Квартиру</button><button type="button" aria-pressed="false" data-q="house">Дом</button><button type="button" aria-pressed="false" data-q="reno">Ремонт</button><button type="button" aria-pressed="false" data-q="mort">Ипотеку</button></div></fieldset>
    <fieldset data-s="2"><legend id="q2l">Какой бюджет?</legend>
      <div class="rng"><label for="qb"><span id="qbl">Бюджет до</span> <b id="qbv"></b></label><input type="range" id="qb" min="3" max="30" step="0.5" value="9"></div>
      <div class="ch2" id="qr" role="group" aria-label="Комнат"><button type="button" aria-pressed="false" data-r="0">Студия</button><button type="button" aria-pressed="true" data-r="1">1</button><button type="button" aria-pressed="true" data-r="2">2</button><button type="button" aria-pressed="false" data-r="3">3</button><button type="button" aria-pressed="false" data-r="4">4+</button></div>
      <p class="qm" id="qMatch" aria-live="polite"></p></fieldset>
    <fieldset data-s="3"><legend>Куда прислать подборку?</legend>
      <div class="f"><label for="ln">Как к вам обращаться</label><input id="ln" autocomplete="name" placeholder="Имя"></div>
      <div class="f"><label for="lp">Телефон</label><input id="lp" type="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" aria-describedby="lpErr"><span class="err" id="lpErr">Введите номер полностью — 10 цифр после +7</span></div></fieldset>
    <div class="qnav"><button type="button" class="btn ghost" id="qBack" hidden>Назад</button><button type="button" class="btn red" id="qNext">Дальше</button><button class="btn red" type="submit" id="qSend" hidden>Получить подборку</button></div>
    <label class="cns" id="lcL"><input type="checkbox" id="lc"> <span>Согласен на <a href="privacy/" target="_blank">обработку персональных данных</a></span></label>
    <div class="done"><b>Заявка принята<i class="o"></i></b>Менеджер позвонит и пришлёт подборку. Если удобнее — напишите в чат на сайте.</div>
  </form>
</div></section>
</main>

