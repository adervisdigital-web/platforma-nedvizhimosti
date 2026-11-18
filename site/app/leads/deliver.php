<?php
// Доставка заявок: Telegram, почта, CRM. Флаги в leads.delivered_*: 0 — не доставлено (повторим), 1 — доставлено, 2 — канал выключен.
interface LeadChannel {
    public function key(): string;                 // tg | mail | crm
    public function enabled(array $s): bool;
    public function send(array $lead, array $s): bool;
}

// Внешние вызовы — через подменяемые функции (тесты подставляют свои).
function pn_http(string $method, string $url, array $headers, string $body): array {
    if (isset($GLOBALS['PN_HTTP'])) return ($GLOBALS['PN_HTTP'])($method, $url, $headers, $body);
    $ch = curl_init($url);
    curl_setopt_array($ch, [CURLOPT_CUSTOMREQUEST => $method, CURLOPT_POSTFIELDS => $body, CURLOPT_HTTPHEADER => $headers, CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 5, CURLOPT_TIMEOUT => 10]);
    $out = curl_exec($ch); $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE); curl_close($ch);
    return [$out === false ? 0 : $code, (string) $out];
}
function pn_mail(string $to, string $subject, string $body, array $s): bool {
    if (isset($GLOBALS['PN_MAIL'])) return ($GLOBALS['PN_MAIL'])($to, $subject, $body);
    $from = $s['smtp_from'] ?? '' ?: 'noreply@' . ($s['domain'] ?? 'p.forma196.ru');
    if (!empty($s['smtp_host'])) return pn_smtp($to, $subject, $body, $from, $s);
    $h = "From: $from\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit";
    return mail($to, mb_encode_mimeheader($subject, 'UTF-8'), $body, $h);
}
// Минимальный SMTP: 465 — SSL, иначе STARTTLS; AUTH LOGIN.
function pn_smtp(string $to, string $subject, string $body, string $from, array $s): bool {
    $port = (int) ($s['smtp_port'] ?? 465) ?: 465;
    $fp = @stream_socket_client(($port === 465 ? 'ssl://' : 'tcp://') . $s['smtp_host'] . ":$port", $en, $es, 10);
    if (!$fp) return false;
    stream_set_timeout($fp, 10);
    $rd = function () use ($fp) { $r = ''; while (($l = fgets($fp, 515)) !== false) { $r .= $l; if (isset($l[3]) && $l[3] === ' ') break; } return (int) substr($r, 0, 3); };
    $cmd = function (string $c, int $want) use ($fp, $rd) { fwrite($fp, $c . "\r\n"); return $rd() === $want; };
    $ok = $rd() === 220 && $cmd('EHLO ' . ($s['domain'] ?? 'localhost'), 250);
    if ($ok && $port !== 465) $ok = $cmd('STARTTLS', 220) && stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT) && $cmd('EHLO ' . ($s['domain'] ?? 'localhost'), 250);
    if ($ok && !empty($s['smtp_user'])) $ok = $cmd('AUTH LOGIN', 334) && $cmd(base64_encode($s['smtp_user']), 334) && $cmd(base64_encode((string) ($s['smtp_pass'] ?? '')), 235);
    $msg = "From: $from\r\nTo: $to\r\nSubject: " . mb_encode_mimeheader($subject, 'UTF-8') . "\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\n"
        . "Content-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($body)) . "\r\n.";
    $ok = $ok && $cmd("MAIL FROM:<$from>", 250) && $cmd("RCPT TO:<$to>", 250) && $cmd('DATA', 354) && $cmd($msg, 250);
    fwrite($fp, "QUIT\r\n"); fclose($fp);
    return $ok;
}

function lead_kind_ru(string $k): string { return ['quiz' => 'Подбор', 'callback' => 'Перезвонить', 'viewing' => 'Просмотр', 'chat' => 'Чат'][$k] ?? $k; }
function lead_text(array $l, array $s): string {
    $ref = (string) $l['object_ref'];
    $link = preg_match('~^(kvartiry|doma)/[a-z0-9-]+/?$~', $ref) ? pn_site_url($s) . rtrim($ref, '/') . '/' : $ref;
    $parts = array_filter(['Новая заявка', lead_kind_ru($l['kind']), $l['want'], $l['budget'], $l['area'], $l['slot'], $l['name'], phone_pretty($l['phone']), $link],
        fn($x) => $x !== null && $x !== '');
    return implode(' · ', $parts);
}

