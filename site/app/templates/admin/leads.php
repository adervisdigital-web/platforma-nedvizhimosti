<?php /** Заявки. Переменные: $rows, $stf, $counts */
$ru = ['new' => 'новая', 'work' => 'в работе', 'closed' => 'закрыта'];
$tabs = ['new' => 'Новые', 'work' => 'В работе', 'closed' => 'Закрыты'];
$undel = count(array_filter($rows, 'lead_undelivered'));
$tz = new DateTimeZone(date_default_timezone_get()); $today = (new DateTime('now', $tz))->format('Y-m-d'); ?>
<div class="ad-stats">
  <a class="ad-stat<?= $stf === '' ? ' cur' : '' ?>" href="/admin/leads"><b><?= array_sum($counts) ?></b><span>Все заявки</span></a>
  <?php foreach ($tabs as $k => $t): ?><a class="ad-stat st-<?= $k ?><?= $stf === $k ? ' cur' : '' ?>" href="/admin/leads?st=<?= $k ?>"><b><?= (int) ($counts[$k] ?? 0) ?></b><span><?= $t ?></span></a><?php endforeach; ?>
  <a class="ad-stat ad-csv" href="/admin/leads/csv"><b>CSV</b><span>Скачать для Excel</span></a>
</div>
<?php if ($undel): ?><form method="post" class="ad-flash ad-warn"><?= csrf_field() ?><input type="hidden" name="do" value="retry"><span>Не доставлено в Telegram или на почту: <b><?= $undel ?></b>. Проверьте настройки доставки.</span> <button class="ad-btn sm">Отправить ещё раз</button></form><?php endif; ?>
<?php if (!$rows): ?><div class="ad-empty"><p><?= $stf ? 'В этом статусе заявок нет.' : 'Заявок пока нет. Они появятся здесь, как только клиент оставит телефон на сайте.' ?></p></div><?php else: ?>
<table class="ad-t ad-leads"><thead><tr><th>Заявка</th><th>Клиент</th><th>Что ищет</th><th>Статус и заметка</th></tr></thead><tbody>
<?php foreach ($rows as $l): $ts = (new DateTime($l['created_at'], new DateTimeZone('UTC')))->setTimezone($tz);
    $when = $ts->format('Y-m-d') === $today ? 'сегодня, ' . $ts->format('H:i') : $ts->format('d.m, H:i'); ?>
<tr class="ld-<?= $l['status'] ?>">
  <td><b class="ad-nw">№<?= $l['id'] ?></b><br><small class="ad-hint"><?= $when ?></small><?php if (lead_undelivered($l)): ?><br><span class="ad-undel">не доставлена</span><?php endif; ?></td>
  <td><a class="ad-phone" href="tel:<?= pn_e($l['phone']) ?>"><?= pn_e(phone_pretty($l['phone'])) ?></a><?php if ($l['name']): ?><br><?= pn_e($l['name']) ?><?php endif; ?></td>
  <td><span class="ad-kind k-<?= pn_e($l['kind']) ?>"><?= pn_e(lead_kind_ru($l['kind'])) ?></span><?= $l['want'] && $l['want'] !== lead_kind_ru($l['kind']) ? ' <b>' . pn_e($l['want']) . '</b>' : '' ?>
    <?php $det = implode(' · ', array_filter([$l['budget'], $l['area'], $l['slot']])); if ($det): ?><br><small class="ad-hint"><?= pn_e($det) ?></small><?php endif; ?>
    <?php if ($l['object_ref']): ?><br><small><?= preg_match('~^(kvartiry|doma)/~', $l['object_ref']) ? '<a href="/' . pn_e(rtrim($l['object_ref'], '/')) . '/" target="_blank">' . pn_e($l['object_ref']) . ' ↗</a>' : pn_e($l['object_ref']) ?></small><?php endif; ?></td>
  <td><form method="post" action="/admin/leads/<?= $l['id'] ?><?= $stf ? '?st=' . $stf : '' ?>" class="ad-lf"><?= csrf_field() ?><input type="hidden" name="do" value="status">
    <select name="status" class="ad-st st-<?= $l['status'] ?>" aria-label="Статус заявки №<?= $l['id'] ?>"><?php foreach ($ru as $k => $t): ?><option value="<?= $k ?>"<?= $l['status'] === $k ? ' selected' : '' ?>><?= $t ?></option><?php endforeach; ?></select>
    <input name="note" value="<?= pn_e($l['note']) ?>" placeholder="Заметка: о чём договорились" aria-label="Заметка к заявке №<?= $l['id'] ?>"><button class="ad-btn sm">Сохранить</button></form></td>
</tr>
<?php endforeach; ?></tbody></table>
<?php endif; ?>
