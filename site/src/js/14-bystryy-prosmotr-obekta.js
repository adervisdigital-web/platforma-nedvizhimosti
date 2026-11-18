// быстрый просмотр объекта
function quick(it) {
  setHash('obj-' + it.id);
  const r = rateOf(it), pay = Math.round(ann(it.p, r)), tg = tagOf(it), ck = CHECKS[it.t === 'sec' ? 'sec' : 'dev'];
  openDlg(title(it), `<div class="qvg"><div><div class="qvph"><img src="assets/img/${it.img}.jpg" alt="${title(it)}">${tg ? `<span class="tag">${tg}</span>` : ''}</div>
    <div class="qvc"><b><i></i>${it.t === 'sec' ? 'Что проверил юрист' : 'Что мы проверили у застройщика'}</b>${ck.map(c => `<span><svg><use href="#check"/></svg>${c[0]}</span>`).join('')}</div></div>
    <div class="qvi"><div class="qic"><button type="button" class="ib share" data-share aria-label="Поделиться ссылкой"><svg class="ico"><use href="#share"/></svg></button><button class="ib fav" id="qvFav" aria-pressed="${fav.has(it.id)}" aria-label="В избранное"><svg class="ico"><use href="#heart"/></svg></button></div><div class="price">${it.p.toLocaleString('ru-RU')} ₽</div><div class="ppm">${it.ppm.toLocaleString('ru-RU')} ₽ за м² · ${it.zk}, ${it.d}</div>
    <dl class="qvp"><div><dt>Площадь</dt><dd>${it.s.toLocaleString('ru-RU')} м²</dd></div><div><dt>Этаж</dt><dd>${it.fl} из ${it.fls}</dd></div>
      <div><dt>Сдача</dt><dd>${it.due ? it.st.replace('Сдача — ', '') : it.t === 'sec' ? 'Готовое жильё' : 'Дом сдан'}</dd></div><div><dt>Отделка</dt><dd>${it.fin}</dd></div></dl>
    <div class="qvm"><div><small>В ипотеку · ${it.t === 'new' ? 'семейная' : 'рыночная'} ${r} %, взнос 20 %</small><b>от ${pay.toLocaleString('ru-RU')} ₽/мес</b></div><button type="button" id="qvCalc">Рассчитать</button></div>
    ${it.fin === 'Без отделки' ? `<div class="qvx"><span class="k">Добавить наш ремонт · гарантия 5 лет</span><div class="seg2" id="qvR">${[['Без ремонта', 0], ['Базовый', 20000], ['Комфорт', 45000], ['Премиум', 80000]].map((x, i) => `<button type="button" aria-pressed="${i === 0}" data-r="${x[1]}">${x[0]}</button>`).join('')}</div><div class="tot"><span class="k" id="qvRk">Квартира</span><b id="qvT">${rub(it.p)}</b></div></div>` : ''}
    <div class="qva"><a class="btn red" href="tel:+79655002918">Позвонить</a><button class="btn white" type="button" id="qvLead">Записаться на просмотр</button></div></div></div>`);
  $('#qvCalc').addEventListener('click', () => { dlg.close(); mortFrom(it); });
  $('#qvLead').addEventListener('click', () => booking('Просмотр', title(it) + ' · ' + it.zk, `${it.zk}, ${it.d}`));
  $$('#qvR button').forEach(b => b.addEventListener('click', () => { $$('#qvR button').forEach(x => x.setAttribute('aria-pressed', x === b)); const add = it.s * +b.dataset.r;
    $('#qvRk').textContent = add ? `Квартира + ремонт «${b.textContent.toLowerCase()}» (${fmtM(add)})` : 'Квартира'; $('#qvT').textContent = rub(it.p + add); }));
  remember(it.id);
  $('#qvFav').addEventListener('click', e => { toggle(fav, 'pn_fav', it.id, 'fav'); e.currentTarget.setAttribute('aria-pressed', fav.has(it.id)); });
}

