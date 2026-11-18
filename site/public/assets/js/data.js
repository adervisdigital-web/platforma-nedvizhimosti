// Слой данных сайта: читает встроенный JSON (#pn-data). Одинаково работает на сервере и в статической сборке.
(() => {
  const el = document.getElementById('pn-data');
  let D = {};
  try { D = el ? JSON.parse(el.textContent) : {}; } catch (e) { console.error('pn-data', e); }
  window.PN = {
    items: () => D.items || [],
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
