<?php
// Загрузка квартир из XML-фидов в формате Яндекс.Недвижимости: фиды застройщиков-партнёров и «База.ПРО» Н-маркет.
// Раз в сутки (cron: php site/app/cli.php feeds:run) или кнопкой в админке «Выгрузки»:
//   скачать фид → разобрать (потоково) → добавить/обновить квартиры, ЖК, застройщиков → пропавшие из фида снять с сайта
//   → показать только квартиры проверенных застройщиков → скачать к себе картинки (WebP) для квартир на сайте.
// Загрузка обновляет только «фидовые» поля (цена, площади, этаж, отделка, срок сдачи, адрес). Описание, спецпредложение,
// скидка, вид из окна, фото и публикация, которые менеджер поменял сам, остаются как есть.

const PN_FEED_MIN_INTERVAL = 20 * 3600;          // автозапуск одного фида — не чаще
const PN_FEED_MAX_BYTES = 1024 * 1024 * 1024;     // фид до 1 ГБ
const PN_FEED_IMG_MAX_BYTES = 20 * 1024 * 1024;
const PN_FEED_IMG_TRIES = 3;
const PN_FEED_PLAN_TAGS = ['plan', 'floorplan'];
const PN_FEED_SKIP_PHOTO_TAGS = ['complexscheme'];

// Скачивание по http(s) в файл. В тестах подменяется $GLOBALS['PN_FETCH'] = fn($url, $dest).
function pn_feed_fetch(string $url, string $dest, int $max = PN_FEED_MAX_BYTES): void {
    if (isset($GLOBALS['PN_FETCH'])) { ($GLOBALS['PN_FETCH'])($url, $dest); return; }
    if (!preg_match('~^https?://~i', $url)) throw new InvalidArgumentException('Адрес должен начинаться с http:// или https://');
    $fh = fopen($dest, 'wb');
    $ch = curl_init($url);
    curl_setopt_array($ch, [CURLOPT_FILE => $fh, CURLOPT_FOLLOWLOCATION => true, CURLOPT_MAXREDIRS => 5, CURLOPT_CONNECTTIMEOUT => 20,
        CURLOPT_TIMEOUT => 900, CURLOPT_ENCODING => '', CURLOPT_USERAGENT => 'PlatformaFeedLoader/1.0',
        CURLOPT_PROTOCOLS => CURLPROTO_HTTP | CURLPROTO_HTTPS, CURLOPT_REDIR_PROTOCOLS => CURLPROTO_HTTP | CURLPROTO_HTTPS,
        CURLOPT_NOPROGRESS => false, CURLOPT_XFERINFOFUNCTION => fn($c, $total, $done) => $done > $max ? 1 : 0]);
    $ok = curl_exec($ch); $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE); $err = curl_error($ch);
    curl_close($ch); fclose($fh);
    if (!$ok) throw new RuntimeException('Не удалось скачать: ' . ($err ?: 'нет ответа'));
    if ($code >= 400) throw new RuntimeException("Сервер ответил HTTP $code");
}

// Ключ картинки: у Н-маркет — pid (в ссылке меняется hash), у остальных — сама ссылка.
function pn_feed_media_key(string $url): string {
    return preg_match('~/photo/pid/([0-9A-Za-z-]+)~', $url, $m) ? 'nm:' . $m[1] : 'u:' . sha1($url);
}

function pn_feed_float(string $s): ?float {
    $s = str_replace([' ', "\u{00A0}", ','], ['', '', '.'], trim($s));
    return $s !== '' && is_numeric($s) ? (float) $s : null;
}
function pn_feed_yes(string $s): ?bool {
    $s = mb_strtolower(trim($s));
    if (in_array($s, ['1', 'true', 'да', '+', 'yes'], true)) return true;
    if (in_array($s, ['0', 'false', 'нет', '-', 'no'], true)) return false;
    return null;
}
// «ЖК «Новый квартал»» → «Новый квартал».
function pn_feed_complex_name(string $s): string {
    $s = trim(preg_replace('/^\s*(жк|жилой комплекс)\s+/iu', '', trim($s)));
    return trim(str_replace(['«', '»', '"', '“', '”', '„'], '', $s));
}
function pn_feed_norm(string $s): string { return mb_strtolower(preg_replace('/\s+/u', ' ', pn_feed_complex_name($s))); }

