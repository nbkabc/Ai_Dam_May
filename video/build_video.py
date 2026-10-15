#!/usr/bin/env python3
"""Dựng video từ bộ hoạt hình: 1 lệnh làm hết (bước chân -> âm thanh -> render khung hình -> ghép mp4).
Ví dụ:  python3 build_video.py --out out/video.mp4 --workers 3
Thử nhanh:  python3 build_video.py --dur 5 --out out/thu.mp4   (đo tốc độ rồi suy ra video dài)"""
import argparse, json, os, subprocess, sys, tempfile, time, shutil, glob
H = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--anim", default="anim2.html"); ap.add_argument("--timeline", default="timeline2.json")
ap.add_argument("--audio-script", default="make_audio2.py"); ap.add_argument("--out", default="out/video.mp4")
ap.add_argument("--workers", type=int, default=3, help="số tiến trình Chromium song song (Mac 8GB nên 2-3)")
ap.add_argument("--fps", type=float, default=0, help="0 = theo timeline"); ap.add_argument("--dur", type=float, default=0, help="0 = cả video; hoặc số giây để thử")
ap.add_argument("--voice", default="", help="file mp3/wav giọng đọc (mặc định lấy từ timeline[\"audio\"] nếu có)"); ap.add_argument("--sfx-vol", type=float, default=.22)
ap.add_argument("--frames-dir", default=""); ap.add_argument("--keep-frames", action="store_true")
a = ap.parse_args()
TL = json.load(open(os.path.join(H, a.timeline)))
fps = a.fps or TL["fps"]; dur = a.dur or TL["dur"]; N = int(round(fps * dur))
frames = a.frames_dir or tempfile.mkdtemp(prefix="frames-")
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
env = dict(os.environ, ANIM=a.anim, TIMELINE=a.timeline, OUT=frames, FPS=str(fps), DUR=str(dur))
t0 = time.time()
def run(cmd, **kw):
    r = subprocess.run(cmd, cwd=H, **kw)
    if r.returncode: sys.exit(f"Lỗi khi chạy: {' '.join(cmd)}")
print(f"[1/4] Trích bước chân...")
run(["node", "steps_extract.js", "steps.json"], env=env)
print("[2/4] Tạo âm thanh...")
wav = os.path.join(frames, "sfx.wav")
run([sys.executable, a.audio_script, wav], env=env)
print(f"[3/4] Render {N} khung hình ({fps:g} fps) bằng {a.workers} tiến trình...")
per = (N + a.workers - 1) // a.workers; procs = []
for k in range(a.workers):
    lo, hi = k * per, min(N - 1, (k + 1) * per - 1)
    if lo > hi: continue
    procs.append(subprocess.Popen(["node", "render_frames.js"], cwd=H, env=dict(env, FROM=str(lo), TO=str(hi))))
while any(p.poll() is None for p in procs):
    n = len(glob.glob(os.path.join(frames, "f_*.jpg"))); el = time.time() - t0
    print(f"\r  {n}/{N} khung ({100 * n // N}%), đã chạy {el / 60:.1f} phút", end="", flush=True); time.sleep(5)
print()
if any(p.returncode for p in procs): sys.exit("Có tiến trình render bị lỗi (thường do thiếu playwright/chromium hoặc hết bộ nhớ). Thử --workers 2.")
print("[4/4] Ghép video + âm thanh...")
voice = a.voice or TL.get("audio", "")
if voice and not os.path.isabs(voice): voice = os.path.join(H, voice)
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", f"{fps:g}", "-i", os.path.join(frames, "f_%05d.jpg"), "-i", wav]
if voice:
    cmd += ["-i", voice, "-filter_complex", f"[1:a]volume={a.sfx_vol}[s];[s][2:a]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[o]", "-map", "0:v", "-map", "[o]"]
else: cmd += ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"]
run(cmd + ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", "-t", f"{dur:g}", os.path.abspath(a.out)])
el = time.time() - t0
print(f"Xong: {a.out} | {dur:g}s video mất {el / 60:.1f} phút ({el / dur:.1f}s render cho mỗi 1s video)")
if not a.keep_frames and not a.frames_dir: shutil.rmtree(frames, ignore_errors=True)
