<?php /** Смена своего пароля. Переменные: $error, $user */ ?>
<form method="post" class="ad-form ad-pass" autocomplete="off">
  <?= csrf_field() ?>
  <?php if ($error): ?><p class="ad-err" role="alert"><?= pn_e($error) ?></p><?php endif; ?>
  <input type="text" name="username" value="<?= pn_e($user['login'] ?? '') ?>" autocomplete="username" hidden>
  <label class="ad-f"><span>Текущий пароль</span><input type="password" name="old" autocomplete="current-password" required></label>
  <label class="ad-f"><span>Новый пароль</span><input type="password" name="new" autocomplete="new-password" minlength="10" required>
    <small>Не короче 10 символов и без логина. Удобно: три-четыре слова через дефис, например «окно-берёза-кран-48».</small></label>
  <label class="ad-f"><span>Новый пароль ещё раз</span><input type="password" name="new2" autocomplete="new-password" minlength="10" required></label>
  <button class="ad-btn red" type="submit">Сменить пароль</button>
</form>
