// ипотечный калькулятор
const fmt = n => Math.round(n).toLocaleString('ru-RU') + ' ₽';
function calc() {
  const P = +$('#cp').value, d = +$('#cd').value, y = +$('#ct').value, r = +$('#rates [aria-pressed=true]').dataset.r;
  const L = P * (1 - d / 100), m = r / 1200, n = y * 12, pay = m ? L * m / (1 - Math.pow(1 + m, -n)) : L / n;
  $('#cpv').textContent = fmt(P); $('#cdv').textContent = d + ' % · ' + fmt(P * d / 100); $('#ctv').textContent = y + ' лет';
  $('#pay').innerHTML = Math.round(pay).toLocaleString('ru-RU') + ' <small>₽/мес</small>'; $('#loan').textContent = fmt(L); $('#over').textContent = fmt(pay * n - L); $('#inc').textContent = fmt(pay / .5);
}
['#cp', '#cd', '#ct'].forEach(s => $(s).addEventListener('input', calc));
$$('#rates button').forEach(b => b.addEventListener('click', () => { $$('#rates button').forEach(x => x.setAttribute('aria-pressed', x === b)); calc(); }));
calc();

$('#baR').addEventListener('input', e => { const v = e.target.value; $('#baBox .after').style.clipPath = `inset(0 0 0 ${v}%)`; $('#baH').style.left = v + '%'; });
const vbtns = $$('.view button');
function setView(v) { $('#cards').classList.toggle('grid', v === 'grid'); vbtns.forEach(b => b.setAttribute('aria-pressed', b.dataset.v === v)); }
vbtns.forEach(b => b.addEventListener('click', () => setView(b.dataset.v)));
setView(innerWidth >= 1700 ? 'grid' : 'list');

