<nav class="tabbar tb2" id="tabbar" aria-label="Меню приложения">
  <a class="on" href="#search" data-sec="search"><svg class="tic"><use href="#t-search"/></svg><span>Поиск</span></a>
  <a href="#list" data-sec="list" data-map><svg class="tic"><use href="#t-map"/></svg><span>Карта</span></a>
  <a href="#calc" data-sec="calc"><svg class="tic"><use href="#t-pct"/></svg><span>Ипотека</span></a>
  <a href="#cab" data-sec="cab"><svg class="tic"><use href="#t-door"/></svg><span>Кабинет</span></a>
  <a href="#" data-chat><svg class="tic"><use href="#t-chat"/></svg><span>Чат 24/7</span></a>
</nav>
<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Меню" hidden>
  <div class="mn-top"><span class="mn-st"><i></i><span id="mnSt">на связи</span></span><button type="button" class="mn-x" id="mnX" aria-label="Закрыть меню">×</button></div>
  <nav class="mn-l" aria-label="Разделы">
    <a href="#list">Квартиры</a><a href="#houses">Дома</a><a href="#ba">Ремонт</a><a href="#calc">Ипотека</a><a href="#how">Как мы проверяем</a><a href="#rev">Отзывы</a>
  </nav>
  <div class="mn-c">
    <a class="mn-tel" href="tel:+79655002918">+7 965 500-29-18</a>
    <div class="mn-b"><a class="btn red" href="tel:+79655002918">Позвонить</a><button type="button" class="btn ghost" data-chat>Чат 24/7</button></div>
    <a class="mn-cab" href="kabinet.html"><svg viewBox="0 0 76 72" aria-hidden="true"><use href="#mark"/></svg>Личный кабинет</a>
  </div>
</div>

<dialog class="dlg" id="dlg" aria-labelledby="dlgT"><div class="dh"><h3 id="dlgT"></h3><button type="button" id="dlgX" aria-label="Закрыть">×</button></div><div class="db" id="dlgB"></div></dialog>
<div class="toast" id="toast" role="status" aria-live="polite"></div>

<button class="chatfab" id="chatFab" aria-expanded="false" aria-controls="chat"><i><svg class="ico" style="width:18px;height:18px"><use href="#msg"/></svg></i><span class="cf-t"><b>Спросить</b><small>ответим 24/7</small></span></button>
<div class="chat" id="chat" role="dialog" aria-label="Помощник Платформы" hidden>
  <div class="ch-h"><svg width="30" height="28" fill="#F4F2EE"><use href="#mark"/></svg><div><b>Помощник Платформы</b><small><i></i>онлайн · отвечает круглосуточно</small></div><button class="ch-x" id="chatX" aria-label="Закрыть">×</button></div>
  <div class="ch-b" id="chatLog" aria-live="polite"></div>
  <div class="ch-q" id="chatQ"></div>
  <form class="ch-f" id="chatForm"><input id="chatIn" placeholder="Напишите вопрос" aria-label="Ваш вопрос" autocomplete="off"><button aria-label="Отправить">→</button></form>
  <div class="ch-m"><a href="#" data-soon="Telegram">Telegram</a><a href="#" data-soon="MAX">MAX</a><a href="tel:+79655002918">Позвонить</a></div>
</div>

