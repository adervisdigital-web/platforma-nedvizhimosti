<?php
// Разбор и проверка полей форм админки.
// Типы полей: text, textarea, int, number, select, bool, lines (список строк), paras (абзацы через пустую строку),
// pairs (строки «подпись | фото»), photos (список фото из виджета + загрузки), photo (одно фото), secret (пустое — не менять).

// «58,4» → 58.4, «9 450 000 ₽» → 9450000.0, «» или мусор → null.
function forms_number(?string $raw): ?float {
    $s = preg_replace('/[\s\x{00A0}\x{202F}₽%]+/u', '', (string) $raw);
    $s = str_replace(',', '.', $s);
    return $s !== '' && is_numeric($s) ? (float) $s : null;
}

function forms_lines(string $raw): array { return array_values(array_filter(array_map('trim', preg_split('/\R/u', $raw)), 'strlen')); }

// Фото из виджета (порядок — как в форме, отмеченные «удалить» — убраны) + новые загрузки.
function forms_photos(array $post, array $files, string $name, array &$errors): array {
    $keep = array_values(array_filter(array_map('strval', (array) ($post[$name] ?? [])), fn($p) => preg_match('~^[a-z0-9_/-]+$~i', $p)));
    $del = array_map('strval', (array) ($post[$name . '_del'] ?? []));
    $keep = array_values(array_diff($keep, $del));
    $up = $files[$name === 'photos' ? 'upload' : $name . '_upload'] ?? null;
    if ($up && is_array($up['name'] ?? null)) {
        foreach ($up['name'] as $i => $orig) {
            if (($up['error'][$i] ?? UPLOAD_ERR_NO_FILE) === UPLOAD_ERR_NO_FILE) continue;
            $e = $up['error'][$i] ?? 0;
            if ($e === UPLOAD_ERR_INI_SIZE || $e === UPLOAD_ERR_FORM_SIZE) { $errors[$name] = 'Фото «' . $orig . '» больше, чем разрешает сервер (' . pn_ini_mb('upload_max_filesize') . ' МБ)'; continue; }
            if ($e !== UPLOAD_ERR_OK) { $errors[$name] = 'Фото «' . $orig . '» не загрузилось — попробуйте ещё раз'; continue; }
            try { $keep[] = pn_image_store($up['tmp_name'][$i], (string) $orig)['id']; }
            catch (InvalidArgumentException $e) { $errors[$name] = '«' . $orig . '»: ' . $e->getMessage(); }
        }
    }
    return $keep;
}

// $fields: [имя => ['label', 'type', 'req' => bool, 'opts' => [значение => подпись], 'min', 'max']]. Возвращает ['data', 'errors'].
function forms_parse(array $fields, array $post, array $files = [], array $old = []): array {
    $data = []; $err = [];
    foreach ($fields as $name => $f) {
        $t = $f['type']; $raw = $post[$name] ?? null; $label = $f['label'];
        switch ($t) {
            case 'int': case 'number':
                $v = forms_number(is_array($raw) ? '' : (string) $raw);
                if ($v === null && trim((string) $raw) !== '') { $err[$name] = "«{$label}»: нужно число"; break; }
                if ($v !== null && $t === 'int') $v = (int) round($v);
                if ($v !== null && isset($f['min']) && $v < $f['min']) $err[$name] = "«{$label}»: не меньше {$f['min']}";
                if ($v !== null && isset($f['max']) && $v > $f['max']) $err[$name] = "«{$label}»: не больше {$f['max']}";
                $data[$name] = $v; break;
            case 'bool': $data[$name] = !empty($raw) ? 1 : 0; break;
            case 'select':
                $v = (string) $raw; $data[$name] = $v === '' ? null : $v;
                if ($v !== '' && !array_key_exists($v, $f['opts'])) $err[$name] = "«{$label}»: выберите из списка";
                break;
            case 'lines': $data[$name] = forms_lines((string) $raw); break;
            case 'paras': $data[$name] = array_values(array_filter(array_map(fn($p) => trim(preg_replace('/\s*\R\s*/u', ' ', $p)), preg_split('/\R\s*\R/u', (string) $raw)), 'strlen')); break;
            case 'pairs': $data[$name] = array_map(fn($l) => array_map('trim', array_pad(explode('|', $l, 2), 2, '')), forms_lines((string) $raw)); break;
            case 'photos': $data[$name] = forms_photos($post, $files, $name, $err); break;
            case 'secret': $data[$name] = trim((string) $raw) === '' ? ($old[$name] ?? '') : trim((string) $raw); break;
            default: $data[$name] = trim((string) $raw);
        }
        $empty = $data[$name] === null || $data[$name] === '' || $data[$name] === [];
        if (!empty($f['req']) && $empty && !isset($err[$name])) $err[$name] = $f['req'] === true ? "Заполните «{$label}»" : $f['req'];
    }
    return ['data' => $data, 'errors' => $err];
}

function forms_apartment(array $post, array $files = []): array {
    $r = forms_parse(pn_entities()['apartments']['fields'], $post, $files);
    $d = &$r['data']; $e = &$r['errors'];
    if (($d['market'] ?? '') === 'new' && empty($d['complex_id'])) $e['complex_id'] = 'Выберите ЖК';
    if (($d['market'] ?? '') === 'secondary' && empty($d['address'])) $e['address'] = 'Для вторички укажите адрес';
    if (!isset($e['floor'], $e['floors']) && $d['floor'] !== null && $d['floors'] !== null && $d['floor'] > $d['floors']) $e['floor'] = 'Этаж больше, чем этажей в доме';
    if (!empty($d['published']) && !$d['photos']) $e['photos'] = 'Чтобы опубликовать, добавьте хотя бы одно фото';
    $d['finish_label'] = ($d['finish'] ?? 'with') === 'without' ? 'Без отделки' : ($d['finish_label'] ?: 'С отделкой');
    $d['discount_pct'] = (int) ($d['discount_pct'] ?? 0);
    $d['due'] = (int) ($d['due'] ?? 0);
    return $r;
}
