-- Подробности квартиры для её страницы: площади, потолки, санузел, балкон, вид, планировки (список картинок).
ALTER TABLE apartments ADD COLUMN living_area REAL;
ALTER TABLE apartments ADD COLUMN kitchen_area REAL;
ALTER TABLE apartments ADD COLUMN ceiling REAL;
ALTER TABLE apartments ADD COLUMN bathroom TEXT;
ALTER TABLE apartments ADD COLUMN balcony TEXT;
ALTER TABLE apartments ADD COLUMN view TEXT;
ALTER TABLE apartments ADD COLUMN plans TEXT NOT NULL DEFAULT '[]';
