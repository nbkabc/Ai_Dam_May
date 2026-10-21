# Dựng video trên PC (Windows / Linux)

## Cấu hình máy
Video dựng ở 1280×720, 24 khung/giây. Mỗi `--workers` là một tiến trình Chromium riêng (~400–600 MB RAM),
nên số nhân CPU và RAM quyết định tốc độ. Không cần card đồ họa rời.

| | Tối thiểu | Khuyên dùng | Mạnh |
|---|---|---|---|
| CPU | 4 nhân (i3 đời 8 / Ryzen 3) | 6–8 nhân (i5-12400 / Ryzen 5 5600) | 12+ nhân (i7/Ryzen 7 trở lên) |
| RAM | 8 GB | 16 GB | 32 GB |
| Ổ đĩa | SSD trống 5 GB | SSD NVMe trống 20 GB | NVMe |
| GPU | không cần | không cần | không cần |
| `--workers` | 2 | 4–6 | 8–12 |

- Quy tắc chọn `--workers`: không quá số nhân CPU, và không quá (RAM GB − 4) / 0,6.
- Khung hình tạm cần vài trăm MB cho mỗi phút video, tự xóa sau khi xong.
- Video 73 giây ≈ 1750 khung. Chạy thử `--dur 5` trước để đo tốc độ thật của máy.

## Cài một lần

### Windows 10/11 (PowerShell)
```powershell
winget install OpenJS.NodeJS.LTS Gyan.FFmpeg Python.Python.3.12
# mở lại PowerShell để nhận PATH mới
cd video
npm i playwright
npx playwright install chromium
pip install numpy pillow
```

### Ubuntu / Debian
```bash
sudo apt install nodejs npm ffmpeg python3 python3-pip python3-numpy python3-pil
cd video
npm i playwright
npx playwright install --with-deps chromium
```

## Thử nhanh 5 giây để đo tốc độ
```bash
python build_video.py --dur 5 --workers 4 --out out/thu.mp4
```
Cuối lệnh in dòng "X giây render cho mỗi 1 giây video". Nhân với độ dài video thật để biết mất bao lâu.
(Trên Linux dùng `python3` thay cho `python`.)

## Dựng cả video
```bash
python build_video.py --anim anim4.html --timeline timeline5.json --audio-script make_audio4.py --out out/video.mp4 --workers 4
```
- Tắt chế độ ngủ của Windows trong lúc render (Settings → System → Power → Sleep: Never).
- Thêm `--fps 15` để giảm gần một nửa thời gian, nét vẽ tay vẫn đẹp.
- Thêm `--keep-frames` để giữ lại khung hình tạm.

## Lỗi thường gặp
| Lỗi | Cách xử lý |
|---|---|
| `Chưa cài playwright` | chạy lại `npm i playwright && npx playwright install chromium` trong thư mục `video` |
| `ffmpeg` / `node` không nhận | mở lại cửa sổ dòng lệnh sau khi cài, hoặc kiểm tra PATH |
| Tiến trình render bị lỗi, máy đơ | giảm `--workers` |
| Chữ tiếng Việt lệch | cài font Arial (Windows có sẵn; Ubuntu: `sudo apt install ttf-mscorefonts-installer`) |
