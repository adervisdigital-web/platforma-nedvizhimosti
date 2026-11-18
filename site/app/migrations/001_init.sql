-- Схема по спецификации 2026-11-18 + решения: market/address у квартир, code у домов (якоря #house-<code> прототипа).
CREATE TABLE developers (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, site TEXT, verified INTEGER NOT NULL DEFAULT 0);
CREATE TABLE complexes (
  id INTEGER PRIMARY KEY, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL, district TEXT,
  developer_id INTEGER REFERENCES developers(id) ON DELETE SET NULL, address TEXT, lat REAL, lng REAL,
  checks TEXT NOT NULL DEFAULT '[]', photos TEXT NOT NULL DEFAULT '[]');
CREATE TABLE apartments (
  id INTEGER PRIMARY KEY, slug TEXT NOT NULL UNIQUE, market TEXT NOT NULL CHECK (market IN ('new','secondary')),
  rooms INTEGER NOT NULL, area REAL NOT NULL, floor INTEGER NOT NULL, floors INTEGER NOT NULL,
  complex_id INTEGER REFERENCES complexes(id) ON DELETE RESTRICT, address TEXT, district TEXT,
  price INTEGER NOT NULL CHECK (price > 0), discount_pct INTEGER NOT NULL DEFAULT 0,
  finish TEXT NOT NULL CHECK (finish IN ('with','without')), finish_label TEXT, house_status TEXT, due INTEGER NOT NULL DEFAULT 0,
  special INTEGER NOT NULL DEFAULT 0, photos TEXT NOT NULL DEFAULT '[]', description TEXT,
  lat REAL, lng REAL, map_x REAL, map_y REAL, published INTEGER NOT NULL DEFAULT 0,
  source TEXT NOT NULL DEFAULT 'manual' CHECK (source IN ('manual','feed')), external_id TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')), updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (source, external_id));
CREATE TABLE houses (
  id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE, slug TEXT NOT NULL UNIQUE, line TEXT NOT NULL, number INTEGER NOT NULL,
  area REAL, motto TEXT, color TEXT, floors INTEGER, rooms TEXT, ceiling TEXT, features TEXT NOT NULL DEFAULT '[]',
  idea TEXT, text TEXT NOT NULL DEFAULT '[]', photos TEXT NOT NULL DEFAULT '[]', plans TEXT NOT NULL DEFAULT '[]',
  price_from INTEGER, sort INTEGER NOT NULL DEFAULT 0, published INTEGER NOT NULL DEFAULT 1);
CREATE TABLE reviews (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, text TEXT NOT NULL, about TEXT, tag TEXT, photo TEXT, rating INTEGER NOT NULL DEFAULT 5,
  topic TEXT CHECK (topic IN ('apartment','house','renovation')), is_demo INTEGER NOT NULL DEFAULT 0,
  published INTEGER NOT NULL DEFAULT 1, sort INTEGER NOT NULL DEFAULT 0);
CREATE TABLE leads (
  id INTEGER PRIMARY KEY, created_at TEXT NOT NULL DEFAULT (datetime('now')),
  kind TEXT NOT NULL CHECK (kind IN ('quiz','callback','viewing','chat')), want TEXT, budget TEXT, area TEXT, name TEXT,
  phone TEXT NOT NULL, object_ref TEXT, slot TEXT, ip_hash TEXT,
  status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new','work','closed')), note TEXT,
  delivered_tg INTEGER NOT NULL DEFAULT 0, delivered_mail INTEGER NOT NULL DEFAULT 0, delivered_crm INTEGER NOT NULL DEFAULT 0,
  attempts INTEGER NOT NULL DEFAULT 0);
CREATE INDEX leads_ip ON leads (ip_hash, created_at);
CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE users (id INTEGER PRIMARY KEY, login TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('admin','manager')), created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE audit (id INTEGER PRIMARY KEY, user_id INTEGER, at TEXT NOT NULL DEFAULT (datetime('now')), action TEXT NOT NULL,
  entity TEXT NOT NULL, entity_id INTEGER, diff TEXT);
