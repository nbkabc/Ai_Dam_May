# Dựng video trên Mac (M1 8GB)

## Cài một lần
```bash
brew install node ffmpeg python
cd video                      # thư mục này trong repo
npm i playwright
npx playwright install chromium
pip3 install numpy pillow
```

## Thử nhanh 5 giây để đo tốc độ
```bash
python3 build_video.py --dur 5 --workers 2 --out out/thu.mp4
```
Cuối lệnh in dòng "X giây render cho mỗi 1 giây video". Nhân với độ dài video thật để biết mất bao lâu.

## Dựng cả video
```bash
caffeinate -i python3 build_video.py --out out/video.mp4 --workers 3
```
- `caffeinate -i` giữ Mac không ngủ khi đang render.
- Máy 8GB: dùng `--workers 2` hoặc `3`. Nếu thấy máy chậm, tràn bộ nhớ, giảm xuống 2.
- Nét vẽ tay vẫn đẹp ở 15 khung/giây, giảm gần một nửa thời gian: thêm `--fps 15`.
- Cần khoảng vài trăm MB ổ đĩa cho khung hình tạm, tự xóa sau khi xong (thêm `--keep-frames` để giữ lại).

## Lỗi thường gặp
| Lỗi | Cách xử lý |
|---|---|
| `Chưa cài playwright` | chạy lại `npm i playwright && npx playwright install chromium` trong thư mục `video` |
| Tiến trình render bị lỗi | thử `--workers 2` |
| Chữ tiếng Việt lệch | cài font Arial (Mac có sẵn) |
