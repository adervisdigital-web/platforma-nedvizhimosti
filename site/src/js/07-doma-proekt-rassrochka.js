// дома: проект + рассрочка
const HOUSES = PN.houses();
let hSel = HOUSES[0], hName = 'Северный Урал 235';
const WARM = +(PN.settings().warm_contour_from || 75000);                 // ₽/м² тёплого контура — из админки (Настройки → Цены)
const hFrom = h => h.n * WARM, hMonth = (h, y = 5) => Math.round(hFrom(h) * .7 / (y * 12));
const flTxt = n => n === 1 ? '1 этаж' : n + ' этажа';
$('#hx').innerHTML = HOUSES.map(h => `<article class="hc" data-h="${h.id}">
  <button class="ph" type="button" data-open="${h.id}" aria-label="Подробнее: ${h.line} ${h.n}"><img src="${PN.img(h.ph[0], 'houses')}" alt="Дом «${h.line} ${h.n}»" loading="lazy"><span class="ln" style="--c:${h.c}"><i></i>${h.line}</span></button>
  <div class="b"><h3>${h.line}<span>${h.n}</span></h3><div class="mt">«${h.motto}»</div>
    <div class="sp"><span>${h.n} м²</span><span>${flTxt(h.fl)}</span><span>${h.rooms.replace(" + кабинет", "")} комн.${h.rooms.includes("кабинет") ? " + кабинет" : ""}</span><span>потолки ${h.ceil}</span></div>
    <div class="pr">Тёплый контур — от <b>${fmtM(hFrom(h))}</b> · <span class="nw">в рассрочку от ${hMonth(h).toLocaleString('ru-RU')} ₽/мес</span></div>
    <div class="ac"><button class="btn dark" type="button" data-open="${h.id}">Планировки и фото</button><button class="btn ghost" type="button" data-calc="${h.id}">Рассчитать</button></div></div>
</article>`).join('');
$('#hproj').innerHTML = HOUSES.map(h => `<button type="button" aria-pressed="${h === hSel}" data-p="${h.id}">${h.line.split(' ')[0]} ${h.n}</button>`).join('');
const byId = id => HOUSES.find(h => h.id === id);
function pickHouse(h, scroll) {
  hSel = h; hName = `${h.line} ${h.n}`; $('#ha').value = h.n;
  $$('#hproj button').forEach(b => b.setAttribute('aria-pressed', b.dataset.p === h.id)); hcalc(); fillAll();
  if (scroll) $('#hproj').closest('.calc').scrollIntoView({behavior: 'smooth', block: 'center'});
}
$$('#hproj button').forEach(b => b.addEventListener('click', () => pickHouse(byId(b.dataset.p))));
$$('[data-calc]').forEach(b => b.addEventListener('click', () => pickHouse(byId(b.dataset.calc), true)));
$$('[data-open]').forEach(b => b.addEventListener('click', () => houseView(byId(b.dataset.open))));
$$('#hfl button').forEach(b => b.addEventListener('click', () => {
  $$('#hfl button').forEach(x => x.setAttribute('aria-pressed', x === b));
  HOUSES.forEach(h => { $(`.hc[data-h="${h.id}"]`).hidden = !(b.dataset.l === undefined ? h.fl === +b.dataset.fl : !b.dataset.l || h.line === b.dataset.l); });
}));
function houseView(h) {
  dlg.classList.add('wide'); setHash('house-' + h.id);
  openDlg(`${h.line} ${h.n}`, `<div class="hdl"><div><div class="hmain"><img id="hvMain" src="${PN.img(h.ph[0], 'houses')}" alt="${h.line} ${h.n}"></div>
      <div class="hth">${h.ph.map((p, i) => `<button type="button" data-p="${p}" aria-pressed="${i === 0}" aria-label="Фото ${i + 1}"><img src="${PN.img(p, 'houses')}" alt=""></button>`).join('')}</div></div>
    <div><span class="ln" style="--c:${h.c}"><i></i>Линейка «${h.line}»</span><p class="mt2">«${h.motto}»</p>
      <dl class="qvp"><div><dt>Площадь</dt><dd>${h.n} м²</dd></div><div><dt>Этажность</dt><dd>${flTxt(h.fl)}</dd></div><div><dt>Жилых комнат</dt><dd>${h.rooms}</dd></div><div><dt>Потолки</dt><dd>${h.ceil}</dd></div></dl>
      <ul class="feats">${h.feats.map(f => `<li><svg><use href="#check"/></svg>${f}</li>`).join('')}</ul>
      <div class="qvm" style="margin-top:16px"><div><small>Тёплый контур от ${fmtM(hFrom(h))} · взнос 30 %</small><b>от ${hMonth(h).toLocaleString('ru-RU')} ₽/мес</b><small>рассрочка на 5 лет без процентов</small></div><button type="button" id="hvCalc">Рассчитать</button></div>
      <div class="qva"><a class="btn red" href="tel:+79655002918">Позвонить</a><button class="btn white" type="button" id="hvLead">Посетить демо-дом</button><button type="button" class="ib share" data-share aria-label="Поделиться ссылкой"><svg class="ico"><use href="#share"/></svg></button></div>
      <p class="hnote">Планировку и фасад настроим под вашу семью. Материал стен — на выбор.</p></div></div>
    <p class="hidea">${h.idea}</p><div class="htext">${h.text.map(t => `<p>${t}</p>`).join('')}</div>
    <div class="hpl"><h4>Планировка</h4>${h.plans.length > 1 ? `<div class="seg2" id="plTabs">${h.plans.map((p, i) => `<button type="button" aria-pressed="${i === 0}" data-i="${i}">${p[0]}</button>`).join('')}</div>` : `<span style="color:var(--mut)">${h.plans[0][0]}</span>`}</div>
    <a class="plan" id="plLink" href="${PN.img(h.plans[0][1], 'houses')}" target="_blank" rel="noopener" title="Открыть в полном размере"><img id="plImg" src="${PN.img(h.plans[0][1], 'houses')}" alt="Планировка: ${h.plans[0][0]}"></a>`);
  $$('#dlgB .hth button').forEach(b => b.addEventListener('click', () => { $('#hvMain').src = `${PN.img(b.dataset.p, 'houses')}`; $$('#dlgB .hth button').forEach(x => x.setAttribute('aria-pressed', x === b)); }));
  $$('#plTabs button').forEach(b => b.addEventListener('click', () => { const p = h.plans[b.dataset.i]; $('#plImg').src = $('#plLink').href = `${PN.img(p[1], 'houses')}`; $('#plImg').alt = 'Планировка: ' + p[0]; $$('#plTabs button').forEach(x => x.setAttribute('aria-pressed', x === b)); }));
  $('#hvCalc').addEventListener('click', () => { dlg.close(); pickHouse(h, true); });
  $('#hvLead').addEventListener('click', () => booking('Экскурсия в демо-дом', `Проект «${h.line} ${h.n}» — смотрим вживую`, 'Демо-дом, Екатеринбург'));
}
dlg.addEventListener('close', () => { dlg.classList.remove('wide'); if (/^#(obj|house)-/.test(location.hash)) history.replaceState(null, '', location.pathname + location.search); });
function hcalc() {
  const a = +$('#ha').value, y = +$('#ht').value, mode = $('#hmode [aria-pressed=true]').dataset.m;
  const sum = a * WARM, pv = sum * .3, rest = sum - pv;
  $('#hav').textContent = a + ' м²'; $('#htv').textContent = y + (y === 1 ? ' год' : y < 5 ? ' года' : ' лет');
  $('#hname').textContent = `Проект «${hName}» · тёплый контур`;
  $('#hsum').textContent = fmt(sum); $('#hpv').textContent = fmt(pv); $('#hrest').textContent = fmt(rest);
  if (mode === 'inst') { $('#hpay').innerHTML = Math.round(rest / (y * 12)).toLocaleString('ru-RU') + ' <small>₽/мес</small>'; $('#hrestL').textContent = `Остаток в рассрочку на ${$('#htv').textContent}`; }
  else { $('#hpay').innerHTML = Math.round(rest / 4).toLocaleString('ru-RU') + ' <small>₽/этап</small>'; $('#hrestL').textContent = 'Остаток — 4 платежа по этапам'; }
  $('#ht').disabled = mode !== 'inst'; $('#ht').closest('.rng').style.opacity = mode === 'inst' ? 1 : .4;
}
['#ha', '#ht'].forEach(q => $(q).addEventListener('input', hcalc));
$$('#hmode button').forEach(b => b.addEventListener('click', () => { $$('#hmode button').forEach(x => x.setAttribute('aria-pressed', x === b)); hcalc(); }));
pickHouse(hSel);

