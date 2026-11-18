<?php /** Главная: куски прототипа по порядку + данные + app.js. Переменные: $order, $base_tag, $data_json, $demo */
include __DIR__ . '/head.php';
foreach ($order as $part) include __DIR__ . '/' . $part . '.php';
include __DIR__ . '/libs.php';
if (isset($data_json)): ?>
<script id="pn-data" type="application/json"><?= $data_json ?></script>
<script src="assets/js/data.js"></script>
<?php endif; ?>
<script src="assets/js/app.js"></script>
<?php include __DIR__ . '/tail.php';
