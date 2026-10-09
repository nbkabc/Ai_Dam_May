"""Ảnh 2D bằng mã theo kiểu video tham chiếu: 1 nhân vật nhất quán, nền trắng, đạo cụ ẩn dụ, phụ đề.
Chạy: python3 gen_vid_style.py  (xuất vào vid-style/)"""
import os
from PIL import Image, ImageDraw, ImageFont
from gen_scenes import render, svg

INK = "#1b1b1f"
DEFS = '''<linearGradient id="blz" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2d4472"/><stop offset=".5" stop-color="#1f3158"/><stop offset="1" stop-color="#16233f"/></linearGradient>
<linearGradient id="pnt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a3350"/><stop offset="1" stop-color="#171d33"/></linearGradient>
<linearGradient id="skn" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6d3b0"/><stop offset="1" stop-color="#e2a97f"/></linearGradient>
<radialGradient id="glw" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffc760" stop-opacity=".9"/><stop offset="1" stop-color="#ffc760" stop-opacity="0"/></radialGradient>
<radialGradient id="glg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#4dffb0" stop-opacity=".6"/><stop offset="1" stop-color="#4dffb0" stop-opacity="0"/></radialGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9b6a3c"/><stop offset="1" stop-color="#5e3c1e"/></linearGradient>'''

POSES = {
 "present": [[(-58,-385),(-72,-320),(-66,-250)], [(58,-385),(112,-345),(170,-338)]],
 "forehead": [[(-58,-385),(-72,-320),(-66,-250)], [(58,-385),(100,-425),(30,-472)]],
 "phone": [[(-58,-385),(-72,-320),(-66,-250)], [(58,-385),(96,-330),(34,-392)]],
 "stop": [[(-58,-385),(-72,-320),(-66,-250)], [(58,-385),(104,-428),(112,-492)]],
}

