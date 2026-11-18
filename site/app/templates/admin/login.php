<?php /** Вход. Переменные: $error, $login */ ?>
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"><base href="/"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Вход · Админка Платформы</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/admin.css">
</head>
<body class="ad ad-login">
<form class="ad-card" method="post" action="/admin/login">
  <a class="ad-logo"><b>ПЛАТФОРМА</b><i></i></a>
  <h1>Вход для менеджеров</h1>
  <?php if ($error): ?><p class="ad-err" role="alert"><?= pn_e($error) ?></p><?php endif; ?>
  <?= csrf_field() ?>
  <label>Логин<input name="login" value="<?= pn_e($login) ?>" autocomplete="username" required autofocus></label>
  <label>Пароль<input name="password" type="password" autocomplete="current-password" required></label>
  <button class="ad-btn red">Войти</button>
</form>
</body>
</html>
