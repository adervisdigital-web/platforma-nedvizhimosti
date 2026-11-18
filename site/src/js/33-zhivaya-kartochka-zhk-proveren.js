// живая карточка «ЖК проверен»
const ZKS = [...new Set(ITEMS.filter(it => it.zk.startsWith('ЖК')).map(it => it.zk))].map(z => ({z, d: ITEMS.find(it => it.zk === z).d, n: ITEMS.filter(it => it.zk === z).length}));
const ZCHK = ['Разрешение на строительство', 'Проектная декларация, эскроу', 'Прошлые дома сданы в срок', 'Нет банкротных дел'];
let zi = 0, zt = [], zPause = false;
function zShow(i) {
  zt.forEach(clearTimeout); zt = []; zi = (i + ZKS.length) % ZKS.length; const z = ZKS[zi];
  $('#cvName').textContent = z.z; $('#cvSub').textContent = `${z.d} · новостройка`;
  $('#cvList').innerHTML = ZCHK.map(c => `<li><svg><use href="#check"/></svg>${c}</li>`).join('');
  $('#cvDots').innerHTML = ZKS.map((_, k) => `<button type="button" aria-label="${ZKS[k].z}" aria-current="${k === zi}"></button>`).join('');
  $$('#cvDots button').forEach((b, k) => b.addEventListener('click', () => zShow(k)));
  const st = $('#cvSt'), go = $('#cvGo'); st.textContent = 'Проверяем'; st.classList.remove('ok'); go.classList.remove('on');
  go.textContent = `${z.n} ${plural(z.n, 'квартира', 'квартиры', 'квартир')} в этом ЖК`;
  const step = reduce ? 0 : 450;
  $$('#cvList li').forEach((li, k) => zt.push(setTimeout(() => li.classList.add('ok'), step * (k + 1))));
  zt.push(setTimeout(() => { st.textContent = 'Проверен'; st.classList.add('ok'); go.classList.add('on'); }, step * 5));
  zt.push(setTimeout(function nx() { if (zPause) { zt.push(setTimeout(nx, 1500)); return; } zShow(zi + 1); }, step * 5 + 4200));
}
$('#cvGo').addEventListener('click', e => { e.preventDefault(); const z = ZKS[zi].z; applyFilter(ITEMS.filter(it => it.zk === z), z); $('#list').scrollIntoView({behavior: 'smooth'}); });
$('#chipv').addEventListener('mouseenter', () => zPause = true); $('#chipv').addEventListener('mouseleave', () => zPause = false);
zShow(0);