def man(x, y, s=1.05, pose="present", expr="smile"):
    o = [f'<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round">']
    o.append('<ellipse cx="0" cy="2" rx="150" ry="16" fill="#000" opacity=".10" stroke="none"/>')
    # legs + shoes
    o.append('<path d="M-60 -232 L-52 -16 L-8 -16 L-4 -232Z" fill="url(#pnt)"/><path d="M60 -232 L52 -16 L8 -16 L4 -232Z" fill="url(#pnt)"/>')
    o.append('<path d="M-58 -16 Q-80 -14 -80 0 L-10 0 L-8 -16Z" fill="#6b3f1d"/><path d="M58 -16 Q80 -14 80 0 L10 0 L8 -16Z" fill="#6b3f1d"/>')
    # torso
    o.append('<path d="M-70 -388 Q0 -412 70 -388 L80 -224 L-80 -224Z" fill="url(#blz)"/>')
    o.append('<path d="M-22 -396 L0 -300 L22 -396Z" fill="#d7dbe3" stroke-width="3"/><path d="M-22 -396 L-8 -330 L-40 -300 L-34 -390Z M22 -396 L8 -330 L40 -300 L34 -390Z" fill="#1a2a4c" stroke-width="3"/>')
    o.append('<path d="M0 -300V-224" stroke-width="3"/><circle cx="0" cy="-262" r="5" fill="#0d1428" stroke-width="2"/>')
    o.append('<rect x="-13" y="-402" width="26" height="22" fill="#e2a97f" stroke-width="3"/>')
    # arms
    for arm in POSES[pose]:
        p = " ".join(f"{a},{b}" for a, b in arm)
        o.append(f'<polyline points="{p}" fill="none" stroke="{INK}" stroke-width="40"/><polyline points="{p}" fill="none" stroke="#243a66" stroke-width="32"/>')
        ex, ey = arm[-1]
        o.append(f'<circle cx="{ex}" cy="{ey}" r="15" fill="url(#skn)" stroke-width="3.5"/>')
    if pose == "phone":
        o.append('<g transform="rotate(-10 34 -400)"><rect x="18" y="-440" width="34" height="58" rx="6" fill="#15151a"/><rect x="22" y="-434" width="26" height="46" rx="3" fill="#143a66" stroke="none"/><path d="M26 -402 L33 -412 L39 -406 L46 -420" fill="none" stroke="#4dffb0" stroke-width="3"/></g>')
    # head
    o.append('<ellipse cx="-41" cy="-428" rx="8" ry="14" fill="#e8b48c" stroke-width="3"/><ellipse cx="41" cy="-428" rx="8" ry="14" fill="#e8b48c" stroke-width="3"/>')
    o.append('<ellipse cx="0" cy="-432" rx="41" ry="50" fill="url(#skn)"/>')
    o.append('<path d="M-44 -440 Q-46 -496 0 -496 Q46 -496 44 -440 Q38 -470 0 -472 Q-38 -470 -44 -440Z" fill="#17120f" stroke-width="3"/>')
    o.append('<g fill="none" stroke-width="3"><circle cx="-17" cy="-434" r="14"/><circle cx="17" cy="-434" r="14"/><path d="M-3 -436H3"/></g>')
    o.append('<ellipse cx="-17" cy="-433" rx="3.6" ry="5" fill="#111" stroke="none"/><ellipse cx="17" cy="-433" rx="3.6" ry="5" fill="#111" stroke="none"/>')
    o.append('<path d="M0 -430 Q-5 -414 3 -413" fill="none" stroke-width="2.5"/>')
    if expr == "smile":
        o.append('<path d="M-30 -454 Q-17 -460 -6 -454M6 -454 Q17 -460 30 -454" fill="none" stroke-width="3.5"/><path d="M-15 -400 Q0 -386 15 -400Z" fill="#fff" stroke-width="3"/>')
    elif expr == "worried":
        o.append('<path d="M-32 -448 L-6 -458M32 -448 L6 -458" fill="none" stroke-width="3.5"/><path d="M-13 -396 Q0 -406 13 -396" fill="none" stroke-width="3.5"/>')
    elif expr == "think":
        o.append('<path d="M-30 -452 L-6 -455M6 -462 Q17 -468 30 -458" fill="none" stroke-width="3.5"/><path d="M-12 -398 Q4 -394 14 -404" fill="none" stroke-width="3.5"/>')
    else:  # alert
        o.append('<path d="M-32 -458 Q-17 -466 -4 -458M4 -458 Q17 -466 32 -458" fill="none" stroke-width="3.5"/><path d="M-12 -400 L12 -400" fill="none" stroke-width="3.5"/>')
    o.append('</g>')
    return "".join(o)

def chart(x, y):
    pts = "30,190 80,160 120,170 170,110 220,125 270,60 310,30"
    return (f'<g transform="translate({x} {y})"><ellipse cx="170" cy="110" rx="230" ry="150" fill="url(#glg)"/>'
            f'<rect width="340" height="230" rx="16" fill="#0d2748" stroke="#00D68F" stroke-width="5"/>'
            f'<g stroke="#2d557f" stroke-width="2"><path d="M30 60H310M30 110H310M30 160H310"/></g>'
            f'<polyline points="{pts}" fill="none" stroke="#4dffb0" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<polygon points="324,14 286,22 312,52" fill="#4dffb0"/></g>')

def hourglass(x, y):
    return (f'<g transform="translate({x} {y})" stroke="{INK}" stroke-width="4" stroke-linejoin="round"><ellipse cx="90" cy="200" rx="190" ry="180" fill="url(#glw)" stroke="none"/>'
            '<rect x="10" y="0" width="160" height="26" rx="8" fill="url(#wood)"/><rect x="10" y="374" width="160" height="26" rx="8" fill="url(#wood)"/>'
            '<path d="M28 26 L152 26 Q152 150 100 200 Q152 250 152 374 L28 374 Q28 250 80 200 Q28 150 28 26Z" fill="#fff6e0" fill-opacity=".55" stroke="#c9822a" stroke-width="5"/>'
            '<path d="M48 40 L132 40 Q130 100 96 150 L84 150 Q50 100 48 40Z" fill="#f08a1c" stroke="none"/>'
            '<path d="M40 372 L140 372 Q136 320 98 290 L82 290 Q44 320 40 372Z" fill="#f08a1c" stroke="none"/><path d="M90 150V290" stroke="#f08a1c" stroke-width="4"/></g>')

