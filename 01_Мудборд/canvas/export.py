"""Render the moodboard artboards (*.dc.html) to PNG + one PDF with Edge headless.
Run: py -3 export.py   (from anywhere). Images are mapped from /_blob/<id> to files in ../../_source/.
"""
import re, os, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)).replace(chr(92), '/')
OUT = os.path.dirname(HERE)
H = OUT + '/_html'
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
BLOBS = {
    'b471f2a087272c564fa40cb48156b5a1': 'houses/house-gable.jpg', '241aa9c6494b7c64ac1bea49f925807d': 'houses/house-flat.jpg',
    '2ef3674ef6e253cb347aaef38d116872': 'houses/house-wood.jpg',
    'f89faa6c932f58546cdda0740096d0e0': 'pick_int1.jpg', '8e65812abbba9b16bf2348f145cc9914': 'pick_int5.jpg', '0a22dcad09ac16551598912f966efe79': 'pick_int9.jpg',
    '5ecf511b79a0350ec3eafc94c05fbc7a': 'pick_int4.jpg', 'b812b7320c42b65d59ee3b3a020fe300': 'pick_ren3.jpg', '9a8263a3ef92a2d197aa73cec44705a3': 'pick_ren6.jpg',
    '95a53e311318c23ef228cf199465704b': 'pick_key2.jpg', '991a5bbcb2d2b09a0cf55d153454e1b4': 'pick_tile3.jpg', '4fe718766c03ccc4223706e3ab431309': 'pick_tile4.jpg',
    'fc2fe74625a2270e261425249e5f64be': 'pick_ekb1.jpg', 'be6be276308286428da8cea58e7a1d97': 'pick_ekb3.jpg', '5698dfef76a05bc97575f7f6bc04aa8d': 'pick_ekb5.jpg',
    'ca00be2acd9690fb9dea9110aaaec783': 'pick_st9.jpg', '597b77d5921d32365d4391f69448844f': 'pick_st6.jpg', '9d65d47d8973af696a8853a112428717': 'pick_st15.jpg',
    '0344505071bafebecba4899d1050d932': 'pick_st14.jpg', '3cf8804347ed096c9289e40971199ef4': 'pick_st10.jpg', 'c2651986b7a52a7642edc879ff44dc4b': 'pick_st4.jpg',
    '2a052deb4b100525d0ae7916e9b9c051': 'pick_bp2.jpg', '3b0d5fe40751fc529ef5cf45f7813f8e': 'pick_bp3.jpg', '9c58a27346cd77441145571d5f7f85fd': 'pick_mal1.jpg',
    '2da24de981f674081698e5d2b3d271ef': 'pick_ural1.jpg',
    'a51f99a2ebaa3290cc815a60538e1744': 'gen/kv_bedroom.jpg', '1947ff52209ccab806cd2be3be49c501': 'gen/kv_building.jpg', '6eb6b66044bc72cd1c691f54afa97fd2': 'gen/kv_kitchen.jpg',
    'e05ef6fc38a92410bfb373f11b4be3cd': 'gen/rem_bathroom.jpg', 'ab22bbc0ab515db845d3dee45c8b5d04': 'gen/rem_before_after.jpg', '3472f23568c92d74ff24b6057454790b': 'gen/rem_detail.jpg', 'de9f3f7fe15a4720d9b574a1e479b7c1': 'gen/rem_process.jpg',
    'cdd11a87d47dc7bbb0f3e9176798d679': 'gen/kv_living2.jpg', '59f13ed8e92015fcbfaa3bf5e84befd1': 'gen/kv_kids.jpg', '068979a2fe76a1232c5d8c3a5afedf7b': 'gen/kv_complex2.jpg', '70ba586a3b88e814a57ca48ecc8caddc': 'gen/house_stone2.jpg', '337e60c28f17034e42ec701b320abb86': 'screen_catalog.jpg', '7b9920c5408169bf27f1722b29c1d985': 'pick_ural6.jpg',
}
NAMES = {'LogoL.dc.html': '1-1_Светлый_Арка_логотип', 'StyleL.dc.html': '1-2_Светлый_Арка_стиль', 'SystemL.dc.html': '1-3_Светлый_Арка_айдентика', 'SiteL.dc.html': '1-4_Светлый_Арка_сайт-приложение', 'LogoD.dc.html': '2-1_Тёмный_Портал_логотип', 'StyleD.dc.html': '2-2_Тёмный_Портал_стиль', 'SystemD.dc.html': '2-3_Тёмный_Портал_айдентика', 'SiteD.dc.html': '2-4_Тёмный_Портал_сайт-приложение', 'LogoY.dc.html': '3-1_Яркий_Сборка_логотип', 'StyleY.dc.html': '3-2_Яркий_Сборка_стиль', 'SystemY.dc.html': '3-3_Яркий_Сборка_айдентика', 'SiteY.dc.html': '3-4_Яркий_Сборка_сайт-приложение'}
os.makedirs(H, exist_ok=True)
pngs = []
for f, n in NAMES.items():
    t = open(f'{HERE}/{f}', encoding='utf8').read()
    head = re.search(r'<helmet>(.*?)</helmet>', t, re.S).group(1)
    body = re.search(r'</helmet>(.*?)</x-dc>', t, re.S).group(1)
    for k, v in BLOBS.items():
        body = body.replace(f'/_blob/{k}', '../../_source/' + v)
    html = f'<!doctype html><html lang="ru"><head><meta charset="utf-8">{head}</head><body style="margin:0">{body}</body></html>'
    hp = f'{H}/{n}.html'
    open(hp, 'w', encoding='utf8').write(html)
    import json as _j
    hh = _j.load(open(f'{HERE}/canvas.json', encoding='utf8'))['boards'][f]['h']
    png = f'{OUT}/{n}.png'
    if os.path.exists(png): os.remove(png)
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--virtual-time-budget=12000', f'--window-size=1440,{hh}', '--force-device-scale-factor=1',
                    f'--screenshot={png.replace("/", chr(92))}', 'file:///' + hp], capture_output=True, timeout=180)
    print(n, os.path.exists(png) and os.path.getsize(png))
    pngs.append(png)
ims = [Image.open(p).convert('RGB') for p in pngs if os.path.exists(p)]
if ims:
    ims[0].save(f'{OUT}/Мудборд_Платформа.pdf', save_all=True, append_images=ims[1:], resolution=144)
    print('pdf ok')