// Отделка: черновая, предчистовая (white box), без отделки — «без»; чистовая, под ключ, евроремонт, дизайнерская — «с отделкой».
function pn_feed_finish(string $label): array {
    $l = mb_strtolower(trim($label));
    if ($l === '') return ['without', null];
    foreach (['без отделки', 'черн', 'подготовк', 'предчистов', 'под чистов', 'white', 'требует'] as $w) if (str_contains($l, $w)) return ['without', $label];
    return ['with', $label];
}
function pn_feed_status(string $state, int $year, int $q): array {
    if (in_array(mb_strtolower($state), ['hand-over', 'built', 'сдан', 'дом сдан'], true)) return ['Дом сдан', 0];
    if ($year < 2000) return ['Срок сдачи уточняйте', 0];
    $roman = [1 => 'I', 2 => 'II', 3 => 'III', 4 => 'IV'];
    if ($q >= 1 && $q <= 4) return ['Сдача — ' . $roman[$q] . ' кв. ' . $year, $year * 100 + $q * 3];
    return ['Сдача — ' . $year, $year * 100 + 12];
}

// Одно <offer> → поля квартиры, или null, если это не квартира на продажу или не хватает обязательных полей.
function pn_feed_map(SimpleXMLElement $o): ?array {
    $s = fn(?SimpleXMLElement $e) => $e === null ? '' : trim((string) $e);
    $ext = trim((string) $o['internal-id']);
    $type = mb_strtolower($s($o->type)); $cat = mb_strtolower($s($o->category));
    if ($ext === '' || !in_array($type, ['продажа', 'sale'], true) || !in_array($cat, ['квартира', 'flat', 'apartment'], true)) return null;
    $area = pn_feed_float($s($o->area->value)); $price = pn_feed_float($s($o->price->value));
    if ($area !== null && $price !== null && preg_match('/м|m/u', $s($o->price->unit))) $price *= $area;     // цена за м²
    $studio = pn_feed_yes($s($o->studio)) === true;
    $rooms = $studio ? 0 : ($s($o->rooms) !== '' ? (int) $s($o->rooms) : null);
    $floor = $s($o->floor) !== '' ? (int) $s($o->floor) : null;
    $floors = $s($o->{'floors-total'}) !== '' ? (int) $s($o->{'floors-total'}) : $floor;
    if (!$area || $area <= 0 || !$price || $price <= 0 || $rooms === null || $floor === null || !$floors) return null;
    // здравый смысл: участки и коммерция с категорией «квартира», цена «за м²» вместо полной — не показываем
    if ($area < 10 || $area > 500 || $price / $area < 20000 || $price / $area > 2000000) return null;
    [$finish, $flabel] = pn_feed_finish($s($o->renovation));
    [$status, $due] = pn_feed_status($s($o->{'building-state'}), (int) $s($o->{'built-year'}), (int) $s($o->{'ready-quarter'}));
    $new = pn_feed_yes($s($o->{'new-flat'}));
    $complex = pn_feed_complex_name($s($o->{'building-name'}));
    $loc = $o->location;
    $district = $s($loc->{'sub-locality-name'}) ?: ($s($loc->{'non-admin-sub-locality'}) ?: null);
    $desc = $s($o->description);
    $dev = null;
    if (in_array(mb_strtolower($s($o->{'sales-agent'}->category)), ['developer', 'застройщик'], true)) $dev = $s($o->{'sales-agent'}->organization) ?: null;
    if (!$dev && preg_match('/Застройщик:\s*([^,.;\n]+)/u', $desc, $m)) $dev = trim($m[1]) ?: null;
    $bath = mb_strtolower($s($o->{'bathroom-unit'}));
    $bathroom = $bath === '' ? null : ((int) $bath >= 2 || str_contains($bath, 'два') ? 'два санузла' : (str_contains($bath, 'раздел') ? 'раздельный' : (str_contains($bath, 'совмещ') ? 'совмещённый' : null)));
    $bal = mb_strtolower($s($o->balcony));
    $balcony = $bal === '' ? null : (str_contains($bal, 'лодж') ? 'лоджия' : (str_contains($bal, 'террас') ? 'терраса'
        : (str_contains($bal, 'балкон') ? (preg_match('/2|два/u', $bal) ? 'два балкона' : 'балкон') : ($bal === 'нет' ? 'нет' : null))));
    $media = [];
    foreach ($o->image as $im) {
        $url = trim((string) $im);
        if (!preg_match('~^https?://~i', $url) || count($media) >= 24) continue;
        $media[] = [mb_strtolower(trim((string) $im['tag'])) ?: 'photo', pn_feed_media_key($url), $url];
    }
    $num = fn(string $v) => ($f = pn_feed_float($v)) !== null && $f > 0 ? $f : null;
    $nmc = $s($o->{'nmarket-complex-id'});
    return [
        'ext' => $ext, 'market' => $new === false || ($new === null && $complex === '') ? 'secondary' : 'new',
        'rooms' => $rooms, 'area' => $area, 'living_area' => $num($s($o->{'living-space'}->value)), 'kitchen_area' => $num($s($o->{'kitchen-space'}->value)),
        'ceiling' => $num($s($o->{'ceiling-height'})), 'floor' => $floor, 'floors' => max($floors, $floor), 'price' => (int) round($price),
        'finish' => $finish, 'finish_label' => $flabel, 'house_status' => $status, 'due' => $due, 'bathroom' => $bathroom, 'balcony' => $balcony,
        'address' => $s($loc->address) ?: null, 'district' => $district,
        'lat' => pn_feed_float($s($loc->latitude)), 'lng' => pn_feed_float($s($loc->longitude)),
        'description' => $desc === '' ? null : mb_substr($desc, 0, 5000),
        'complex' => $complex === '' ? null : $complex, 'complex_ext' => $complex === '' ? null : ($nmc !== '' ? 'nm:' . $nmc : 'name:' . pn_feed_norm($complex)),
        'developer' => $dev, 'media' => $media,
    ];
}

