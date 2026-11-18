<?php
// Подключение к базе (SQLite по умолчанию; DSN — в конфиге, для тестов — $GLOBALS['PN_DSN']).
function pn_db(): PDO {
    if (!empty($GLOBALS['PN_DB'])) return $GLOBALS['PN_DB'];
    $dsn = $GLOBALS['PN_DSN'] ?? pn_config()['dsn'];
    if (str_starts_with($dsn, 'sqlite:')) {
        $dir = dirname(substr($dsn, 7));
        if (!is_dir($dir)) mkdir($dir, 0775, true);
    }
    $db = new PDO($dsn, null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
    if (str_starts_with($dsn, 'sqlite:')) {
        $db->exec('PRAGMA journal_mode=WAL');
        $db->exec('PRAGMA foreign_keys=ON');
        $db->exec('PRAGMA busy_timeout=5000');
    }
    return $GLOBALS['PN_DB'] = $db;
}

// Применяет app/migrations/*.sql, которых ещё нет в таблице migrations. Возвращает число применённых.
function pn_migrate(PDO $db): int {
    $db->exec("CREATE TABLE IF NOT EXISTS migrations (name TEXT PRIMARY KEY, at TEXT NOT NULL DEFAULT (datetime('now')))");
    $done = $db->query('select name from migrations')->fetchAll(PDO::FETCH_COLUMN);
    $n = 0;
    foreach (glob(__DIR__ . '/migrations/*.sql') as $f) {
        $name = basename($f);
        if (in_array($name, $done, true)) continue;
        $db->beginTransaction();
        try {
            $db->exec(file_get_contents($f));
            $db->prepare('insert into migrations(name) values (?)')->execute([$name]);
            $db->commit();
            $n++;
        } catch (Throwable $e) {
            $db->rollBack();
            throw $e;
        }
    }
    return $n;
}

function pn_json_enc($v): string {
    return json_encode($v, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR);
}

// Стартовые данные из data/seed в пустую базу. Фото — имена файлов прототипа в assets/img (WebP-версии — задача 9).
function pn_seed_db(PDO $db): void {
    $s = pn_seed_all();
    $db->beginTransaction();
    $cx = [];
    $ins = $db->prepare('insert into complexes(slug,name,district,lat,lng,checks) values (?,?,?,?,?,?)');
    foreach ($s['complexes'] as $c) {
        $ins->execute([$c['slug'], $c['name'], $c['district'], $c['lat'], $c['lng'], pn_json_enc($c['checks'])]);
        $cx[$c['name']] = (int) $db->lastInsertId();
    }
    $ins = $db->prepare('insert into apartments(id,slug,market,rooms,area,floor,floors,complex_id,address,district,price,discount_pct,finish,
        finish_label,house_status,due,special,photos,map_x,map_y,published,source) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)');
    foreach ($s['apartments'] as $a) {
        $ins->execute([$a['id'], $a['slug'], $a['market'], $a['rooms'], $a['area'], $a['floor'], $a['floors'], $a['complex'] ? $cx[$a['complex']] : null,
            $a['address'], $a['district'], $a['price'], $a['discount_pct'], $a['finish'], $a['finish_label'], $a['house_status'], $a['due'], $a['special'],
            pn_json_enc($a['photos']), $a['map_x'], $a['map_y'], $a['published'], $a['source']]);
    }
    $ins = $db->prepare('insert into houses(code,slug,line,number,area,motto,color,floors,rooms,ceiling,features,idea,text,photos,plans,sort)
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)');
    foreach ($s['houses'] as $h) {
        $ins->execute([$h['id'], $h['slug'], $h['line'], $h['n'], $h['n'], $h['motto'], $h['c'], $h['fl'], $h['rooms'], $h['ceil'],
            pn_json_enc($h['feats']), $h['idea'], pn_json_enc($h['text']), pn_json_enc($h['ph']), pn_json_enc($h['plans']), $h['sort']]);
    }
    $topic = ['Новостройка' => 'apartment', 'Вторичка' => 'apartment', 'Ремонт' => 'renovation', 'Дом' => 'house'];
    $ins = $db->prepare('insert into reviews(name,text,about,tag,photo,rating,topic,is_demo,published,sort) values (?,?,?,?,?,?,?,?,?,?)');
    foreach ($s['reviews'] as $k => $r) {
        $ins->execute([$r['name'], $r['text'], $r['about'], $r['tag'], $r['photo'], $r['rating'], $topic[$r['tag']] ?? null, $r['is_demo'], $r['published'], $k]);
    }
    $ins = $db->prepare('insert into settings(key,value) values (?,?)');
    foreach ($s['settings'] as $k => $v) $ins->execute([$k, pn_json_enc($v)]);
    $ins->execute(['faq', pn_json_enc($s['faq'])]);
    $ins->execute(['quick', pn_json_enc($s['quick'])]);
    $ins->execute(['salt', pn_json_enc(bin2hex(random_bytes(16)))]);
    $db->commit();
}