final class TelegramChannel implements LeadChannel {
    public function key(): string { return 'tg'; }
    public function enabled(array $s): bool { return !empty($s['tg_token']) && !empty($s['tg_chat_id']); }
    public function send(array $l, array $s): bool {
        [$code] = pn_http('POST', "https://api.telegram.org/bot{$s['tg_token']}/sendMessage", ['Content-Type: application/json'],
            pn_json_enc(['chat_id' => $s['tg_chat_id'], 'text' => lead_text($l, $s), 'disable_web_page_preview' => true]));
        return $code === 200;
    }
}
final class MailChannel implements LeadChannel {
    public function key(): string { return 'mail'; }
    public function enabled(array $s): bool { return !empty($s['mail_to']); }
    public function send(array $l, array $s): bool {
        $subj = 'Заявка с сайта: ' . lead_kind_ru($l['kind']) . ', ' . phone_pretty($l['phone']);
        return pn_mail($s['mail_to'], $subj, str_replace(' · ', "\n", lead_text($l, $s)) . "\n\nЗаявка №{$l['id']}, " . $l['created_at'] . ' UTC', $s);
    }
}
// CRM заказчика: когда появится API, поменять только формат тела запроса здесь.
final class CrmChannel implements LeadChannel {
    public function key(): string { return 'crm'; }
    public function enabled(array $s): bool { return !empty($s['crm_enabled']) && !empty($s['crm_url']); }
    public function send(array $l, array $s): bool {
        $h = ['Content-Type: application/json']; if (!empty($s['crm_token'])) $h[] = 'Authorization: Bearer ' . $s['crm_token'];
        [$code] = pn_http('POST', $s['crm_url'], $h, pn_json_enc(['source' => 'site', 'id' => (int) $l['id'], 'kind' => $l['kind'], 'want' => $l['want'],
            'budget' => $l['budget'], 'area' => $l['area'], 'name' => $l['name'], 'phone' => $l['phone'], 'object' => $l['object_ref'], 'slot' => $l['slot'],
            'created_at' => $l['created_at']]));
        return $code >= 200 && $code < 300;
    }
}
function lead_channels(): array { return [new TelegramChannel, new MailChannel, new CrmChannel]; }

// Отправляет по каналам, где флаг 0. Возвращает [канал => результат].
function deliver_lead(int $id): array {
    $st = pn_db()->prepare('select * from leads where id = ?'); $st->execute([$id]);
    $l = $st->fetch(); if (!$l) return [];
    $s = Repo::settingsAll(); $res = []; $set = [];
    foreach (lead_channels() as $ch) {
        $col = 'delivered_' . $ch->key();
        if ((int) $l[$col] !== 0) continue;
        if (!$ch->enabled($s)) { $set[$col] = 2; $res[$ch->key()] = 'off'; continue; }
        try { $ok = $ch->send($l, $s); } catch (Throwable $e) { $ok = false; }
        $set[$col] = $ok ? 1 : 0; $res[$ch->key()] = $ok;
    }
    $sql = 'update leads set attempts = attempts + 1' . implode('', array_map(fn($c) => ", $c = ?", array_keys($set))) . ' where id = ?';
    pn_db()->prepare($sql)->execute([...array_values($set), $id]);
    return $res;
}
function lead_undelivered(array $l): bool { return in_array(0, [(int) $l['delivered_tg'], (int) $l['delivered_mail'], (int) $l['delivered_crm']], true); }
// Повтор недоставленных (вход менеджера в админку, cron). Возвращает, сколько заявок теперь доставлены полностью.
function deliver_pending(int $limit = 20): int {
    $ids = pn_db()->query('select id from leads where (delivered_tg = 0 or delivered_mail = 0 or delivered_crm = 0) and attempts < 10 order by id limit ' . (int) $limit)->fetchAll(PDO::FETCH_COLUMN);
    $n = 0;
    foreach ($ids as $id) {
        deliver_lead((int) $id);
        $st = pn_db()->prepare('select * from leads where id = ?'); $st->execute([$id]);
        if (!lead_undelivered($st->fetch())) $n++;
    }
    return $n;
}
