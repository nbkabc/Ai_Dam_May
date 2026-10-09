"""Sinh nhiều cảnh 2D phong cách doodle người lớn (SVG -> PNG). Chạy: python3 gen_scenes.py"""
import subprocess, os
from PIL import Image

INK = "#0a0f1a"
SKINS = {"light": "#e6d3be", "tan": "#d7b997", "deep": "#b98d6a"}

def person(x, y, s=1.1, shirt="#4f6d8f", pants="#2f3b4f", hair="#14100e", skin="light",
           female=False, hairstyle="short", glasses=False, expr="tired", pose="down", tie=None, flip=False):
    sk = SKINS[skin]
    f = -1 if flip else 1
    o = []
    o.append(f'<g transform="translate({x} {y}) scale({s*f} {s})" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">')
    if hairstyle == "long":
        o.append(f'<path d="M-30 -305 Q-34 -250 -26 -228 L26 -228 Q34 -250 30 -305Z" fill="{hair}"/>')
    # legs
    if female:
        o.append(f'<path d="M-40 -150 L-48 -100 L48 -100 L40 -150Z" fill="{pants}"/>')
        for lx in (-14, 14):
            o.append(f'<rect x="{lx-9}" y="-100" width="18" height="92" fill="{sk}"/>')
    else:
        for lx in (-14, 14):
            o.append(f'<rect x="{lx-12}" y="-150" width="24" height="142" fill="{pants}"/>')
    for lx in (-15, 15):
        o.append(f'<ellipse cx="{lx}" cy="-5" rx="17" ry="7" fill="#e9e9e6"/>')
    # torso
    o.append(f'<path d="M-44 -262 Q0 -280 44 -262 L40 -146 L-40 -146Z" fill="{shirt}"/>')
    if tie:
        o.append(f'<path d="M-9 -268 L9 -268 L12 -170 L0 -158 L-12 -170Z" fill="{tie}"/>')
    # neck
    o.append(f'<rect x="-9" y="-276" width="18" height="18" fill="{sk}"/>')
    # arms
    P = {
     "down":   [[(-40,-256),(-54,-206),(-52,-160)], [(40,-256),(54,-206),(52,-160)]],
     "phone":  [[(-40,-256),(-54,-206),(-52,-160)], [(40,-256),(62,-200),(30,-232)]],
     "crossed":[[(-40,-256),(-56,-208),(16,-204)], [(40,-256),(56,-208),(-16,-196)]],
     "shock":  [[(-40,-256),(-74,-236),(-60,-296)], [(40,-256),(74,-236),(60,-296)]],
     "point":  [[(-40,-256),(-54,-206),(-52,-160)], [(40,-256),(84,-250),(130,-262)]],
     "head":   [[(-40,-256),(-54,-206),(-52,-160)], [(40,-256),(68,-282),(22,-314)]],
    }[pose]
    for arm in P:
        pts = " ".join(f"{a},{b}" for a, b in arm)
        o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="21"/>')
        o.append(f'<polyline points="{pts}" fill="none" stroke="{shirt}" stroke-width="14"/>')
        ex, ey = arm[-1]
        o.append(f'<circle cx="{ex}" cy="{ey}" r="9" fill="{sk}"/>')
    if pose == "phone":
        o.append('<g transform="rotate(-8 30 -236)"><rect x="18" y="-264" width="26" height="44" rx="5" fill="#222"/><rect x="21" y="-259" width="20" height="34" rx="2" fill="#14304f" stroke="none"/><path d="M23 -232 L29 -240 L34 -236 L40 -250" fill="none" stroke="#00E08A" stroke-width="2.5"/></g>')
    # head
    o.append(f'<ellipse cx="0" cy="-302" rx="28" ry="33" fill="{sk}"/>')
    o.append(f'<ellipse cx="-28" cy="-300" rx="5" ry="9" fill="{sk}"/><ellipse cx="28" cy="-300" rx="5" ry="9" fill="{sk}"/>')
    if hairstyle == "long":
        o.append(f'<path d="M-30 -302 Q-32 -340 0 -338 Q32 -340 30 -302 Q22 -322 0 -322 Q-20 -322 -30 -302Z" fill="{hair}"/>')
    else:
        o.append(f'<path d="M-29 -306 Q-32 -342 0 -338 Q32 -342 29 -306 Q18 -324 0 -322 Q-18 -324 -29 -306Z" fill="{hair}"/>')
    ey_ = -304
    if glasses:
        o.append(f'<g fill="none" stroke-width="2.5"><rect x="-23" y="{ey_-9}" width="19" height="15" rx="5"/><rect x="4" y="{ey_-9}" width="19" height="15" rx="5"/><path d="M-4 {ey_-2}H4"/></g>')
    if expr == "tired":
        o.append(f'<path d="M-20 {ey_} Q-13 {ey_+5} -6 {ey_}M6 {ey_} Q13 {ey_+5} 20 {ey_}" fill="none" stroke-width="2.6"/><path d="M-22 {ey_-12} L-5 {ey_-9}M22 {ey_-12} L5 {ey_-9}" stroke-width="3"/><path d="M-9 -284 L9 -284" fill="none" stroke-width="2.8"/>')
    elif expr == "shock":
        o.append(f'<circle cx="-12" cy="{ey_}" r="6" fill="#fff" stroke-width="2"/><circle cx="12" cy="{ey_}" r="6" fill="#fff" stroke-width="2"/><circle cx="-12" cy="{ey_}" r="2" fill="{INK}"/><circle cx="12" cy="{ey_}" r="2" fill="{INK}"/><path d="M-20 {ey_-14} Q-12 {ey_-20} -4 {ey_-14}M4 {ey_-14} Q12 {ey_-20} 20 {ey_-14}" fill="none" stroke-width="2.6"/><ellipse cx="0" cy="-285" rx="5" ry="7" fill="#2a2a2a"/>')
    elif expr == "smirk":
        o.append(f'<circle cx="-12" cy="{ey_}" r="2.4" fill="{INK}"/><circle cx="12" cy="{ey_}" r="2.4" fill="{INK}"/><path d="M-20 {ey_-9} L-5 {ey_-8}M5 {ey_-12} Q13 {ey_-17} 20 {ey_-11}" fill="none" stroke-width="2.8"/><path d="M-7 -285 Q4 -282 11 -290" fill="none" stroke-width="2.8"/>')
    elif expr == "worried":
        o.append(f'<circle cx="-12" cy="{ey_}" r="2.4" fill="{INK}"/><circle cx="12" cy="{ey_}" r="2.4" fill="{INK}"/><path d="M-21 {ey_-6} L-5 {ey_-13}M21 {ey_-6} L5 {ey_-13}" fill="none" stroke-width="2.8"/><path d="M-8 -283 Q-3 -288 0 -283 Q3 -278 8 -284" fill="none" stroke-width="2.6"/>')
    else:  # happy
        o.append(f'<path d="M-19 {ey_+1} Q-12 {ey_-7} -5 {ey_+1}M5 {ey_+1} Q12 {ey_-7} 19 {ey_+1}" fill="none" stroke-width="2.8"/><path d="M-10 -288 Q0 -276 10 -288Z" fill="#fff" stroke-width="2.5"/>')
    o.append('</g>')
    return "".join(o)

