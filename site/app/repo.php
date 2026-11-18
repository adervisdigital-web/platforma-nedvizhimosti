<?php
// Выборки из базы в той же форме, что data/seed/*.json, — чтобы pn_page_data() и шаблоны не зависели от источника.
final class Repo {
    private static function dec(?string $j) { return $j === null || $j === '' ? null : json_decode($j, true, 512, JSON_THROW_ON_ERROR); }

    public static function apartments(bool $onlyPublished = true): array {
        $sql = 'select a.*, c.name as complex, coalesce(a.district, c.district) as district from apartments a left join complexes c on c.id = a.complex_id'
            . ($onlyPublished ? ' where a.published = 1' : '') . ' order by a.id';
        return array_map([self::class, 'apt'], pn_db()->query($sql)->fetchAll());
    }
    public static function apartment(string $slug): ?array {
        $st = pn_db()->prepare('select a.*, c.name as complex, coalesce(a.district, c.district) as district, c.checks as complex_checks, c.slug as complex_slug
            from apartments a left join complexes c on c.id = a.complex_id where a.slug = ? and a.published = 1');
        $st->execute([$slug]);
        $r = $st->fetch();
        if (!$r) return null;
        $a = self::apt($r);
        $a['complex_checks'] = self::dec($r['complex_checks']) ?? [];
        $a['complex_slug'] = $r['complex_slug'];
        $a['description'] = $r['description'];
        return $a;
    }
    private static function apt(array $r): array {
        return ['id' => (int) $r['id'], 'rooms' => (int) $r['rooms'], 'area' => pn_num($r['area']), 'floor' => (int) $r['floor'], 'floors' => (int) $r['floors'],
            'complex' => $r['complex'], 'address' => $r['address'], 'district' => $r['district'], 'market' => $r['market'], 'price' => (int) $r['price'],
            'discount_pct' => (int) $r['discount_pct'], 'finish' => $r['finish'], 'finish_label' => $r['finish_label'], 'house_status' => $r['house_status'],
            'due' => (int) $r['due'], 'special' => (int) $r['special'], 'photos' => self::dec($r['photos']) ?? [], 'map_x' => pn_num($r['map_x']),
            'map_y' => pn_num($r['map_y']), 'published' => (int) $r['published'], 'source' => $r['source'], 'external_id' => $r['external_id'], 'slug' => $r['slug']];
    }
    public static function complexes(): array {
        return array_map(fn($c) => ['name' => $c['name'], 'slug' => $c['slug'], 'district' => $c['district'], 'developer' => $c['developer'],
            'checks' => self::dec($c['checks']) ?? [], 'lat' => $c['lat'], 'lng' => $c['lng']],
            pn_db()->query('select c.*, d.name as developer from complexes c left join developers d on d.id = c.developer_id order by c.id')->fetchAll());
    }
    // Дома — в форме прототипа (id = код для якорей #house-<id>).
    public static function houses(bool $onlyPublished = true): array {
        return array_map([self::class, 'house_proto'], pn_db()->query('select * from houses' . ($onlyPublished ? ' where published = 1' : '') . ' order by sort, id')->fetchAll());
    }
    public static function house(string $slug): ?array {
        $st = pn_db()->prepare('select * from houses where slug = ? and published = 1');
        $st->execute([$slug]);
        $r = $st->fetch();
        return $r ? self::house_proto($r) + ['price_from' => $r['price_from'] === null ? null : (int) $r['price_from'], 'area' => pn_num($r['area'])] : null;
    }
    private static function house_proto(array $h): array {
        return ['id' => $h['code'], 'line' => $h['line'], 'n' => (int) $h['number'], 'motto' => $h['motto'], 'c' => $h['color'], 'fl' => (int) $h['floors'],
            'rooms' => $h['rooms'], 'ceil' => $h['ceiling'], 'feats' => self::dec($h['features']) ?? [], 'idea' => $h['idea'], 'text' => self::dec($h['text']) ?? [],
            'ph' => self::dec($h['photos']) ?? [], 'plans' => self::dec($h['plans']) ?? [], 'slug' => $h['slug'], 'sort' => (int) $h['sort']];
    }
    public static function reviews(): array {
        return array_map(fn($r) => ['name' => $r['name'], 'text' => $r['text'], 'about' => $r['about'], 'tag' => $r['tag'], 'photo' => $r['photo'],
            'rating' => (int) $r['rating'], 'is_demo' => (int) $r['is_demo'], 'published' => (int) $r['published']],
            pn_db()->query('select * from reviews order by sort, id')->fetchAll());
    }
    // Все настройки (с секретами) — только для серверного кода. Наружу — через pn_public_settings().
    public static function settingsAll(): array {
        $o = [];
        foreach (pn_db()->query('select key, value from settings')->fetchAll() as $r) $o[$r['key']] = self::dec($r['value']);
        return $o;
    }
    public static function settings(): array { return pn_public_settings(self::settingsAll()); }
}

function pn_db_source(): array {
    $all = Repo::settingsAll();
    return ['apartments' => Repo::apartments(), 'complexes' => Repo::complexes(), 'houses' => Repo::houses(), 'reviews' => Repo::reviews(),
        'settings' => $all, 'faq' => $all['faq'] ?? [], 'quick' => $all['quick'] ?? []];
}
