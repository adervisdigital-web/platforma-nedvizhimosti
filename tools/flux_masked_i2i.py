"""FLUX.1-dev (GGUF Q4) через ComfyUI: перерисовка кадра поверх исходника. Маска необязательна (белое — перерисовать).
Нужен узел ComfyUI-GGUF и модели: unet/flux1-dev-Q4_K_S.gguf, text_encoders/t5xxl_fp8_e4m3fn + clip_l, vae/ae.safetensors.
Usage: py -3 tools/flux_masked_i2i.py <src.png в ComfyUI/input> <mask.png|-> <prefix> "<prompt>" <denoise> [seed] [steps] [W H]"""
import json, random, sys, time, urllib.request

URL = 'http://127.0.0.1:8188'
a = sys.argv
src, mask, prefix, pos, den = a[1], a[2], a[3], a[4], float(a[5])
seed = int(a[6]) if len(a) > 6 and a[6] else random.randint(1, 2 ** 31)
steps = int(a[7]) if len(a) > 7 else 24
wf = {
    '1': {'class_type': 'LoadImage', 'inputs': {'image': src}},
    '20': {'class_type': 'UnetLoaderGGUF', 'inputs': {'unet_name': 'flux1-dev-Q4_K_S.gguf'}},
    '21': {'class_type': 'DualCLIPLoader', 'inputs': {'clip_name1': 't5xxl_fp8_e4m3fn.safetensors', 'clip_name2': 'clip_l.safetensors', 'type': 'flux'}},
    '22': {'class_type': 'VAELoader', 'inputs': {'vae_name': 'ae.safetensors'}},
    '6': {'class_type': 'CLIPTextEncode', 'inputs': {'text': pos, 'clip': ['21', 0]}},
    '7': {'class_type': 'CLIPTextEncode', 'inputs': {'text': '', 'clip': ['21', 0]}},
    '23': {'class_type': 'FluxGuidance', 'inputs': {'conditioning': ['6', 0], 'guidance': 3.0}},
    '5': {'class_type': 'VAEEncode', 'inputs': {'pixels': ['1', 0], 'vae': ['22', 0]}},
    '3': {'class_type': 'KSampler', 'inputs': {'seed': seed, 'steps': steps, 'cfg': 1.0, 'sampler_name': 'euler', 'scheduler': 'beta', 'denoise': den,
                                               'model': ['20', 0], 'positive': ['23', 0], 'negative': ['7', 0], 'latent_image': ['5', 0]}},
    '8': {'class_type': 'VAEDecode', 'inputs': {'samples': ['3', 0], 'vae': ['22', 0]}},
    '9': {'class_type': 'SaveImage', 'inputs': {'filename_prefix': prefix, 'images': ['8', 0]}},
}
if len(a) > 9:   # масштаб перед кодированием
    wf['2'] = {'class_type': 'ImageScale', 'inputs': {'image': ['1', 0], 'upscale_method': 'lanczos', 'width': int(a[8]), 'height': int(a[9]), 'crop': 'disabled'}}
    wf['5']['inputs']['pixels'] = ['2', 0]
if mask != '-':
    wf['2m'] = {'class_type': 'LoadImageMask', 'inputs': {'image': mask, 'channel': 'red'}}
    wf['10'] = {'class_type': 'SetLatentNoiseMask', 'inputs': {'samples': ['5', 0], 'mask': ['2m', 0]}}
    wf['3']['inputs']['latent_image'] = ['10', 0]
t = time.time()
req = urllib.request.Request(URL + '/prompt', data=json.dumps({'prompt': wf}).encode(), headers={'Content-Type': 'application/json'})
try:
    pid = json.load(urllib.request.urlopen(req))['prompt_id']
except urllib.error.HTTPError as e:
    print('ERROR', e.read().decode()[:1500]); sys.exit(1)
while True:
    h = json.load(urllib.request.urlopen(f'{URL}/history/{pid}'))
    if pid in h:
        st = h[pid].get('status', {})
        outs = [i['filename'] for n in h[pid]['outputs'].values() for i in n.get('images', [])]
        msg = [m for m in st.get('messages', []) if m[0] == 'execution_error']
        print(st.get('status_str', '?'), outs, f'seed={seed}', f'{time.time() - t:.0f}s', (msg[0][1].get('exception_message', '')[:300] if msg else '')); break
    time.sleep(3)
