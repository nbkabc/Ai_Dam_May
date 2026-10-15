"""Cảnh phong cách 'nhân vật hình khối', nét đen dày, nền xanh dịu. Chạy: python3 gen_block_style.py"""
import os
from gen_scenes import render, svg

INK = "#2a1f16"
F = 'font-family="Arial,Helvetica,sans-serif"'
DEFS = '''<filter id="wob" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>'''

def heart(x, y, s=1):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 8 C-14 -4 -6 -16 0 -8 C6 -16 14 -4 0 8Z" fill="#f08aa6" stroke="{INK}" stroke-width="3"/>'

def box_char(x, y, w, h, color, arms="up", mouth="o", extra=""):
    o = f'<g transform="translate({x} {y})" stroke="{INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">'
    # legs
    for lx in (w*0.2, w*0.5, w*0.8):
        o += f'<rect x="{lx-7}" y="{h}" width="14" height="30" fill="{color}"/>'
    # arms
    if arms == "up":
        o += f'<path d="M0 {h*0.35} L-34 {h*0.1}" fill="none"/><path d="M{w} {h*0.35} L{w+34} {h*0.6}" fill="none"/>'
    elif arms == "both":
        o += f'<path d="M0 {h*0.35} L-34 {h*0.05}" fill="none"/><path d="M{w} {h*0.35} L{w+34} {h*0.05}" fill="none"/>'
    else:
        o += f'<path d="M0 {h*0.45} L-30 {h*0.7}" fill="none"/><path d="M{w} {h*0.45} L{w+30} {h*0.7}" fill="none"/>'
    o += f'<rect width="{w}" height="{h}" fill="{color}"/>'
    o += f'<rect x="{w*0.25}" y="{h*0.2}" width="11" height="11" fill="{INK}" stroke="none"/><rect x="{w*0.65}" y="{h*0.2}" width="11" height="11" fill="{INK}" stroke="none"/>'
    if mouth == "o":
        o += f'<ellipse cx="{w*0.5}" cy="{h*0.55}" rx="10" ry="15" fill="{INK}" stroke="none"/>'
    else:
        o += f'<path d="M{w*0.3} {h*0.5} Q{w*0.5} {h*0.68} {w*0.7} {h*0.5}" fill="none"/>'
    return o + extra + '</g>'

