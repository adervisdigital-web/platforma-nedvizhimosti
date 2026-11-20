// подбор за 3 шага
let qs = 1, qType = 'flat';
const Q2 = {
  flat: {l: 'Какой бюджет на квартиру?', bl: 'Бюджет до', min: 3, max: 20, step: .5, v: 9, rooms: true},
  house: {l: 'Какой бюджет на дом?', bl: 'Бюджет до', min: 10, max: 40, step: 1, v: 20},
  reno: {l: 'Какая площадь квартиры?', bl: 'Площадь', min: 20, max: 160, step: 1, v: 55},
  mort: {l: 'Сколько стоит квартира?', bl: 'Стоимость', min: 3, max: 20, step: .5, v: 8},
};
function qMatch() {
  const c = Q2[qType], v = +$('#qb').value, mil = v * 1e6;
  $('#qbv').textContent = qType === 'reno' ? v + ' м²' : v.toLocaleString('ru-RU') + ' млн ₽';
  let t;
  if (qType === 'flat') {
    const rooms = $$('#qr [aria-pressed=true]').map(b => +b.dataset.r);
    const n = ALL.filter(it => it.p <= mil && (!rooms.length || rooms.some(r => r === 4 ? it.r >= 4 : it.r === r))).length;
    t = n ? `Подходит <b>${n} ${plural(n, 'квартира', 'квартиры', 'квартир')}</b> из проверенных. Пришлём их и новые, как только появятся.` : 'Сейчас таких нет — подберём под ваши условия и сообщим первыми.';
  } else if (qType === 'house') {
    const ok = HOUSES.filter(h => hFrom(h) <= mil);
    t = ok.length ? `Укладываются: <b>${ok.map(h => h.line + ' ' + h.n).join(', ')}</b>. Остаток — равными платежами без процентов до 5 лет.` : 'Подберём площадь и материал под ваш бюджет — проекты настраиваются.';
  } else if (qType === 'reno') {
    t = `Ориентир с материалами: <b>от ${fmtM(v * 20000)}</b> за базовую отделку до ${fmtM(v * 100000)} за премиум. Точную цену даст смета после замера.`;
  } else {
    const fp = PN.mort.def(true);
    t = `По семейной ипотеке (${PN.mort.terms(fp).rate} % с одним ребёнком, с двумя и больше — ниже) со взносом 20 % на 30 лет: <b>от ${Math.round(PN.mort.pay(mil, 20, 30, fp).pay).toLocaleString('ru-RU')} ₽/мес</b>. Подберём банк с индивидуальной ставкой.`;
  }
  $('#qMatch').innerHTML = t;
  $('#qr').hidden = !c.rooms;
}
function qSet(type) {
  qType = type; const c = Q2[type], r = $('#qb');
  Object.assign(r, {min: c.min, max: c.max, step: c.step}); r.value = c.v;
  $('#q2l').textContent = c.l; $('#qbl').textContent = c.bl; qMatch(); fillAll();
}
function qGo(n) {
  qs = n; $$('#leadForm fieldset').forEach(f => f.classList.toggle('on', +f.dataset.s === n));
  $('#qStep').textContent = `Шаг ${n} из 3`; $$('.qd i').forEach((d, i) => d.classList.toggle('on', i < n));
  $('#qBack').hidden = n === 1; $('#qNext').hidden = n === 3; $('#qSend').hidden = n !== 3;
  if (n === 3) $('#ln').focus();
}
$$('#leadForm .ch button').forEach(b => b.addEventListener('click', () => qSet(b.dataset.q)));
$$('#qr button').forEach(b => b.addEventListener('click', () => { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true'); qMatch(); }));
$('#qb').addEventListener('input', qMatch);
$('#qNext').addEventListener('click', () => qGo(qs + 1));
$('#qBack').addEventListener('click', () => qGo(qs - 1));
qSet('flat');