def svg(body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs>{defs}</defs>{body}</svg>'

def grad(id_, c1, c2, vertical=True):
    d = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    return f'<linearGradient id="{id_}" {d}><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'

L = f'stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"'

def street():
    b = f'<rect width="1280" height="720" fill="url(#g)"/><g {L}>'
    b += '<rect x="880" y="140" width="420" height="110" fill="#e4d9b5"/><text x="1090" y="212" font-family="Arial" font-weight="700" font-size="44" text-anchor="middle" fill="#161616" stroke="none">TIỀN SỐ</text>'
    b += '<rect x="880" y="250" width="420" height="50" fill="#cfc4a0"/><path d="M920 300V520M960 300V520M1000 300V520"/><rect x="1060" y="330" width="100" height="190" fill="#dfd4b0"/>'
    b += '<path d="M770 520V380" stroke-width="22"/><path d="M770 520V380" stroke="#e6dcc0" stroke-width="14"/><path d="M730 360Q690 340 705 300Q695 255 745 262Q770 225 805 255Q850 245 850 300Q870 340 830 365Q800 392 770 380Q745 392 730 360Z" fill="#9da58a"/>'
    b += '<rect y="520" width="1280" height="80" fill="#bfc4a0" stroke="none"/><path d="M0 520H1280M0 600H1280"/><rect y="602" width="1280" height="118" fill="#9b9b9a" stroke="none"/><path d="M300 668H430M850 668H980" stroke="#fff" stroke-width="14"/></g>'
    b += person(470, 565, shirt="#b97a56", pants="#6b8f71", female=True, hairstyle="long", expr="smirk", pose="phone", skin="tan")
    b += person(640, 565, shirt="#8aa0b8", pants="#5f7189", expr="shock", pose="shock")
    return svg(b, grad("g", "#7d776a", "#ece0bd"))

def cafe():
    b = f'<rect width="1280" height="720" fill="#5b4636"/><rect y="400" width="1280" height="320" fill="#3b2c20"/><g {L}>'
    b += '<rect x="90" y="110" width="340" height="250" fill="#a8c7d6"/><path d="M260 110V360M90 235H430"/><text x="260" y="95" font-family="Arial" font-weight="800" font-size="40" text-anchor="middle" fill="#f2c94c" stroke="none">CAFÉ</text>'
    b += '<rect x="820" y="130" width="360" height="230" fill="#2a1d14"/><path d="M850 330H1150" /><text x="1000" y="260" font-family="Arial" font-weight="700" font-size="30" text-anchor="middle" fill="#e8d6b4" stroke="none">COFFEE &amp; CODE</text>'
    b += '<rect x="0" y="560" width="1280" height="160" fill="#2a1d14" stroke="none"/></g>'
    b += person(520, 600, shirt="#d9dde3", pants="#2f3b4f", glasses=True, expr="tired", pose="down", tie="#00a86b")
    b += person(760, 600, shirt="#6b8f71", pants="#2c3b57", female=True, hairstyle="long", expr="happy", pose="point", skin="light", hair="#3a2415")
    b += f'<g {L}><ellipse cx="640" cy="560" rx="260" ry="26" fill="#8a6a45"/><rect x="615" y="580" width="50" height="110" fill="#5a4430"/><path d="M570 540H700L690 520H580Z" fill="#9aa3b2"/><path d="M820 536H860L856 566H824Z" fill="#e8e8e6"/><path d="M450 540H490L486 566H454Z" fill="#e8e8e6"/></g>'
    return svg(b)

def bank():
    b = f'<rect width="1280" height="720" fill="#c9d2dc"/><rect y="560" width="1280" height="160" fill="#8e99a8"/><g {L}>'
    b += '<path d="M0 560H1280" />'
    for i in range(0, 1280, 160): b += f'<path d="M{i} 560L{i-60} 720"/>'
    b += '<rect x="800" y="180" width="220" height="400" rx="12" fill="#3a4a63"/><rect x="822" y="206" width="176" height="130" rx="6" fill="#0b1424"/>'
    b += '<text x="910" y="262" font-family="Arial" font-weight="700" font-size="28" text-anchor="middle" fill="#ff6b6b" stroke="none">SỐ DƯ</text><text x="910" y="308" font-family="Arial" font-weight="700" font-size="40" text-anchor="middle" fill="#ff6b6b" stroke="none">0 đ</text>'
    b += '<rect x="830" y="360" width="160" height="90" rx="6" fill="#5f7189"/><rect x="850" y="470" width="120" height="14" fill="#0b1424"/><text x="910" y="168" font-family="Arial" font-weight="800" font-size="38" text-anchor="middle" fill="#0b1424" stroke="none">ATM</text></g>'
    b += person(560, 600, shirt="#4f6d8f", pants="#5f7189", expr="shock", pose="head", glasses=False, skin="tan")
    b += person(330, 600, shirt="#b97a56", pants="#2c3b57", female=True, hairstyle="long", expr="worried", pose="crossed", hair="#14100e")
    return svg(b)

def meeting():
    b = f'<rect width="1280" height="720" fill="#dfe6ee"/><rect y="580" width="1280" height="140" fill="#9aa7b8"/><g {L}>'
    b += '<rect x="400" y="90" width="520" height="320" fill="#f7f8fa"/><path d="M450 350L540 300L610 330L720 220L830 150" fill="none" stroke="#00a86b" stroke-width="10"/><polygon points="850,135 812,142 838,172" fill="#00a86b"/><path d="M450 360H880M450 360V130" stroke-width="3"/><text x="660" y="130" font-family="Arial" font-weight="700" font-size="32" text-anchor="middle" fill="#0b1f3a" stroke="none">LỢI NHUẬN QUÝ</text>'
    b += '<rect x="60" y="120" width="260" height="260" fill="#a8c7d6"/><path d="M190 120V380M60 250H320"/>'
    b += '<path d="M1100 580V470" stroke-width="10"/><path d="M1060 470Q1100 380 1140 470Z" fill="#6b8f71"/><path d="M0 580H1280"/></g>'
    b += person(360, 600, shirt="#2c3b57", pants="#2c3b57", glasses=True, expr="smirk", pose="crossed", tie="#ff6b6b", skin="tan")
    b += person(720, 600, shirt="#d9dde3", pants="#2f3b4f", female=True, hairstyle="long", expr="happy", pose="point", hair="#14100e", flip=False)
    return svg(b)

def home():
    b = f'<rect width="1280" height="720" fill="url(#g)"/><g {L}>'
    b += '<rect x="80" y="140" width="220" height="440" fill="#2a1f3d"/>'
    for y in (240, 340, 440): b += f'<path d="M80 {y}H300"/>'
    b += '<rect x="100" y="180" width="26" height="60" fill="#6b8f71"/><rect x="132" y="190" width="22" height="50" fill="#b97a56"/><rect x="170" y="280" width="30" height="60" fill="#4f6d8f"/><rect x="110" y="380" width="26" height="60" fill="#d9dde3"/>'
    b += '<rect x="850" y="150" width="300" height="200" fill="#0b1a35"/><path d="M1000 150V350M850 250H1150"/><circle cx="1090" cy="200" r="22" fill="#f4e9b8" stroke="none"/>'
    b += '<rect x="780" y="440" width="440" height="140" rx="26" fill="#4a3a66"/><rect x="760" y="500" width="480" height="90" rx="20" fill="#5a4a7a"/>'
    b += '<rect y="580" width="1280" height="140" fill="#161024" stroke="none"/><path d="M0 580H1280"/></g>'
    b += person(560, 620, shirt="#8aa0b8", pants="#6b5a4a", expr="worried", pose="phone", skin="light")
    b += f'<circle cx="580" cy="400" r="190" fill="#ff5a5a" opacity=".10"/>'
    return svg(b, grad("g", "#1a1330", "#2d2150"))

def rooftop():
    b = f'<rect width="1280" height="720" fill="url(#g)"/><circle cx="1010" cy="150" r="58" fill="#f4e9b8"/><g {L}>'
    for i, (x, w, h) in enumerate([(0,110,260),(120,90,360),(220,130,300),(370,100,420),(480,120,280),(870,110,340),(990,90,430),(1090,130,300),(1230,60,380)]):
        b += f'<rect x="{x}" y="{600-h}" width="{w}" height="{h}" fill="#142645"/>'
    b += '<rect y="600" width="1280" height="120" fill="#0b1527"/><path d="M0 600H1280"/><path d="M0 560H1280" stroke-width="8"/>'
    for x in range(40, 1280, 120): b += f'<path d="M{x} 560V600"/>'
    b += '</g><g fill="#ffd27a">'
    import random; random.seed(3)
    for _ in range(70): b += f'<rect x="{random.randint(10,1260)}" y="{random.randint(230,560)}" width="5" height="6" opacity=".6"/>'
    b += '</g>'
    b += person(520, 640, shirt="#2c3b57", pants="#14100e", expr="smirk", pose="crossed", tie="#00a86b", glasses=True, skin="deep")
    b += person(760, 640, shirt="#b97a56", pants="#2f3b4f", female=True, hairstyle="long", expr="happy", pose="head", hair="#3a2415", skin="tan")
    return svg(b, grad("g", "#070f22", "#1c3560"))

SCENES = {"01-pho": street, "02-cafe": cafe, "03-atm": bank, "04-hop": meeting, "05-nha": home, "06-san-thuong": rooftop}

def render(svg_path, png_path, w=1280, h=720):
    html = svg_path + ".html"
    open(html, "w").write(f"<body style='margin:0'><img src='{os.path.basename(svg_path)}' width={w} height={h} style='display:block'>")
    subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--hide-scrollbars",
                    f"--screenshot={png_path}", f"--window-size={w},{h+90}", "file://" + os.path.abspath(html)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(html)
    Image.open(png_path).crop((0, 0, w, h)).save(png_path)

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    pngs = []
    for name, fn in SCENES.items():
        p = f"out/{name}.svg"; open(p, "w").write(fn()); render(p, f"out/{name}.png"); pngs.append(f"out/{name}.png")
    sheet = Image.new("RGB", (1920, 720), "white")
    for i, p in enumerate(pngs):
        sheet.paste(Image.open(p).resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
    sheet.save("out/tong-hop.png")
