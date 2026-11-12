"""FLUX.1-dev (GGUF) + optional In-Context-LoRA via the local ComfyUI API.
Usage: py -3 tools/flux_gen.py jobs.json   (job: name, pos, w, h, steps, lora (0..1), seed)"""
import json, random, sys, time, urllib.request

URL = 'http://127.0.0.1:8188'


def wf(j):
    seed = j.get('seed') or random.randint(1, 2 ** 31)
    g = {
        '1': {'class_type': 'UnetLoaderGGUF', 'inputs': {'unet_name': j.get('unet', 'flux1-dev-Q4_K_S.gguf')}},
        '2': {'class_type': 'DualCLIPLoader', 'inputs': {'clip_name1': 't5xxl_fp8_e4m3fn.safetensors', 'clip_name2': 'clip_l.safetensors', 'type': 'flux'}},
        '3': {'class_type': 'VAELoader', 'inputs': {'vae_name': 'ae.safetensors'}},
        '6': {'class_type': 'CLIPTextEncode', 'inputs': {'text': j['pos'], 'clip': ['2', 0]}},
        '7': {'class_type': 'FluxGuidance', 'inputs': {'guidance': j.get('guidance', 3.5), 'conditioning': ['6', 0]}},
        '8': {'class_type': 'EmptySD3LatentImage', 'inputs': {'width': j.get('w', 1024), 'height': j.get('h', 1024), 'batch_size': 1}},
        '9': {'class_type': 'KSampler', 'inputs': {'seed': seed, 'steps': j.get('steps', 22), 'cfg': 1.0, 'sampler_name': 'euler', 'scheduler': 'simple',
                                                   'denoise': 1.0, 'model': ['1', 0], 'positive': ['7', 0], 'negative': ['7', 0], 'latent_image': ['8', 0]}},
        '10': {'class_type': 'VAEDecode', 'inputs': {'samples': ['9', 0], 'vae': ['3', 0]}},
        '11': {'class_type': 'SaveImage', 'inputs': {'filename_prefix': j['name'], 'images': ['10', 0]}},
    }
    if j.get('lora'):
        g['4'] = {'class_type': 'LoraLoaderModelOnly', 'inputs': {'lora_name': j.get('lora_name', 'visual-identity-design.safetensors'), 'strength_model': j['lora'], 'model': ['1', 0]}}
        g['9']['inputs']['model'] = ['4', 0]
    return g


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
        time.sleep(2)


if __name__ == '__main__':
    for j in json.load(open(sys.argv[1], encoding='utf8')):
        run(j)