// Потоковый разбор: по одному <offer> — фид на десятки тысяч квартир не держится в памяти целиком. null — пропущенное предложение.
function pn_feed_iter(string $file): Generator {
    $prev = libxml_use_internal_errors(true); libxml_clear_errors();
    $r = new XMLReader();
    if (!@$r->open($file, null, LIBXML_NONET | LIBXML_COMPACT | LIBXML_PARSEHUGE)) throw new RuntimeException('Файл фида не открывается');
    $root = false;
    try {
        $ok = @$r->read();
        while ($ok) {
            if ($r->nodeType === XMLReader::ELEMENT) {
                if (!$root) { $root = true; if ($r->localName !== 'realty-feed') throw new RuntimeException('Это не фид Яндекс.Недвижимости (нет <realty-feed>)'); }
                if ($r->localName === 'offer') {
                    $xml = preg_replace('/\sxmlns="[^"]*"/', '', $r->readOuterXml(), 1);
                    $sx = @simplexml_load_string($xml, SimpleXMLElement::class, LIBXML_NONET);
                    yield $sx === false ? null : pn_feed_map($sx);
                    $ok = @$r->next(); continue;
                }
            }
            $ok = @$r->read();
        }
        if (!$root) throw new RuntimeException('Файл не похож на XML-фид: ' . trim((libxml_get_errors()[0] ?? null)?->message ?? 'пусто'));
        foreach (libxml_get_errors() as $e) if ($e->level === LIBXML_ERR_FATAL) throw new RuntimeException('Фид оборван или повреждён: ' . trim($e->message) . " (строка {$e->line})");
    } finally {
        $r->close(); libxml_clear_errors(); libxml_use_internal_errors($prev);
    }
}
function pn_feed_offers(string $file): array {
    $o = ['offers' => [], 'skipped' => 0];
    foreach (pn_feed_iter($file) as $x) { if ($x === null) $o['skipped']++; else $o['offers'][] = $x; }
    return $o;
}

