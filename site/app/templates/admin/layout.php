<?php /** Каркас админки. Переменные: $title, $user, $active, $flash, $content */
$nav = ['overview' => 'Обзор', 'leads' => 'Заявки', 'apartments' => 'Квартиры', 'complexes' => 'ЖК', 'developers' => 'Застройщики', 'houses' => 'Дома', 'reviews' => 'Отзывы',
    'feeds' => 'Выгрузки', 'settings' => 'Настройки', 'users' => 'Менеджеры'];
$ico = [
    'overview' => '<rect x="3.5" y="3.5" width="7" height="9" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="5" rx="1.5"/><rect x="3.5" y="15.5" width="7" height="5" rx="1.5"/><rect x="13.5" y="11.5" width="7" height="9" rx="1.5"/>',
    'leads' => '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    'apartments' => '<path d="M5 21V4h10v17M15 9h4v12M3 21h18M8.5 8h3M8.5 12h3M8.5 16h3"/>',
    'complexes' => '<path d="M3 21V9l6-3v15M9 21V3l12 4v14M3 21h18M13 9h4M13 13h4M13 17h4"/>',
    'developers' => '<path d="M4 17a8 8 0 0 1 16 0M2 17h20v3H2zM10 9V5h4v4"/>',
    'houses' => '<path d="M3 11l9-7 9 7M5 9.5V21h14V9.5M10 21v-6h4v6"/>',
    'reviews' => '<path d="M12 3.5l2.6 5.3 5.8.8-4.2 4.1 1 5.8L12 16.8l-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/>',
    'feeds' => '<path d="M12 3v11M7.5 9.5L12 14l4.5-4.5M4 15v4.5h16V15"/>',
    'settings' => '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
    'users' => '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.6a3.5 3.5 0 0 1 0 6.8M17.5 14a6 6 0 0 1 4 6"/>',
];
try { $newN = (int) pn_db()->query("select count(*) from leads where status = 'new'")->fetchColumn(); } catch (Throwable $e) { $newN = 0; }
$secs = pn_admin_sections(); ?>
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"><base href="/"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title><?= pn_e($title) ?> · Админка Платформы</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 76 72'%3E%3Cpath fill='%230E0E0F' d='M0 72V24A24 24 0 0 1 48 24V72H33V26A9 9 0 0 0 15 26V72Z'/%3E%3Ccircle cx='67' cy='63' r='9' fill='%23F5553C'/%3E%3C/svg%3E">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/admin.css">
</head>
<body class="ad">
<aside class="ad-side">
  <a class="ad-logo" href="/admin/" aria-label="Админка Платформы"><svg viewBox="0 0 76 72" aria-hidden="true"><path fill="currentColor" d="M0 72V24A24 24 0 0 1 48 24V72H33V26A9 9 0 0 0 15 26V72Z"/><circle cx="67" cy="63" r="9" fill="#F5553C"/></svg><span><b>ПЛАТФОРМА</b><small>админка</small></span></a>
  <nav><?php foreach ($nav as $k => $t): if (!isset($secs[$k]) || ($secs[$k][1] === 'admin' && ($user['role'] ?? '') !== 'admin')) continue; ?>
    <a href="/admin/<?= $k ?>"<?= $active === $k ? ' aria-current="page"' : '' ?>><svg viewBox="0 0 24 24" aria-hidden="true"><?= $ico[$k] ?? '' ?></svg><span><?= $t ?></span><?php if ($k === 'leads' && $newN): ?><em title="Новых заявок"><?= $newN ?></em><?php endif; ?></a><?php endforeach; ?></nav>
  <div class="ad-me"><span class="ad-av"><?= pn_e(mb_strtoupper(mb_substr($user['login'] ?? '?', 0, 1))) ?></span><span><b><?= pn_e($user['login'] ?? '') ?></b><small><?= ($user['role'] ?? '') === 'admin' ? 'администратор' : 'менеджер' ?></small></span>
    <span class="ad-me-a"><a href="/" target="_blank">Сайт ↗</a><a href="/admin/password">Пароль</a><form method="post" action="/admin/logout" class="ad-out"><?= csrf_field() ?><button type="submit">Выйти</button></form></span></div>
</aside>
<main class="ad-main">
  <h1><?= pn_e($title) ?></h1>
  <?php if (!empty($_SESSION['weak']) && $active !== 'password'): ?><p class="ad-flash ad-warn" role="status">Пароль ненадёжный — <a href="/admin/password">смените его</a>, это займёт минуту.</p><?php endif; ?>
  <?php if ($flash): ?><p class="ad-flash" role="status"><?= pn_e($flash) ?></p><?php endif; ?>
  <?= $content ?>
</main>
<script src="/assets/js/admin.js" defer></script>
</body>
</html>
