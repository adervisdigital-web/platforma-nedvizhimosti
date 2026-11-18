<?php /** Вход. Переменные: $error, $login */ ?>
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"><base href="/"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Вход · Админка Платформы</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 76 72'%3E%3Cpath fill='%230E0E0F' d='M0 72V24A24 24 0 0 1 48 24V72H33V26A9 9 0 0 0 15 26V72Z'/%3E%3Ccircle cx='67' cy='63' r='9' fill='%23F5553C'/%3E%3C/svg%3E">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/admin.css">
</head>
<body class="ad ad-login">
<form class="ad-card" method="post" action="/admin/login">
  <a class="ad-logo" href="/" aria-label="На сайт"><svg viewBox="0 0 76 72" aria-hidden="true"><path fill="currentColor" d="M0 72V24A24 24 0 0 1 48 24V72H33V26A9 9 0 0 0 15 26V72Z"/><circle cx="67" cy="63" r="9" fill="#F5553C"/></svg><span><b>ПЛАТФОРМА</b><small>недвижимости</small></span></a>
  <h1>Вход для менеджеров</h1>
  <?php if ($error): ?><p class="ad-err" role="alert"><?= pn_e($error) ?></p><?php endif; ?>
  <?= csrf_field() ?>
  <label>Логин<input name="login" value="<?= pn_e($login) ?>" autocomplete="username" required autofocus></label>
  <label>Пароль<input name="password" type="password" autocomplete="current-password" required></label>
  <button class="ad-btn red">Войти</button>
  <p class="ad-hint">Забыли пароль — попросите администратора выдать новый.</p>
</form>
</body>
</html>
