"""Storyboard mẫu: 'Ví điện tử miễn phí, vậy họ kiếm tiền từ đâu?' (8 cảnh). Chạy: python3 gen_storyboard.py"""
import os, math
from PIL import Image, ImageDraw, ImageFont
from gen_scenes import render, svg
from gen_styles import F
from gen_styles_people import figure
import gen_styles as gs

G = "#00D68F"; NAVY = "#0B1F3A"; MUTED = "#8fa6c4"
DEFS = '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1F3A"/><stop offset="1" stop-color="#12335E"/></linearGradient><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#00D68F"/></marker><marker id="ar2" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#f2b632"/></marker>'

def T(x, y, t, size=30, fill="#fff", w=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" {F} font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {extra}>{t}</text>'

def frame(tag, body, narr):
    b = f'<rect width="1280" height="720" fill="url(#bg)"/>' + T(60, 70, tag, 24, MUTED, 400, extra='letter-spacing="3"') + body
    b += '<rect y="610" width="1280" height="110" fill="#000" opacity=".55"/>'
    for i, line in enumerate(narr):
        b += T(640, 656 + i * 40, line, 31, "#fff", 400, "middle")
    return svg(b, DEFS)

def s1():
    body = T(90, 230, "MIỄN PHÍ?", 110, "#fff", 800) + T(94, 290, "Chuyển tiền", 30, MUTED) + T(94, 335, "Thanh toán", 30, MUTED) + T(94, 380, "Nạp điện thoại", 30, MUTED)
    body += '<g transform="translate(180 0)"><rect x="760" y="110" width="250" height="470" rx="34" fill="#0d2748" stroke="#00D68F" stroke-width="6"/><rect x="782" y="150" width="206" height="390" rx="14" fill="#08162b"/>'
    body += T(885, 290, "PHÍ", 28, MUTED, 700, "middle") + T(885, 380, "0 đ", 78, G, 800, "middle") + '<rect x="820" y="440" width="130" height="46" rx="23" fill="#00D68F"/>' + T(885, 472, "GỬI", 24, NAVY, 800, "middle") + '</g>'
    body += figure(790, 600, 0.9, coat="#17365e", pants="#0a1830", shirt="#cfe0f5", stroke=G, sw=2.5, pose="phone")
    return frame("01 · MỞ ĐẦU · 0–6 giây", body, ["Chuyển tiền, thanh toán đều miễn phí.", "Vậy ai trả tiền cho ứng dụng đó?"])

def s2():
    b = '<polygon points="200,520 640,740 1080,520 640,300" fill="#12335E"/>'
    for x, h, lab in ((430, 120, "Máy chủ"), (640, 190, "Bảo mật"), (850, 150, "Nhân sự")):
        b += gs.iso(x, 520, 60, 60, h, "#8ba6cf", "#2a4770", "#3b5f93")
        b += T(x, 565, lab, 26, "#cfe0f5", 700, "middle")
    b += '<circle cx="640" cy="215" r="52" fill="#f2b632"/>' + T(640, 248, "?", 76, "#8a5d00", 800, "middle")
    b += T(640, 130, "CHI PHÍ VẬN HÀNH", 28, MUTED, 700, "middle", 'letter-spacing="4"')
    return frame("02 · BÀI TOÁN · 6–14 giây", b, ["Vận hành ví cần máy chủ, bảo mật và đội ngũ.", "Chi phí này lớn, và phải có nguồn thu bù lại."])

def node(x, y, t, c="#17365e"):
    return f'<circle cx="{x}" cy="{y}" r="86" fill="{c}" stroke="{G}" stroke-width="5"/>' + T(x, y + 10, t, 26, "#fff", 700, "middle")

def s3():
    b = node(220, 300, "Người mua") + node(640, 300, "Ví điện tử", "#0f4a3a") + node(1060, 300, "Cửa hàng")
    b += f'<path d="M310 300H540" stroke="{G}" stroke-width="6" marker-end="url(#ar)"/><path d="M740 300H960" stroke="{G}" stroke-width="6" marker-end="url(#ar)"/>'
    b += T(425, 280, "100 đ", 28, "#fff", 700, "middle") + T(850, 280, "gần đủ", 28, "#fff", 700, "middle")
    b += f'<path d="M640 392V470" stroke="#f2b632" stroke-width="6" marker-end="url(#ar2)"/><rect x="410" y="490" width="460" height="70" rx="12" fill="#2a2210" stroke="#f2b632" stroke-width="3"/>' + T(640, 535, "Phí nhỏ trên mỗi giao dịch", 28, "#f2b632", 700, "middle")
    b += T(640, 140, "NGUỒN THU 1 · PHÍ TỪ CỬA HÀNG", 30, MUTED, 700, "middle", 'letter-spacing="3"')
    return frame("03 · NGUỒN THU 1 · 14–24 giây", b, ["Thứ nhất, cửa hàng thường trả một khoản phí nhỏ", "cho mỗi giao dịch, người mua thì không thấy."])

def s4():
    b = '<rect x="150" y="260" width="320" height="220" rx="28" fill="#17365e" stroke="#00D68F" stroke-width="5"/><rect x="380" y="330" width="140" height="80" rx="20" fill="#0f4a3a" stroke="#00D68F" stroke-width="4"/><circle cx="420" cy="370" r="10" fill="#7DFFC4"/>'
    for i in range(4): b += f'<ellipse cx="{260+i*0}" cy="{250-i*18}" rx="52" ry="14" fill="#f2b632" stroke="#8a5d00" stroke-width="3"/>'
    b += T(310, 530, "Tiền nhàn rỗi trong ví", 28, "#cfe0f5", 700, "middle")
    b += '<polygon points="820,260 1000,190 1180,260" fill="#cfe0f5"/><rect x="840" y="260" width="320" height="30" fill="#8ba6cf"/>' + "".join(f'<rect x="{860+i*70}" y="290" width="36" height="150" fill="#cfe0f5"/>' for i in range(4)) + '<rect x="830" y="440" width="340" height="30" fill="#8ba6cf"/>'
    b += T(1000, 530, "Ngân hàng", 28, "#cfe0f5", 700, "middle")
    b += f'<path d="M530 340H800" stroke="{G}" stroke-width="6" marker-end="url(#ar)"/><path d="M800 410H530" stroke="#f2b632" stroke-width="6" marker-end="url(#ar2)"/>' + T(665, 325, "gửi", 26, G, 700, "middle") + T(665, 450, "lãi", 26, "#f2b632", 700, "middle")
    b += T(640, 130, "NGUỒN THU 2 · LÃI TỪ TIỀN TRONG VÍ", 30, MUTED, 700, "middle", 'letter-spacing="3"')
    return frame("04 · NGUỒN THU 2 · 24–34 giây", b, ["Thứ hai, số dư nằm trong ví có thể được gửi", "theo quy định, và tạo ra lãi. (cần kiểm chứng theo từng ví)"])

def card(x, title, icon):
    return f'<rect x="{x}" y="190" width="320" height="330" rx="22" fill="#0d2748" stroke="#fff" stroke-width="3" stroke-dasharray="10 8"/>' + icon + T(x + 160, 480, title, 34, "#fff", 700, "middle")

def s5():
    ic1 = f'<g transform="translate(210 320)" fill="none" stroke="{G}" stroke-width="7"><circle r="52"/><path d="M-22 -8H22M-22 14H22"/></g>'
    ic2 = f'<g transform="translate(640 320)" fill="none" stroke="{G}" stroke-width="7"><path d="M0 -62L52 -38V12Q52 52 0 70Q-52 52 -52 12V-38Z"/><path d="M-20 4L-4 20L24 -14"/></g>'
    ic3 = f'<g transform="translate(1070 320)" fill="none" stroke="{G}" stroke-width="7" stroke-linecap="round"><path d="M-58 50L-20 8L8 28L56 -40"/><path d="M30 -42H58V-14"/></g>'
    b = card(50, "Cho vay", ic1) + card(480, "Bảo hiểm", ic2) + card(910, "Đầu tư", ic3)
    b += T(640, 140, "NGUỒN THU 3 · DỊCH VỤ TÀI CHÍNH", 30, MUTED, 700, "middle", 'letter-spacing="3"')
    return frame("05 · NGUỒN THU 3 · 34–44 giây", b, ["Thứ ba, ví bán thêm dịch vụ: vay, bảo hiểm, đầu tư,", "thường qua đối tác và có hoa hồng."])

def pie(cx, cy, r, vals, cols):
    tot = sum(vals); a = -math.pi / 2; o = ""
    for v, c in zip(vals, cols):
        a2 = a + 2 * math.pi * v / tot
        x1, y1, x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a), cx + r * math.cos(a2), cy + r * math.sin(a2)
        o += f'<path d="M{cx} {cy}L{x1:.0f} {y1:.0f}A{r} {r} 0 {1 if v/tot>.5 else 0} 1 {x2:.0f} {y2:.0f}Z" fill="{c}" stroke="{NAVY}" stroke-width="5"/>'
        a = a2
    return o