def scene():
    b = '<rect width="1280" height="720" fill="#a9c498"/>'
    b += f'<g filter="url(#wob)" stroke="{INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">'
    # cork board + sticky notes
    b += '<rect x="80" y="60" width="170" height="120" rx="8" fill="#d9a35c"/><rect x="100" y="80" width="46" height="42" fill="#f6e27a"/><rect x="156" y="76" width="40" height="40" fill="#f2a9be"/><rect x="108" y="128" width="42" height="38" fill="#fff"/><rect x="164" y="126" width="64" height="40" fill="#f6e27a"/>'
    # lamp
    b += '<path d="M330 0V40"/><path d="M296 70 L330 36 L364 70Z" fill="#f6e27a"/>'
    # hanging sign
    b += '<path d="M500 0V70M780 0V70" fill="none"/><rect x="470" y="60" width="340" height="140" rx="10" fill="#fbf6ea"/>'
    b += f'<text x="640" y="125" {F} font-size="52" font-weight="800" text-anchor="middle" fill="{INK}" stroke="none">Ví điện tử</text><text x="640" y="178" {F} font-size="46" font-style="italic" font-weight="700" text-anchor="middle" fill="#9a5a2c" stroke="none">miễn phí?</text>'
    b += heart(478, 66, 1.3) + heart(804, 66, 1.3) + heart(478, 196, 1.3) + heart(804, 196, 1.3)
    # clock
    b += '<circle cx="1130" cy="110" r="56" fill="#fff"/><path d="M1130 110V70M1130 110L1158 126" fill="none"/>'
    # window
    b += '<rect x="290" y="240" width="350" height="190" fill="#fbf6ea"/><rect x="304" y="254" width="322" height="162" fill="#86bfea"/><ellipse cx="380" cy="290" rx="42" ry="14" fill="#fff" stroke-width="3"/>'
    for i, (bx, bw, bh, c) in enumerate([(314, 54, 80, "#d6a07c"), (376, 62, 60, "#f0dca8"), (446, 56, 96, "#c9a07a"), (510, 60, 70, "#e9d29a"), (576, 44, 84, "#d6a07c")]):
        b += f'<rect x="{bx}" y="{416-bh}" width="{bw}" height="{bh}" fill="{c}" stroke-width="3"/>'
        for wy in range(416-bh+10, 410, 22): b += f'<rect x="{bx+10}" y="{wy}" width="9" height="9" fill="#86bfea" stroke="none"/>'
    b += '<path d="M465 254V416M304 335H626" fill="none"/>'
    # chart poster
    b += '<rect x="700" y="230" width="200" height="140" fill="#fff"/><path d="M718 340 L770 300 L810 320 L880 258" fill="none" stroke="#2f9e63" stroke-width="7"/><polygon points="890,250 862,254 884,278" fill="#2f9e63" stroke-width="3"/>'
    # shelf + books + plant
    b += '<path d="M950 340H1230" fill="none" stroke-width="7"/>'
    for i, (c, h) in enumerate([("#d9703a", 70), ("#4f86c6", 56), ("#fbf6ea", 78), ("#f2c14e", 50), ("#8a6bbf", 64), ("#5aa36b", 44)]):
        b += f'<rect x="{960+i*22}" y="{340-h}" width="20" height="{h}" fill="{c}" stroke-width="3"/>'
    b += '<path d="M1170 340 L1180 300 L1216 300 L1226 340Z" fill="#d9703a"/><path d="M1198 300 Q1180 262 1196 244 Q1204 276 1198 300 M1198 300 Q1218 262 1204 244" fill="#5aa36b"/>'
    # counter / cabinets
    b += '<rect x="0" y="500" width="1280" height="220" fill="#efe0b8"/><path d="M0 500H1280M0 570H1280M0 640H1280" fill="none"/>'
    for i in range(5):
        b += f'<path d="M{20+i*256} 530H{70+i*256}" fill="none"/>'
    for i in range(1, 5): b += f'<path d="M{i*256} 500V640" fill="none"/>'
    b += '<rect x="0" y="640" width="1280" height="80" fill="#b9803f"/>'
    for i in range(5): b += f'<rect x="{20+i*256}" y="656" width="216" height="48" rx="4" fill="#c88f4a" stroke-width="4"/>'
    # calculator + coins on counter
    b += '<rect x="880" y="440" width="110" height="62" fill="#c9ccd0"/><rect x="892" y="450" width="86" height="16" fill="#e7f1e0" stroke-width="3"/>' + "".join(f'<rect x="{894+c*27}" y="{474+r*13}" width="18" height="9" fill="#eee" stroke-width="2"/>' for r in range(2) for c in range(3))
    for i in range(4): b += f'<ellipse cx="1090" cy="{494-i*14}" rx="40" ry="11" fill="#f2c14e" stroke-width="4"/>'
    b += '</g>'
    # characters (outline wobble too)
    b += '<g filter="url(#wob)">'
    b += box_char(120, 360, 130, 110, "#c8683a", "up", "o")
    b += box_char(420, 330, 120, 140, "#b9d3e8", "both", "o")
    b += box_char(700, 380, 110, 90, "#f2c14e", "down", "s")
    b += '</g>'
    # caption bar
    b += f'<rect x="270" y="600" width="740" height="84" rx="42" fill="#fbf6ea" stroke="{INK}" stroke-width="5"/><text x="640" y="655" {F} font-size="46" font-weight="800" text-anchor="middle" fill="{INK}">Ví không thu phí, vậy ai trả tiền?</text>'
    return svg(b, DEFS)

if __name__ == "__main__":
    os.makedirs("block-style", exist_ok=True)
    open("block-style/01.svg", "w").write(scene()); render("block-style/01.svg", "block-style/01.png")
