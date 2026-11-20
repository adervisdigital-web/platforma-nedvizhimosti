// ремонт
function rcalc() {
  const a = +$('#ra').value, l = +$('#rl').value;
  const lvl = l <= 35000 ? 'базовый' : l <= 65000 ? 'комфорт' : 'премиум';
  $('#rav').textContent = a + ' м²'; $('#rlv').textContent = lvl + ' · ' + l.toLocaleString('ru-RU') + ' ₽/м²';
  // полная сумма: «3 320 тыс. ₽» заказчик прочитал как цифру без нулей
  $('#rpay').innerHTML = Math.round(a * l).toLocaleString('ru-RU') + ' <small>₽</small>'; $('#rppm').textContent = fmt(l);
}
['#ra', '#rl'].forEach(q => $(q).addEventListener('input', rcalc)); rcalc();

