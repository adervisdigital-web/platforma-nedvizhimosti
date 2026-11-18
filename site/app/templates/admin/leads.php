<?php /** Заявки. Переменные: $rows, $stf, $counts */
$ru = ['new' => 'новая', 'work' => 'в работе', 'closed' => 'закрыта'];
$undel = count(array_filter($rows, 'lead_undelivered')); ?>
<form class="ad-bar" method="get">
  <a class="ad-btn<?= $stf === '' ? ' red' : '' ?>" href="/admin/leads">Все (<?= array_sum($counts) ?>)</a>
  <?php foreach ($ru as $k => $t): ?><a class="ad-btn<?= $stf === $k ? ' red' : '' ?>" href="/admin/leads?st=<?= $k ?>"><?= ucfirst($t) ?> (<?= (int) ($counts[$k] ?? 0) ?>)</a><?php endforeach; ?>
  <a class="ad-btn ghost" href="/admin/leads/csv">Скачать CSV</a>
</form>
<?php if ($undel): ?><form method="post" class="ad-flash"><?= csrf_field() ?><input type="hidden" name="do" value="retry">Не доставлено в Telegram или на почту: <?= $undel ?>. <button class="ad-btn sm">Отправить ещё раз</button></form><?php endif; ?>
<?php if (!$rows): ?><p class="ad-hint">Заявок пока нет.</p><?php else: ?>
<table class="ad-t"><thead><tr><th>№ / когда</th><th>Телефон</th><th>Что ищет</th><th>Статус и заметка</th></tr></thead><tbody>
<?php foreach ($rows as $l): $ts = (new DateTime($l['created_at'], new DateTimeZone('UTC')))->setTimezone(new DateTimeZone(date_default_timezone_get())); ?>
<tr>
  <td>№<?= $l['id'] ?><br><small class="ad-hint"><?= $ts->format('d.m H:i') ?></small><?php if (lead_undelivered($l)): ?><br><span class="ad-undel">не доставлена</span><?php endif; ?></td>
  <td><a href="tel:<?= pn_e($l['phone']) ?>"><b><?= pn_e(phone_pretty($l['phone'])) ?></b></a><br><?= pn_e($l['name']) ?></td>
  <td><b><?= pn_e(lead_kind_ru($l['kind'])) ?></b><?= $l['want'] && $l['want'] !== lead_kind_ru($l['kind']) ? ' · ' . pn_e($l['want']) : '' ?><br>
    <small class="ad-hint"><?= pn_e(implode(' · ', array_filter([$l['budget'], $l['area'], $l['slot']]))) ?></small>
    <?php if ($l['object_ref']): ?><br><small><?= preg_match('~^(kvartiry|doma)/~', $l['object_ref']) ? '<a href="/' . pn_e(rtrim($l['object_ref'], '/')) . '/" target="_blank">' . pn_e($l['object_ref']) . '</a>' : pn_e($l['object_ref']) ?></small><?php endif; ?></td>
  <td><form method="post" action="/admin/leads/<?= $l['id'] ?><?= $stf ? '?st=' . $stf : '' ?>" class="ad-inline" style="margin:0"><?= csrf_field() ?><input type="hidden" name="do" value="status">
    <select name="status" class="st-<?= $l['status'] ?>"><?php foreach ($ru as $k => $t): ?><option value="<?= $k ?>"<?= $l['status'] === $k ? ' selected' : '' ?>><?= $t ?></option><?php endforeach; ?></select>
    <input name="note" value="<?= pn_e($l['note']) ?>" placeholder="заметка" style="min-width:180px;flex:1"><button class="ad-btn sm">Сохранить</button></form></td>
</tr>
<?php endforeach; ?></tbody></table>
<?php endif; ?>
