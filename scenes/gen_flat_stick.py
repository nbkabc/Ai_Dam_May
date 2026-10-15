"""Người que đầu tròn trắng, nét mảnh, áo mảng phẳng, nền phẳng không viền. Chạy: python3 gen_flat_stick.py"""
import os
from gen_scenes import render, svg

INK = "#1a1a1a"
F = 'font-family="Arial,Helvetica,sans-serif"'

# khớp: (khuỷu, bàn tay) cho tay trái/phải, (đầu gối, bàn chân) cho chân trái/phải; vai (0,-108)
POSES = {
 "stand": [((-22,-84),(-24,-58)), ((22,-84),(24,-58)), ((-8,-32),(-14,0)), ((8,-32),(14,0))],
 "walk":  [((-24,-86),(-34,-62)), ((20,-90),(34,-72)), ((-18,-34),(-34,0)), ((14,-36),(32,-2))],
 "shock": [((-34,-122),(-44,-158)), ((34,-122),(44,-158)), ((-8,-32),(-14,0)), ((8,-32),(14,0))],
 "point": [((-22,-84),(-24,-58)), ((34,-112),(70,-124)), ((-8,-32),(-14,0)), ((8,-32),(14,0))],
 "phone": [((-22,-84),(-24,-58)), ((26,-92),(10,-112)), ((-8,-32),(-14,0)), ((8,-32),(14,0))],
 "cheer": [((-34,-122),(-48,-152)), ((34,-122),(48,-152)), ((-10,-32),(-18,0)), ((10,-32),(18,0))],
}

def L(*pts, w=4): return f'<polyline points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

def man(x, y, s=1.6, pose="stand", expr="neutral", shirt="#4f86c6", tie=None, skirt=False, tuft=False, flip=False, prop=""):
    j = POSES[pose]
    o = f'<g transform="translate({x} {y}) scale({s * (-1 if flip else 1)} {s})">'
    # chân và tay (nét mảnh)
    o += L((-6, -62), *j[2]) + L((6, -62), *j[3])
    o += L((0, -108), *j[0]) + L((0, -108), *j[1])
    o += L((0, -114), (0, -62))
    # áo: mảng phẳng
    if skirt: o += f'<polygon points="-16,-112 16,-112 12,-72 26,-46 -26,-46 -12,-72" fill="{shirt}"/>'
    else: o += f'<polygon points="-18,-112 18,-112 15,-58 -15,-58" fill="{shirt}"/>'
    if tie: o += f'<polygon points="-4,-112 4,-112 6,-78 0,-70 -6,-78" fill="{tie}"/>'
    # đầu: tròn trắng, mặt tối giản
    o += f'<circle cx="0" cy="-146" r="35" fill="#fff" stroke="{INK}" stroke-width="4"/>'
    if tuft: o += L((-2, -181), (-6, -196), (4, -190), w=4)
    o += f'<circle cx="-12" cy="-150" r="3.2" fill="{INK}"/><circle cx="12" cy="-150" r="3.2" fill="{INK}"/>'
    if expr == "smile": o += L((-9, -134), (0, -128), (9, -134), w=3.5)
    elif expr == "shock": o += f'<ellipse cx="0" cy="-131" rx="5" ry="7" fill="none" stroke="{INK}" stroke-width="3.5"/>'
    elif expr == "worry": o += L((-9, -130), (0, -135), (9, -130), w=3.5) + L((-19, -160), (-6, -164), w=3) + L((19, -160), (6, -164), w=3)
    else: o += L((-7, -132), (7, -132), w=3.5)
    return o + prop + '</g>'

def tree(x, y, s=1.0): return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 L-4 -90 Q-8 -110 -30 -118 M-4 -90 Q8 -110 26 -122" fill="none" stroke="#2a2a2a" stroke-width="7"/><ellipse cx="0" cy="-130" rx="110" ry="22" fill="#2f6b3a"/><ellipse cx="-50" cy="-118" rx="60" ry="14" fill="#2f6b3a"/></g>'
def coin(x, y, rx=40, ry=11, c="#f2c14e"): return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/><ellipse cx="{x}" cy="{y-5}" rx="{rx}" ry="{ry}" fill="#f7d774"/>'

