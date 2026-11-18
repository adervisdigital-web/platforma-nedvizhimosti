<?php /** Форма записи. Переменные: $E (fields, one, publish, copy), $ent, $id, $row, $vals, $errors, $secret_set? */
$secret_set = $secret_set ?? [];
$action = $ent === 'settings' ? '/admin/settings' : "/admin/$ent/" . ($id ?: 'new'); ?>
<?php if (!empty($errors['_'])): ?><p class="ad-err" role="alert"><?= pn_e($errors['_']) ?></p><?php endif; ?>
<?php if ($errors): ?><p class="ad-err" role="alert">Проверьте отмеченные поля.</p><?php endif; ?>
<form class="ad-form" method="post" action="<?= $action ?>" enctype="multipart/form-data" novalidate>
  <?= csrf_field() ?><input type="hidden" name="do" value="save">
<?php foreach ($E['fields'] as $n => $f):
    $v = $vals[$n] ?? ''; $bad = isset($errors[$n]); $cls = trim((!empty($f['wide']) || in_array($f['type'], ['photos', 'textarea', 'lines', 'paras', 'pairs'], true) ? 'wide ' : '') . ($bad ? 'ad-bad' : '')); ?>
<?php if (!empty($f['sec'])): ?>  <h2 class="ad-sec"><?= pn_e($f['sec']) ?></h2>
<?php endif; ?>
  <div class="<?= $cls ?>">
  <?php if ($f['type'] === 'bool'): ?>
    <label class="ad-check"><input type="checkbox" name="<?= $n ?>" value="1"<?= $v ? ' checked' : '' ?>> <?= pn_e($f['label']) ?></label>
  <?php elseif ($f['type'] === 'select'): ?>
    <label><?= pn_e($f['label']) ?><select name="<?= $n ?>"><option value="">—</option><?php foreach ($f['opts'] as $k => $t): ?>
      <option value="<?= pn_e((string) $k) ?>"<?= (string) $k === (string) $v ? ' selected' : '' ?>><?= pn_e($t) ?></option><?php endforeach; ?></select></label>
  <?php elseif (in_array($f['type'], ['textarea', 'lines', 'paras', 'pairs'], true)): ?>
    <label><?= pn_e($f['label']) ?><textarea name="<?= $n ?>" rows="<?= $f['type'] === 'paras' ? 8 : 5 ?>"><?= pn_e((string) $v) ?></textarea></label>
  <?php elseif ($f['type'] === 'photos'): $up = $n === 'photos' ? 'upload' : $n . '_upload'; ?>
    <span class="lbl"><?= pn_e($f['label']) ?></span>
    <div class="ad-photos<?= $n === 'photos' ? ' cov' : '' ?><?= $n === 'plans' ? ' pl' : '' ?>" data-sortable><?php foreach (array_values((array) $v) as $pi => $ph): ?>
      <figure><img <?= pn_img_attrs(($ent === 'houses' ? 'houses/' : '') . $ph, '140px') ?> alt=""><input type="hidden" name="<?= $n ?>[]" value="<?= pn_e($ph) ?>">
        <figcaption><button type="button" class="ad-ico" data-move="-1" aria-label="Левее" title="Левее">‹</button><button type="button" class="ad-ico" data-move="1" aria-label="Правее" title="Правее">›</button>
        <label class="ad-del" title="Удалить при сохранении"><input type="checkbox" name="<?= $n ?>_del[]" value="<?= pn_e($ph) ?>"> удалить</label></figcaption></figure><?php endforeach; ?></div>
    <label class="ad-drop"><span class="ad-drop-t">Перетащите фото сюда</span><span class="ad-btn sm">Выбрать файлы</span><small>JPG, PNG, WebP до 25 МБ · сожмутся сами</small><input class="ad-vh" type="file" name="<?= $up ?>[]" accept="image/jpeg,image/png,image/webp" multiple></label>
  <?php else: ?>
    <label><?= pn_e($f['label']) ?><input name="<?= $n ?>" value="<?= pn_e((string) $v) ?>"<?= $f['type'] === 'secret' ? ' type="password" autocomplete="new-password" placeholder="' . (isset($secret_set[$n]) ? 'задан — оставьте пустым, чтобы не менять' : 'не задан') . '"' : '' ?><?= in_array($f['type'], ['int', 'number'], true) ? ' inputmode="decimal"' : '' ?>></label>
  <?php endif; ?>
  <?php if (!empty($f['hint'])): ?><small class="ad-hint"><?= pn_e($f['hint']) ?></small><?php endif; ?>
  <?php if ($bad): ?><small><?= pn_e($errors[$n]) ?></small><?php endif; ?>
  </div>
<?php endforeach; ?>
  <div class="wide ad-save"><button class="ad-btn red">Сохранить</button><?php if ($ent !== 'settings'): ?><a class="ad-btn ghost" href="/admin/<?= $ent ?>">К списку</a><?php endif; ?></div>
</form>
<?php if ($row): ?>
<div class="ad-row-act ad-after">
  <?php if (!empty($E['publish'])): ?><form method="post" action="<?= $action ?>"><?= csrf_field() ?><input type="hidden" name="do" value="<?= $row['published'] ? 'unpublish' : 'publish' ?>"><button class="ad-btn"><?= $row['published'] ? 'Снять с сайта' : 'Опубликовать' ?></button></form><?php endif; ?>
  <?php if (!empty($E['copy'])): ?><form method="post" action="<?= $action ?>"><?= csrf_field() ?><input type="hidden" name="do" value="copy"><button class="ad-btn">Копировать</button></form><?php endif; ?>
  <?php if ($ent === 'apartments' && $row['published']): ?><a class="ad-btn ghost" href="/kvartiry/<?= pn_e($row['slug']) ?>/" target="_blank">Открыть на сайте</a><?php endif; ?>
  <?php if ($ent === 'houses' && $row['published']): ?><a class="ad-btn ghost" href="/doma/<?= pn_e($row['slug']) ?>/" target="_blank">Открыть на сайте</a><?php endif; ?>
  <form method="post" action="<?= $action ?>" data-confirm="Удалить безвозвратно?"><?= csrf_field() ?><input type="hidden" name="do" value="delete"><button class="ad-btn ghost">Удалить</button></form>
</div>
<?php endif; ?>
