<?php /** Страница не найдена: крупный заголовок как на главной и быстрые переходы в разделы. */ ?>
<article class="pg-doc pg-404">
  <p class="pg-404n" aria-hidden="true">404</p>
  <h1>Здесь точку ещё не&nbsp;поставили<i class="o"></i></h1>
  <p class="pg-404t">Возможно, квартиру уже продали или ссылка устарела. Выберите раздел — или позвоните, подберём вариант под вашу задачу.</p>
  <nav class="pg-404l" aria-label="Разделы">
    <a href="kvartiry/"><b>Квартиры</b><span>новостройки и вторичка</span></a>
    <a href="doma/"><b>Дома</b><span>проекты и рассрочка 0 %</span></a>
    <a href="remont/"><b>Ремонт</b><span>под ключ, смета до начала</span></a>
    <a href="ipoteka/"><b>Ипотека</b><span>калькулятор и программы</span></a>
  </nav>
  <p><a class="pg-btn red" href="./">На главную</a> <a class="pg-btn" href="tel:<?= pn_e($settings['phone_tel'] ?? '+79655002918') ?>"><?= pn_e($settings['phone'] ?? '+7 965 500-29-18') ?></a></p>
</article>
