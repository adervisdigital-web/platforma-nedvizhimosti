# Рендер презентации 07 в PNG/JPG (1440 px, низ обрезается по зелёному фону html). Run: bash tools/render_pres.sh
R="$(cd "$(dirname "$0")/.." && pwd -W)"; T="${TEMP:-/tmp}/pn_render"; mkdir -p "$T"
U="file:///C:/Users/MSI/Desktop/%D0%9F%D0%9B%D0%90%D0%A2%D0%A4%D0%9E%D0%A0%D0%9C%D0%90%20-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5/07_%D0%9F%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F/index.html"
bash "$R/tools/shot.sh" "$U" "$T/pres_raw.png" 1440,20000
py -I -c "
import numpy as np
from PIL import Image
im=Image.open(r'$T/pres_raw.png').convert('RGB'); a=np.asarray(im)
g=(a[:,:,0]<10)&(a[:,:,1]>245)&(a[:,:,2]<10); r=np.where(g.mean(1)>.98)[0]; H=r[0] if len(r) else a.shape[0]
im=im.crop((0,0,1440,H)); im.save(r'$R/07_Презентация/Презентация_бренда.png'); im.save(r'$R/07_Презентация/Презентация_бренда.jpg',quality=88); print('pres',H)"
