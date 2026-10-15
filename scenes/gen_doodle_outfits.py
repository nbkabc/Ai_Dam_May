"""Bảng nhân vật người que nét bút lông (đầu trứng méo) có trang phục. Chạy: python3 gen_doodle_outfits.py"""
import os
from gen_scenes import render, svg
from gen_doodle import P, face, INK, F, LEGS

PAPER = "#fbfbf6"
MONO = True
ARMS = {  # (tay trái, tay phải) + toạ độ bàn tay
 "down":   ("M-2 -170 Q-30 -120 -48 -86", "M2 -170 Q34 -120 52 -86", (-48, -86), (52, -86)),
 "holdR":  ("M-2 -170 Q-30 -120 -48 -86", "M2 -170 Q40 -142 68 -124", (-48, -86), (68, -124)),
 "upR":    ("M-2 -170 Q-30 -120 -48 -86", "M2 -170 Q46 -176 72 -152", (-48, -86), (72, -152)),
 "shield": ("M-2 -170 Q-46 -150 -64 -118", "M2 -170 Q46 -176 72 -152", (-64, -118), (72, -152)),
 "both":   ("M-2 -170 Q-30 -140 -4 -112", "M2 -170 Q30 -140 8 -112", (-4, -112), (8, -112)),
}

def cp(d, col, w=15, frac=1.0, ow=25):
    da = f' stroke-dasharray="{frac * 100:.0f} 100"' if frac < 1 else ''
    return (f'<path d="{d}" pathLength="100"{da} fill="none" stroke="{INK}" stroke-width="{ow}" stroke-linecap="round"/>'
            f'<path d="{d}" pathLength="100"{da} fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')

def torso(col, bot=-78, wt=42, wb=36, extra=""):
    return f'<path d="M{-wt} -196 Q-4 -210 {wt} -196 L{wb} {bot} Q0 {bot + 10} {-wb} {bot}Z" fill="{col}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>' + extra

def hand(p): return f'<circle cx="{p[0]}" cy="{p[1]}" r="8" fill="#fff" stroke="{INK}" stroke-width="6"/>'

HEAD = "M-60 -300 C-66 -372 -22 -386 22 -380 C64 -376 72 -332 66 -298 C62 -250 22 -224 -10 -228 C-48 -232 -58 -262 -60 -300Z"

def char(x, y, s, arm="down", legs=("#fff", 0), sleeves=None, shoes="#222", garment="", pre="", post="", expr="smile", hair=None, hat="", flip=False, bare_legs=True, pants=None, front=""):
    """garment: svg thân áo; pre: vẽ trước thân (balo...), post: vẽ sau đầu (mũ...); front: sau cùng."""
    a = ARMS[arm]; lg = LEGS["stand"]
    o = f'<g transform="translate({x} {y}) scale({s * (-1 if flip else 1)} {s})">'
    o += pre
    # chân
    if pants: o += cp(lg[0], pants, 15) + cp(lg[1], pants, 15)
    else: o += P(lg[0], 10) + P(lg[1], 10)
    o += f'<ellipse cx="-36" cy="0" rx="22" ry="9" fill="{shoes}" stroke="{INK}" stroke-width="6"/><ellipse cx="42" cy="0" rx="22" ry="9" fill="{shoes}" stroke="{INK}" stroke-width="6"/>'
    o += P("M-4 -228 Q-8 -160 4 -90", 10)
    # tay
    if sleeves: o += cp(a[0], sleeves[0], 13, sleeves[1]) + cp(a[1], sleeves[0], 13, sleeves[1])
    else: o += P(a[0], 10) + P(a[1], 10)
    o += hand(a[2]) + hand(a[3])
    o += garment
    # đầu
    o += P(HEAD, 10, "#fff")
    if hair: o += hair
    o += face(expr) + hat + front
    return o + '</g>'

def label(x, y, t, sub=""):
    return f'<text x="{x}" y="{y}" {F} font-size="30" font-weight="800" text-anchor="middle" fill="{INK}">{t}</text>' + (f'<text x="{x}" y="{y+28}" {F} font-size="20" text-anchor="middle" fill="#666">{sub}</text>' if sub else '')

