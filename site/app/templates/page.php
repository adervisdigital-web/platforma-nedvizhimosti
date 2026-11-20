<?php /** Каркас подстраницы (каталог, квартира, дом, ЖК, услуги, политика, 404) — шапка, подвал и меню как на главной.
 * Переменные: $base_tag, $seo_head, $jsonld, $content, $settings, $cur (раздел для подсветки меню), $shell_json (данные для чата и «перезвоним») */
include __DIR__ . '/head.php';
preg_match('~<svg width="0".*?</svg>~s', pn_render('top'), $sprite);   // символы иконок (#mark и др.) без заставки главной
$sub = true; $cur = $cur ?? ''; $hero = str_contains($content, 'sx-hero'); ?>
<body class="pg<?= $hero ? ' pg-hero' : '' ?>">
<?= $sprite[0] ?? '' ?>
<div class="prog" id="prog" aria-hidden="true"><i></i><b></b></div>
<?php include __DIR__ . '/header.php'; ?>
<main class="pg-m w"><?= $content ?></main>
<?php include __DIR__ . '/footer.php'; include __DIR__ . '/overlays.php'; ?>
<input id="pnHp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px">
<script id="pn-data" type="application/json"><?= $shell_json ?? '{}' ?></script>
<script src="assets/js/data.js"></script>
<script src="assets/js/lead.js" defer></script>
<script src="assets/js/shell.js" defer></script>
</body>
</html>
