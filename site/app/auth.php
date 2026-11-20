<?php
// Вход в админку: сессия, роли, блокировка после 5 ошибок на 15 минут, журнал действий.
final class PnHttp extends Exception {
    public function __construct(public int $status, public array $headers = [], string $msg = '') { parent::__construct($msg ?: "HTTP $status"); }
}
function pn_now(): int { return $GLOBALS['PN_NOW'] ?? time(); }
function pn_ip(): string { return $_SERVER['REMOTE_ADDR'] ?? 'cli'; }

function pn_session(): void {
    if (PHP_SAPI === 'cli') { $_SESSION ??= []; return; }
    if (session_status() === PHP_SESSION_ACTIVE) return;
    ini_set('session.use_strict_mode', '1'); ini_set('session.use_only_cookies', '1');   // чужой id сессии из ссылки не принимается
    session_name('pn_admin');
    session_set_cookie_params(['lifetime' => 0, 'path' => '/', 'httponly' => true, 'samesite' => 'Lax', 'secure' => !empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off']);
    session_start();
}

final class Auth {
    const MAX_FAILS = 5, LOCK = 15 * 60, IDLE = 2 * 3600, MAX_AGE = 12 * 3600;   // выход после 2 ч бездействия и не позже 12 ч после входа
    private static string $err = '';
    public static function lastError(): string { return self::$err; }

    private static function locked(string $key): bool {
        $st = pn_db()->prepare('select count(*) from login_attempts where key = ? and at > ?');
        $st->execute([$key, pn_now() - self::LOCK]);
        return (int) $st->fetchColumn() >= self::MAX_FAILS;
    }
    public static function login(string $login, string $pass): bool {
        pn_session(); self::$err = '';
        $keys = ['login:' . mb_strtolower(trim($login)), 'ip:' . pn_ip()];
        foreach ($keys as $k) if (self::locked($k)) { self::$err = 'Слишком много попыток, попробуйте через 15 минут'; return false; }
        $st = pn_db()->prepare('select * from users where login = ?');
        $st->execute([trim($login)]);
        $u = $st->fetch();
        if (!$u || !password_verify($pass, $u['password_hash'])) {
            $ins = pn_db()->prepare('insert into login_attempts(key, at) values (?, ?)');
            foreach ($keys as $k) $ins->execute([$k, pn_now()]);
            self::$err = 'Неверный логин или пароль';
            return false;
        }
        pn_db()->prepare('delete from login_attempts where key = ?')->execute([$keys[0]]);
        if (PHP_SAPI !== 'cli') session_regenerate_id(true);
        $_SESSION['uid'] = (int) $u['id']; $_SESSION['since'] = $_SESSION['seen'] = pn_now();
        $_SESSION['weak'] = pn_password_weak($pass, (string) $u['login']);   // напомнить сменить пароль
        return true;
    }
    public static function logout(): void { pn_session(); $_SESSION = []; if (PHP_SAPI !== 'cli' && session_status() === PHP_SESSION_ACTIVE) session_destroy(); }
    public static function user(): ?array {
        pn_session();
        if (empty($_SESSION['uid'])) return null;
        $now = pn_now();
        if ($now - (int) ($_SESSION['seen'] ?? 0) > self::IDLE || $now - (int) ($_SESSION['since'] ?? 0) > self::MAX_AGE) { self::logout(); return null; }
        $_SESSION['seen'] = $now;
        $st = pn_db()->prepare('select id, login, role from users where id = ?');
        $st->execute([$_SESSION['uid']]);
        return $st->fetch() ?: null;
    }
    // Без входа — 302 на страницу входа; не та роль — 403.
    public static function require(string $role = 'manager'): array {
        $u = self::user();
        if (!$u) throw new PnHttp(302, ['Location' => '/admin/login']);
        if ($role === 'admin' && $u['role'] !== 'admin') throw new PnHttp(403, [], 'Раздел доступен только администратору');
        return $u;
    }
}

function audit(string $action, string $entity, ?int $id, array $diff = []): void {
    $u = $_SESSION['uid'] ?? null;
    pn_db()->prepare('insert into audit(user_id, action, entity, entity_id, diff) values (?,?,?,?,?)')
        ->execute([$u, $action, $entity, $id, $diff ? pn_json_enc($diff) : null]);
}
