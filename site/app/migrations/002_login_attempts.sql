-- Неудачные попытки входа: блокировка 15 минут после 5 ошибок (по логину и по IP).
CREATE TABLE login_attempts (key TEXT NOT NULL, at INTEGER NOT NULL);
CREATE INDEX login_attempts_key ON login_attempts (key, at);