// Загрузка одного фида. Возвращает ['total', 'added', 'updated', 'gone', 'skipped', 'hide_skipped', 'error'].
function pn_feed_import(int $feedId): array {
    $db = pn_db();
    $st = $db->prepare('select * from feeds where id = ?'); $st->execute([$feedId]); $feed = $st->fetch();
    if (!$feed) throw new InvalidArgumentException("Нет выгрузки $feedId");
    $S = ['total' => 0, 'added' => 0, 'updated' => 0, 'gone' => 0, 'skipped' => 0, 'hide_skipped' => false, 'error' => null];
    $now = gmdate('Y-m-d H:i:s'); $token = $now . '#' . bin2hex(random_bytes(4));
    $tmp = tempnam(sys_get_temp_dir(), 'pnfeed');
    @set_time_limit(0);
    try {
        pn_feed_fetch((string) $feed['url'], $tmp);
        $q = $db->prepare("select count(*) from apartments where feed_id = ? and feed_state = 'active'"); $q->execute([$feedId]); $before = (int) $q->fetchColumn();
        $db->beginTransaction();
        $ctx = pn_feed_ctx($db, $feed);
        foreach (pn_feed_iter($tmp) as $o) {
            if ($o === null) { $S['skipped']++; continue; }
            $S['total']++;
            pn_feed_upsert($db, $ctx, $feedId, $o, $token) ? $S['added']++ : $S['updated']++;
        }
        if ($S['total'] === 0) throw new RuntimeException('В фиде нет ни одной квартиры на продажу — проверьте ссылку');
        foreach ($ctx['cmedia'] as $cid => $m)
            $db->prepare('update complexes set feed_media = ? where id = ?')->execute([pn_json_enc(array_slice($m, 0, 12)), $cid]);
        if ($before > 0 && $S['total'] < $before * 0.5) $S['hide_skipped'] = true;      // резкое падение — скорее сбой фида, чем распродажа
        else {
            $g = $db->prepare("update apartments set feed_state = 'gone', published = 0 where feed_id = ? and feed_state = 'active' and feed_seen_at <> ?");
            $g->execute([$feedId, $token]); $S['gone'] = $g->rowCount();
        }
        $db->commit();
    } catch (Throwable $e) {
        if ($db->inTransaction()) $db->rollBack();
        $S['error'] = $e->getMessage();
    } finally {
        @unlink($tmp);
    }
    pn_feed_visibility();
    $msg = $S['error'] !== null ? 'Ошибка: ' . $S['error']
        : "квартир в фиде {$S['total']}: добавлено {$S['added']}, обновлено {$S['updated']}, снято {$S['gone']}"
            . ($S['skipped'] ? ", пропущено {$S['skipped']} (не квартиры на продажу или без цены)" : '')
            . ($S['hide_skipped'] ? '. Квартир стало вдвое меньше — пропавшие не сняты с сайта, проверьте фид' : '');
    $db->prepare('update feeds set last_run_at = ?, last_status = ?, last_stats = ?' . ($S['error'] === null ? ', last_ok_at = ?' : '') . ' where id = ?')
        ->execute($S['error'] === null ? [$now, $msg, pn_json_enc($S), $now, $feedId] : [$now, $msg, pn_json_enc($S), $feedId]);
    return $S;
}

