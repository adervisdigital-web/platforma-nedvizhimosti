// запись на просмотр / в демо-дом
const DOW = ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'];
function booking(kind, subj, place) {
  const days = Array.from({length: 7}, (_, i) => { const d = new Date(); d.setDate(d.getDate() + i + 1); return d; });
  let day = 0, slot = '';
  const slotsFor = d => ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'].map((t, i) => [t, (d.getDate() * 7 + i * 3) % 5 === 0 || (d.getDay() === 0 && i > 5)]);
  const draw = () => {
    $('#dlgB').innerHTML = `<div class="bk"><p style="margin:0;color:#4A4741">${subj}</p>
      <div><h4>День</h4><div class="days" style="margin-top:10px">${days.map((d, i) => `<button type="button" data-d="${i}" aria-pressed="${i === day}"><small>${DOW[d.getDay()]}</small><b>${d.getDate()}</b><small>${MONTHS[d.getMonth()].slice(0, 3)}</small></button>`).join('')}</div></div>
      <div><h4>Время</h4><div class="slots" style="margin-top:10px">${slotsFor(days[day]).map(([t, busy]) => `<button type="button" data-t="${t}" ${busy ? 'disabled aria-label="' + t + ' занято"' : ''} aria-pressed="${t === slot}">${t}</button>`).join('')}</div></div>
      <div class="f" id="bkF"><label for="bkP">Телефон для подтверждения</label><input id="bkP" type="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" value="${$('#lp').value}"><span class="err">Введите номер полностью — 10 цифр после +7</span></div>
      <label class="cns" id="bkCL"><input type="checkbox" id="bkC"> <span>Согласен на <a href="privacy/" target="_blank">обработку персональных данных</a></span></label>
      <button class="btn red" type="button" id="bkGo" ${slot ? '' : 'disabled style="opacity:.45"'}>${slot ? `Записаться на ${days[day].getDate()} ${MONTHS[days[day].getMonth()]}, ${slot}` : 'Выберите время'}</button></div>`;
    $$('#dlgB [data-d]').forEach(b => b.addEventListener('click', () => { day = +b.dataset.d; slot = ''; draw(); }));
    $$('#dlgB [data-t]').forEach(b => b.addEventListener('click', () => { slot = b.dataset.t; draw(); }));
    const ip = $('#bkP'); ip.addEventListener('input', () => { lp.value = ip.value; lp.dispatchEvent(new Event('input')); ip.value = lp.value; $('#bkF').classList.remove('bad'); });
    $('#bkGo').addEventListener('click', () => {
      if (ip.value.replace(/\D/g, '').length !== 11) { $('#bkF').classList.add('bad'); ip.focus(); return; }
      if (!$('#bkC').checked) { $('#bkCL').classList.add('bad'); $('#bkC').focus(); return; }
      { const d0 = days[day], p2 = n => String(n).padStart(2, '0');
        PN.send({kind: 'viewing', want: kind, object_ref: subj, slot: `${d0.getFullYear()}-${p2(d0.getMonth() + 1)}-${p2(d0.getDate())} ${slot}`, phone: ip.value}); }
      const d = days[day], [hh, mm] = slot.split(':'), st = new Date(d.getFullYear(), d.getMonth(), d.getDate(), +hh, +mm), en = new Date(st.getTime() + 36e5);
      const f = x => x.toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
      const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Platforma//RU', 'BEGIN:VEVENT', `UID:${Date.now()}@p.forma196.ru`, `DTSTAMP:${f(new Date())}`, `DTSTART:${f(st)}`, `DTEND:${f(en)}`,
        `SUMMARY:${kind} — Платформа недвижимости`, `DESCRIPTION:${subj}. Телефон менеджера +7 965 500-29-18`, `LOCATION:${place}`, 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
      const url = URL.createObjectURL(new Blob([ics], {type: 'text/calendar'}));
      $('#dlgT').textContent = 'Записали';
      $('#dlgB').innerHTML = `<div class="bkok"><span class="big"><i></i></span><h4>${d.getDate()} ${MONTHS[d.getMonth()]}, ${slot}<i class="o"></i></h4>
        <p>${kind}: ${subj}. Менеджер позвонит накануне и пришлёт адрес. Поменять время — по телефону <a href="tel:+79655002918" style="font-weight:700">+7 965 500-29-18</a>.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center"><a class="btn dark" href="${url}" download="platforma-${d.getDate()}-${MONTHS[d.getMonth()]}.ics">Добавить в календарь</a><button class="btn ghost" type="button" onclick="dlg.close()">Готово</button></div></div>`;
    });
  };
  $('#dlgT').textContent = kind; dlg.classList.remove('wide'); draw();
  if (!dlg.open) dlg.showModal();
}

