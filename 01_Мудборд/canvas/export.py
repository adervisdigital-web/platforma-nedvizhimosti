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
    'cdd11a87d47dc7bbb0f3e9176798d679': 'gen/kv_living2.jpg', '59f13ed8e92015fcbfaa3bf5e84befd1': 'gen/kv_kids.jpg', '068979a2fe76a1232c5d8c3a5afedf7b': 'gen/kv_complex2.jpg', '70ba586a3b88e814a57ca48ecc8caddc': 'gen/house_stone2.jpg',
    'a9a387416fc9107965b27f505644a667': 'gen/site_build.jpg',
    'bedc0a1cac16ddf51df5b213a1ab753e': 'gen/life_D_bag.jpg',
    '6aea6f11b9e90f887efe4a7e0792da3d': 'gen/life_D_billboard.jpg',
    '14c4bcfa0e1981a9e9e7f2a93b263107': 'gen/life_D_facade.jpg',
    '94e09345ab81f929d96ea12a47f69769': 'gen/life_D_fence.jpg',
    'ff79d90e626b5b946f355778b096982a': 'gen/life_D_helmet.jpg',
    'f55f19b75ae27d1f3a52acdaa94b1c28': 'gen/life_D_keys.jpg',
    'd25addfea8bfc01d500628426a83ea04': 'gen/life_D_plate.jpg',
    'b1cd0e904b4a45d297614ec72f571e19': 'gen/life_D_store.jpg',
    '1b3de3ee3a20f5c57fb5fa369689cbb5': 'gen/life_D_vest.jpg',
    '202b752bb21c31ba765aa3bd356b4990': 'gen/life_L_bag.jpg',
    'b53b022c7bef717ba1a05e496f360764': 'gen/life_L_billboard.jpg',
    '06a0f35736ead4c26f51fafa1abf3437': 'gen/life_L_facade.jpg',
    '4a64a38817ad8d3029c3ed9a1c4b2ab9': 'gen/life_L_fence.jpg',
    '2c0b8992e8f879860d67f66ced4e14f2': 'gen/life_L_helmet.jpg',
    '91ed8c7a5b82eca24c0f9d52c57f8826': 'gen/life_L_keys.jpg',
    '5673c015c61d70614ec906e6bd6895a9': 'gen/life_L_plate.jpg',
    '5e8bc4ccb202985d35eff727fb99df5f': 'gen/life_L_store.jpg',
    '5b2a5baeb9551831851bcedfbe4b4f5f': 'gen/life_L_vest.jpg',
    '3de4c671ce28cddf5540b49afcf063c0': 'gen/life_Y_bag.jpg',
    '214a596ec3adaa6d7f71a4bc8f9128e1': 'gen/life_Y_billboard.jpg',
    '2b94772934cceb52bbb176899e2f830c': 'gen/life_Y_facade.jpg',
    '1ec846b06b929a0f6b1a92cb357ebf7e': 'gen/life_Y_fence.jpg',
    '887335cb27ff0889fae4bb13350cf582': 'gen/life_Y_helmet.jpg',
    '3a01bbc3515f6cee039ef397a78822ec': 'gen/life_Y_keys.jpg',
    '6a259b765536d5cbe5ed2e7291713025': 'gen/life_Y_plate.jpg',
    '56263368762c30dafd39a97ae79a8581': 'gen/life_Y_store.jpg',
    '206f1b584b38fdbb694267787cfb26ea': 'gen/life_Y_vest.jpg', '54a8cb8b2a50e5f05f21d5a0f2f7d073': 'gen/mk_facade.jpg', 'ffdaa51adb3c5d7e31c8fd6a6a5f75d1': 'gen/mk_billboard.jpg', '1bb80de6ed3a83f08009427e96bfeec5': 'gen/mk_keys.jpg', '108a4f5c54f07e918b981646718007eb': 'gen/mk_helmet.jpg', '94be6ec097df12c9c8e43aeaa5861c54': 'gen/mk_vest.jpg', 'f3ac65a57af9466d01fd447e312cbf65': 'gen/mk_bag.jpg', '337e60c28f17034e42ec701b320abb86': 'screen_catalog.jpg', '7b9920c5408169bf27f1722b29c1d985': 'pick_ural6.jpg',
}
NAMES = {'LogoL.dc.html': '1-1_Светлый_Арка_логотип', 'StyleL.dc.html': '1-2_Светлый_Арка_стиль', 'SystemL.dc.html': '1-3_Светлый_Арка_айдентика', 'SiteL.dc.html': '1-4_Светлый_Арка_сайт-приложение', 'LifeL.dc.html': '1-5_Светлый_Арка_в-жизни', 'LogoD.dc.html': '2-1_Тёмный_Портал_логотип', 'StyleD.dc.html': '2-2_Тёмный_Портал_стиль', 'SystemD.dc.html': '2-3_Тёмный_Портал_айдентика', 'SiteD.dc.html': '2-4_Тёмный_Портал_сайт-приложение', 'LifeD.dc.html': '2-5_Тёмный_Портал_в-жизни', 'LogoY.dc.html': '3-1_Яркий_Сборка_логотип', 'StyleY.dc.html': '3-2_Яркий_Сборка_стиль', 'SystemY.dc.html': '3-3_Яркий_Сборка_айдентика', 'SiteY.dc.html': '3-4_Яркий_Сборка_сайт-приложение', 'LifeY.dc.html': '3-5_Яркий_Сборка_в-жизни'}
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
    for _try in range(4):
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                        '--virtual-time-budget=12000', f'--window-size=1440,{hh}', '--force-device-scale-factor=1',
                        f'--screenshot={png.replace("/", chr(92))}', 'file:///' + hp], capture_output=True, timeout=180)
        if os.path.exists(png): break
        import time; time.sleep(2)
    print(n, os.path.exists(png) and os.path.getsize(png))
    pngs.append(png)
ims = [Image.open(p).convert('RGB') for p in pngs if os.path.exists(p)]
if ims:
    ims[0].save(f'{OUT}/Мудборд_Платформа.pdf', save_all=True, append_images=ims[1:], resolution=144)
    print('pdf ok')
