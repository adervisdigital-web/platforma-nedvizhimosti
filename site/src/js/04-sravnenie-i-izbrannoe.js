// сравнение и избранное
const dlg = $('#dlg');
function openDlg(t, html) { $('#dlgT').textContent = t; $('#dlgB').innerHTML = html; if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', ''); }
$('#dlgX').addEventListener('click', () => dlg.close());
dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
function cmpHTML() {
  const L = [...cmp].map(itemById).filter(Boolean), minP = Math.min(...L.map(i => i.ppm)), minPay = Math.min(...L.map(i => payOf(i)));
  const row = (h, f) => `<tr><th>${h}</th>${L.map(it => `<td>${f(it)}</td>`).join('')}</tr>`;
  return `<table class="ctab"><tbody>${row('', it => `<img src="${PN.img(it.img)}" alt=""><b>${title(it)}</b><br><span style="color:var(--mut)">${it.zk} · ${it.d}</span>`)}
    ${row('Цена', it => `<b>${it.p.toLocaleString('ru-RU')} ₽</b>`)}${row('За м²', it => `<span class="${it.ppm === minP ? 'best' : ''}">${it.ppm.toLocaleString('ru-RU')} ₽${it.ppm === minP ? ' · дешевле всех' : ''}</span>`)}
    ${row('Платёж в ипотеку', it => { const p = payOf(it); return `<span class="${p === minPay ? 'best' : ''}">от ${Math.round(p).toLocaleString('ru-RU')} ₽/мес</span><br><small style="color:var(--mut)">${rateOf(it)} %, взнос 20 %</small>`; })}
    ${row('Сдача', it => it.st)}${row('Отделка', it => it.fin)}${row('Проверка', it => it.t === 'sec' ? 'Юрист: сделка чистая' : 'Застройщик проверен')}
    ${row('', it => `<button class="rm" data-rm="${it.id}">Убрать из сравнения</button>`)}</tbody></table>`;
}
function showCmp() {
  if (!cmp.size) { toast('Добавьте квартиры к сравнению — кнопка на фото в карточке'); return; }
  itemsEnsure(cmp, () => { openDlg(`Сравнение · ${cmp.size}`, cmpHTML());
  $$('#dlgB [data-rm]').forEach(b => b.addEventListener('click', () => { toggle(cmp, 'pn_cmp', +b.dataset.rm, 'cmp'); cmp.size ? showCmp() : dlg.close(); })); });
}
$('#cmpBtn').addEventListener('click', showCmp);
$('#favBtn').addEventListener('click', () => {
  if (!fav.size) { toast('Пока пусто — нажмите сердечко на карточке квартиры'); return; }
  itemsEnsure(fav, () => openDlg(`Избранное · ${fav.size}`, `<div class="flist">${[...fav].map(itemById).filter(Boolean).map(it => `<div class="fi"><img src="${PN.img(it.img)}" alt=""><div><b>${it.p.toLocaleString('ru-RU')} ₽</b>${title(it)}<br><span style="color:var(--mut)">${it.zk} · ${it.d}</span></div></div>`).join('')}</div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px"><a class="btn red" href="#lead" onclick="dlg.close()" data-lead="viewing" data-title="Записаться на просмотр" data-want="Просмотр: квартиры из избранного — ${[...fav].map(itemById).filter(Boolean).map(it => it.zk + ', ' + (it.r ? it.r + '-комн.' : 'студия') + ' ' + it.s + ' м²').join('; ').replace(/"/g, '')}" data-ref="#fav">Записаться на просмотр</a><a class="btn white" href="tel:+79655002918">+7 965 500-29-18</a></div>`));
});
counts(); render();
// с подстраниц «Избранное» и «Сравнить» ведут сюда: ./?open=fav|cmp — открываем список и убираем параметр из адреса
(() => { const op = new URLSearchParams(location.search).get('open'); if (op !== 'fav' && op !== 'cmp') return;
  history.replaceState(null, '', location.pathname + location.hash); setTimeout(() => $(op === 'cmp' ? '#cmpBtn' : '#favBtn').click(), 400); })();
function single(sel) { $$(sel).forEach(b => b.addEventListener('click', () => { $$(sel).forEach(x => x.setAttribute('aria-pressed', x === b)); })); }
single('.form .ch button');

