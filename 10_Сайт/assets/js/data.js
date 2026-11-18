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
    demo: !!D.demo,
    api: D.api || 'api/',
  };
  // Витрина на GitHub Pages: заявки никуда не уходят — после «принято» прототипа говорим об этом честно.
  if (D.demo) {
    const note = () => setTimeout(() => window.toast && toast('Это демо-версия сайта: заявка никуда не отправлена'), 1600);
    document.addEventListener('submit', e => { if (['leadForm', 'hbCb'].includes(e.target.id)) note(); }, true);
    document.addEventListener('click', e => { if (e.target.closest && e.target.closest('#bkGo')) note(); }, true);
  }
})();