def bank_street():
    b = '<rect width="1280" height="720" fill="#2f4d6b"/>'
    b += '<rect y="330" width="1280" height="130" fill="#243c55"/>'                       # dãy nhà xa
    for i, (x, w, h) in enumerate([(60, 90, 120), (170, 70, 170), (260, 100, 140), (900, 80, 150), (1000, 110, 190), (1130, 90, 130)]): b += f'<rect x="{x}" y="{460-h}" width="{w}" height="{h}" fill="#243c55"/>'
    b += '<rect y="460" width="1280" height="260" fill="#b98a4e"/><rect y="560" width="1280" height="160" fill="#a2773f"/>'
    # ngân hàng (nhà phẳng)
    b += '<polygon points="470,250 640,190 810,250" fill="#e8dcc0"/><rect x="480" y="250" width="320" height="26" fill="#cdbf9a"/>' + "".join(f'<rect x="{500+i*62}" y="276" width="34" height="150" fill="#e8dcc0"/>' for i in range(5)) + '<rect x="470" y="426" width="340" height="34" fill="#cdbf9a"/>'
    b += f'<text x="640" y="244" {F} font-size="30" font-weight="800" text-anchor="middle" fill="#2f4d6b">NGÂN HÀNG</text>'
    # ATM phẳng
    b += '<rect x="900" y="330" width="110" height="130" rx="8" fill="#5a6b7a"/><rect x="914" y="346" width="82" height="48" fill="#bfe3c8"/><rect x="922" y="410" width="66" height="14" fill="#2d3a45"/>'
    b += tree(180, 470, .9)
    b += man(330, 600, 1.7, "shock", "shock", "#e08a4a", tuft=True)
    b += man(560, 600, 1.7, "point", "smile", "#4f86c6", tie="#d9703a")
    b += man(1100, 600, 1.7, "phone", "worry", "#5aa36b", skirt=True, flip=True)
    b += f'<text x="640" y="680" {F} font-size="44" font-weight="800" text-anchor="middle" fill="#fff" stroke="{INK}" stroke-width="7" paint-order="stroke">Ví không thu phí, vậy ai trả tiền?</text>'
    return svg(b)

def coin_tower():
    b = '<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a5f86"/><stop offset="1" stop-color="#e6b87a"/></linearGradient></defs><rect width="1280" height="720" fill="url(#sk)"/>'
    b += '<polygon points="0,470 160,330 300,430 430,300 600,470" fill="#7a5a3a"/><polygon points="760,470 940,320 1100,440 1280,360 1280,470" fill="#8a6a44"/>'
    b += '<rect y="470" width="1280" height="250" fill="#b98a4e"/>'
    for k in range(9): b += coin(640, 560 - k * 22, 120 - k * 2, 28)
    b += f'<text x="640" y="{560-9*22+8}" {F} font-size="90" font-weight="800" text-anchor="middle" fill="#8a5d00">$</text>'
    b += man(340, 610, 1.3, "shock", "shock", "#e08a4a", tuft=True) + man(470, 610, 2.0, "cheer", "smile", "#4f86c6", tie="#d9703a")
    b += man(940, 610, 1.6, "walk", "worry", "#5aa36b", skirt=True, flip=True)
    b += tree(1150, 600, .8)
    b += f'<text x="640" y="684" {F} font-size="44" font-weight="800" text-anchor="middle" fill="#fff" stroke="{INK}" stroke-width="7" paint-order="stroke">Tiền ở đâu ra nhiều vậy?</text>'
    return svg(b)

if __name__ == "__main__":
    os.makedirs("flat-stick", exist_ok=True)
    for n, fn in (("01-ngan-hang", bank_street), ("02-thap-xu", coin_tower)):
        open(f"flat-stick/{n}.svg", "w").write(fn()); render(f"flat-stick/{n}.svg", f"flat-stick/{n}.png")
