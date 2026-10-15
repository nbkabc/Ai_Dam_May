#!/usr/bin/env python3
"""Tạo timeline4.json từ kịch bản: chia câu thành đoạn ngắn, ước tính thời lượng theo tốc độ đọc."""
import json, sys
WPS = float(sys.argv[1]) if len(sys.argv) > 1 else 3.8   # tiếng/giây (ước tính, thay bằng giọng thật sau)
GAP = .2; LEAD = .6; TAIL = 1.6; MINC = 1.5
SC = [
 ("office",  [("Giới trẻ bây giờ có một chuyện nghe vậy mà thật,", "nghe vậy mà thật"), ("lương không cao, việc cũng chẳng nhẹ,", "lương không cao"), ("vậy mà vẫn ở lại công ty rất lâu.", "rất lâu")]),
 ("notwhy",  [("Không phải vì mê công việc,", "mê công việc"), ("cũng không phải vì không dám đi.", "không dám đi")]),
 ("friends", [("Mà vì ở đó có tụi bạn.", "có tụi bạn")]),
 ("boba",    [("Trên công ty thì rủ nhau đặt trà sữa,", "trà sữa"), ("chia nhau đồ ăn vặt,", "đồ ăn vặt"), ("ngồi tán dóc tới giờ về.", "tán dóc")]),
 ("cafe",    [("Cuối tuần hẹn nhau đi cà phê,", "cà phê")]),
 ("travel",  [("tới dịp lễ còn rủ nhau đi chơi, đi du lịch.", "đi du lịch")]),
 ("lodge",   [("Nhiều bạn đi làm xa nhà,", "xa nhà"), ("ra khỏi công ty là về phòng trọ,", "phòng trọ"), ("nên công ty thành nơi có người để nói chuyện.", "có người để nói chuyện")]),
 ("night",   [("Có đợt người ta rủ qua chỗ lương cao hơn,", "lương cao hơn"), ("bạn ngồi nghĩ cả đêm,", "nghĩ cả đêm")]),
 ("morning", [("rồi sáng ra thấy ly trà sữa ai đó để sẵn trên bàn,", "ly trà sữa"), ("là thôi, ở lại.", "ở lại")]),
 ("price",   [("Cái giá của chuyện đó thì ít ai nói ra.", "Cái giá")]),
 ("wallet",  [("Cuối tháng vẫn chật,", "vẫn chật"), ("mà ly trà sữa nào, chuyến đi nào cũng tốn tiền.", "tốn tiền")]),
 ("leave",   [("Và khi mấy người đó lần lượt nghỉ,", "lần lượt nghỉ"), ("cái lý do để ở lại cũng đi theo.", "đi theo")]),
 ("realize", [("Lúc đó nhiều bạn mới giật mình,", "giật mình"), ("hóa ra mình gắn bó với những người ngồi cạnh mình,", "gắn bó với những người ngồi cạnh"), ("chứ đâu phải với công ty.", "đâu phải với công ty")]),
 ("noname",  [("Chuyện này chẳng có đúng sai,", "chẳng có đúng sai"), ("chỉ là nhiều bạn trẻ đang sống như vậy,", "đang sống như vậy"), ("mà chưa ai gọi nó ra thành tên.", "gọi nó ra thành tên")]),
 ("end",     [("Nếu bạn thấy mình trong đó,", "thấy mình trong đó"), ("kể mình nghe ở bình luận nha.", "kể mình nghe")]),
]
t = LEAD; scenes = {}; caps = []; order = []
for sid, chunks in SC:
    s = t
    for text, hl in chunks:
        d = max(MINC, len(text.replace(",", "").split()) / WPS + GAP)
        caps.append({"s": round(t, 2), "e": round(t + d, 2), "text": text, "hl": hl}); t += d
    scenes[sid] = {"s": round(s, 2), "e": round(t, 2)}; order.append(sid)
dur = round(t + TAIL, 2)
json.dump({"fps": 24, "dur": dur, "cps": 18, "ground": 612, "scenes": scenes, "order": order, "captions": caps}, open("timeline4.json", "w"), ensure_ascii=False, indent=1)
print("tổng", dur, "s;", len(caps), "đoạn phụ đề"); [print(f"  {k:8s} {v['s']:6.2f} - {v['e']:6.2f}") for k, v in scenes.items()]
