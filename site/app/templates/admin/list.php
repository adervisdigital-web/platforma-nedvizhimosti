<?php /** Список записей раздела. Переменные: $E, $ent, $rows, $q */
$fmt = function (string $col, array $r) use ($ent) {
    $v = $r[$col] ?? '';
    if ($col === 'photo') {
        $ph = json_decode((string) ($r['photos'] ?? '[]'), true)[0] ?? null;
        return $ph ? '<img class="ad-thumb" ' . pn_img_attrs(($ent === 'houses' ? 'houses/' : '') . $ph, '96px') . ' alt="" loading="lazy">' : '<span class="ad-thumb"></span>';
    }
    if ($col === 'complex') return '<b>' . pn_e($r['complex'] ?? $r['address'] ?? '') . '</b>' . (!empty($r['district']) ? '<br><small class="ad-hint">' . pn_e($r['district']) . '</small>' : '');
    if ($col === 'name' || $col === 'line') return '<b>' . pn_e((string) $v) . '</b>';
    if ($col === 'rooms' && $ent === 'apartments') return (int) $v === 0 ? 'студия' : (int) $v . '-комн.';
    if ($col === 'price') return '<b class="ad-nw">' . pn_rub((int) $v) . '</b>';
    if ($col === 'area') return pn_e(str_replace('.', ',', (string) pn_num($v))) . ($v !== '' && $v !== null ? ' м²' : '');
    if ($col === 'published') return $v ? '<span class="ad-pill on">на сайте</span>' : '<span class="ad-pill">скрыт</span>';
    if ($col === 'verified') return $v ? '<span class="ad-pill on">проверен</span>' : '<span class="ad-pill">нет</span>';
    if ($col === 'is_demo') return $v ? '<span class="ad-pill demo">демо</span>' : '';
    if ($col === 'last_status') return $v === null || $v === '' ? '<span class="ad-hint">ещё не загружалась</span>' : (str_starts_with((string) $v, 'Ошибка') ? '<span class="ad-pill">ошибка</span> ' : '') . pn_e(mb_strimwidth((string) $v, 0, 140, '…')) . (!empty($r['last_run_at']) ? '<br><small class="ad-hint">' . pn_e(date('d.m.Y H:i', strtotime($r['last_run_at'] . ' UTC'))) . '</small>' : '');
    if ($col === 'site' && $v) return '<a href="' . pn_e(preg_match('~^https?://~', $v) ? $v : 'https://' . $v) . '" target="_blank" rel="noopener">' . pn_e($v) . '</a>';
    return (string) $v === '' ? '<span class="ad-hint">—</span>' : pn_e((string) $v);
}; ?>
<?php if (!empty($E['intro'])): ?><p class="ad-hint ad-intro"><?= pn_e($E['intro']) ?></p><?php endif; ?>
<form class="ad-bar" method="get">
  <label class="ad-search"><span class="ad-vh">Поиск</span><input name="q" value="<?= pn_e($q) ?>" placeholder="Поиск: название, адрес, район" type="search"></label>
  <button class="ad-btn">Найти</button><?php if ($q !== ''): ?><a class="ad-btn ghost" href="/admin/<?= $ent ?>">Сбросить</a><?php endif; ?>
  <span class="ad-bar-sp"></span>
  <a class="ad-btn red" href="/admin/<?= $ent ?>/new">+ Добавить</a>
</form>
<?php if (!$rows): ?><div class="ad-empty"><p><?= $q !== '' ? 'Ничего не найдено.' : 'Здесь пока пусто.' ?></p><a class="ad-btn red" href="/admin/<?= $ent ?>/new">+ Добавить</a></div><?php else: ?>
<p class="ad-hint ad-count">Всего: <?= count($rows) ?></p>
<table class="ad-t ad-list"><thead><tr><?php foreach ($E['cols'] as $c => $t): ?><th class="c-<?= $c ?>"><?= pn_e($t) ?></th><?php endforeach; ?><th></th></tr></thead><tbody>
<?php foreach ($rows as $r): $href = "/admin/$ent/" . (int) $r['id']; ?>
<tr data-href="<?= $href ?>"><?php foreach ($E['cols'] as $c => $t): ?><td class="c-<?= $c ?>"<?= $t !== '' ? ' data-l="' . pn_e($t) . '"' : '' ?>><?= $fmt($c, $r) ?></td><?php endforeach; ?>
<td class="c-go"><a class="ad-btn sm" href="<?= $href ?>">Открыть</a></td></tr>
<?php endforeach; ?></tbody></table>
<?php endif; ?>
