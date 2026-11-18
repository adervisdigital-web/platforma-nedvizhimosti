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
})();