# ---------- LỊCH SỬ ----------
def caveman(x, y, s):
    spots = "".join(f'<ellipse cx="{px}" cy="{py}" rx="6" ry="4" fill="#4a2c14"/>' for px, py in [(-18, -150), (10, -170), (22, -120), (-26, -110), (0, -128)])
    tun = '<path d="M-42 -196 Q-4 -210 30 -198 L44 -150 L40 -88 L28 -70 L18 -86 L6 -64 L-8 -84 L-22 -62 L-34 -84 L-40 -120Z" fill="#a8703f" stroke="#222" stroke-width="8" stroke-linejoin="round"/>'
    hair = P("M-40 -352 L-52 -372 M-18 -378 L-22 -402 M6 -382 L10 -408 M30 -374 L44 -396 M50 -352 L66 -366", 8)
    beard = P("M-30 -262 L-38 -246 M-12 -250 L-16 -232 M8 -246 L10 -228 M26 -256 L34 -240", 7)
    club = '<path d="M60 -60 L84 -190" stroke="#222" stroke-width="22" stroke-linecap="round"/><path d="M60 -60 L84 -190" stroke="#c89a5a" stroke-width="13" stroke-linecap="round"/><ellipse cx="88" cy="-206" rx="24" ry="30" fill="#c89a5a" stroke="#222" stroke-width="7" transform="rotate(14 88 -206)"/>'
    return char(x, y, s, "holdR", garment=tun + spots, hair=hair, front=beard + club, expr="angry", shoes="#fff")

def roman(x, y, s):
    tun = torso("#c0392b", -80, 42, 38) + P("M-40 -150 L40 -150 M-38 -120 L38 -120", 6) + '<path d="M-30 -196 L30 -196 L26 -178 L-26 -178Z" fill="#d9a53a" stroke="#222" stroke-width="6"/>'
    helm = f'<path d="M-62 -318 C-66 -380 -24 -392 22 -386 C66 -380 72 -340 66 -310 L-60 -310Z" fill="#c9822a" stroke="#222" stroke-width="9"/><path d="M-30 -388 Q4 -440 40 -384 L30 -380 Q4 -420 -22 -382Z" fill="#c0392b" stroke="#222" stroke-width="7"/>'
    shield = '<circle cx="-70" cy="-120" r="52" fill="#c0392b" stroke="#222" stroke-width="9"/><circle cx="-70" cy="-120" r="18" fill="#f2c14e" stroke="#222" stroke-width="6"/>'
    spear = '<path d="M84 -20 L84 -400" stroke="#222" stroke-width="10" stroke-linecap="round"/><path d="M84 -420 L74 -392 L94 -392Z" fill="#cfd6dd" stroke="#222" stroke-width="6" stroke-linejoin="round"/>'
    return char(x, y, s, "shield", garment=tun, shoes="#8a5a2c", expr="angry", hat=helm, front=shield + spear)

def knight(x, y, s):
    arm = "#8f9ba8"
    tab = torso("#8f9ba8", -80, 44, 38) + '<path d="M-30 -190 L30 -190 L26 -90 L-26 -90Z" fill="#2d5aa0" stroke="#222" stroke-width="6"/><path d="M0 -190 L0 -92 M-20 -160 L20 -160" stroke="#fff" stroke-width="9"/>'
    helm = f'<path d="{HEAD}" fill="#9aa5b1" stroke="#222" stroke-width="10"/><rect x="-44" y="-322" width="92" height="22" rx="4" fill="#222"/><path d="M-6 -382 Q10 -438 38 -400 Q22 -404 14 -382Z" fill="#c0392b" stroke="#222" stroke-width="6"/>'
    shield = '<path d="M-98 -160 L-40 -160 L-40 -110 Q-40 -70 -68 -52 Q-98 -70 -98 -110Z" fill="#2d5aa0" stroke="#222" stroke-width="9"/><path d="M-69 -150 L-69 -76 M-90 -128 L-48 -128" stroke="#fff" stroke-width="8"/>'
    sword = '<path d="M74 -150 L74 -300" stroke="#222" stroke-width="16" stroke-linecap="round"/><path d="M74 -150 L74 -296" stroke="#e3e8ee" stroke-width="8" stroke-linecap="round"/><path d="M56 -156 L92 -156" stroke="#222" stroke-width="10" stroke-linecap="round"/>'
    return char(x, y, s, "shield", sleeves=(arm, 1.0), pants=arm, garment=tab, shoes="#6d7782", expr="neutral", pre="", front="", post="") .replace('<g transform', '<g transform', 1)[:-4] + helm_after(helm) + shield + sword + '</g>'

