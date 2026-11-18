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
function pn_ini_mb(string $k): int { return (int) round(pn_bytes((string) ini_get($k)) / 1048576); }
function pn_redirect(string $to, ?string $flash = null): array { if ($flash) pn_flash($flash); return [302, ['Location' => $to], '']; }

// Разделы: путь → [заголовок, роль, обработчик(method, rest, post, files, user)]
function pn_admin_sections(): array {
    $s = ['leads' => ['Заявки', 'manager', 'pn_admin_leads']];
    foreach (['apartments', 'complexes', 'developers', 'houses', 'reviews'] as $e)
        $s[$e] = [pn_entities()[$e]['title'], 'manager', fn($m, $sub, $p, $f, $u) => pn_crud($e, $m, $sub, $p, $f, $u)];
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
    if ($rest === 'logout') { Auth::logout(); return pn_redirect('/admin/login'); }
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
    return pn_admin_page('Заявки', 'admin/leads', ['active' => 'leads', 'rows' => $st->fetchAll(), 'stf' => $stf, 'counts' => $counts]);
}
