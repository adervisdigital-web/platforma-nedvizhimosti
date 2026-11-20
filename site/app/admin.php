<?php
// Админка: маршруты /admin/*. Разделы добавляются в pn_admin_sections() (задачи 11 и 13).
function pn_admin_page(string $title, string $tpl, array $vars = []): array {
    $u = Auth::user();
    return pn_html_response(200, pn_render('admin/layout', ['title' => $title, 'user' => $u, 'active' => $vars['active'] ?? '',
        'flash' => pn_flash(), 'content' => pn_render($tpl, $vars + ['user' => $u])]));
}
function pn_flash(?string $msg = null): ?string {
    pn_session();
    if ($msg !== null) { $_SESSION['flash'] = $msg; return null; }
    $m = $_SESSION['flash'] ?? null; unset($_SESSION['flash']); return $m;
}
function pn_plural(int $n, string $one, string $few, string $many): string { $m = $n % 10; $h = $n % 100; return $m === 1 && $h !== 11 ? $one : ($m >= 2 && $m <= 4 && ($h < 12 || $h > 14) ? $few : $many); }
function pn_ini_mb(string $k): int { return (int) round(pn_bytes((string) ini_get($k)) / 1048576); }
function pn_redirect(string $to, ?string $flash = null): array { if ($flash) pn_flash($flash); return [302, ['Location' => $to], '']; }

// Разделы: путь → [заголовок, роль, обработчик(method, rest, post, files, user)]
function pn_admin_sections(): array {
    $s = ['overview' => ['Обзор', 'manager', 'pn_admin_overview'], 'leads' => ['Заявки', 'manager', 'pn_admin_leads']];
    foreach (['apartments', 'complexes', 'developers', 'houses', 'reviews'] as $e)
        $s[$e] = [pn_entities()[$e]['title'], 'manager', fn($m, $sub, $p, $f, $u) => pn_crud($e, $m, $sub, $p, $f, $u)];
    $s['password'] = ['Смена пароля', 'manager', 'pn_admin_password'];
    $s['settings'] = ['Настройки', 'admin', 'pn_admin_settings'];
    $s['users'] = ['Менеджеры', 'admin', 'pn_admin_users'];
    foreach ($GLOBALS['PN_ADMIN_SECTIONS'] ?? [] as $k => $v) $s[$k] = $v;
    return $s;
}