def helm_after(h): return h

def musketeer(x, y, s):
    coat = torso("#b8322a", -76, 42, 38) + P("M-38 -196 L36 -88 M38 -196 L-34 -88", 11) + '<path d="M-38 -196 L36 -88 M38 -196 L-34 -88" stroke="#fff" stroke-width="6" fill="none"/>' + "".join(f'<circle cx="0" cy="{yy}" r="4" fill="#f2c14e"/>' for yy in (-170, -140, -110))
    hat = '<path d="M-48 -366 L-40 -460 L40 -460 L48 -366Z" fill="#222" stroke="#222" stroke-width="8" stroke-linejoin="round"/><rect x="-54" y="-376" width="108" height="16" rx="6" fill="#222"/><path d="M0 -460 Q6 -500 -8 -520" stroke="#222" stroke-width="10" stroke-linecap="round" fill="none"/><circle cx="-8" cy="-522" r="10" fill="#c0392b" stroke="#222" stroke-width="5"/>'
    musket = '<path d="M86 -24 L86 -330" stroke="#222" stroke-width="12" stroke-linecap="round"/><path d="M86 -24 L86 -330" stroke="#6b6f76" stroke-width="5" stroke-linecap="round"/><path d="M86 -24 L90 -110" stroke="#8a5a2c" stroke-width="12" stroke-linecap="round"/>'
    return char(x, y, s, "upR", sleeves=("#b8322a", 1.0), pants="#fff", garment=coat, shoes="#222", expr="smile", hat=hat, front=musket)

def soldier(x, y, s):
    vest = torso("#556b3a", -80, 44, 38) + '<rect x="-30" y="-150" width="22" height="26" rx="4" fill="#45572f" stroke="#222" stroke-width="5"/><rect x="8" y="-150" width="22" height="26" rx="4" fill="#45572f" stroke="#222" stroke-width="5"/><path d="M-42 -100 L40 -100" stroke="#222" stroke-width="9"/>'
    helm = '<path d="M-64 -326 C-70 -392 -24 -402 24 -396 C70 -390 76 -350 68 -318 L-62 -316Z" fill="#4e6a35" stroke="#222" stroke-width="9"/><path d="M-60 -326 L66 -326" stroke="#222" stroke-width="8"/>'
    shades = '<path d="M-48 -322 L-10 -322 L-12 -296 L-44 -296Z M12 -320 L48 -320 L46 -296 L16 -296Z" fill="#111"/><path d="M-12 -312 L14 -312" stroke="#111" stroke-width="6"/>'
    pack = '<rect x="-84" y="-190" width="50" height="86" rx="10" fill="#45572f" stroke="#222" stroke-width="8"/>'
    binoc = '<rect x="46" y="-140" width="16" height="34" rx="6" fill="#333" stroke="#222" stroke-width="5"/><rect x="66" y="-140" width="16" height="34" rx="6" fill="#333" stroke="#222" stroke-width="5"/>'
    return char(x, y, s, "holdR", sleeves=("#556b3a", 1.0), pants="#556b3a", garment=vest, shoes="#222", expr="neutral", pre=pack, hat=helm + shades, front=binoc)

