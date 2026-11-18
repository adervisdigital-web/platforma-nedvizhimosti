<?php /** Список записей раздела. Переменные: $E, $ent, $rows, $q */
$fmt = function (string $col, array $r) use ($ent) {
    $v = $r[$col] ?? '';
    if ($col === 'complex') return pn_e($r['complex'] ?? $r['address'] ?? '');
    if ($col === 'price') return pn_rub((int) $v);
    if ($col === 'area') return pn_e(str_replace('.', ',', (string) pn_num($v)));
    if (in_array($col, ['published', 'verified', 'is_demo'], true)) return $v ? '<span class="st-new">да</span>' : '<span class="st-closed">нет</span>';
    return pn_e((string) $v);
}; ?>
<form class="ad-bar" method="get">
  <label>Поиск<input name="q" value="<?= pn_e($q) ?>" placeholder="название, адрес, район"></label>
  <button class="ad-btn">Найти</button>
  <a class="ad-btn red" href="/admin/<?= $ent ?>/new">Добавить</a>
</form>
<?php if (!$rows): ?><p class="ad-hint">Ничего не найдено.</p><?php else: ?>
<table class="ad-t"><thead><tr><?php foreach ($E['cols'] as $c => $t): ?><th><?= pn_e($t) ?></th><?php endforeach; ?><th></th></tr></thead><tbody>
<?php foreach ($rows as $r): ?>
<tr><?php foreach ($E['cols'] as $c => $t): ?><td><?= $fmt($c, $r) ?></td><?php endforeach; ?>
<td><a class="ad-btn sm" href="/admin/<?= $ent ?>/<?= (int) $r['id'] ?>">Открыть</a></td></tr>
<?php endforeach; ?></tbody></table>
<?php endif; ?>
