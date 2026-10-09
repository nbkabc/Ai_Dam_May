"""So sánh phong cách minh họa cho cùng chủ đề: giá Bitcoin tăng. Chạy: python3 gen_styles.py"""
import os, math
from PIL import Image, ImageDraw, ImageFont
from gen_scenes import render, svg, grad

DATA = [20, 24, 22, 30, 28, 38, 36, 48, 55, 52, 68, 75]
F = 'font-family="Arial,Helvetica,sans-serif"'

def pts(x0, y0, w, h, data=DATA):
    lo, hi = min(data), max(data)
    n = len(data) - 1
    return [(x0 + w * i / n, y0 + h - h * (v - lo) / (hi - lo)) for i, v in enumerate(data)]

def s_data():
    p = pts(120, 220, 1040, 380)
    line = " ".join(f"{x:.0f},{y:.0f}" for x, y in p)
    area = line + f" 1160,600 120,600"
    b = '<rect width="1280" height="720" fill="#0B1F3A"/>'
    b += '<g stroke="#2a4468" stroke-width="2">' + "".join(f'<path d="M120 {y}H1160"/>' for y in (220, 315, 410, 505, 600)) + '</g>'
    b += f'<polygon points="{area}" fill="url(#a)"/><polyline points="{line}" fill="none" stroke="#00D68F" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>'
    b += f'<circle cx="{p[-1][0]:.0f}" cy="{p[-1][1]:.0f}" r="13" fill="#0B1F3A" stroke="#7DFFC4" stroke-width="6"/>'
    b += f'<text x="120" y="120" {F} font-size="30" fill="#8fa6c4" letter-spacing="4">BTC / USD · 12 THÁNG</text>'
    b += f'<text x="120" y="190" {F} font-size="76" font-weight="700" fill="#fff">+275%</text>'
    b += f'<text x="1160" y="650" {F} font-size="22" fill="#6f87a8" text-anchor="end">Số liệu minh họa</text>'
    defs = '<linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00D68F" stop-opacity=".45"/><stop offset="1" stop-color="#00D68F" stop-opacity="0"/></linearGradient>'
    return svg(b, defs)

def iso(x, y, w, d, h, top, left, right):
    # x,y: góc đáy giữa; w,d nửa kích thước theo trục
    a = (x, y); r = (x + w, y - w / 2); l = (x - d, y - d / 2); f = (x + w - d, y - w / 2 - d / 2)
    def up(p): return (p[0], p[1] - h)
    P = lambda *q: " ".join(f"{u:.0f},{v:.0f}" for u, v in q)
    o = f'<polygon points="{P(l,a,up(a),up(l))}" fill="{left}"/>'
    o += f'<polygon points="{P(a,r,up(r),up(a))}" fill="{right}"/>'
    o += f'<polygon points="{P(up(l),up(a),up(r),up(f))}" fill="{top}"/>'
    return o

def s_iso():
    b = '<rect width="1280" height="720" fill="#E8EEF6"/>'
    b += '<polygon points="140,560 640,810 1140,560 640,310" fill="#cfd9e8"/><polygon points="140,560 640,810 640,830 140,580" fill="#aebbd0"/><polygon points="1140,560 640,810 640,830 1140,580" fill="#97a7bf"/>'
    hs = [40, 70, 60, 110, 150, 210]
    for i, h in enumerate(hs):
        x = 270 + i * 130; y = 560 + i * 26 - 150 + 150
        y = 520 + i * 0
        xx = 250 + i * 135; yy = 560 - i * 8 + 40
        b += iso(xx, yy, 56, 56, h, "#4bd8a4", "#0f6f58", "#16a37f") if i == 5 else iso(xx, yy, 56, 56, h, "#8ba6cf", "#2a4770", "#3b5f93")
    cx, cy = 250 + 5 * 135 + 0, 560 - 5 * 8 + 40 - 210 - 90
    b += f'<ellipse cx="{cx}" cy="{cy+60}" rx="60" ry="14" fill="#000" opacity=".12"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="52" ry="52" fill="#f2b632"/><ellipse cx="{cx}" cy="{cy}" rx="40" ry="40" fill="none" stroke="#c88a0a" stroke-width="5"/>'
    b += f'<text x="{cx}" y="{cy+16}" {F} font-size="48" font-weight="700" text-anchor="middle" fill="#9a6a05">₿</text>'
    b += f'<text x="90" y="110" {F} font-size="52" font-weight="700" fill="#0B1F3A">Bitcoin tăng tốc</text><text x="90" y="156" {F} font-size="26" fill="#58708f">Minh họa isometric</text>'
    return svg(b)

def s_blueprint():
    p = pts(160, 230, 960, 330)
    line = " ".join(f"{x:.0f},{y:.0f}" for x, y in p)
    b = '<rect width="1280" height="720" fill="#0B3A6B"/>'
    b += '<g stroke="#2b5f95" stroke-width="1.5">' + "".join(f'<path d="M{x} 0V720"/>' for x in range(0, 1280, 40)) + "".join(f'<path d="M0 {y}H1280"/>' for y in range(0, 720, 40)) + '</g>'
    b += '<g stroke="#fff" fill="none" stroke-width="3"><rect x="60" y="60" width="1160" height="600"/><path d="M160 230V570H1120"/></g>'
    b += f'<polyline points="{line}" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="14 8"/>'
    for x, y in p[::3]: b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="#0B3A6B" stroke="#fff" stroke-width="3"/>'
    b += '<g stroke="#9fd0ff" stroke-width="2" fill="none"><path d="M1160 230V570"/><path d="M1148 230H1172M1148 570H1172"/></g>'
    b += f'<text x="1180" y="410" {F} font-size="22" fill="#9fd0ff" transform="rotate(90 1180 410)" text-anchor="middle">Δ = +275%</text>'
    b += f'<text x="100" y="125" {F} font-size="34" fill="#fff" letter-spacing="3">FIG. 01 — BTC/USD PRICE RESPONSE</text>'
    b += f'<text x="1180" y="630" {F} font-size="20" fill="#9fd0ff" text-anchor="end">SCALE 1:1 · SỐ LIỆU MINH HỌA</text>'
    return svg(b)

