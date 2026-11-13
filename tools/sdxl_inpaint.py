"""Перерисовка области по маске (RealVisXL + VAEEncodeForInpaint).
Usage: py -3 tools/sdxl_inpaint.py <rgba.png в ComfyUI/input, прозрачное = перерисовать> <prefix> "<prompt>" [steps]"""
import json, sys, time, urllib.request, random

URL = 'http://127.0.0.1:8188'
src, prefix, pos = sys.argv[1], sys.argv[2], sys.argv[3]
steps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
NEG = 'keys, metal, strap, lanyard, ribbon, string, deformed, blurry, text, watermark'
wf = {
    '1': {'class_type': 'LoadImage', 'inputs': {'image': src}},
    '4': {'class_type': 'CheckpointLoaderSimple', 'inputs': {'ckpt_name': 'RealVisXL_V5.0_fp16.safetensors'}},
    '5': {'class_type': 'VAEEncodeForInpaint', 'inputs': {'pixels': ['1', 0], 'vae': ['4', 2], 'mask': ['1', 1], 'grow_mask_by': 10}},
    '6': {'class_type': 'CLIPTextEncode', 'inputs': {'text': pos, 'clip': ['4', 1]}},
    '7': {'class_type': 'CLIPTextEncode', 'inputs': {'text': NEG, 'clip': ['4', 1]}},
    '3': {'class_type': 'KSampler', 'inputs': {'seed': random.randint(1, 2 ** 31), 'steps': steps, 'cfg': 5.0, 'sampler_name': 'dpmpp_2m_sde', 'scheduler': 'karras',
                                               'denoise': 1.0, 'model': ['4', 0], 'positive': ['6', 0], 'negative': ['7', 0], 'latent_image': ['5', 0]}},
    '8': {'class_type': 'VAEDecode', 'inputs': {'samples': ['3', 0], 'vae': ['4', 2]}},
    '9': {'class_type': 'SaveImage', 'inputs': {'filename_prefix': prefix, 'images': ['8', 0]}},
}
t = time.time()
req = urllib.request.Request(URL + '/prompt', data=json.dumps({'prompt': wf}).encode(), headers={'Content-Type': 'application/json'})
pid = json.load(urllib.request.urlopen(req))['prompt_id']
while True:
    h = json.load(urllib.request.urlopen(f'{URL}/history/{pid}'))
    if pid in h:
        print(h[pid]['status'].get('status_str'), [i['filename'] for n in h[pid]['outputs'].values() for i in n.get('images', [])], f'{time.time() - t:.0f}s')
        break
    time.sleep(2)
