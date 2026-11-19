# Efectos de sonido sintetizados a partir de events.json + colchón suave -> out/foley.wav
import json, os, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
ev = json.load(open(f'{HERE}/events.json')); dur = ev['dur']
buf = np.zeros((int((dur + .5) * SR), 2), np.float32)
R = np.random.default_rng(7)
def t_(d): return np.arange(int(d * SR)) / SR
def env(d, tau, att=.004):
    t = t_(d); return np.minimum(1, t / att) * np.exp(-t / tau)
def noise(d): return R.standard_normal(int(d * SR))
def lp(x, a):
    y = np.zeros_like(x); s = 0.
    for i in range(len(x)): s += a * (x[i] - s); y[i] = s
    return y
def norm(x): m = np.abs(x).max(); return x / m if m > 0 else x
def tone(f, d, tau, h=(1, .3, .1)):
    t = t_(d); return norm(sum(a * np.sin(2 * np.pi * f * (k + 1) * t) for k, a in enumerate(h)) * env(d, tau))
def add(x, at, g=1., pan=0.):
    i = int(max(0, at) * SR); x = x[:len(buf) - i]
    buf[i:i + len(x), 0] += x * g * (1 - max(0, pan)); buf[i:i + len(x), 1] += x * g * (1 + min(0, pan))
def whoosh(d=.5):
    t = t_(d); w = np.sin(np.pi * t / d) ** 2
    hi = noise(d) - lp(noise(d), .05)
    return norm(lp(hi, .25) * w)
def pop(): d = .12; t = t_(d); f = 520 * np.exp(-t * 18) + 380; return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .03))
def tick(): d = .03; return norm((noise(d) - lp(noise(d), .2)) * env(d, .004))
def shutter():
    a = norm((noise(.05) - lp(noise(.05), .3)) * env(.05, .008)); b = np.zeros(int(.09 * SR)); return np.concatenate([a, b, a * .8])
def ding(f=1318.5): return tone(f, .7, .2, (1, 0, .25, 0, .08)) * .8 + tone(f * 1.5, .7, .15, (1,)) * .3
def slide(): d = .5; t = t_(d); return norm(lp(noise(d), .08) * np.sin(np.pi * t / d) ** 1.5)
def marker(): d = .45; t = t_(d); return norm(lp(noise(d), .35) * np.sin(np.pi * t / d) ** .8)
def thump(): d = .3; t = t_(d); f = 110 * np.exp(-t * 8) + 50; return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .09))
G = {'whoosh': (lambda e: whoosh(), .2), 'pop': (lambda e: pop(), .22), 'tick': (lambda e: tick(), .08),
     'shutter': (lambda e: shutter(), .5), 'ding': (lambda e: ding(), .3), 'slide': (lambda e: slide(), .25),
     'marker': (lambda e: marker(), .28), 'drop': (lambda e: thump(), .45)}
cache = {}
for i, e in enumerate(ev['ev']):
    f, g = G[e['type']]
    if e['type'] not in ('whoosh', 'slide', 'marker'):
        if e['type'] not in cache: cache[e['type']] = f(e).astype(np.float32)
        x = cache[e['type']]
    else: x = f(e).astype(np.float32)
    add(x, e['t'], g, ((i * .37) % .6 - .3) if e['type'] in ('pop', 'tick') else 0.)
t = t_(dur + .5)
pad = sum(np.sin(2 * np.pi * f * t + p) for f, p in [(146.83, 0), (220., 1), (293.66, 2), (329.63, 3), (440., .5)])
pad *= (.6 + .4 * np.sin(2 * np.pi * t / 7.)) * np.minimum(1, t / 2.) * np.minimum(1, (dur + .5 - t) / 2.)
pad = np.convolve(pad / 5, np.ones(200) / 200, mode='same')
buf[:, 0] += pad * .05; buf[:, 1] += pad * .05
buf *= .35 / np.abs(buf).max()
os.makedirs(f'{HERE}/out', exist_ok=True)
sf.write(f'{HERE}/out/foley.wav', buf, SR); print('foley ok', buf.shape)
