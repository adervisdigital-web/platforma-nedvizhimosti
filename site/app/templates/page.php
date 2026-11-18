<?php /** Каркас подстраницы (квартира, дом, политика, 404). Переменные: $base_tag, $seo_head, $jsonld, $content, $settings */
include __DIR__ . '/head.php';
preg_match('~<svg width="0".*?</svg>~s', pn_render('top'), $sprite);   // символы иконок (#mark и др.) без заставки главной
$tel = $settings['phone_tel'] ?? '+79655002918'; ?>
<body class="pg">
<?= $sprite[0] ?? '' ?>
<header class="pg-h"><div class="w">
  <a class="logo" href="./" aria-label="Платформа недвижимости — на главную"><svg width="38" height="36" fill="#161617"><use href="#mark"/></svg><span><b>ПЛАТФОРМА</b><small>НЕДВИЖИМОСТИ</small></span></a>
  <nav class="pg-nav" aria-label="Разделы"><a href="kvartiry/">Квартиры</a><a href="./#houses">Дома</a><a href="./#ba">Ремонт</a><a href="./#calc">Ипотека</a></nav>
  <a class="pg-tel" href="tel:<?= pn_e($tel) ?>"><?= pn_e($settings['phone'] ?? '') ?></a>
</div></header>
<main class="pg-m w"><?= $content ?></main>
<footer class="pg-f"><div class="w"><span><?= pn_e($settings['legal'] ?? '') ?> · <?= pn_e($settings['domain'] ?? '') ?></span><a href="./privacy/">Политика обработки персональных данных</a><span>Ставим точку.</span></div></footer>
</body>
</html>
