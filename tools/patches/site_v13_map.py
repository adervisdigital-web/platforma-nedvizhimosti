"""Сайт v13 — настоящая карта Екатеринбурга (Leaflet 1.9.4 + тайлы OpenStreetMap) вместо нарисованной схемы.
Метки — по районам объектов, следуют за фильтрами и сортировкой. Если карта не загрузилась (нет сети) — остаётся схема.
Тайлы OpenStreetMap (обесцвечены фильтром под палитру). Для боевого сайта — Яндекс.Карты с ключом заказчика (политика OSM не для больших нагрузок).
Run из корня репо: py -3 tools/patches/site_v13_map.py  (исходник — 08_Сайт_пример/v12.html)"""
P = '08_Сайт_пример/'
s = open(P + 'v12.html', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<link href="https://fonts.googleapis.com', '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n<link href="https://fonts.googleapis.com')
rep('<script>\nconst $ = (s, r = document)', '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>\n<script>\nconst $ = (s, r = document)')
CSS = r'''
/* v13 — карта */
.map{isolation:isolate}
#lmap{position:absolute;inset:0;z-index:0;background:#EEECE8;font:inherit}
.leaflet-tile-pane{filter:grayscale(1) sepia(.12) contrast(.92) brightness(1.06)}
.map.live svg.base,.map.live #pins{display:none}
.mapcap{z-index:500}
.lpin .pin{position:absolute;cursor:pointer}
.lpin .pin.dn{transform:translate(-50%,10px)}.lpin .pin.dn::after{bottom:auto;top:-6px}.lpin .pin.dn.on{transform:translate(-50%,10px) scale(1.08)}
.leaflet-control-attribution{font-size:10px;background:#ffffffcc!important}
.leaflet-bar a{width:34px!important;height:34px!important;line-height:34px!important;color:var(--ink)!important}
.leaflet-bar{border:0!important;box-shadow:0 6px 16px #0000001f!important;border-radius:12px!important;overflow:hidden}
.leaflet-container a.leaflet-popup-close-button{display:none}
'''
rep('@media(prefers-reduced-motion:reduce)', CSS + '@media(prefers-reduced-motion:reduce)')

# отрисовка меток вместе со списком
a = "  $('#pins').innerHTML = list.map("
rep(a, "  mapRender(list);\n" + a)

JS = r'''
// карта Екатеринбурга
const GEO = {'Академический': [56.7905, 60.516], 'Уралмаш': [56.893, 60.59], 'ВИЗ': [56.842, 60.553], 'Центр': [56.8385, 60.6045], 'Ботанический': [56.7985, 60.628],
  'Юго-Западный': [56.8135, 60.561], 'Старая Сортировка': [56.886, 60.533], 'Пионерский': [56.865, 60.641], 'Широкая речка': [56.7995, 60.49]};
let lmap = null, layer = null, lastPts = [];
function mapRender(list) {
  if (!window.L) return;
  if (!lmap) {
    $('.map').classList.add('live'); $('.map').insertAdjacentHTML('afterbegin', '<div id="lmap"></div>');
    lmap = L.map('lmap', {scrollWheelZoom: false, zoomControl: false}).setView([56.84, 60.59], 11);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18, attribution: '© участники OpenStreetMap'}).addTo(lmap);
    L.control.zoom({position: 'bottomright', zoomInTitle: 'Приблизить', zoomOutTitle: 'Отдалить'}).addTo(lmap);
    lmap.attributionControl.setPrefix(false);
    layer = L.layerGroup().addTo(lmap);
  }
  layer.clearLayers(); const seen = {};
  lastPts = list.map((it, k) => {
    const g = GEO[it.d] || [56.84, 60.6], n = seen[it.d] = (seen[it.d] || 0) + 1, ll = n === 3 ? [g[0] - .004, g[1] + .024] : g;
    L.marker(ll, {riseOnHover: true, icon: L.divIcon({className: 'lpin', iconSize: null, html: `<button class="pin${k === 0 ? ' on' : ''}${n === 2 ? ' dn' : ''}" data-i="${it.id}">${(it.p / 1e6).toLocaleString('ru-RU', {maximumFractionDigits: 1})} млн</button>`})}).addTo(layer);
    return ll;
  });
  mapFit();
}
function mapFit() { if (lmap && lastPts.length) lmap.fitBounds(lastPts, {padding: [60, 60], maxZoom: 13}); }
$('#mapBtn').addEventListener('click', () => setTimeout(() => { if (lmap) { lmap.invalidateSize(); mapFit(); } }, 60));
'''
# функция должна существовать до первого render(): вставляем перед логикой объявлений
a = "const store = {get(k)"
rep(a, JS.strip() + '\n' + a)
open(P + 'index.html', 'w', encoding='utf8').write(s)
print('ok')
