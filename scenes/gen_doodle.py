"""Người que kiểu vẽ tay thô (đầu trứng méo, nét bút dày). Chạy: python3 gen_doodle.py"""
import os, random
from gen_scenes import render, svg
import gen_block_style as gb

INK = "#222"
F = 'font-family="Arial,Helvetica,sans-serif"'

def P(d, w=9, fill="none"): return f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

ARMS = {  # từ điểm vai (-2,-170): đường cong tay trái, tay phải
 "down":  ("M-2 -170 Q-30 -120 -48 -86", "M2 -170 Q34 -120 52 -86"),
 "droop": ("M-4 -170 Q-60 -140 -96 -96", "M2 -170 Q50 -166 96 -150 Q104 -146 108 -136"),
 "shock": ("M-2 -170 Q-50 -190 -64 -250", "M2 -170 Q50 -190 66 -250"),
 "point": ("M-2 -170 Q-30 -120 -46 -86", "M2 -170 Q60 -178 120 -204"),
 "think": ("M-2 -170 Q-30 -120 -46 -86", "M2 -170 Q34 -140 6 -222"),
 "cheer": ("M-2 -170 Q-56 -200 -78 -262", "M2 -170 Q56 -200 78 -262"),
}
LEGS = {
 "stand": ("M4 -90 Q-14 -50 -34 0", "M4 -90 Q24 -50 40 0"),
 "walk":  ("M4 -90 Q-26 -60 -62 -8", "M4 -90 Q40 -56 78 -14"),
}

def face(kind):
    L = []
    if kind == "angry":   # như hình mẫu: mắt giọt nước + mắt nhỏ + mũi chữ b
        L += [P("M-36 -322 Q-34 -296 -20 -298 Q-8 -300 -10 -318 Q-24 -326 -36 -322Z", 7), P("M18 -318 Q30 -314 30 -302 Q22 -298 16 -306Z", 7), P("M12 -330 L30 -334", 6)]
        L += [P("M-2 -280 Q-10 -262 6 -262 Q16 -270 2 -280", 6), P("M-14 -250 L10 -252", 6)]
    elif kind == "shock":
        L += [f'<circle cx="-22" cy="-310" r="13" fill="#fff" stroke="{INK}" stroke-width="7"/><circle cx="22" cy="-310" r="13" fill="#fff" stroke="{INK}" stroke-width="7"/><circle cx="-22" cy="-310" r="3.5" fill="{INK}"/><circle cx="22" cy="-310" r="3.5" fill="{INK}"/>']
        L += [P("M-40 -336 Q-24 -346 -10 -336", 6), P("M10 -336 Q24 -346 40 -336", 6), f'<ellipse cx="0" cy="-262" rx="11" ry="16" fill="{INK}"/>']
    elif kind == "smile":
        L += [f'<circle cx="-22" cy="-312" r="5" fill="{INK}"/><circle cx="22" cy="-312" r="5" fill="{INK}"/>']
        L += [P("M-4 -296 Q-10 -278 4 -278", 6), P("M-28 -262 Q0 -238 28 -262", 7)]
    else:  # worry
        L += [f'<circle cx="-22" cy="-312" r="5" fill="{INK}"/><circle cx="22" cy="-312" r="5" fill="{INK}"/>', P("M-38 -326 L-12 -338", 6), P("M38 -326 L12 -338", 6)]
        L += [P("M-4 -296 Q-10 -278 4 -278", 6), P("M-24 -254 Q-12 -266 0 -254 Q12 -242 24 -254", 6)]
    return "".join(L)

def doodle(x, y, s, pose="down", leg="stand", expr="angry", flip=False, hair=True, prop=""):
    o = f'<g transform="translate({x} {y}) scale({s * (-1 if flip else 1)} {s})">'
    o += P("M-60 -300 C-66 -372 -22 -386 22 -380 C64 -376 72 -332 66 -298 C62 -250 22 -224 -10 -228 C-48 -232 -58 -262 -60 -300Z", 10, "#fbfbf6")
    if hair: o += P("M-24 -366 Q-4 -382 10 -376", 8)
    o += P("M-4 -228 Q-8 -160 4 -90", 10)               # thân
    a = ARMS[pose]; o += P(a[0], 10) + P(a[1], 10)
    l = LEGS[leg]; o += P(l[0], 10) + P(l[1], 10)
    o += face(expr) + prop + '</g>'
    return o

def coin(x, y, r=26): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="7"/><text x="{x}" y="{y+r*.38}" {F} font-size="{r*1.1}" font-weight="800" text-anchor="middle" fill="{INK}">$</text>'

def white_scene():
    b = '<rect width="1280" height="720" fill="#fbfbf6"/>'
    b += '<g filter="url(#wob)">'
    b += P("M40 560 Q400 552 760 560 T1240 556", 8)           # đường nền
    # biểu đồ vẽ tay
    b += P("M760 250 L760 430 L1020 430", 8) + P("M780 400 L850 340 L900 372 L990 270", 9) + P("M990 270 L964 274 M990 270 L986 296", 9)
    b += coin(1130, 380, 34) + coin(1130, 458, 34) + coin(1130, 536, 34)
    b += doodle(200, 556, 1.0, "shock", "stand", "shock", hair=True)
    b += doodle(470, 556, 1.0, "point", "stand", "smile")
    b += doodle(690, 556, .95, "droop", "walk", "angry", flip=True)
    b += '</g>'
    b += f'<text x="640" y="650" {F} font-size="48" font-weight="800" text-anchor="middle" fill="{INK}">Ví không thu phí, vậy ai trả tiền?</text>'
    return svg(b, gb.DEFS)

def room_scene():
    base = gb.scene("none")
    ch = '<g filter="url(#wob)">' + doodle(190, 500, .72, "shock", "stand", "shock") + doodle(470, 500, .72, "point", "stand", "smile") + doodle(760, 500, .72, "think", "stand", "worry", flip=True) + '</g>'
    return base.replace('</svg>', ch + '</svg>')

if __name__ == "__main__":
    os.makedirs("doodle", exist_ok=True)
    for name, fn in (("01-giay-trang", white_scene), ("02-phong-xanh", room_scene)):
        open(f"doodle/{name}.svg", "w").write(fn()); render(f"doodle/{name}.svg", f"doodle/{name}.png")
