"""Hi-res проход RealVisXL (img2img): увеличивает картинку и дорисовывает детали.
Usage: py -3 tools/sdxl_hires.py <input.png из ComfyUI/output> <W> <H> <prefix> "<prompt>" [denoise]"""
import json, sys, time, urllib.request, random

URL = 'http://127.0.0.1:8188'
src, W, H, prefix, pos = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
den = float(sys.argv[6]) if len(sys.argv) > 6 else 0.32
NEG = 'cartoon, illustration, cgi, text, watermark, logo, deformed, blurry, lowres, extra fingers, bad hands, oversaturated'
wf = {
    '1': {'class_type': 'LoadImage', 'inputs': {'image': src}},
    '2': {'class_type': 'ImageScale', 'inputs': {'image': ['1', 0], 'upscale_method': 'lanczos', 'width': W, 'height': H, 'crop': 'disabled'}},
    '4': {'class_type': 'CheckpointLoaderSimple', 'inputs': {'ckpt_name': 'RealVisXL_V5.0_fp16.safetensors'}},
    '5': {'class_type': 'VAEEncode', 'inputs': {'pixels': ['2', 0], 'vae': ['4', 2]}},
    '6': {'class_type': 'CLIPTextEncode', 'inputs': {'text': pos, 'clip': ['4', 1]}},
    '7': {'class_type': 'CLIPTextEncode', 'inputs': {'text': NEG, 'clip': ['4', 1]}},
    '3': {'class_type': 'KSampler', 'inputs': {'seed': random.randint(1, 2 ** 31), 'steps': 28, 'cfg': 4.5, 'sampler_name': 'dpmpp_2m_sde', 'scheduler': 'karras',
                                               'denoise': den, 'model': ['4', 0], 'positive': ['6', 0], 'negative': ['7', 0], 'latent_image': ['5', 0]}},
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
