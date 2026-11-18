<?php /** Каркас админки. Переменные: $title, $user, $active, $flash, $content */
$nav = ['leads' => 'Заявки', 'apartments' => 'Квартиры', 'complexes' => 'ЖК', 'developers' => 'Застройщики', 'houses' => 'Дома', 'reviews' => 'Отзывы',
    'settings' => 'Настройки', 'users' => 'Менеджеры'];
$secs = pn_admin_sections(); ?>
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title><?= pn_e($title) ?> · Админка Платформы</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/admin.css">
</head>
<body class="ad">
<aside class="ad-side">
  <a class="ad-logo" href="/admin/"><b>ПЛАТФОРМА</b><i></i></a>
  <nav><?php foreach ($nav as $k => $t): if (!isset($secs[$k]) || ($secs[$k][1] === 'admin' && ($user['role'] ?? '') !== 'admin')) continue; ?>
    <a href="/admin/<?= $k ?>"<?= $active === $k ? ' aria-current="page"' : '' ?>><?= $t ?></a><?php endforeach; ?></nav>
  <div class="ad-me"><span><?= pn_e($user['login'] ?? '') ?> · <?= ($user['role'] ?? '') === 'admin' ? 'администратор' : 'менеджер' ?></span><a href="/admin/logout">Выйти</a> · <a href="/" target="_blank">Сайт</a></div>
</aside>
<main class="ad-main">
  <h1><?= pn_e($title) ?></h1>
  <?php if ($flash): ?><p class="ad-flash" role="status"><?= pn_e($flash) ?></p><?php endif; ?>
  <?= $content ?>
</main>
<script src="/assets/js/admin.js" defer></script>
</body>
</html>