function pn_admin_route(string $method, string $path, array $post = [], array $files = []): array {
    $rest = trim(substr($path, strlen('/admin')), '/');
    if ($method === 'POST' && !$post && (int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 0)   // PHP выбросил тело целиком: больше post_max_size
        throw new PnHttp(413, [], 'Файлы слишком большие для сервера: за один раз можно отправить до ' . pn_ini_mb('post_max_size')
            . ' МБ. Загрузите фото по несколько штук.');
    if ($method === 'POST') csrf_check($post);
    if ($rest === 'login') {
        if ($method === 'POST') {
            if (Auth::login((string) ($post['login'] ?? ''), (string) ($post['password'] ?? ''))) { deliver_pending_safe(); return pn_redirect('/admin/'); }
            return pn_html_response(200, pn_render('admin/login', ['error' => Auth::lastError(), 'login' => $post['login'] ?? '']));
        }
        return pn_html_response(200, pn_render('admin/login', ['error' => '', 'login' => '']));
    }
    if ($rest === 'logout') { if ($method !== 'POST') return pn_redirect('/admin/'); Auth::logout(); return pn_redirect('/admin/login'); }
    $u = Auth::require();
    if ($rest === '') return isset(pn_admin_sections()['leads']) ? pn_redirect('/admin/leads') : pn_admin_page('Админка', 'admin/home', ['active' => '']);
    [$sec, $sub] = array_pad(explode('/', $rest, 2), 2, '');
    $secs = pn_admin_sections();
    if (!isset($secs[$sec])) throw new PnHttp(404, [], 'Нет такого раздела');
    [$title, $role, $fn] = $secs[$sec];
    Auth::require($role);
    return $fn($method, $sub, $post, $files, $u);
}
// Повторная доставка заявок при входе менеджера (задача 13); до неё — ничего.
function deliver_pending_safe(): void { if (function_exists('deliver_pending')) { try { deliver_pending(20, 3.0); } catch (Throwable $e) {} } }   // вход не ждёт дольше ~3 с

function pn_admin_password(string $method, string $sub, array $post, array $files, array $u): array {
    $err = '';
    if ($method === 'POST') {
        $st = pn_db()->prepare('select password_hash from users where id = ?'); $st->execute([(int) $u['id']]);
        $new = (string) ($post['new'] ?? '');
        if (!password_verify((string) ($post['old'] ?? ''), (string) $st->fetchColumn())) $err = 'Текущий пароль указан неверно';
        elseif ($new !== (string) ($post['new2'] ?? '')) $err = 'Новые пароли не совпадают';
        elseif ($p = pn_password_problem($new, (string) $u['login'])) $err = $p;
        else {
            pn_db()->prepare('update users set password_hash = ? where id = ?')->execute([password_hash($new, PASSWORD_DEFAULT), (int) $u['id']]);
            if (PHP_SAPI !== 'cli') session_regenerate_id(true);
            $_SESSION['weak'] = false; audit('change_password', 'users', (int) $u['id']);
            return pn_redirect('/admin/', 'Пароль изменён');
        }
    }
    return pn_admin_page('Смена пароля', 'admin/password', ['active' => 'password', 'error' => $err]);
}

function pn_admin_users(string $method, string $sub, array $post, array $files, array $u): array {
    $db = pn_db();
    if ($method === 'POST' && ($post['do'] ?? '') === 'add') {
        $login = trim((string) ($post['login'] ?? '')); $role = in_array($post['role'] ?? '', ['admin', 'manager'], true) ? $post['role'] : 'manager';
        if (!preg_match('/^[\p{L}0-9._-]{3,40}$/u', $login)) return pn_redirect('/admin/users', 'Логин: 3–40 символов, буквы, цифры, точка, дефис');
        $pass = rtrim(strtr(base64_encode(random_bytes(12)), '+/', 'kx'), '=');
        try { $db->prepare('insert into users(login,password_hash,role) values (?,?,?)')->execute([$login, password_hash($pass, PASSWORD_DEFAULT), $role]); }
        catch (PDOException $e) { return pn_redirect('/admin/users', 'Такой логин уже есть'); }
        audit('create', 'users', (int) $db->lastInsertId(), ['login' => $login, 'role' => $role]);
        return pn_redirect('/admin/users', "Менеджер $login добавлен. Пароль: $pass — передайте лично, он показывается один раз");
    }
    if ($method === 'POST' && ($post['do'] ?? '') === 'reset') {
        $id = (int) ($post['id'] ?? 0); $pass = rtrim(strtr(base64_encode(random_bytes(12)), '+/', 'kx'), '=');
        $db->prepare('update users set password_hash = ? where id = ?')->execute([password_hash($pass, PASSWORD_DEFAULT), $id]);
        audit('reset_password', 'users', $id);
        return pn_redirect('/admin/users', "Новый пароль: $pass — передайте лично, он показывается один раз");
    }
    if ($method === 'POST' && ($post['do'] ?? '') === 'delete') {
        $id = (int) ($post['id'] ?? 0);
        if ($id === (int) $u['id']) return pn_redirect('/admin/users', 'Нельзя удалить самого себя');
        $db->prepare('delete from users where id = ?')->execute([$id]); audit('delete', 'users', $id);
        return pn_redirect('/admin/users', 'Менеджер удалён');
    }
    return pn_admin_page('Менеджеры', 'admin/users', ['active' => 'users', 'rows' => $db->query('select id, login, role, created_at from users order by id')->fetchAll()]);
}

// Заявки: первый экран админки — новые сверху, статус, заметка, фильтр, CSV, метка «не доставлена».
function pn_admin_leads(string $method, string $sub, array $post, array $files, array $u): array {
    $db = pn_db();
    if ($sub === 'csv') {
        $rows = $db->query('select id, created_at, kind, want, budget, area, name, phone, object_ref, slot, status, note from leads order by id desc')->fetchAll();
        $f = fopen('php://temp', 'w+'); fwrite($f, "\xEF\xBB\xBF");
        fputcsv($f, ['№', 'Дата (UTC)', 'Тип', 'Что ищет', 'Бюджет', 'Площадь/комнаты', 'Имя', 'Телефон', 'Объект', 'Время просмотра', 'Статус', 'Заметка'], ';');
        $safe = fn($v) => is_string($v) && $v !== '' && strpbrk($v[0], "=+-@\t\r") !== false && !preg_match('/^\+7\d{10}$/', $v) ? "'" . $v : $v;   // формулы Excel
        foreach ($rows as $r) { $r['kind'] = lead_kind_ru($r['kind']); fputcsv($f, array_map($safe, array_values($r)), ';'); }
        rewind($f); $csv = stream_get_contents($f); fclose($f);
        audit('export', 'leads', null, ['rows' => count($rows)]);
        return [200, ['Content-Type' => 'text/csv; charset=utf-8', 'Content-Disposition' => 'attachment; filename="zayavki-' . date('Y-m-d') . '.csv"'], $csv];
    }
    if ($method === 'POST' && ctype_digit($sub) && ($post['do'] ?? '') === 'status') {
        $st = in_array($post['status'] ?? '', ['new', 'work', 'closed'], true) ? $post['status'] : 'new';
        $db->prepare('update leads set status = ?, note = ? where id = ?')->execute([$st, mb_substr(trim((string) ($post['note'] ?? '')), 0, 1000), (int) $sub]);
        audit('status', 'leads', (int) $sub, ['status' => $st]);
        return pn_redirect('/admin/leads' . (isset($_GET['st']) ? '?st=' . urlencode((string) $_GET['st']) : ''), 'Заявка №' . (int) $sub . ' обновлена');
    }
    if ($method === 'POST' && ($post['do'] ?? '') === 'retry') { $n = deliver_pending(); return pn_redirect('/admin/leads', "Повторно доставлено: $n"); }
    $stf = in_array($_GET['st'] ?? '', ['new', 'work', 'closed'], true) ? $_GET['st'] : '';
    $st = $db->prepare('select * from leads' . ($stf ? ' where status = ?' : '') . ' order by (status = \'new\') desc, id desc limit 500');
    $st->execute($stf ? [$stf] : []);
    $counts = array_column($db->query('select status, count(*) n from leads group by status')->fetchAll(), 'n', 'status');
    $set = Repo::settingsAll();
    return pn_admin_page('Заявки', 'admin/leads', ['active' => 'leads', 'rows' => $st->fetchAll(), 'stf' => $stf, 'counts' => $counts,
        'deliv' => ['tg' => !empty($set['tg_token']) && !empty($set['tg_chat_id']), 'mail' => !empty($set['mail_to'])]]);
}

// Обзор: сводка, заявки за 14 дней, чек-лист перед запуском, последние заявки, журнал действий.
function pn_admin_overview(string $method, string $sub, array $post, array $files, array $u): array {
    $db = pn_db(); $set = Repo::settingsAll();
    $tz = new DateTimeZone(date_default_timezone_get()); $days = [];
    for ($i = 13; $i >= 0; $i--) { $d = (new DateTime("-$i days", $tz))->format('Y-m-d'); $days[$d] = 0; }
    foreach ($db->query("select created_at from leads where created_at >= datetime('now', '-15 days')")->fetchAll(PDO::FETCH_COLUMN) as $c) {
        $d = (new DateTime($c, new DateTimeZone('UTC')))->setTimezone($tz)->format('Y-m-d');
        if (isset($days[$d])) $days[$d]++;
    }
    $n = fn(string $sql) => (int) $db->query($sql)->fetchColumn();
    $stats = [
        'new' => $n("select count(*) from leads where status = 'new'"), 'week' => array_sum(array_slice($days, -7)),
        'apt' => $n('select count(*) from apartments where published = 1'), 'apt_hidden' => $n('select count(*) from apartments where published = 0'),
        'houses' => $n('select count(*) from houses where published = 1'), 'reviews' => $n('select count(*) from reviews where published = 1'),
        'reviews_demo' => $n('select count(*) from reviews where published = 1 and is_demo = 1'),
    ];
    $me = $db->prepare('select password_hash from users where id = ?'); $me->execute([(int) $u['id']]); $hash = (string) $me->fetchColumn();
    $weak = password_verify('admin', $hash) || password_verify((string) $u['login'], $hash);   // пароль «admin» или равный логину
    $demoApts = $n("select count(*) from apartments where published = 1 and description like '%демонстрационное%'");
    $check = [
        ['Заявки приходят в Telegram', !empty($set['tg_token']) && !empty($set['tg_chat_id']), 'Укажите токен бота и chat_id группы менеджеров', '/admin/settings'],
        ['Копия заявок на почту', !empty($set['mail_to']), 'Укажите почту для заявок', '/admin/settings'],
        ['Надёжный пароль у вас', !$weak, 'Пароль совпадает с логином или «admin» — смените его', '/admin/password'],
        ['Реальные квартиры вместо демо', $demoApts === 0, "Демо-квартир на сайте: $demoApts — замените настоящими", '/admin/apartments'],
        ['Настоящие отзывы', empty($set['show_demo_reviews']) || $stats['reviews_demo'] === 0, 'Демо-отзывы показываются на сайте — выключите в настройках', '/admin/settings'],
        ['Снята пометка «демо-данные»', empty($set['demo_data']), 'В подвале сайта стоит пометка «демо-данные»', '/admin/settings'],
        ['Ставки ипотеки актуальны', !empty($set['rates_date']) && strtotime((string) $set['rates_date']) > time() - 30 * 86400,
            'Ставки' . (!empty($set['rates_date']) ? ' от ' . pn_rates_date_ru($set) : ' без даты') . ' — сверьте с банками и обновите в настройках', '/admin/settings'],
        ['Текст политики обработки ПДн', false, 'Нужен текст от юриста — пришлите, вставим на страницу политики', '/privacy/'],
    ];
    $recent = $db->query('select * from leads order by id desc limit 5')->fetchAll();
    $log = $db->query('select a.*, u.login from audit a left join users u on u.id = a.user_id order by a.at desc, a.id desc limit 12')->fetchAll();
    return pn_admin_page('Обзор', 'admin/overview', ['active' => 'overview', 'days' => $days, 'stats' => $stats, 'check' => $check, 'recent' => $recent, 'log' => $log]);
}