// Справочники на время загрузки: ЖК по внешнему ключу и по названию, застройщики по названию, слаги ЖК.
function pn_feed_ctx(PDO $db, array $feed): array {
    $c = ['feed' => $feed, 'cx_ext' => [], 'cx_name' => [], 'dev' => [], 'cmedia' => [], 'cxdev' => [], 'slugs' => []];
    foreach ($db->query('select id, name, slug, external_id, developer_id from complexes')->fetchAll() as $r) {
        if ($r['external_id']) $c['cx_ext'][$r['external_id']] = (int) $r['id'];
        $c['cx_name'][pn_feed_norm($r['name'])] = (int) $r['id'];
        $c['cxdev'][(int) $r['id']] = $r['developer_id'] === null ? null : (int) $r['developer_id'];
        $c['slugs'][$r['slug']] = true;
    }
    foreach ($db->query('select id, name from developers')->fetchAll() as $r) $c['dev'][mb_strtolower(trim($r['name']))] = (int) $r['id'];
    return $c;
}
function pn_feed_developer(PDO $db, array &$c, ?string $name): ?int {
    if (!empty($c['feed']['developer_id'])) return (int) $c['feed']['developer_id'];
    if ($name === null) return null;
    $k = mb_strtolower(trim($name));
    if (!isset($c['dev'][$k])) {
        $db->prepare('insert into developers(name, verified) values (?, 0)')->execute([trim($name)]);
        $c['dev'][$k] = (int) $db->lastInsertId();
    }
    return $c['dev'][$k];
}
function pn_feed_complex(PDO $db, array &$c, array $o, ?int $devId): ?int {
    if ($o['complex'] === null) return null;
    $id = $c['cx_ext'][$o['complex_ext']] ?? $c['cx_name'][pn_feed_norm($o['complex'])] ?? null;
    if ($id === null) {
        $name = 'ЖК ' . $o['complex']; $base = pn_slug($name); $slug = $base; $k = 2;
        while (isset($c['slugs'][$slug])) $slug = $base . '-' . $k++;
        $db->prepare('insert into complexes(slug, name, district, developer_id, address, lat, lng, external_id) values (?,?,?,?,?,?,?,?)')
            ->execute([$slug, $name, $o['district'], $devId, $o['address'], $o['lat'], $o['lng'], $o['complex_ext']]);
        $id = (int) $db->lastInsertId();
        $c['slugs'][$slug] = true; $c['cx_name'][pn_feed_norm($name)] = $id; $c['cxdev'][$id] = $devId;
    } else {
        $db->prepare('update complexes set external_id = coalesce(external_id, ?), developer_id = coalesce(developer_id, ?) where id = ?')->execute([$o['complex_ext'], $devId, $id]);
        if (($c['cxdev'][$id] ?? null) === null) $c['cxdev'][$id] = $devId;
        if (!empty($c['feed']['developer_id'])) $db->prepare('update complexes set developer_id = ? where id = ?')->execute([$devId, $id]);
    }
    $c['cx_ext'][$o['complex_ext']] = $id;
    return $id;
}
// Добавляет или обновляет квартиру. true — новая.
function pn_feed_upsert(PDO $db, array &$c, int $feedId, array $o, string $token): bool {
    $devId = pn_feed_developer($db, $c, $o['developer']);
    $cid = pn_feed_complex($db, $c, $o, $devId);
    $own = []; $cm = [];
    foreach ($o['media'] as $m) {
        if (in_array($m[0], PN_FEED_PLAN_TAGS, true) || $cid === null) $own[] = $m; else $cm[] = $m;
    }
    if ($cid !== null && $cm) {
        $have = array_column($c['cmedia'][$cid] ?? [], 1);
        foreach ($cm as $m) if (!in_array($m[1], $have, true) && !in_array($m[0], PN_FEED_SKIP_PHOTO_TAGS, true)) { $c['cmedia'][$cid][] = $m; $have[] = $m[1]; }
        if (isset($c['cmedia'][$cid])) usort($c['cmedia'][$cid], fn($a, $b) => ($b[0] === 'housemain') <=> ($a[0] === 'housemain'));
    }
    $f = ['market' => $o['market'], 'rooms' => $o['rooms'], 'area' => $o['area'], 'living_area' => $o['living_area'], 'kitchen_area' => $o['kitchen_area'],
        'ceiling' => $o['ceiling'], 'floor' => $o['floor'], 'floors' => $o['floors'], 'complex_id' => $cid, 'address' => $o['address'], 'district' => $o['district'],
        'price' => $o['price'], 'finish' => $o['finish'], 'finish_label' => $o['finish_label'], 'house_status' => $o['house_status'], 'due' => $o['due'],
        'bathroom' => $o['bathroom'], 'balcony' => $o['balcony'], 'lat' => $o['lat'], 'lng' => $o['lng'],
        'feed_state' => 'active', 'feed_seen_at' => $token, 'feed_media' => pn_json_enc(array_map(fn($m) => [$m[0], $m[1], $m[2]], $own))];
    $ext = "$feedId:{$o['ext']}";
    $st = $db->prepare("select id, description from apartments where source = 'feed' and external_id = ?"); $st->execute([$ext]); $row = $st->fetch();
    if ($row) {
        if (($row['description'] ?? '') === '' && $o['description'] !== null) $f['description'] = $o['description'];
        $f['updated_at'] = gmdate('Y-m-d H:i:s'); $f['feed_id'] = $feedId;
        $db->prepare('update apartments set ' . implode(', ', array_map(fn($k) => "$k = ?", array_keys($f))) . ' where id = ?')->execute([...array_values($f), $row['id']]);
        return false;
    }
    $f += ['description' => $o['description'], 'published' => 0, 'source' => 'feed', 'external_id' => $ext, 'feed_id' => $feedId, 'slug' => 'tmp-' . bin2hex(random_bytes(6))];
    $db->prepare('insert into apartments(' . implode(',', array_keys($f)) . ') values (' . implode(',', array_fill(0, count($f), '?')) . ')')->execute(array_values($f));
    $id = (int) $db->lastInsertId();
    $where = $cid !== null ? 'ЖК ' . $o['complex'] : ($o['address'] ?? 'kvartira');
    $db->prepare('update apartments set slug = ? where id = ?')->execute([$id . '-' . pn_slug($where), $id]);
    return true;
}

