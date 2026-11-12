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
    'c84226ab98d1cba847c8b95647f62254': 'gen/life_M_facade.jpg',
    'c0a35b11f88f9f59203574474e812e3d': 'gen/life_M_billboard.jpg',
    '8bcd5d93eccf581c49df61701a7fe96b': 'gen/life_M_keys.jpg',
    'a8cbb4acb9cc4f316359ea6430459ad7': 'gen/life_M_helmet.jpg',
    '1ceac7d48b677c4c90617d1d6fde89df': 'gen/life_M_bag.jpg',
    '3244e30c7b616b51691665f12399d5d8': 'gen/life_M_fence.jpg',
    'b797d1c558b8658203c778d2df2824a9': 'gen/life_M_store.jpg',
    '853a030f09bbbd234ecb12b919a4970a': 'gen/life_M_plate.jpg',
    '25cd37a5a5bb7a7f6f582822c243005c': 'gen/life_M_vest.jpg',
    'b313526825d09dd4b2bb941ddd90e3d8': 'gen/life_K_facade.jpg',
    '5bffee33ad1e78c538ef3f378db9dbd6': 'gen/life_K_billboard.jpg',
    'a770362918a46121f17415941f7d7304': 'gen/life_K_keys.jpg',
    '174c191b1eba87a2673d887d139888db': 'gen/life_K_helmet.jpg',
    'd21896daf058369148427d36a2d2e998': 'gen/life_K_bag.jpg',
    '9f81ffc9f31f0b9b64ad7d22f9a06f13': 'gen/life_K_fence.jpg',
    'a1910ecb40ebe44ba94e31220b3f92bb': 'gen/life_K_store.jpg',
    '8b92c4e7be74e4e18eb859470b2dae15': 'gen/life_K_plate.jpg',
    '93311f306a6fa8d2996b827b887a2db0': 'gen/life_K_vest.jpg',
    '83a68c4da0eea7fa07469c950b472aa5': 'gen/life_S_facade.jpg',
    '2efef7f10b10f9acd5e2f49ac2d01346': 'gen/life_S_billboard.jpg',
    'ed814d26d69738f6f1581ca7ff9bdbf2': 'gen/life_S_keys.jpg',
    'f6471c12b26a8b7cb48c4fe4ae0328b5': 'gen/life_S_helmet.jpg',
    '4425ce77e8811f177f97fe453f8dd4ef': 'gen/life_S_bag.jpg',
    'b6326f120fe0da2af12c8654ee064b4e': 'gen/life_S_fence.jpg',
    '0fba08127959132df066c1039dba9e1d': 'gen/life_S_store.jpg',
    '4a8fd9219109de865706aafcc37cff1a': 'gen/life_S_plate.jpg',
    'f475b84ef79905b7b53146188ebecdd9': 'gen/life_S_vest.jpg',
    '47a828b820eaa13ea863248ec795c209': 'gen/life_D_bag.jpg',
    'cd43ecbcec8d91a8daf51192edfa6146': 'gen/life_D_billboard.jpg',
    'db6310cdb5c2b8701bd0034026a9f8ea': 'gen/life_D_facade.jpg',
    '26569775edfa992d6da6c329dcc8fcd6': 'gen/life_D_fence.jpg',
    'a6bb03648c517102c3a69b8e081072c6': 'gen/life_D_helmet.jpg',
    '3634e0b31f2659709f9d3085759e0a49': 'gen/life_D_keys.jpg',
    '53f57f68bf5e190ef6b364d468a47f7e': 'gen/life_D_plate.jpg',
    '43e650bfa7905e508a537eb59ec1904e': 'gen/life_D_store.jpg',
    'd8d2c62a998179e5296a41f461574877': 'gen/life_D_vest.jpg',
    '8c88a4592108bb3095af8eedc6068f97': 'gen/life_L_bag.jpg',
    '01a3b029974d5e1d645b424def80639a': 'gen/life_L_billboard.jpg',
    'dd0d9a37ceb4c0bc5ce8dabec839926c': 'gen/life_L_facade.jpg',
    'f658f6f766cab67979cd51c9bb868319': 'gen/life_L_fence.jpg',
    'ffabff88c220126fff267b4a44759322': 'gen/life_L_helmet.jpg',
    '1125ffa7b9c1e31a3fce3344697b38a9': 'gen/life_L_keys.jpg',
    '5e45afe72689cbcd1e9a3884ce472c85': 'gen/life_L_plate.jpg',
    'b518b8a6f66f7eddc32097a9fe586495': 'gen/life_L_store.jpg',
    'e0b35317c829ebfc9accfd979058c78e': 'gen/life_L_vest.jpg',
    '77024bf73daaebd5b297113d09902e6e': 'gen/life_Y_bag.jpg',
    'b1146ea39d699aec3657d74894691614': 'gen/life_Y_billboard.jpg',
    '6bf43adceddace6da3bbf006ee453674': 'gen/life_Y_facade.jpg',
    'aef21b2189e8cfad895773447ea1fb71': 'gen/life_Y_fence.jpg',
    '63b28824a29b1310909e291e0eabf775': 'gen/life_Y_helmet.jpg',
    '853712aa745e06bac7ca0458710a74c4': 'gen/life_Y_keys.jpg',
    'ea3bd9a3f4d96c5c8d3015f59ebb0064': 'gen/life_Y_plate.jpg',
    '60de7378741b6827e0538187a1691369': 'gen/life_Y_store.jpg',
    'f2b6441c1b9e3ae94997e5862e17e616': 'gen/life_Y_vest.jpg', '54a8cb8b2a50e5f05f21d5a0f2f7d073': 'gen/mk_facade.jpg', 'ffdaa51adb3c5d7e31c8fd6a6a5f75d1': 'gen/mk_billboard.jpg', '1bb80de6ed3a83f08009427e96bfeec5': 'gen/mk_keys.jpg', '108a4f5c54f07e918b981646718007eb': 'gen/mk_helmet.jpg', '94be6ec097df12c9c8e43aeaa5861c54': 'gen/mk_vest.jpg', 'f3ac65a57af9466d01fd447e312cbf65': 'gen/mk_bag.jpg', '337e60c28f17034e42ec701b320abb86': 'screen_catalog.jpg', '7b9920c5408169bf27f1722b29c1d985': 'pick_ural6.jpg',
}
NAMES = {'LogoL.dc.html': '1-1_Светлый_Арка_логотип', 'StyleL.dc.html': '1-2_Светлый_Арка_стиль', 'SystemL.dc.html': '1-3_Светлый_Арка_айдентика', 'SiteL.dc.html': '1-4_Светлый_Арка_сайт-приложение', 'LifeL.dc.html': '1-5_Светлый_Арка_в-жизни', 'LogoD.dc.html': '2-1_Тёмный_Портал_логотип', 'StyleD.dc.html': '2-2_Тёмный_Портал_стиль', 'SystemD.dc.html': '2-3_Тёмный_Портал_айдентика', 'SiteD.dc.html': '2-4_Тёмный_Портал_сайт-приложение', 'LifeD.dc.html': '2-5_Тёмный_Портал_в-жизни', 'LogoY.dc.html': '3-1_Яркий_Сборка_логотип', 'StyleY.dc.html': '3-2_Яркий_Сборка_стиль', 'SystemY.dc.html': '3-3_Яркий_Сборка_айдентика', 'SiteY.dc.html': '3-4_Яркий_Сборка_сайт-приложение', 'LifeY.dc.html': '3-5_Яркий_Сборка_в-жизни', 'LogoK.dc.html': '4-1_Красный_Кладка_логотип', 'StyleK.dc.html': '4-2_Красный_Кладка_стиль', 'SystemK.dc.html': '4-3_Красный_Кладка_айдентика', 'SiteK.dc.html': '4-4_Красный_Кладка_сайт-приложение', 'LifeK.dc.html': '4-5_Красный_Кладка_в-жизни', 'LogoS.dc.html': '5-1_Зелёный_Свод_логотип', 'StyleS.dc.html': '5-2_Зелёный_Свод_стиль', 'SystemS.dc.html': '5-3_Зелёный_Свод_айдентика', 'SiteS.dc.html': '5-4_Зелёный_Свод_сайт-приложение', 'LifeS.dc.html': '5-5_Зелёный_Свод_в-жизни', 'LogoM.dc.html': '6-1_Бирюзовый_Модуль_логотип', 'StyleM.dc.html': '6-2_Бирюзовый_Модуль_стиль', 'SystemM.dc.html': '6-3_Бирюзовый_Модуль_айдентика', 'SiteM.dc.html': '6-4_Бирюзовый_Модуль_сайт-приложение', 'LifeM.dc.html': '6-5_Бирюзовый_Модуль_в-жизни'}
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