def s_neon():
    p = pts(140, 200, 1000, 300)
    line = " ".join(f"{x:.0f},{y:.0f}" for x, y in p)
    b = '<rect width="1280" height="720" fill="#05070F"/>'
    b += '<g stroke="#7a2cff" stroke-width="2" opacity=".6">'
    for i in range(-10, 21): b += f'<path d="M{640+i*70} 520L{640+i*220} 720"/>'
    for k, y in enumerate((540, 570, 610, 660)): b += f'<path d="M0 {y}H1280"/>'
    b += '</g>'
    b += f'<polyline points="{line}" fill="none" stroke="#00FFA3" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" filter="url(#g)"/><polyline points="{line}" fill="none" stroke="#C9FFE9" stroke-width="4"/>'
    b += f'<text x="140" y="130" {F} font-size="84" font-weight="800" fill="#fff" filter="url(#g2)">BTC</text><text x="140" y="170" {F} font-size="26" fill="#ff3df2" letter-spacing="8">ĐANG TĂNG</text>'
    defs = '<filter id="g" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="10"/></filter><filter id="g2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    return svg(b, defs)

def s_editorial():
    p = pts(110, 250, 1060, 300)
    line = " ".join(f"{x:.0f},{y:.0f}" for x, y in p)
    b = '<rect width="1280" height="720" fill="#F5F0E6"/><rect width="1280" height="14" fill="#C8102E"/><rect x="60" y="14" width="90" height="34" fill="#C8102E"/>'
    b += f'<text x="60" y="130" {F} font-size="54" font-weight="700" fill="#111">Bitcoin leo thang</text><text x="60" y="178" {F} font-size="28" fill="#555">Giá Bitcoin, USD, chỉ số cơ sở = 100</text>'
    ticks = [(150, 495), (200, 441), (250, 386), (300, 332), (350, 277)]
    b += '<g stroke="#cfc8b8" stroke-width="2">' + "".join(f'<path d="M60 {y}H1220"/>' for _, y in ticks) + '</g>'
    b += f'<polyline points="{line}" fill="none" stroke="#0B6E8E" stroke-width="6" stroke-linejoin="round"/>'
    b += f'<circle cx="{p[-1][0]:.0f}" cy="{p[-1][1]:.0f}" r="9" fill="#C8102E"/><text x="{p[-1][0]-14:.0f}" y="{p[-1][1]-22:.0f}" {F} font-size="30" font-weight="700" fill="#C8102E" text-anchor="end">375</text>'
    b += "".join(f'<text x="1226" y="{y-8}" {F} font-size="22" fill="#555" text-anchor="end">{v}</text>' for v, y in ticks)
    b += f'<text x="60" y="650" {F} font-size="20" fill="#777">Nguồn: số liệu minh họa</text>'
    return svg(b)

def s_geo():
    b = '<rect width="1280" height="720" fill="#0B1F3A"/>'
    b += '<g fill="none" stroke="#1d3d66" stroke-width="3">' + "".join(f'<circle cx="900" cy="360" r="{r}"/>' for r in (120, 200, 280, 360)) + '</g>'
    for i in range(7):
        h = 90 + i * 55
        b += f'<rect x="{130 + i*70}" y="{600-h}" width="46" height="{h}" rx="6" fill="{"#00D68F" if i==6 else "#2f5b93"}"/>'
    b += '<circle cx="900" cy="360" r="110" fill="#F2B632"/><circle cx="900" cy="360" r="86" fill="none" stroke="#B8860B" stroke-width="8"/>'
    b += f'<text x="900" y="395" {F} font-size="110" font-weight="700" text-anchor="middle" fill="#8a5d00">₿</text>'
    b += '<g stroke="#00D68F" stroke-width="3" fill="none"><path d="M1010 360H1180V240H1240"/><path d="M790 360H700V500"/></g><g fill="#00D68F"><circle cx="1240" cy="240" r="8"/><circle cx="700" cy="500" r="8"/></g>'
    b += f'<text x="130" y="130" {F} font-size="48" font-weight="700" fill="#fff">Dòng tiền số</text><text x="130" y="176" {F} font-size="26" fill="#8fa6c4">Hình học trừu tượng</text>'
    return svg(b)

STYLES = [("1 · Motion graphics dữ liệu", s_data), ("2 · Isometric", s_iso), ("3 · Blueprint", s_blueprint),
          ("4 · Neon / cyber", s_neon), ("5 · Editorial tối giản", s_editorial), ("6 · Hình học trừu tượng", s_geo)]

if __name__ == "__main__":
    os.makedirs("styles", exist_ok=True)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24) if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf") else ImageFont.load_default()
    sheet = Image.new("RGB", (1920, 840), "white")
    for i, (name, fn) in enumerate(STYLES):
        k = f"styles/{i+1}"
        open(k + ".svg", "w").write(fn()); render(k + ".svg", k + ".png")
        im = Image.open(k + ".png").resize((640, 360))
        x, y = (i % 3) * 640, (i // 3) * 420
        sheet.paste(im, (x, y + 60))
        ImageDraw.Draw(sheet).text((x + 12, y + 16), name, fill="black", font=font)
    sheet.save("styles/tong-hop.png")