# ---------- ĐỜI SỐNG & TÀI CHÍNH ----------
def office(x, y, s):
    sh = torso("#fff", -78, 40, 34) + '<polygon points="-8,-196 8,-196 12,-130 0,-118 -12,-130" fill="#2d5aa0" stroke="#222" stroke-width="5"/><rect x="18" y="-168" width="22" height="30" rx="3" fill="#fff" stroke="#222" stroke-width="5"/>'
    hair = P("M-40 -358 Q0 -392 40 -366", 12)
    lap = '<rect x="46" y="-142" width="64" height="8" rx="3" fill="#9aa5b1" stroke="#222" stroke-width="5"/><path d="M50 -142 L58 -176 L108 -176 L104 -142" fill="#cfd6dd" stroke="#222" stroke-width="5" stroke-linejoin="round"/>'
    return char(x, y, s, "holdR", sleeves=("#fff", .9), pants="#3b3f46", garment=sh, hair=hair, shoes="#222", expr="worry", front=lap)

def boss(x, y, s):
    suit = torso("#27456f", -70, 44, 40) + '<path d="M-14 -196 L0 -150 L14 -196" fill="#f1f1ee" stroke="#222" stroke-width="5"/><polygon points="-6,-170 6,-170 9,-120 0,-108 -9,-120" fill="#c0392b" stroke="#222" stroke-width="5"/>'
    hair = P("M-44 -352 Q-36 -378 -26 -372 M44 -350 Q40 -374 30 -370", 9)
    glass = '<circle cx="-20" cy="-312" r="16" fill="none" stroke="#222" stroke-width="6"/><circle cx="22" cy="-312" r="16" fill="none" stroke="#222" stroke-width="6"/><path d="M-4 -312 L6 -312" stroke="#222" stroke-width="5"/>'
    case = '<rect x="30" y="-96" width="64" height="48" rx="6" fill="#8a5a2c" stroke="#222" stroke-width="7"/><path d="M52 -96 L52 -108 L72 -108 L72 -96" fill="none" stroke="#222" stroke-width="6"/>'
    return char(x, y, s, "down", sleeves=("#27456f", 1.0), pants="#27456f", garment=suit, hair=hair, shoes="#222", expr="angry", front=glass + case)

def teller(x, y, s):
    vest = torso("#fff", -78, 40, 34) + '<path d="M-38 -196 L-24 -90 L24 -90 L38 -196 L10 -196 L0 -150 L-10 -196Z" fill="#2a9d8f" stroke="#222" stroke-width="7" stroke-linejoin="round"/><rect x="14" y="-150" width="24" height="14" rx="2" fill="#fff" stroke="#222" stroke-width="4"/>'
    hair = '<path d="M-60 -318 C-72 -388 -22 -396 22 -390 C66 -384 74 -340 62 -300 Q50 -350 0 -356 Q-44 -352 -60 -300Z" fill="#222"/>'
    head = P("M-62 -318 Q-70 -250 -48 -236", 12) + '<path d="M-60 -312 Q-72 -386 0 -396" fill="none" stroke="#222" stroke-width="9"/><path d="M-62 -300 L-66 -270 Q-54 -256 -46 -270" fill="#2a9d8f" stroke="#222" stroke-width="5"/><path d="M-62 -270 Q-48 -230 -20 -228" fill="none" stroke="#222" stroke-width="5"/>'
    coin = '<circle cx="76" cy="-124" r="20" fill="#f2c14e" stroke="#222" stroke-width="7"/><text x="76" y="-117" font-family="Arial" font-size="22" font-weight="800" text-anchor="middle" fill="#222">$</text>'
    return char(x, y, s, "holdR", sleeves=("#fff", .95), pants="#2f3b4f", garment=vest, hair=hair, shoes="#222", expr="smile", hat=head, front=coin)

def shipper(x, y, s):
    jk = torso("#2e9e5b", -80, 44, 38) + P("M0 -196 L0 -86", 6)
    box = '<rect x="-96" y="-206" width="62" height="84" rx="6" fill="#f08a3c" stroke="#222" stroke-width="8"/><path d="M-96 -170 L-34 -170" stroke="#222" stroke-width="6"/>'
    helm = '<path d="M-64 -318 C-70 -388 -24 -400 24 -394 C70 -388 76 -346 68 -312 L-62 -310Z" fill="#f08a3c" stroke="#222" stroke-width="9"/><path d="M40 -312 L76 -312" stroke="#222" stroke-width="9" stroke-linecap="round"/>'
    return char(x, y, s, "down", sleeves=("#2e9e5b", 1.0), pants="#2a2d33", garment=jk, pre=box, hat=helm, shoes="#222", expr="smile")

