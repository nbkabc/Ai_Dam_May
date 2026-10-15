#!/usr/bin/env python3
"""Canh timeline4.json theo file giọng thật: python3 make_timeline_voice.py voice.mp3
Tìm các quãng lặng, chia câu thành đoạn phụ đề theo tỉ lệ số từ, chọn quãng lặng gần nhất làm ranh giới."""
import json, re, subprocess, sys
mp3 = sys.argv[1]; TAIL = 1.8
src = open("make_timeline4.py").read(); SC = eval("[" + src.split("SC = [", 1)[1].split("\nt = LEAD")[0])
dur_a = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3]))
out = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", "silencedetect=noise=-35dB:d=0.18", "-f", "null", "-"], capture_output=True, text=True).stderr
S = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]; E = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
pauses = list(zip(S, E[:len(S)]))
if len(E) < len(S): pauses[-1] = (S[-1], dur_a)
speech_end = pauses[-1][0] if pauses and pauses[-1][1] >= dur_a - .6 else dur_a
if pauses and pauses[-1][1] >= dur_a - .6: pauses = pauses[:-1]
LONG = [p for p in pauses if p[1] - p[0] > .8]
OVERRIDE = {'Lúc đó': [51.3, 54.96]}  # chỉnh tay khi tỉ lệ số từ lệch (thời điểm bắt đầu các đoạn sau)
words = lambda s: len(s.replace(",", "").split())
# câu = các chunk liên tiếp kết thúc bằng dấu chấm
sents = []; cur = []
for sid, chunks in SC:
    for c in chunks:
        cur.append((sid, c))
        if c[0].rstrip().endswith("."): sents.append(cur); cur = []
if cur: sents.append(cur)
assert len(sents) == len(LONG) + 1, (len(sents), len(LONG))
bounds = [0.0] + [p[1] for p in LONG] + [speech_end]
caps = []; order = []; scenes = {}
for k, sn in enumerate(sents):
    a, b = bounds[k], (LONG[k][0] if k < len(LONG) else speech_end)
    inner = [p for p in pauses if a + .05 < p[0] and p[1] < b - .05 and p[1] - p[0] <= .8]
    # trục thời gian chỉ tính tiếng nói
    def sp(t): return t - sum(min(max(t, x) , y) - x for x, y in inner if t > x)
    total = sp(b); W = [words(c[0]) for _, c in sn]; cums = [sum(W[:j + 1]) for j in range(len(sn) - 1)]
    import itertools
    best = None
    for comb in itertools.combinations(range(len(inner)), len(sn) - 1):
        err = sum(abs(sp(inner[q][0]) - total * cm / sum(W)) for q, cm in zip(comb, cums))
        if best is None or err < best[0]: best = (err, comb)
    starts = [a] + ([inner[q][1] for q in best[1]] if best else [])
    ov = OVERRIDE.get(sn[0][1][0][:6])
    if ov: starts = [a] + ov
    starts = sorted(starts)
    for j, (sid, c) in enumerate(sn):
        s = starts[j]; e = starts[j + 1] if j + 1 < len(sn) else b
        caps.append({"s": round(s, 2), "e": round(e, 2), "text": c[0], "hl": c[1], "sid": sid})
# kéo dài đoạn phụ đề tới khi đoạn kế tiếp bắt đầu (liền mạch cảnh)
for i, c in enumerate(caps):
    nxt = caps[i + 1]["s"] if i + 1 < len(caps) else None
    c["e"] = round(nxt if nxt is not None else speech_end + .3, 2)
    c["cps"] = round(max(14, min(40, len(c["text"]) / max(.5, (min(c["e"], c["s"] + 4) - c["s"]) * .8))), 1)
    if i + 1 < len(caps) and caps[i + 1]["s"] - c["s"] > 0:
        # tiếng nói thật của đoạn kết thúc ở quãng lặng; cho chữ chạy xong trước đó
        pass
for sid, _ in SC:
    cs = [c for c in caps if c["sid"] == sid]; order.append(sid)
    scenes[sid] = {"s": cs[0]["s"], "e": 0}
for i, sid in enumerate(order): scenes[sid]["e"] = scenes[order[i + 1]]["s"] if i + 1 < len(order) else caps[-1]["e"]
scenes[order[0]]["s"] = 0.0
dur = round(caps[-1]["e"] + TAIL, 2)
for c in caps: del c["sid"]
json.dump({"fps": 24, "dur": dur, "cps": 18, "ground": 612, "scenes": scenes, "order": order, "captions": caps, "audio": mp3}, open("timeline5.json", "w"), ensure_ascii=False, indent=1)
print("tổng", dur, "s"); [print(f"  {k:8s} {v['s']:6.2f} - {v['e']:6.2f}  ({v['e']-v['s']:.2f}s)") for k, v in scenes.items()]
