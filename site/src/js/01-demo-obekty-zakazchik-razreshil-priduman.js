// демо-объекты: заказчик разрешил придуманные данные до запуска
const prep = (it, i) => ({...it, id: it.id ?? i, disc: it.disc || 0, ppm: Math.round(it.p / it.s)});
const ITEMS = PN.items().map(prep);                    // на главной: все квартиры или подборка (PN.capped())
const ALL = PN.capped() ? PN.all() : ITEMS;            // для счётчиков — все опубликованные
const EXTRA = [];                                      // квартиры не из подборки: избранное, сравнение, «Вы смотрели», ссылка #obj-N
const itemById = id => ITEMS.find(x => x.id === +id) || EXTRA.find(x => x.id === +id);
function itemsEnsure(ids, done) {
  const miss = [...ids].map(Number).filter(id => id >= 0 && !itemById(id));
  if (!miss.length || !PN.capped()) { done(); return; }
  fetch(PN.api + 'items?ids=' + miss.slice(0, 50).join(','), {headers: {Accept: 'application/json'}}).then(r => r.ok ? r.json() : [])
    .then(a => a.forEach(it => { if (!itemById(it.id)) EXTRA.push(prep(it)); })).catch(() => {}).finally(done);
}
const catalogUrl = q => 'kvartiry/' + (q && q.toString() ? '?' + q : '');
const head = it => `${it.r ? it.r + '-комн. квартира' : 'Студия'} · ${it.s.toLocaleString('ru-RU')} м²`;
const title = it => `${it.r ? it.r + '-комн. квартира' : 'Студия'}, ${it.s.toLocaleString('ru-RU')} м², ${it.fl}/${it.fls} этаж`;
const FILTERS = {
  best: ['Самые выгодные', it => it.disc || it.special],
  done: ['Сданные дома', it => it.t === 'new' && !it.due],
  fin: ['С отделкой или ремонтом', it => it.fin !== 'Без отделки'],
  fam: ['Под семейную ипотеку', it => it.t === 'new'],
  sec: ['Вторичка', it => it.t === 'sec'],
};
const CHECKS = {
  dev: [['Разрешение на строительство', 'документы'], ['Проектная декларация и эскроу-счета', 'ЕИСЖС'], ['Прошлые дома сданы в срок', 'история'], ['Нет банкротных и крупных судебных дел', 'суды'], ['Отзывы жильцов сданных домов', 'люди']],
  sec: [['Собственники и доли', 'Росреестр'], ['Обременения и аресты', 'выписка'], ['История переходов права', 'юрист'], ['Долги по коммунальным платежам', 'справки'], ['Перепланировки', 'план БТИ']],
  our: [['Замер и смета до начала работ', 'выезд'], ['Предварительный договор', 'документы'], ['Промежуточный акт на каждый этап', 'приёмка'], ['Камера на объекте в личном кабинете', '24/7'], ['Гарантия на работы', '5 лет']],
};
function showChecks(k) { $('#clist').innerHTML = CHECKS[k].map(([a, b]) => `<li>${a}<span>${b}</span></li>`).join(''); }
showChecks('dev');
$$('.ctabs button').forEach(b => b.addEventListener('click', () => { $$('.ctabs button').forEach(x => x.setAttribute('aria-pressed', x === b)); showChecks(b.dataset.k); scanStart(); }));