LEG = [("Phí giao dịch", "#00D68F"), ("Lãi từ số dư", "#3b7bd1"), ("Dịch vụ tài chính", "#f2b632"), ("Khác (đối tác, quảng cáo)", "#8ba6cf")]

def legend(x, y):
    return "".join(f'<rect x="{x}" y="{y+i*58}" width="28" height="28" rx="6" fill="{c}"/>' + T(x + 46, y + 24 + i * 58, t, 28, "#fff", 400) for i, (t, c) in enumerate(LEG))

def s6():
    b = pie(360, 340, 200, [40, 25, 20, 15], [c for _, c in LEG]) + legend(680, 190)
    b += T(640, 130, "CƠ CẤU DOANH THU (MINH HỌA)", 30, MUTED, 700, "middle", 'letter-spacing="3"')
    b += '<rect x="680" y="450" width="520" height="70" rx="12" fill="#3a1a1a" stroke="#ff6b6b" stroke-width="3"/>' + T(940, 496, "SỐ MINH HỌA, thay bằng số thật + nguồn", 24, "#ff9a9a", 700, "middle")
    return frame("06 · TỔNG HỢP · 44–52 giây", b, ["Mỗi ví có tỷ lệ khác nhau.", "Muốn biết chính xác, hãy xem báo cáo của từng công ty."])

