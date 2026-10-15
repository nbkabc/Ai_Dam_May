"""Tổng hợp tiếng động (không cần file mẫu) khớp timeline.json. Chạy: python3 make_audio.py out.wav"""
import json, sys, wave
import numpy as np
SR = 44100
TL = json.load(open(__file__.replace("make_audio2.py", "timeline2.json")))
rng = np.random.default_rng(7)
def tt(d): return np.arange(int(SR * d)) / SR
def lp(x, a):
    y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x): s += a * (v - s); y[i] = s
    return y
def pop():
    t = tt(.12); f = 200 + 700 * np.exp(-t * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35) * .8
def boing():
    t = tt(.55); f = 190 + 130 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4) + 260 * np.exp(-t * 14)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5) * .8
def whoosh(d=.4):
    t = tt(d); n = rng.standard_normal(len(t)); x = lp(n, .12) - lp(n, .02); e = np.sin(np.pi * t / d) ** 2
    return x * e * 5.0
def ting():
    t = tt(.8); return (np.sin(2 * np.pi * 1318 * t) * np.exp(-t * 7) + .6 * np.sin(2 * np.pi * 1976 * t) * np.exp(-t * 9) + .3 * np.sin(2 * np.pi * 2637 * t) * np.exp(-t * 12)) * .55
def ding():
    t = tt(1.0); return (np.sin(2 * np.pi * 1047 * t) * np.exp(-t * 4) + .7 * np.sin(2 * np.pi * 1568 * t) * np.exp(-t * 5)) * .5
def tick():
    t = tt(.025); n = rng.standard_normal(len(t)); return (n - lp(n, .3)) * np.exp(-t * 260) * .35
def clock():
    t = tt(.04); return np.sin(2 * np.pi * 1500 * t) * np.exp(-t * 130) * .5
def thunk():
    t = tt(.25); return np.sin(2 * np.pi * 85 * t) * np.exp(-t * 20) * .9
def huh():
    t = tt(.3); f = 300 + 260 * (t / .3) ** 1.3; return np.sin(2 * np.pi * np.cumsum(f) / SR + 4 * np.sin(2 * np.pi * 8 * t)) * np.sin(np.pi * t / .3) * .45
def sparkle():
    out = np.zeros(int(SR * .7))
    for k in range(8):
        f = rng.uniform(2200, 4200); t = tt(.12); s = np.sin(2 * np.pi * f * t) * np.exp(-t * 30) * .25; i = int(rng.uniform(0, .5) * SR); out[i:i + len(s)] += s
    return out
def tada():
    out = np.zeros(int(SR * 1.4))
    for k, f in enumerate([523, 659, 784, 1047]):
        t = tt(1.2 - .06 * k); s = (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t * 3.2) * .35; i = int(.06 * k * SR); out[i:i + len(s)] += s
    t = tt(.7); n = rng.standard_normal(len(t)); sh = (n - lp(n, .35)) * np.exp(-t * 5) * .5; out[:len(sh)] += sh
    return out
def pop_high(): return pop()[::1] * 0 + np.sin(2 * np.pi * np.cumsum(500 + 1300 * np.exp(-tt(.1) * 40)) / SR) * np.exp(-tt(.1) * 40)


def step(loud=1.0):
    t = tt(.09); n = rng.standard_normal(len(t)); body = np.sin(2 * np.pi * 110 * t) * np.exp(-t * 45); tap = (n - lp(n, .25)) * np.exp(-t * 90) * .35
    return (body * .8 + tap) * .5 * loud
def beep():
    t = tt(.09); return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 12) * .35
def thud():
    t = tt(.2); return np.sin(2 * np.pi * 70 * t) * np.exp(-t * 22) * .8
steps = json.load(open(__file__.replace("make_audio2.py", "steps.json")))
ev = []
add = lambda t, s, g=1.0: ev.append((t, s, g))
for s in steps: add(s["t"], step(1.5 if s["run"] else 1.0), .55 if s["run"] else .4)
add(3.3, beep(), .8); add(3.42, beep(), .8)
add(3.4, boing(), .8); add(3.45, huh(), .6)
for c in TL["captions"]:
    add(c["s"] - .05, whoosh(.3), .3)
    for k in range(0, len(c["text"]), 3): add(c["s"] + .25 + k / TL["cps"], tick(), .5)
for j in TL["jumps"]: add(j["t"], pop(), .5); add(j["t"] + j["d"], thud(), .7)
for d in TL["drops"]: add(d + .22, ting(), .8)
add(TL["walletIn"], pop(), .8); add(14.6, ding(), .6)
for h in TL["coinHops"]: add(h + .9, ting(), .7)
add(18.5, sparkle(), .6)
for c in TL["cards"]: add(c + .12, pop(), .8)
add(24.6, thunk(), .5)
add(TL["confetti"], tada(), .9); add(TL["endcard"], pop(), .8)
buf = np.zeros(int(SR * (TL["dur"] + 1.5)))
for t, s, g in ev:
    i = int(t * SR); n = min(len(s), len(buf) - i)
    if n > 0: buf[i:i + n] += s[:n] * g
buf = buf[:int(SR * TL["dur"])]; buf *= .89 / max(1e-6, np.abs(buf).max())
fade = int(.05 * SR); buf[-fade:] *= np.linspace(1, 0, fade)
pcm = (buf * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", len(ev), "âm thanh,", round(len(pcm) / SR, 1), "s")