def shopkeeper(x, y, s):
    tee = torso("#f2a9be", -78, 42, 36) + '<path d="M-26 -176 L26 -176 L34 -80 L-34 -80Z" fill="#fff" stroke="#222" stroke-width="7" stroke-linejoin="round"/><path d="M-26 -176 L-24 -196 M26 -176 L24 -196" stroke="#222" stroke-width="6"/>'
    cap = '<path d="M-60 -330 C-66 -384 -22 -392 22 -388 C64 -384 70 -352 64 -330Z" fill="#f2c14e" stroke="#222" stroke-width="8"/>'
    bag = '<path d="M62 -120 L72 -70 L120 -70 L130 -120Z" fill="#c89a5a" stroke="#222" stroke-width="7" stroke-linejoin="round"/><path d="M74 -120 Q96 -150 118 -120" fill="none" stroke="#222" stroke-width="6"/>'
    return char(x, y, s, "holdR", sleeves=("#f2a9be", .6), pants="#8a5a2c", garment=tee, hat=cap, shoes="#fff", expr="smile", front=bag)

def student(x, y, s):
    hd = torso("#f2c14e", -76, 44, 38) + '<path d="M-24 -196 Q0 -160 24 -196" fill="#e0a82e" stroke="#222" stroke-width="6"/><path d="M-4 -160 L-4 -128 M6 -160 L6 -128" stroke="#222" stroke-width="5"/>'
    pack = '<rect x="-90" y="-196" width="54" height="92" rx="12" fill="#d9483b" stroke="#222" stroke-width="8"/><rect x="-80" y="-150" width="34" height="28" rx="6" fill="#b83a30" stroke="#222" stroke-width="5"/>'
    book = '<rect x="46" y="-150" width="46" height="58" rx="4" fill="#4f86c6" stroke="#222" stroke-width="7"/><path d="M52 -134 L86 -134" stroke="#fff" stroke-width="5"/>'
    hair = P("M-44 -352 Q-10 -396 44 -362", 14)
    return char(x, y, s, "holdR", sleeves=("#f2c14e", 1.0), pants="#3d5a8a", garment=hd, pre=pack, hair=hair, shoes="#fff", expr="smile", front=book)

def it(x, y, s):
    hd = torso("#3a3d45", -76, 44, 38) + '<path d="M-26 -196 Q0 -160 26 -196" fill="#2b2d34" stroke="#222" stroke-width="6"/>'
    phones = '<path d="M-60 -330 Q-4 -420 62 -330" fill="none" stroke="#222" stroke-width="12" stroke-linecap="round"/><rect x="-76" y="-336" width="22" height="42" rx="9" fill="#4f86c6" stroke="#222" stroke-width="6"/><rect x="54" y="-336" width="22" height="42" rx="9" fill="#4f86c6" stroke="#222" stroke-width="6"/>'
    lap = '<path d="M46 -146 L56 -184 L112 -184 L106 -146Z" fill="#cfd6dd" stroke="#222" stroke-width="6" stroke-linejoin="round"/><rect x="40" y="-146" width="76" height="8" rx="3" fill="#9aa5b1" stroke="#222" stroke-width="5"/><circle cx="84" cy="-166" r="6" fill="#222"/>'
    return char(x, y, s, "holdR", sleeves=("#3a3d45", 1.0), pants="#4b5d8a", garment=hd, hat=phones, shoes="#fff", expr="neutral", front=lap)

