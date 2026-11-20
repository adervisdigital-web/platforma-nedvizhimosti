-- Загрузка квартир из XML-фидов в формате Яндекс.Недвижимости (фиды застройщиков, База.ПРО Н-маркет).
CREATE TABLE feeds (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, url TEXT NOT NULL,
  developer_id INTEGER REFERENCES developers(id) ON DELETE SET NULL,     -- фид одного застройщика: всем его ЖК ставим этого застройщика
  only_verified INTEGER NOT NULL DEFAULT 1,                             -- показывать только квартиры застройщиков с отметкой «Проверен»
  enabled INTEGER NOT NULL DEFAULT 1,
  last_run_at TEXT, last_ok_at TEXT, last_status TEXT, last_stats TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')));

ALTER TABLE apartments ADD COLUMN feed_id INTEGER REFERENCES feeds(id) ON DELETE SET NULL;
ALTER TABLE apartments ADD COLUMN feed_state TEXT;                       -- active — есть в последней выгрузке, gone — пропала (продана/снята)
ALTER TABLE apartments ADD COLUMN feed_seen_at TEXT;
ALTER TABLE apartments ADD COLUMN feed_media TEXT NOT NULL DEFAULT '[]'; -- [[тег, ключ картинки], …] из последней выгрузки
ALTER TABLE apartments ADD COLUMN feed_manual INTEGER NOT NULL DEFAULT 0; -- менеджер сам включил/снял с сайта — загрузка публикацию не трогает
ALTER TABLE apartments ADD COLUMN feed_own_media INTEGER NOT NULL DEFAULT 0; -- менеджер менял фото/планировки — загрузка их не трогает
ALTER TABLE complexes ADD COLUMN external_id TEXT;
ALTER TABLE complexes ADD COLUMN feed_media TEXT NOT NULL DEFAULT '[]';
CREATE INDEX apartments_feed ON apartments (feed_id, feed_state);

-- Картинки из фидов: скачиваются к нам (WebP), одна и та же картинка — один раз.
CREATE TABLE feed_images (
  key TEXT PRIMARY KEY, url TEXT NOT NULL, img TEXT, status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new','ok','err')),
  tries INTEGER NOT NULL DEFAULT 0, updated_at TEXT NOT NULL DEFAULT (datetime('now')));
