"""Мини-клиент Chrome DevTools Protocol на стандартной библиотеке (без сторонних пакетов).
Запускает установленный Chrome в headless-режиме с портом отладки, даёт: open(url), ev(js), shot(path), sleep, mouse, viewport.
Анимации идут в реальном времени (в отличие от --virtual-time-budget, где CSS-анимации застывают)."""
import base64, json, os, random, socket, struct, subprocess, time, urllib.request

CHROME = r'C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe'


class WS:
    def __init__(self, url):
        host, rest = url[len('ws://'):].split('/', 1)
        h, p = host.split(':')
        self.s = socket.create_connection((h, int(p)), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((f'GET /{rest} HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                        f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
        buf = b''
        while b'\r\n\r\n' not in buf:
            buf += self.s.recv(4096)
        self.buf = buf.split(b'\r\n\r\n', 1)[1]

    def send(self, text):
        data = text.encode(); n = len(data); mask = os.urandom(4)
        hdr = bytes([0x81]) + (bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + struct.pack('>H', n) if n < 65536 else bytes([0x80 | 127]) + struct.pack('>Q', n))
        self.s.sendall(hdr + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.s.recv(1 << 20)
            if not chunk: raise ConnectionError('ws closed')
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def recv(self):
        msg = b''
        while True:
            b1, b2 = self._read(2); n = b2 & 0x7F
            if n == 126: n = struct.unpack('>H', self._read(2))[0]
            elif n == 127: n = struct.unpack('>Q', self._read(8))[0]
            payload = self._read(n); op = b1 & 0x0F
            if op in (0, 1, 2): msg += payload
            if b1 & 0x80 and op in (0, 1, 2): return msg.decode('utf8', 'replace')


class Browser:
    def __init__(self, port=None, profile=None):
        self.port = port or random.randint(9300, 9399)
        self.profile = profile or os.path.join(os.environ['TEMP'], 'pn_cdp_profile')
        self.proc = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', f'--remote-debugging-port={self.port}', f'--user-data-dir={self.profile}',
                                      '--allow-file-access-from-files', '--hide-scrollbars', '--window-size=1440,900', 'about:blank'],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{self.port}/json')); break
            except Exception:
                time.sleep(.2)
        page = [t for t in tabs if t.get('type') == 'page'][0]
        self.ws = WS(page['webSocketDebuggerUrl']); self.i = 0
        self.call('Page.enable'); self.call('Runtime.enable')

    def call(self, method, **params):
        self.i += 1; mid = self.i
        self.ws.send(json.dumps({'id': mid, 'method': method, 'params': params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get('method') == 'Inspector.detached': raise ConnectionError('detached')
            if m.get('id') == mid:
                if 'error' in m: raise RuntimeError(f"{method}: {m['error']}")
                return m.get('result', {})

    def viewport(self, w, h, mobile=False):
        self.vp = (w, h, mobile)
        self.call('Emulation.setDeviceMetricsOverride', width=w, height=h, deviceScaleFactor=1, mobile=mobile)
        self.call('Emulation.setTouchEmulationEnabled', enabled=mobile)

    def attach(self):
        tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{self.port}/json'))
        page = [t for t in tabs if t.get('type') == 'page'][0]
        self.ws = WS(page['webSocketDebuggerUrl']); self.call('Page.enable'); self.call('Runtime.enable')
        if getattr(self, 'vp', None): self.viewport(*self.vp)

    def open(self, url, wait=0):
        try: self.call('Page.navigate', url=url)
        except Exception: pass
        time.sleep(.25)
        try: self.ev('1')
        except Exception: self.attach()
        if self.ev('location.href') == 'about:blank' or 'EXC' in str(self.ev('1')): self.attach()
        time.sleep(wait)

    def ev(self, js):
        r = self.call('Runtime.evaluate', expression=js, returnByValue=True, awaitPromise=True)
        if 'exceptionDetails' in r: return 'EXC ' + json.dumps(r['exceptionDetails'].get('exception', {}).get('description', r['exceptionDetails']))[:300]
        return r.get('result', {}).get('value')

    def shot(self, path, clip=None):
        p = {'format': 'png'}
        if clip: p['clip'] = dict(x=clip[0], y=clip[1], width=clip[2], height=clip[3], scale=1)
        open(path, 'wb').write(base64.b64decode(self.call('Page.captureScreenshot', **p)['data']))

    def mouse(self, x, y, kind='mouseMoved'):
        self.call('Input.dispatchMouseEvent', type=kind, x=x, y=y, button='left' if kind != 'mouseMoved' else 'none', clickCount=1 if kind != 'mouseMoved' else 0)

    def close(self):
        try: self.call('Browser.close')
        except Exception: pass
        try: self.proc.wait(5)
        except Exception: self.proc.kill()
