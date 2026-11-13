"""RealVisXL V5 (SDXL) via the local ComfyUI API. Usage: py -3 tools/sdxl_gen.py jobs.json
job: name, pos, [neg], [w], [h], [seed], [steps]"""
import json, random, sys, time, urllib.request

URL = 'http://127.0.0.1:8188'
NEG = 'cartoon, illustration, 3d render, cgi, text, watermark, logo, letters, deformed, blurry, lowres, extra fingers, bad hands, oversaturated'


def wf(j):
    return {
        '4': {'class_type': 'CheckpointLoaderSimple', 'inputs': {'ckpt_name': 'RealVisXL_V5.0_fp16.safetensors'}},
        '5': {'class_type': 'EmptyLatentImage', 'inputs': {'width': j.get('w', 1344), 'height': j.get('h', 768), 'batch_size': 1}},
        '6': {'class_type': 'CLIPTextEncode', 'inputs': {'text': j['pos'], 'clip': ['4', 1]}},
        '7': {'class_type': 'CLIPTextEncode', 'inputs': {'text': j.get('neg', NEG), 'clip': ['4', 1]}},
        '3': {'class_type': 'KSampler', 'inputs': {'seed': j.get('seed') or random.randint(1, 2 ** 31), 'steps': j.get('steps', 30), 'cfg': 5.0,
                                                   'sampler_name': 'dpmpp_2m_sde', 'scheduler': 'karras', 'denoise': 1.0,
                                                   'model': ['4', 0], 'positive': ['6', 0], 'negative': ['7', 0], 'latent_image': ['5', 0]}},
        '8': {'class_type': 'VAEDecode', 'inputs': {'samples': ['3', 0], 'vae': ['4', 2]}},
        '9': {'class_type': 'SaveImage', 'inputs': {'filename_prefix': j['name'], 'images': ['8', 0]}},
    }


def run(j):
    t = time.time()
    req = urllib.request.Request(URL + '/prompt', data=json.dumps({'prompt': wf(j)}).encode(), headers={'Content-Type': 'application/json'})
    pid = json.load(urllib.request.urlopen(req))['prompt_id']
    while True:
        h = json.load(urllib.request.urlopen(f'{URL}/history/{pid}'))
        if pid in h:
            outs = [i['filename'] for n in h[pid]['outputs'].values() for i in n.get('images', [])]
            print(h[pid]['status'].get('status_str'), outs, f'{time.time() - t:.0f}s', flush=True)
            return outs
        time.sleep(1)


if __name__ == '__main__':
    for j in json.load(open(sys.argv[1], encoding='utf8')):
        run(j)
