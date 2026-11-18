// ипотека: полоса и сравнение программ
const PROGS = PN.progs();
function calcExtra() {
  const P = +$('#cp').value, d = +$('#cd').value, y = +$('#ct').value, r = +$('#rates [aria-pressed=true]').dataset.r, L = P * (1 - d / 100), n = y * 12;
  const pm = rr => { const m = rr / 1200; return m ? L * m / (1 - Math.pow(1 + m, -n)) : L / n; }, over = pm(r) * n - L;
  $('#cbL').style.width = L / (L + over) * 100 + '%'; $('#cbO').style.width = over / (L + over) * 100 + '%';
  $('#cbLv').textContent = fmtM(L); $('#cbOv').textContent = fmtM(over);
  $('#cprog').innerHTML = PROGS.map(([nm, rr]) => `<button type="button" data-r="${rr}" aria-pressed="${rr === r}"><small>${nm} · ${rr} %</small><b>${Math.round(pm(rr)).toLocaleString('ru-RU')} ₽</b></button>`).join('');
  $$('#cprog button').forEach(b => b.addEventListener('click', () => $(`#rates [data-r="${b.dataset.r}"]`).click()));
}
new MutationObserver(calcExtra).observe($('#loan'), {childList: true, characterData: true, subtree: true});
calcExtra();

