<?php /** Заявки. Переменные: $rows, $stf, $counts, $deliv ['tg' => bool, 'mail' => bool] */
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
<?php if (!$rows && $stf): ?><div class="ad-empty"><p>В этом статусе заявок нет.</p><a class="ad-btn" href="/admin/leads">Все заявки</a></div>
<?php elseif (!$rows): ?><div class="ad-empty ad-onb">
  <div class="ad-onb-ic" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/></svg></div>
  <h2>Заявок пока нет</h2>
  <p>Как только клиент оставит телефон на сайте, заявка появится здесь, а менеджер получит уведомление.</p>
  <ol class="ad-steps">
    <li><b>Клиент</b> оставляет телефон: подбор, «перезвоните», запись на просмотр</li>
    <li><b>Заявка</b> сохраняется здесь — даже если Telegram и почта недоступны</li>
    <li><b>Менеджер</b> получает уведомление и отмечает статус: в работе, закрыта</li>
  </ol>
  <div class="ad-deliv">
    <span class="ad-pill<?= $deliv['tg'] ? ' on' : '' ?>">Telegram <?= $deliv['tg'] ? 'подключён' : 'не подключён' ?></span>
    <span class="ad-pill<?= $deliv['mail'] ? ' on' : '' ?>">Почта <?= $deliv['mail'] ? 'подключена' : 'не подключена' ?></span>
    <?php if (!$deliv['tg'] || !$deliv['mail']): ?><a class="ad-btn red sm" href="/admin/settings">Подключить уведомления</a><?php endif; ?>
    <a class="ad-btn sm" href="/" target="_blank">Открыть сайт ↗</a>
  </div>
</div><?php else: ?>
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
