"""Перерисовка кадра поверх исходника по маске (img2img с маской шума): белое в маске — перерисовать, чёрное — оставить.
Геометрия сохраняется (не «с нуля», как при inpaint), закрытые области потом вклеиваются из исходника пиксель в пиксель.
Usage: py -3 tools/sdxl_masked_i2i.py <src.png в ComfyUI/input> <mask.png в ComfyUI/input> <prefix> "<prompt>" <denoise> [seed] ["<negative>"]"""
import json, random, sys, time, urllib.request

URL = 'http://127.0.0.1:8188'
src, mask, prefix, pos, den = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5])
seed = int(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6] else random.randint(1, 2 ** 31)
neg = sys.argv[7] if len(sys.argv) > 7 else ('cartoon, illustration, 3d render, cgi, text, watermark, logo, deformed, blurry, lowres, fisheye, '
                                            'oversaturated, fireplace, people, clutter, ugly furniture, distorted perspective')
wf = {
    '1': {'class_type': 'LoadImage', 'inputs': {'image': src}},
    '2': {'class_type': 'LoadImageMask', 'inputs': {'image': mask, 'channel': 'red'}},
    '4': {'class_type': 'CheckpointLoaderSimple', 'inputs': {'ckpt_name': 'RealVisXL_V5.0_fp16.safetensors'}},
    '5': {'class_type': 'VAEEncode', 'inputs': {'pixels': ['1', 0], 'vae': ['4', 2]}},
    '10': {'class_type': 'SetLatentNoiseMask', 'inputs': {'samples': ['5', 0], 'mask': ['2', 0]}},
    '6': {'class_type': 'CLIPTextEncode', 'inputs': {'text': pos, 'clip': ['4', 1]}},
    '7': {'class_type': 'CLIPTextEncode', 'inputs': {'text': neg, 'clip': ['4', 1]}},
    '3': {'class_type': 'KSampler', 'inputs': {'seed': seed, 'steps': 32, 'cfg': 5.0, 'sampler_name': 'dpmpp_2m_sde', 'scheduler': 'karras',
                                               'denoise': den, 'model': ['4', 0], 'positive': ['6', 0], 'negative': ['7', 0], 'latent_image': ['10', 0]}},
    '8': {'class_type': 'VAEDecode', 'inputs': {'samples': ['3', 0], 'vae': ['4', 2]}},
    '9': {'class_type': 'SaveImage', 'inputs': {'filename_prefix': prefix, 'images': ['8', 0]}},
}
t = time.time()
req = urllib.request.Request(URL + '/prompt', data=json.dumps({'prompt': wf}).encode(), headers={'Content-Type': 'application/json'})
pid = json.load(urllib.request.urlopen(req))['prompt_id']
while True:
    h = json.load(urllib.request.urlopen(f'{URL}/history/{pid}'))
    if pid in h:
        st = h[pid].get('status', {})
        outs = [i['filename'] for n in h[pid]['outputs'].values() for i in n.get('images', [])]
        print(st.get('status_str', '?'), outs, f'seed={seed}', f'{time.time() - t:.0f}s'); break
    time.sleep(2)
