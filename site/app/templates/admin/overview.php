<?php /** Обзор. Переменные: $days [Y-m-d => n], $stats, $check [[название, ok, что сделать, ссылка]], $recent, $log, $user */
$max = max(1, max($days)); $wd = ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'];
$okN = count(array_filter($check, fn($c) => $c[1]));
$act = ['create' => 'добавил(а)', 'update' => 'изменил(а)', 'delete' => 'удалил(а)', 'publish' => 'опубликовал(а)', 'unpublish' => 'снял(а) с сайта',
    'copy' => 'скопировал(а)', 'status' => 'обновил(а) статус', 'export' => 'выгрузил(а) CSV', 'reset_password' => 'выдал(а) новый пароль'];
$ent = ['apartments' => 'квартиру', 'complexes' => 'ЖК', 'developers' => 'застройщика', 'houses' => 'проект дома', 'reviews' => 'отзыв', 'leads' => 'заявку',
    'users' => 'менеджера', 'settings' => 'настройки'];
$href = ['apartments', 'complexes', 'developers', 'houses', 'reviews'];
$tz = new DateTimeZone(date_default_timezone_get());
$h = (int) (new DateTime('now', $tz))->format('G'); ?>
<p class="ad-hello"><?= $h < 5 ? 'Доброй ночи' : ($h < 12 ? 'Доброе утро' : ($h < 18 ? 'Добрый день' : 'Добрый вечер')) ?>, <?= pn_e($user['login']) ?>.
  <?= $stats['new'] ? 'Ждут ответа: <a href="/admin/leads?st=new"><b>' . $stats['new'] . ' ' . pn_plural($stats['new'], 'новая заявка', 'новые заявки', 'новых заявок') . '</b></a>.' : 'Новых заявок нет.' ?></p>

<div class="ad-kpi">
  <a class="ad-stat st-new" href="/admin/leads?st=new"><b><?= $stats['new'] ?></b><span>Новых заявок</span></a>
  <a class="ad-stat" href="/admin/leads"><b><?= $stats['week'] ?></b><span>Заявок за 7 дней</span></a>
  <a class="ad-stat" href="/admin/apartments"><b><?= $stats['apt'] ?></b><span>Квартир на сайте<?= $stats['apt_hidden'] ? ' · скрыто ' . $stats['apt_hidden'] : '' ?></span></a>
  <a class="ad-stat" href="/admin/houses"><b><?= $stats['houses'] ?></b><span>Проектов домов</span></a>
  <a class="ad-stat" href="/admin/reviews"><b><?= $stats['reviews'] ?></b><span>Отзывов<?= $stats['reviews_demo'] ? ' · демо ' . $stats['reviews_demo'] : '' ?></span></a>
</div>

<div class="ad-ov">
  <section class="ad-box ad-chart-box"><h2 class="ad-sec">Заявки за 14 дней</h2>
    <div class="ad-chart" role="img" aria-label="Заявок за 14 дней: <?= array_sum($days) ?>">
      <?php foreach ($days as $d => $c): $dt = new DateTime($d, $tz); ?>
      <div class="ad-bar-c<?= $dt->format('Y-m-d') === array_key_last($days) ? ' today' : '' ?>" title="<?= $dt->format('d.m') ?>: <?= $c ?>">
        <span class="ad-bar-v"><?= $c ?: '' ?></span><i style="height:<?= $c ? max(6, round($c / $max * 100)) : 2 ?>%"></i>
        <small><?= $dt->format('j') ?><br><?= $wd[(int) $dt->format('w')] ?></small></div>
      <?php endforeach; ?>
    </div>
    <?php if (!array_sum($days)): ?><p class="ad-hint">Пока заявок нет — график оживёт с первой заявкой с сайта.</p><?php endif; ?>
  </section>

  <section class="ad-box"><h2 class="ad-sec">Перед запуском <span class="ad-prog"><?= $okN ?> из <?= count($check) ?></span></h2>
    <div class="ad-progbar"><i style="width:<?= round($okN / count($check) * 100) ?>%"></i></div>
    <ul class="ad-check-l"><?php foreach ($check as [$t, $ok, $todo, $link]): ?>
      <li class="<?= $ok ? 'ok' : '' ?>"><i aria-hidden="true"></i><span><b><?= pn_e($t) ?></b><?php if (!$ok): ?><small><?= pn_e($todo) ?></small><?php endif; ?></span>
        <?php if (!$ok): ?><a class="ad-btn sm" href="<?= pn_e($link) ?>"<?= $link[1] === 'p' ? ' target="_blank"' : '' ?>>Открыть</a><?php endif; ?></li>
    <?php endforeach; ?></ul>
  </section>

  <section class="ad-box"><h2 class="ad-sec">Последние заявки <a class="ad-more" href="/admin/leads">Все →</a></h2>
    <?php if (!$recent): ?><p class="ad-hint">Заявок пока нет.</p><?php else: ?>
    <ul class="ad-mini"><?php foreach ($recent as $l): $ts = (new DateTime($l['created_at'], new DateTimeZone('UTC')))->setTimezone($tz); ?>
      <li class="ld-<?= $l['status'] ?>"><a href="/admin/leads<?= $l['status'] === 'new' ? '?st=new' : '' ?>"><b><?= pn_e(phone_pretty($l['phone'])) ?></b>
        <span><?= pn_e(lead_kind_ru($l['kind'])) ?><?= $l['name'] ? ' · ' . pn_e($l['name']) : '' ?></span></a><small><?= $ts->format('d.m H:i') ?></small></li>
    <?php endforeach; ?></ul><?php endif; ?>
  </section>

  <section class="ad-box"><h2 class="ad-sec">Журнал действий</h2>
    <?php if (!$log): ?><p class="ad-hint">Здесь появятся изменения: кто, что и когда поменял.</p><?php else: ?>
    <ul class="ad-log"><?php foreach ($log as $r): $ts = (new DateTime($r['at'], new DateTimeZone('UTC')))->setTimezone($tz);
        $what = match ($r['action']) {
            'export' => 'выгрузил(а) заявки в CSV',
            'status' => 'обновил(а) статус заявки №' . (int) $r['entity_id'],
            'reset_password' => 'выдал(а) новый пароль менеджеру',
            default => ($act[$r['action']] ?? $r['action']) . ' ' . ($ent[$r['entity']] ?? $r['entity']) . ($r['entity_id'] ? ' №' . (int) $r['entity_id'] : ''),
        }; ?>
      <li><span class="ad-av sm"><?= pn_e(mb_strtoupper(mb_substr($r['login'] ?? '?', 0, 1))) ?></span>
        <span><b><?= pn_e($r['login'] ?? 'система') ?></b> <?= in_array($r['entity'], $href, true) && $r['entity_id'] && $r['action'] !== 'delete'
          ? '<a href="/admin/' . $r['entity'] . '/' . (int) $r['entity_id'] . '">' . pn_e($what) . '</a>' : pn_e($what) ?></span><small><?= $ts->format('d.m H:i') ?></small></li>
    <?php endforeach; ?></ul><?php endif; ?>
  </section>
</div>