def chest(x, y):
    return (f'<g transform="translate({x} {y})" stroke="{INK}" stroke-width="4" stroke-linejoin="round"><ellipse cx="100" cy="-30" rx="150" ry="120" fill="url(#glw)" stroke="none"/>'
            '<text x="100" y="-12" font-family="Arial" font-weight="800" font-size="130" text-anchor="middle" fill="#ffc23a" stroke="#c9822a" stroke-width="5">?</text>'
            '<path d="M0 80 Q0 20 100 20 Q200 20 200 80Z" fill="url(#wood)"/><rect x="0" y="80" width="200" height="110" rx="6" fill="url(#wood)"/>'
            '<path d="M60 22V190M140 22V190M0 80H200" stroke="#3a3a42" stroke-width="10" fill="none"/><rect x="82" y="66" width="36" height="42" rx="6" fill="#d9a53a"/><circle cx="100" cy="86" r="6" fill="#3a2a10"/></g>')

def stop(x, y):
    o = f'<g transform="translate({x} {y})" stroke="{INK}" stroke-width="4" stroke-linejoin="round">'
    for i in range(4): o += f'<ellipse cx="110" cy="{150-i*22}" rx="70" ry="18" fill="#f2b632"/>'
    o += '<rect x="10" y="160" width="76" height="76" rx="12" fill="#fff"/>' + "".join(f'<circle cx="{cx}" cy="{cy}" r="7" fill="#222" stroke="none"/>' for cx, cy in ((34,184),(62,184),(48,198),(34,212),(62,212)))
    o += '<g stroke="#E02626" stroke-width="26" stroke-linecap="round"><path d="M-30 -40L240 250M240 -40L-30 250"/></g></g>'
    return o

def cap(t):
    return f'<text x="640" y="690" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="34" text-anchor="middle" fill="#fff" stroke="#111" stroke-width="9" paint-order="stroke" stroke-linejoin="round">{t}</text>'

def scene(body, caption):
    return svg('<rect width="1280" height="720" fill="#fff"/>' + body + cap(caption), DEFS)

SCENES = [
 ("01", lambda: scene(man(470, 640, pose="present", expr="smile") + chart(790, 190), "VÍ ĐIỆN TỬ ĐANG TĂNG TRƯỞNG RẤT NHANH")),
 ("02", lambda: scene(man(470, 640, pose="forehead", expr="worried") + hourglass(860, 170), "THỜI GIAN TRÔI, TIỀN KHÔNG TỰ SINH RA")),
 ("03", lambda: scene(man(470, 640, pose="phone", expr="think") + chest(790, 400), "ỨNG DỤNG MIỄN PHÍ, VẬY TIỀN Ở ĐÂU RA?")),
 ("04", lambda: scene(man(470, 640, pose="stop", expr="alert") + stop(820, 330), "CẨN TRỌNG VỚI ƯU ĐÃI QUÁ HẤP DẪN")),
]

if __name__ == "__main__":
    os.makedirs("vid-style", exist_ok=True)
    sheet = Image.new("RGB", (1280, 720), "#ccc")
    for i, (k, fn) in enumerate(SCENES):
        p = f"vid-style/{k}"
        open(p + ".svg", "w").write(fn()); render(p + ".svg", p + ".png")
        sheet.paste(Image.open(p + ".png").resize((638, 358)), ((i % 2) * 642, (i // 2) * 362))
    sheet.save("vid-style/tong-hop.png")
