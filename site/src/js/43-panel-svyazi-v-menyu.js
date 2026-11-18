// панель связи в меню
(() => {
  const ph = $('#hbPh'), pop = $('#hbPop'), cb = $('#hbCb'), inp = $('#hbTel');
  const ekb = () => { const d = new Date(), u = d.getTime() + d.getTimezoneOffset() * 6e4; return new Date(u + 5 * 36e5); };
  function clock() { const t = ekb(), h = t.getHours(), open = h >= 9 && h < 21;
    $('#hbClk').textContent = String(h).padStart(2, '0') + ':' + String(t.getMinutes()).padStart(2, '0');
    $('#hbStatus').textContent = open ? 'на связи' : 'перезвоним с 9:00'; $('#hbDot').classList.toggle('off', !open);
    $('#hbCbNote').textContent = cb.classList.contains('sent') ? $('#hbCbNote').textContent : open ? 'Оставьте номер — менеджер наберёт сам' : 'Сейчас офис закрыт — позвоним в 9:00'; }
  clock(); setInterval(clock, 15000);
  function open(o) { pop.hidden = !o; ph.setAttribute('aria-expanded', o); if (o) setTimeout(() => inp.focus(), 50); }
  ph.addEventListener('click', e => { e.stopPropagation(); open(pop.hidden); });
  pop.addEventListener('click', e => e.stopPropagation());
  document.addEventListener('click', () => open(false));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !pop.hidden) { open(false); ph.focus(); } });
  $$('[data-chat]', pop).forEach(b => b.addEventListener('click', () => open(false)));
  inp.addEventListener('input', () => { cb.classList.remove('bad'); let d = inp.value.replace(/\D/g, ''); if (!d) { inp.value = ''; return; }
    if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; const p = d.slice(1, 11);
    inp.value = '+7' + (p.length ? ' (' + p.slice(0, 3) : '') + (p.length > 3 ? ') ' + p.slice(3, 6) : '') + (p.length > 6 ? '-' + p.slice(6, 8) : '') + (p.length > 8 ? '-' + p.slice(8, 10) : ''); });
  cb.addEventListener('submit', e => { e.preventDefault();
    if (inp.value.replace(/\D/g, '').length !== 11) { cb.classList.add('bad'); inp.focus(); return; }
    if (!$('#hbCc').checked) { $('#hbCcL').classList.add('bad'); $('#hbCc').focus(); return; }
    PN.send({kind: 'callback', phone: inp.value});
    const h = ekb().getHours(), openNow = h >= 9 && h < 21; cb.classList.add('sent');
    $('#hbCbNote').textContent = openNow ? `Звоним на ${inp.value} — держите телефон рядом` : `Позвоним на ${inp.value} завтра в 9:00`;
    cb.querySelector('b').textContent = openNow ? 'Уже набираем' : 'Заявка принята';
    toast(openNow ? 'Перезвоним в течение 30 секунд' : 'Перезвоним завтра в 9:00'); });
})();