def investor(x, y, s):
    bl = torso("#fff", -78, 40, 34) + '<path d="M-42 -196 L-28 -86 L-10 -86 L-4 -150 L4 -150 L10 -86 L28 -86 L42 -196 L16 -196 L0 -156 L-16 -196Z" fill="#8a6f9e" stroke="#222" stroke-width="7" stroke-linejoin="round"/>'
    hair = P("M-40 -356 Q-6 -396 44 -358", 12)
    ph = '<rect x="58" y="-176" width="40" height="66" rx="8" fill="#222" stroke="#222" stroke-width="6"/><rect x="63" y="-170" width="30" height="50" rx="3" fill="#143a66"/><path d="M66 -134 L74 -146 L82 -138 L90 -158" fill="none" stroke="#4dffb0" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    return char(x, y, s, "holdR", sleeves=("#8a6f9e", 1.0), pants="#3d5a8a", garment=bl, hair=hair, shoes="#fff", expr="smile", front=ph)

FILT = '<filter id="wob" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>'

import re
MONO_DEFS = ('<pattern id="h1" width="11" height="11" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="11" height="11" fill="#fff"/><line x1="0" y1="0" x2="0" y2="11" stroke="#222" stroke-width="3.4"/></pattern>'
             '<pattern id="h2" width="9" height="9" patternUnits="userSpaceOnUse"><rect width="9" height="9" fill="#fff"/><path d="M0 0L9 9M9 0L0 9" stroke="#222" stroke-width="2.6"/></pattern>')
def mono(markup):
    def f(m):
        attr, col = m.group(1), m.group(2).lower()
        if col in ('#222', '#fff', '#ffffff', '#1a1a1a'): return m.group(0)
        r, g, b = (int(col[i:i + 2], 16) / 255 for i in (1, 3, 5)); lum = .2126 * r + .7152 * g + .0722 * b
        if lum < .26: return f'{attr}="#222"'
        if lum < .46: return f'{attr}="url(#h2)"'
        if lum < .72: return f'{attr}="url(#h1)"'
        return f'{attr}="#fff"'
    return re.sub(r'(fill|stroke)="(#[0-9a-fA-F]{6})"', f, markup)

def sheet(title, items, cols, rows, s, ttl):
    b = '<g filter="url(#wob)">'
    cw, rh = 1600 // cols, (900 - 70) // rows
    out = ""
    for i, (fn, name, sub) in enumerate(items):
        cx, cy = (i % cols) * cw + cw // 2, 70 + (i // cols) * rh + rh - 70
        b += fn(cx, cy, s)
        out += label(cx, cy + 40, name, sub)
    if MONO: b = mono(b)
    b += '</g>' + out + f'<text x="800" y="48" {F} font-size="36" font-weight="800" text-anchor="middle" fill="{INK}">{ttl}</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900"><defs>{FILT}{MONO_DEFS}</defs><rect width="1600" height="900" fill="{PAPER}"/>{b}</svg>'
    return svg(b, '<filter id="wob" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>')

if __name__ == "__main__":
    os.makedirs("outfits", exist_ok=True)
    hist = [(caveman, "Người tiền sử", "da thú"), (roman, "Chiến binh La Mã", "mũ, khiên, giáo"), (knight, "Hiệp sĩ", "giáp, khiên, kiếm"), (musketeer, "Lính thế kỷ 18", "mũ cao, áo đỏ"), (soldier, "Lính hiện đại", "mũ, áo giáp, balo")]
    life = [(office, "Nhân viên văn phòng", "sơ mi, cà vạt"), (boss, "Giám đốc", "vest, kính, cặp"), (teller, "Nhân viên ngân hàng", "áo gile, tai nghe"), (shipper, "Shipper", "mũ, áo khoác, thùng hàng"),
            (shopkeeper, "Chủ tiệm", "tạp dề, túi hàng"), (student, "Sinh viên", "áo hoodie, balo"), (it, "Dân công nghệ", "hoodie, tai nghe, laptop"), (investor, "Nhà đầu tư", "áo khoác, điện thoại")]
    for name, items, cols, rows, s, ttl in (("01-lich-su-nen-trang", hist, 5, 1, 1.2, "Nhân vật lịch sử (kiểu người que nét bút lông)"), ("02-doi-song-nen-trang", life, 4, 2, .74, "Nhân vật đời sống và tài chính")):
        open(f"outfits/{name}.svg", "w").write(sheet(name, items, cols, rows, s, ttl)); render(f"outfits/{name}.svg", f"outfits/{name}.png", 1600, 900)