def s7():
    b = pie(230, 340, 130, [40, 25, 20, 15], [c for _, c in LEG])
    b += figure(1170, 600, 1.0, coat="#17365e", pants="#0a1830", shirt="#cfe0f5", stroke=G, sw=2.5, pose="point", flip=True)
    b += T(420, 230, "Miễn phí cho người dùng", 36, "#fff", 800) + T(420, 280, "không có nghĩa là không có chi phí", 36, G, 800)
    b += T(420, 370, "• Đọc điều khoản và phí ẩn", 30, "#cfe0f5") + T(420, 420, "• Biết dữ liệu nào được dùng", 30, "#cfe0f5") + T(420, 470, "• Cẩn trọng với ưu đãi quá hấp dẫn", 30, "#cfe0f5")
    return frame("07 · KẾT LUẬN · 52–58 giây", b, ["Miễn phí với người dùng không có nghĩa là không có chi phí.", "Hãy đọc kỹ điều khoản trước khi dùng."])

def s8():
    mark = '<g transform="translate(470 120) scale(1.4)"><rect width="240" height="240" rx="52" fill="#0E2A4D" stroke="#00C27A" stroke-width="3"/><rect x="62" y="62" width="116" height="26" rx="8" fill="#fff"/><rect x="107" y="62" width="26" height="116" rx="8" fill="#fff"/><polyline points="48,178 92,140 118,156 188,92" fill="none" stroke="#5CF2B0" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><polygon points="196,82 170,86 190,108" fill="#5CF2B0"/></g>'
    b = mark + T(640, 520, "TRUNG MONEY TECH", 56, "#fff", 800, "middle", 'letter-spacing="4"') + T(640, 570, "Theo dõi để xem tập tiếp theo", 30, G, 700, "middle")
    return frame("08 · KẾT · 58–65 giây", b, ["Nếu thấy hữu ích, hãy theo dõi kênh.", "Hẹn gặp lại ở video sau."])

SC = [s1, s2, s3, s4, s5, s6, s7, s8]

if __name__ == "__main__":
    os.makedirs("storyboard", exist_ok=True)
    fp = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(fp, 22) if os.path.exists(fp) else ImageFont.load_default()
    sheet = Image.new("RGB", (1280, 4 * 396), "white")
    for i, fn in enumerate(SC):
        k = f"storyboard/{i+1:02d}"
        open(k + ".svg", "w").write(fn()); render(k + ".svg", k + ".png")
        sheet.paste(Image.open(k + ".png").resize((640, 360)), ((i % 2) * 640, (i // 2) * 396 + 36))
        ImageDraw.Draw(sheet).text(((i % 2) * 640 + 10, (i // 2) * 396 + 6), f"Cảnh {i+1}", fill="black", font=font)
    sheet.save("storyboard/tong-hop.png")
