// ипотека: полоса и сравнение программ
const PROGS = PN.progs();
function calcExtra() {
  const P = +$('#cp').value, d = +$('#cd').value, y = +$('#ct').value, sel = progSel(), L = P * (1 - d / 100), n = y * 12, k = kidsOf();
  const pm = p => PN.mort.pay(P, d, y, p, k).pay, over = pm(sel) * n - L;
  $('#cbL').style.width = L / (L + over) * 100 + '%'; $('#cbO').style.width = over / (L + over) * 100 + '%';
  $('#cbLv').textContent = fmtM(L); $('#cbOv').textContent = fmtM(over);
  $('#cprog').innerHTML = PN.mort.cfg.progs.map((p, i) => `<button type="button" data-p="${i}" aria-pressed="${p === sel}"><small>${p.name} · ${String(PN.mort.terms(p, k).rate).replace('.', ',')} %</small><b>${Math.round(pm(p)).toLocaleString('ru-RU')} ₽</b></button>`).join('');
  $$('#cprog button').forEach(b => b.addEventListener('click', () => $(`#rates [data-p="${b.dataset.p}"]`).click()));
}
new MutationObserver(calcExtra).observe($('#loan'), {childList: true, characterData: true, subtree: true});
calcExtra();

