<?php
// Приём заявки: проверки → сохранение в базу (до любой отправки) → доставка (задача 13).
const PN_LEAD_KINDS = ['quiz', 'callback', 'viewing', 'chat'];
const PN_LEAD_RATE = 5, PN_LEAD_MIN_SECONDS = 3;

function lead_messages(array $s): array {
    $tel = $s['phone'] ?? '+7 965 500-29-18';
    return [
        'ok' => 'Заявка принята, перезвоним до ' . ($s['hours_to'] ?? '21:00'),
        'consent' => 'Отметьте согласие на обработку персональных данных',
        'phone' => 'Проверьте номер: нужен российский номер, 10 цифр после +7',
        'rate' => "Слишком много заявок подряд — позвоните нам: $tel",
        'too_fast' => "Форма отправлена слишком быстро — попробуйте ещё раз или позвоните: $tel",
        'bot' => 'Заявка не принята', 'kind' => 'Неизвестный тип заявки',
    ];
}

// $in — поля формы; $ip — адрес; $now — текущее время (unix). Возвращает ['ok', 'id'?, 'error'?, 'message', 'ics'?]
function lead_accept(array $in, string $ip, int $now): array {
    $s = Repo::settingsAll(); $M = lead_messages($s);
    $fail = fn(string $e) => ['ok' => false, 'error' => $e, 'message' => $M[$e]];
    $kind = (string) ($in['kind'] ?? '');
    if (!in_array($kind, PN_LEAD_KINDS, true)) return $fail('kind');
    if (trim((string) ($in['hp'] ?? '')) !== '') return $fail('bot');                 // ловушка заполнена — бот
    if (empty($in['consent'])) return $fail('consent');
    $t0 = (int) ($in['t0'] ?? 0);
    if ($t0 <= 0 || $now - $t0 < PN_LEAD_MIN_SECONDS) return $fail('too_fast');
    $phone = phone_norm((string) ($in['phone'] ?? ''));
    if (!$phone) return $fail('phone');
    $ipHash = hash('sha256', $ip . ($s['salt'] ?? ''));
    $st = pn_db()->prepare("select count(*) from leads where ip_hash = ? and created_at > ?");
    $st->execute([$ipHash, gmdate('Y-m-d H:i:s', $now - 3600)]);
    if ((int) $st->fetchColumn() >= PN_LEAD_RATE) return $fail('rate');
    $cut = fn($k, $n = 200) => mb_substr(trim(strip_tags((string) ($in[$k] ?? ''))), 0, $n);
    pn_db()->prepare('insert into leads(created_at, kind, want, budget, area, name, phone, object_ref, slot, ip_hash) values (?,?,?,?,?,?,?,?,?,?)')
        ->execute([gmdate('Y-m-d H:i:s', $now), $kind, $cut('want'), $cut('budget'), $cut('area'), $cut('name', 80), $phone, $cut('object_ref'), $cut('slot', 40), $ipHash]);
    $id = (int) pn_db()->lastInsertId();
    if (function_exists('deliver_lead')) { try { deliver_lead($id); } catch (Throwable $e) { /* заявка уже в базе; повтор — deliver_pending */ } }
    $out = ['ok' => true, 'id' => $id, 'message' => $M['ok']];
    if ($kind === 'viewing' && ($ics = lead_ics($cut('slot', 40), $cut('object_ref'), $s))) $out['ics'] = $ics;
    return $out;
}

// Файл календаря для записи на просмотр. Слот — местное время «ГГГГ-ММ-ДД ЧЧ:ММ».
function lead_ics(string $slot, string $ref, array $s): ?string {
    $t = DateTime::createFromFormat('Y-m-d H:i', $slot, new DateTimeZone(date_default_timezone_get()));
    if (!$t) return null;
    $u = fn(DateTime $d) => (clone $d)->setTimezone(new DateTimeZone('UTC'))->format('Ymd\THis\Z');
    $end = (clone $t)->modify('+1 hour');
    return implode("\r\n", ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Platforma//RU', 'BEGIN:VEVENT', 'UID:' . bin2hex(random_bytes(6)) . '@' . ($s['domain'] ?? 'p.forma196.ru'),
        'DTSTAMP:' . gmdate('Ymd\THis\Z'), 'DTSTART:' . $u($t), 'DTEND:' . $u($end), 'SUMMARY:Просмотр — Платформа недвижимости',
        'DESCRIPTION:' . ($ref ? "Объект: $ref. " : '') . 'Телефон менеджера ' . ($s['phone'] ?? ''), 'END:VEVENT', 'END:VCALENDAR']);
}
