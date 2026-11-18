// ипотечный калькулятор
const fmt = n => Math.round(n).toLocaleString('ru-RU') + ' ₽';
const kidsOf = () => +(($('#kids [aria-pressed=true]') || {dataset: {k: 1}}).dataset.k);
const progSel = () => PN.mort.cfg.progs[+(($('#rates [aria-pressed=true]') || {dataset: {p: 0}}).dataset.p)] || PN.mort.def(true);
function calc() {
  const P = +$('#cp').value, d = +$('#cd').value, y = +$('#ct').value, pr = progSel(), res = PN.mort.pay(P, d, y, pr, kidsOf());
  const L = res.loan, n = y * 12, pay = res.pay;
  if ($('#kids')) $('#kids').hidden = !pr.family;
  if ($('#cparts')) $('#cparts').innerHTML = res.parts.length > 1
    ? `${fmtM(res.parts[0][0])} под ${String(res.parts[0][1]).replace('.', ',')} % + ${fmtM(res.parts[1][0])} под ${String(res.parts[1][1]).replace('.', ',')} % — сверх лимита программы банк даёт по рыночной ставке`
    : `${pr.name}: ${String(res.parts[0][1]).replace('.', ',')} % на всю сумму`;
  $('#cpv').textContent = fmt(P); $('#cdv').textContent = d + ' % · ' + fmt(P * d / 100); $('#ctv').textContent = y + ' лет';
  $('#pay').innerHTML = Math.round(pay).toLocaleString('ru-RU') + ' <small>₽/мес</small>'; $('#loan').textContent = fmt(L); $('#over').textContent = fmt(pay * n - L); $('#inc').textContent = fmt(pay / .5);
}
['#cp', '#cd', '#ct'].forEach(s => $(s).addEventListener('input', calc));
$$('#rates button').forEach(b => b.addEventListener('click', () => { $$('#rates button').forEach(x => x.setAttribute('aria-pressed', x === b)); calc(); }));
$$('#kids button').forEach(b => b.addEventListener('click', () => { $$('#kids button').forEach(x => x.setAttribute('aria-pressed', x === b)); calc(); }));
calc();

$('#baR').addEventListener('input', e => { const v = e.target.value; $('#baBox .after').style.clipPath = `inset(0 0 0 ${v}%)`; $('#baH').style.left = v + '%'; });
const vbtns = $$('.view button');
function setView(v) { $('#cards').classList.toggle('grid', v === 'grid'); vbtns.forEach(b => b.setAttribute('aria-pressed', b.dataset.v === v)); }
vbtns.forEach(b => b.addEventListener('click', () => setView(b.dataset.v)));
setView(innerWidth >= 1700 ? 'grid' : 'list');