// Публикация квартир из фидов: есть в последней выгрузке, выгрузка включена и (без отбора или застройщик проверен).
// Квартиры, которые менеджер сам включил или снял, не трогаем — кроме пропавших из фида.
function pn_feed_visibility(): int {
    $st = pn_db()->prepare("update apartments set published = case when feed_state = 'active'
            and exists (select 1 from feeds f where f.id = apartments.feed_id and f.enabled = 1)
            and ((select f.only_verified from feeds f where f.id = apartments.feed_id) = 0
                 or exists (select 1 from complexes c join developers d on d.id = c.developer_id where c.id = apartments.complex_id and d.verified = 1))
            then 1 else 0 end
        where source = 'feed' and (feed_manual = 0 or coalesce(feed_state, '') <> 'active')");
    $st->execute();
    return $st->rowCount();
}

// Картинки из фидов для квартир на сайте: скачать (по бюджету и времени), сохранить WebP, разложить по планировкам и фото.
function pn_feed_images(int $budget = 300, float $seconds = 240): array {
    $db = pn_db(); $t0 = microtime(true); $R = ['ok' => 0, 'err' => 0, 'left' => 0];
    $need = []; $cids = [];
    foreach ($db->query("select complex_id, feed_media, feed_own_media from apartments where source = 'feed' and published = 1")->fetchAll() as $a) {
        if (!(int) $a['feed_own_media']) foreach (json_decode($a['feed_media'], true) ?: [] as $m) $need[$m[1]] = $m[2];
        if ($a['complex_id']) $cids[(int) $a['complex_id']] = true;
    }
    if ($cids) foreach ($db->query('select feed_media from complexes where id in (' . implode(',', array_keys($cids)) . ')')->fetchAll(PDO::FETCH_COLUMN) as $j)
        foreach (json_decode($j, true) ?: [] as $m) $need[$m[1]] = $m[2];
    $ins = $db->prepare('insert or ignore into feed_images(key, url) values (?, ?)');
    foreach ($need as $k => $u) $ins->execute([$k, $u]);
    if ($need) {
        $keys = array_keys($need);
        $ph = implode(',', array_fill(0, count($keys), '?'));
        $st = $db->prepare("select key, url from feed_images where key in ($ph) and (status = 'new' or (status = 'err' and tries < " . PN_FEED_IMG_TRIES . ')) order by tries, rowid');
        $st->execute($keys); $pending = $st->fetchAll();
        $ok = $db->prepare("update feed_images set status = 'ok', img = ?, updated_at = datetime('now') where key = ?");
        $bad = $db->prepare("update feed_images set status = 'err', tries = tries + 1, updated_at = datetime('now') where key = ?");
        foreach ($pending as $i => $p) {
            if ($i >= $budget || microtime(true) - $t0 > $seconds) { $R['left'] = count($pending) - $i; break; }
            $tmp = tempnam(sys_get_temp_dir(), 'pnimg');
            try { pn_feed_fetch($p['url'], $tmp, PN_FEED_IMG_MAX_BYTES); $ok->execute([pn_image_store($tmp, 'feed')['id'], $p['key']]); $R['ok']++; }
            catch (Throwable $e) { $bad->execute([$p['key']]); $R['err']++; }
            finally { @unlink($tmp); }
        }
    }
    pn_feed_apply_media();
    return $R;
}

// Скачанные картинки → поля photos/plans. ЖК: фото из фида, если у ЖК нет своих (или стоят прежние из фида). Квартира: планировки — свои, фото — фото ЖК.
function pn_feed_apply_media(): void {
    $db = pn_db();
    $img = array_column($db->query("select key, img from feed_images where status = 'ok'")->fetchAll(), 'img', 'key');
    $cphotos = [];
    foreach ($db->query("select id, photos, feed_media from complexes where feed_media <> '[]'")->fetchAll() as $c) {
        $auto = array_values(array_filter(array_map(fn($m) => $img[$m[1]] ?? null, json_decode($c['feed_media'], true) ?: [])));
        $cur = json_decode($c['photos'], true) ?: [];
        $all = array_values(array_filter(array_map(fn($m) => $img[$m[1]] ?? null, json_decode($c['feed_media'], true) ?: [])));
        if ($auto && $cur !== $auto && (!$cur || !array_diff($cur, $all))) {
            $db->prepare('update complexes set photos = ? where id = ?')->execute([pn_json_enc($auto), $c['id']]); $cur = $auto;
        }
        $cphotos[(int) $c['id']] = $cur;
    }
    $up = $db->prepare('update apartments set photos = ?, plans = ? where id = ?');
    foreach ($db->query("select a.id, a.complex_id, a.feed_media, a.photos, a.plans, c.photos as cph from apartments a left join complexes c on c.id = a.complex_id
            where a.source = 'feed' and a.feed_own_media = 0")->fetchAll() as $a) {
        $plans = []; $own = [];
        foreach (json_decode($a['feed_media'], true) ?: [] as $m) {
            if (!isset($img[$m[1]])) continue;
            if (in_array($m[0], PN_FEED_PLAN_TAGS, true)) $plans[] = $img[$m[1]]; elseif (!in_array($m[0], PN_FEED_SKIP_PHOTO_TAGS, true)) $own[] = $img[$m[1]];
        }
        $photos = array_slice($own ?: ($cphotos[(int) $a['complex_id']] ?? (json_decode((string) $a['cph'], true) ?: [])), 0, 8);
        $pj = pn_json_enc($photos); $lj = pn_json_enc($plans);
        if ($pj !== $a['photos'] || $lj !== $a['plans']) $up->execute([$pj, $lj, $a['id']]);
    }
}

// По расписанию: включённые фиды, которые не загружались 20 часов (или все — $force), затем картинки.
function pn_feeds_run(bool $force = false): array {
    $out = ['feeds' => [], 'images' => null];
    foreach (pn_db()->query('select id, last_run_at from feeds where enabled = 1 order by id')->fetchAll() as $f) {
        if (!$force && $f['last_run_at'] && strtotime($f['last_run_at'] . ' UTC') > time() - PN_FEED_MIN_INTERVAL) continue;
        $out['feeds'][(int) $f['id']] = pn_feed_import((int) $f['id']);
    }
    $out['images'] = pn_feed_images();
    return $out;
}
