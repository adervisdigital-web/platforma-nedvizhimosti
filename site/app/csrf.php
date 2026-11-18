<?php
// Защита форм админки от подделки запросов: токен в сессии + скрытое поле _csrf.
function csrf_token(): string {
    pn_session();
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(16));
}
function csrf_field(): string { return '<input type="hidden" name="_csrf" value="' . csrf_token() . '">'; }
function csrf_check(array $post): void {
    if (!hash_equals(csrf_token(), (string) ($post['_csrf'] ?? ''))) throw new PnHttp(403, [], 'Форма устарела — обновите страницу и попробуйте снова');
}
