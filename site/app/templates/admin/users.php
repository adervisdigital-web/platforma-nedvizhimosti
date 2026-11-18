<?php /** Менеджеры. Переменные: $rows, $user */ ?>
<table class="ad-t"><thead><tr><th>Логин</th><th>Роль</th><th>Добавлен</th><th></th></tr></thead><tbody>
<?php foreach ($rows as $r): ?>
<tr><td><b><?= pn_e($r['login']) ?></b></td><td><span class="ad-pill<?= $r['role'] === 'admin' ? ' on' : '' ?>"><?= $r['role'] === 'admin' ? 'администратор' : 'менеджер' ?></span></td><td><?= pn_e(substr($r['created_at'], 0, 10)) ?></td>
<td class="ad-row-act">
  <form method="post"><?= csrf_field() ?><input type="hidden" name="do" value="reset"><input type="hidden" name="id" value="<?= $r['id'] ?>"><button class="ad-btn sm">Новый пароль</button></form>
  <?php if ((int) $r['id'] !== (int) $user['id']): ?><form method="post" data-confirm="Удалить менеджера <?= pn_e($r['login']) ?>?"><?= csrf_field() ?><input type="hidden" name="do" value="delete"><input type="hidden" name="id" value="<?= $r['id'] ?>"><button class="ad-btn sm ghost">Удалить</button></form><?php endif; ?>
</td></tr>
<?php endforeach; ?></tbody></table>
<form class="ad-inline ad-panel" method="post"><h2 class="ad-sec">Новый менеджер</h2><?= csrf_field() ?><input type="hidden" name="do" value="add">
  <label>Логин<input name="login" required minlength="3" maxlength="40"></label>
  <label>Роль<select name="role"><option value="manager">менеджер</option><option value="admin">администратор</option></select></label>
  <button class="ad-btn red">Добавить</button>
</form>
<p class="ad-hint">Пароль создаётся автоматически и показывается один раз.</p>
