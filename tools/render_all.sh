# Перерендер: сайт (desktop/mobile), презентация (PNG/JPG). Run: bash tools/render_all.sh
R="$(cd "$(dirname "$0")/.." && pwd -W)"; T="${TEMP:-/tmp}/pn_render"; mkdir -p "$T"
B="file:///C:/Users/MSI/Desktop/%D0%9F%D0%9B%D0%90%D0%A2%D0%A4%D0%9E%D0%A0%D0%9C%D0%90%20-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5"
SITE="$B/08_%D0%A1%D0%B0%D0%B9%D1%82_%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80/index.html"
bash "$R/tools/shot.sh" "$SITE" "$T/site_full.png" 1440,16000
bash "$R/tools/shot.sh" "$SITE" "$T/site_first.png" 1440,900
printf '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0}iframe{border:0;width:390px;height:22000px;display:block}</style></head><body><iframe src="08_Сайт_пример/index.html"></iframe></body></html>' > "$R/_m.html"
bash "$R/tools/shot.sh" "$B/_m.html" "$T/site_m.png" 800,22000; rm -f "$R/_m.html"
py -I "$R/tools/crop_renders.py" "$T" "$R"
