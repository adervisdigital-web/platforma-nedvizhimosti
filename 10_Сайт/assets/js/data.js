// Слой данных сайта: читает встроенный JSON (#pn-data). Одинаково работает на сервере и в статической сборке.
(() => {
  const el = document.getElementById('pn-data');
  let D = {};
  try { D = el ? JSON.parse(el.textContent) : {}; } catch (e) { console.error('pn-data', e); }
  window.PN = {
    items: () => D.items || [],
    total: () => D.total ?? (D.items || []).length,
    capped: () => !!D.capped,                        // на главной — подборка, весь список — в каталоге
    // все квартиры для счётчиков (поиск, районы, ЖК, плитки); при подборке — из компактного индекса
    all: () => !D.all ? (D.items || []) : D.all.rows.map(([t, r, p, f, due, di, zi, disc, sp]) =>
      ({t, r, p, fin: f ? 'С отделкой' : 'Без отделки', due, d: D.all.d[di], zk: D.all.z[zi], disc, special: sp})),
    houses: () => D.houses || [],
    reviews: () => D.reviews || [],
    faq: () => (D.faq || []).map(([src, flags, answer]) => [new RegExp(src, flags), answer]),
    quick: () => D.quick || [],
    progs: () => D.progs || [],
    geo: () => D.geo || {},
    settings: () => D.settings || {},
    // Путь к фото: загруженные в админке ('u/ГГГГММ/id') — WebP из uploads/, фото прототипа — JPG из assets/img/<папка>/.
    img: (name, folder = '', w = 960) => String(name).startsWith('u/') ? `uploads/${String(name).slice(2)}-${w}.webp` : `assets/img/${folder ? folder + '/' : ''}${name}.jpg`,
    demo: !!D.demo,
    api: D.api || 'api/',
  };
  // Ипотека по правилам из админки (как app/mortgage.php): лимит льготной части, сверх лимита — рыночная ставка;
  // у семейной ставка и лимит — по числу детей. pay(цена, взнос %, лет, программа, детей) → {pay, loan, over, parts: [[сумма, ставка]]}.
  PN.mort = (() => {
    const c = Object.assign({progs: [], tiers: [], market: 20, date: null}, D.mort || {});
    const ann = (L, r, n) => L <= 0 ? 0 : r > 0 ? L * (r / 1200) / (1 - Math.pow(1 + r / 1200, -n)) : L / n;
    const terms = (p, kids = 1) => {
      if (p && p.family && c.tiers.length) {
        let t = null; c.tiers.forEach(x => { if (x.kids <= Math.max(1, kids) && (!t || x.kids > t.kids)) t = x; });
        if (t) return {rate: +t.rate, limit: t.limit || null};
      }
      return {rate: +(p ? p.rate : c.market), limit: p && p.limit || null};
    };
    const pay = (price, down, years, p, kids = 1) => {
      const L = price * (1 - down / 100), n = years * 12, t = terms(p, kids);
      const parts = t.limit && L > t.limit ? [[t.limit, t.rate], [L - t.limit, +c.market]] : [[L, t.rate]];
      const m = parts.reduce((s, [a, r]) => s + ann(a, r, n), 0);
      return {pay: m, loan: L, over: m * n - L, parts};
    };
    const def = isNew => (isNew ? c.progs.find(p => p.family) : c.progs.find(p => /рыноч/i.test(p.name))) || c.progs[c.progs.length - 1] || {name: 'Рыночная', rate: c.market};
    const date = () => c.date ? c.date.split('-').reverse().join('.') : '';
    return {cfg: c, ann, terms, pay, def, date};
  })();
  // Отправка заявки: на витрине (demo) — никуда, честно говорим об этом; на сервере — POST api/lead.
  const T0 = Math.floor(Date.now() / 1000);
  const say = m => setTimeout(() => window.toast && toast(m), 1600);
  PN.send = (fields, onOk = () => {}, onFail = () => {}) => {
    if (D.demo) { onOk({ok: true, demo: true}); say('Это демо-версия сайта: заявка никуда не отправлена'); return; }
    const hp = (document.getElementById('pnHp') || {}).value || '';
    fetch(PN.api + 'lead', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({...fields, consent: 1, hp, t0: T0})})
      .then(r => r.json())
      .catch(() => ({ok: false, message: 'Нет связи с сервером — позвоните нам: ' + ((D.settings || {}).phone || '')}))
      .then(r => { if (r.ok) onOk(r); else { window.toast && toast(r.message || 'Заявка не отправлена — позвоните нам'); onFail(r); } });
  };
})();
