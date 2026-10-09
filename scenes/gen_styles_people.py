"""6 phong cách minh họa + nhân vật người lớn không mặt (silhouette/editorial). Chạy: python3 gen_styles_people.py"""
import os
from PIL import Image, ImageDraw, ImageFont
from gen_scenes import render
import gen_styles as gs

SK = {"light": "#e3c9b1", "tan": "#cfa883", "deep": "#a97c5a"}

def figure(x, y, s=1.0, coat="#2c3b57", pants="#1b2740", shirt="#e8ecf2", hair="#14100e", skin="light",
           female=False, pose="pocket", flip=False, stroke="#0a0f1a", sw=3):
    sk = SK[skin]; f = -1 if flip else 1
    o = [f'<g transform="translate({x} {y}) scale({s*f} {s})" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">']
    if female:
        o.append(f'<path d="M-20 -312 Q-30 -270 -22 -236 L22 -236 Q30 -270 20 -312Z" fill="{hair}"/>')
        for lx in (-9, 9): o.append(f'<path d="M{lx-6} -112 L{lx-5} -10 L{lx+5} -10 L{lx+6} -112Z" fill="{sk}"/>')
        o.append(f'<path d="M-30 -165 L-38 -100 L38 -100 L30 -165Z" fill="{pants}"/>')
        for lx in (-9, 9): o.append(f'<ellipse cx="{lx}" cy="-6" rx="11" ry="5" fill="{INK_}"/>')
    else:
        o.append(f'<path d="M-24 -156 L-20 -8 L-3 -8 L0 -130 L3 -8 L20 -8 L24 -156Z" fill="{pants}"/>')
        for lx in (-12, 12): o.append(f'<ellipse cx="{lx}" cy="-6" rx="14" ry="6" fill="{INK_}"/>')
    o.append(f'<path d="M-34 -272 Q0 -288 34 -272 L31 {-150 if female else -138} L-31 {-150 if female else -138}Z" fill="{coat}"/>')
    o.append(f'<path d="M-9 -280 L0 -230 L9 -280Z" fill="{shirt}" stroke-width="2"/>')
    o.append(f'<rect x="-7" y="-292" width="14" height="16" fill="{sk}"/>')
    A = {"point": [[(-30,-266),(-38,-210),(-34,-165)], [(30,-266),(70,-258),(108,-268)]],
         "phone": [[(-30,-266),(-38,-210),(-34,-165)], [(30,-266),(46,-214),(22,-248)]],
         "pocket": [[(-30,-266),(-42,-212),(-24,-168)], [(30,-266),(42,-212),(24,-168)]],
         "crossed": [[(-30,-266),(-44,-216),(14,-212)], [(30,-266),(44,-216),(-14,-204)]]}[pose]
    for arm in A:
        p = " ".join(f"{a},{b}" for a, b in arm)
        o.append(f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{13+sw*2}"/><polyline points="{p}" fill="none" stroke="{coat}" stroke-width="13"/>')
        o.append(f'<circle cx="{arm[-1][0]}" cy="{arm[-1][1]}" r="6.5" fill="{sk}" stroke-width="2"/>')
    if pose == "phone":
        o.append('<rect x="14" y="-272" width="16" height="26" rx="3" fill="#111" stroke-width="2"/><rect x="16" y="-269" width="12" height="19" fill="#14304f" stroke="none"/><path d="M17 -255 L21 -260 L24 -257 L28 -266" fill="none" stroke="#00E08A" stroke-width="1.6"/>')
    o.append(f'<ellipse cx="0" cy="-310" rx="18" ry="22" fill="{sk}"/>')
    if female: o.append(f'<path d="M-19 -312 Q-22 -336 0 -334 Q22 -336 19 -312 Q10 -326 0 -326 Q-10 -326 -19 -312Z" fill="{hair}" stroke-width="2"/>')
    else: o.append(f'<path d="M-19 -314 Q-21 -336 0 -334 Q21 -336 19 -314 Q10 -326 0 -326 Q-10 -326 -19 -314Z" fill="{hair}" stroke-width="2"/>')
    o.append('</g>')
    return "".join(o)

INK_ = "#0a0f1a"

def add(svgtxt, figs): return svgtxt.replace("</svg>", "".join(figs) + "</svg>")

def s1():
    return add(gs.s_data(), [
        figure(1060, 650, 1.0, coat="#10294a", pants="#0a1830", shirt="#cfe0f5", stroke="#00D68F", sw=2.5, pose="point", flip=True),
        figure(1180, 650, 0.95, coat="#17365e", pants="#0a1830", shirt="#cfe0f5", female=True, hair="#050b16", stroke="#00D68F", sw=2.5, pose="pocket", skin="tan")])
def s2():
    return add(gs.s_iso(), [
        figure(160, 575, 0.5, coat="#2a4770", pants="#1b2a46", pose="point"),
        figure(235, 612, 0.5, coat="#e7a53c", pants="#2c3b57", female=True, hair="#3a2415", pose="pocket", skin="tan")])
def s3():
    return add(gs.s_blueprint(), [
        figure(1050, 650, 1.0, coat="#0d4b86", pants="#0b3f73", shirt="#0B3A6B", hair="#0B3A6B", stroke="#ffffff", sw=2.5, pose="point", flip=True)])
def s4():
    return add(gs.s_neon(), [
        figure(1120, 700, 1.0, coat="#0a0f1f", pants="#05070f", shirt="#0a0f1f", hair="#05070f", stroke="#00FFA3", sw=3, pose="crossed", skin="deep")])
def s5():
    return add(gs.s_editorial(), [
        figure(150, 650, 0.78, coat="#0B6E8E", pants="#222b36", shirt="#f5f0e6", pose="phone", skin="tan")])
def s6():
    return add(gs.s_geo(), [
        figure(1090, 650, 1.0, coat="#17365e", pants="#08142a", shirt="#cfe0f5", pose="point", flip=True, stroke="#00D68F", sw=2.5),
        figure(1190, 650, 0.95, coat="#1f4d84", pants="#08142a", shirt="#cfe0f5", female=True, hair="#050b16", pose="pocket", stroke="#00D68F", sw=2.5, skin="tan")])

STYLES = [("1 · Dữ liệu + người", s1), ("2 · Isometric + người", s2), ("3 · Blueprint + người", s3),
          ("4 · Neon + người", s4), ("5 · Editorial + người", s5), ("6 · Hình học + người", s6)]

if __name__ == "__main__":
    os.makedirs("styles-people", exist_ok=True)
    fp = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(fp, 24) if os.path.exists(fp) else ImageFont.load_default()
    sheet = Image.new("RGB", (1920, 840), "white")
    for i, (name, fn) in enumerate(STYLES):
        k = f"styles-people/{i+1}"
        open(k + ".svg", "w").write(fn()); render(k + ".svg", k + ".png")
        x, y = (i % 3) * 640, (i // 3) * 420
        sheet.paste(Image.open(k + ".png").resize((640, 360)), (x, y + 60))
        ImageDraw.Draw(sheet).text((x + 12, y + 16), name, fill="black", font=font)
    sheet.save("styles-people/tong-hop.png")
