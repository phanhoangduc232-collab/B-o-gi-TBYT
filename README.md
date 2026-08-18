# Cổng thu thập báo giá trực tuyến - Bệnh viện E

Web app nhỏ để nhà cung cấp (NCC) tự đăng ký (bằng Tên công ty + Mã số thuế + mật khẩu tự đặt) và điền báo giá thiết bị y tế theo đúng cấu trúc Phụ lục I (bảng báo giá) + Phụ lục II (bảo trì mở rộng) của YCBG, kèm upload file đính kèm (catalogue, giấy phép lưu hành...). Mỗi NCC chỉ xem/sửa được dữ liệu của chính mình. Hệ thống chỉ cho đăng ký/nộp trong đúng khung giờ cấu hình sẵn; ngoài khung giờ đó NCC cũ chỉ xem lại được (không sửa), NCC mới không đăng ký được. Bệnh viện có trang quản trị riêng để xem toàn bộ báo giá đã nộp và xuất ra file Excel đúng cấu trúc "Tổng hợp báo giá - Dự toán" đang dùng.

Toàn bộ phần này viết cho người **CHƯA từng deploy website bao giờ** - làm theo từng bước là chạy được.

---

## 1. Bạn cần chuẩn bị gì trước

- 1 tài khoản GitHub (miễn phí) - để lưu code: https://github.com/signup
- 1 tài khoản Render.com (miễn phí, đăng nhập bằng GitHub luôn cho nhanh): https://dashboard.render.com/register
- Không cần biết lập trình, chỉ cần làm đúng theo các bước dưới.

Render.com được chọn vì: có gói miễn phí, hỗ trợ **ổ đĩa lưu trữ bền vững (persistent disk)** để không mất dữ liệu NCC đã nộp mỗi khi server khởi động lại (nhiều nền tảng miễn phí khác như Vercel KHÔNG hỗ trợ việc này, sẽ mất dữ liệu).

---

## 2. Đưa code lên GitHub

1. Đăng nhập GitHub, bấm nút **New repository** (góc trên bên phải, dấu +).
2. Đặt tên ví dụ `bve-vendor-quote-portal`, để **Private** (riêng tư) cho an toàn, bấm **Create repository**.
3. Trên máy tính của bạn (hoặc nhờ người IT), giải nén file `vendor-quote-portal.zip` tôi gửi kèm, mở terminal/cmd tại thư mục đó rồi chạy lần lượt:

```bash
git init
git add .
git commit -m "Khoi tao cong thu thap bao gia"
git branch -M main
git remote add origin https://github.com/<ten-tai-khoan-cua-ban>/bve-vendor-quote-portal.git
git push -u origin main
```

(Thay `<ten-tai-khoan-cua-ban>` bằng username GitHub thật của bạn. GitHub sẽ hỏi đăng nhập/token khi push lần đầu - làm theo hướng dẫn trên màn hình của GitHub.)

Nếu bạn chưa cài Git, tải tại: https://git-scm.com/downloads (cài đặt mặc định, Next liên tục).

---

## 3. Deploy lên Render.com

### Cách 1: Deploy bằng Render Blueprint (khuyến nghị - ít bước nhất)

1. Đăng nhập https://dashboard.render.com
2. Bấm **New** → **Blueprint**.
3. Chọn repository `bve-vendor-quote-portal` bạn vừa tạo ở bước 2 (Render sẽ tự đọc file `render.yaml` có sẵn trong code).
4. Render sẽ hiện ra danh sách: 1 Web Service + 1 Disk. Bấm **Apply**.
5. Render sẽ hỏi giá trị cho biến `ADMIN_PASSWORD` (vì tôi đã đánh dấu `sync: false` để bạn tự nhập, không lưu sẵn trong code cho an toàn) - hãy đặt 1 mật khẩu quản trị THẬT MẠNH (chỉ mình bạn/phòng Vật tư biết).
6. Bấm **Deploy**. Đợi khoảng 2-3 phút để Render build và chạy.
7. Sau khi chạy xong, Render cho bạn 1 đường link dạng `https://bve-vendor-quote-portal.onrender.com` - đây chính là link gửi cho các nhà cung cấp.

### Cách 2: Deploy thủ công (nếu Blueprint không khả dụng)

1. **New** → **Web Service** → chọn repo của bạn.
2. Runtime: chọn **Python 3**.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Chọn gói **Free**.
6. Mục **Disks**: bấm **Add Disk**, Mount Path đặt là `/var/data`, dung lượng 1GB là đủ.
7. Mục **Environment Variables**, thêm đủ các biến sau (xem giải thích ở mục 4 bên dưới):
   - `DATA_DIR` = `/var/data`
   - `SECRET_KEY` = (một chuỗi ký tự ngẫu nhiên dài, tự gõ bừa 30-40 ký tự)
   - `ADMIN_PASSWORD` = (mật khẩu quản trị của bạn)
   - `SUBMISSION_OPEN_AT` = `2026-08-01T10:00:00`
   - `SUBMISSION_CLOSE_AT` = `2026-08-15T16:00:00`
8. Bấm **Create Web Service**, đợi build xong.

---

## 4. Giải thích các biến môi trường quan trọng

| Biến | Ý nghĩa | Ví dụ |
|---|---|---|
| `SUBMISSION_OPEN_AT` | Thời điểm MỞ cổng (giờ Việt Nam) | `2026-08-01T10:00:00` = 10h00 ngày 01/08/2026 |
| `SUBMISSION_CLOSE_AT` | Thời điểm ĐÓNG cổng | `2026-08-15T16:00:00` = 16h00 ngày 15/08/2026 |
| `ADMIN_PASSWORD` | Mật khẩu vào trang quản trị `/admin` | tự đặt, càng dài càng khó đoán |
| `SECRET_KEY` | Chuỗi bí mật để mã hoá phiên đăng nhập | tự đặt 1 chuỗi ngẫu nhiên, không chia sẻ |
| `DATA_DIR` | Nơi lưu database + file upload (phải trỏ đúng Mount Path của Disk) | `/var/data` |
| `MAX_CONTENT_LENGTH_MB` | Giới hạn dung lượng mỗi file NCC upload | mặc định 25 (MB) |

Muốn đổi khung giờ cho đợt sau: vào Render → chọn service → **Environment** → sửa `SUBMISSION_OPEN_AT`/`SUBMISSION_CLOSE_AT` → **Save Changes** (Render tự khởi động lại).

**Quan trọng**: đồng hồ hệ thống được set theo giờ Việt Nam (Asia/Ho_Chi_Minh) sẵn trong code (`app.py`), bạn chỉ cần ghi giờ Việt Nam bình thường, không cần quy đổi UTC.

---

## 5. Cách gửi link cho nhà cung cấp

Gửi đúng 1 đường link Render cấp cho bạn (VD `https://bve-vendor-quote-portal.onrender.com`) qua email/thông báo mời báo giá, cùng hướng dẫn ngắn:

> "Truy cập [link], đăng ký bằng Tên công ty + Mã số thuế + tự đặt 1 mật khẩu (ghi nhớ mật khẩu này để có thể quay lại sửa báo giá trước hạn chót), điền đầy đủ các dòng báo giá thiết bị và tải kèm tài liệu chứng minh. Chỉ nhận báo giá từ [giờ mở] đến [giờ đóng]."

Nhà cung cấp KHÔNG cần tài khoản gì trước - tự đăng ký ngay trên trang.

---

## 6. Cách bạn (Bệnh viện) xem báo giá & xuất Excel

1. Vào `https://<link-cua-ban>/admin`
2. Nhập `ADMIN_PASSWORD` đã đặt ở bước 3.
3. Xem danh sách toàn bộ NCC đã đăng ký, bấm vào từng NCC để xem chi tiết + tải file đính kèm.
4. Bấm nút **"⬇ Xuất Excel tổng hợp"** ở góc trên - hệ thống tự tạo file Excel đúng cấu trúc sheet `Tong_hop_bao_gia` (bảng chi tiết A-M, vùng tham chiếu 20 danh mục, bảng tổng hợp/chốt giá dự toán bên dưới, tô màu xanh/đỏ giá thấp nhất/cao nhất) - y hệt file bạn đang dùng để tổng hợp thủ công, chỉ khác là tự động điền sẵn dữ liệu NCC đã nộp qua web thay vì phải đọc từng file PDF/Excel/Word như trước.

**Lưu ý về tô màu**: một số phiên bản Excel/LibreOffice cũ có thể không hiển thị ngay màu xanh/đỏ tự động nếu mở lần đầu - nếu gặp trường hợp này, hãy mở file, bấm `Ctrl+Shift+F9` (tính lại toàn bộ công thức) hoặc lưu lại 1 lần bằng Excel thật.

---

## 7. Bảo mật & giới hạn cần biết (đọc kỹ)

- **Xác thực NCC bằng MST + mật khẩu tự đặt**: đây là mức bảo mật cơ bản, phù hợp quy mô một đợt mời báo giá nội bộ. Nó CHẶN được việc NCC vô tình/cố ý bấm nhầm xem dữ liệu công ty khác, nhưng KHÔNG chống được việc ai đó cố tình đoán đúng MST + mật khẩu của công ty khác (MST doanh nghiệp là thông tin có thể tra cứu công khai). Nếu cần mức bảo mật cao hơn (email OTP xác thực), cần phát triển thêm - có thể trao đổi thêm nếu bạn cần.
- **Không có virus-scan cho file upload** - nếu cần, nên bật tính năng quét virus của Render hoặc quét thủ công trước khi mở file NCC gửi.
- **Gói Free của Render sẽ "ngủ" sau ~15 phút không có ai truy cập** rồi mất khoảng 30-50 giây để "thức dậy" ở lượt truy cập tiếp theo - NCC có thể thấy trang load chậm ở lượt đầu, đây là bình thường với gói miễn phí. Nếu muốn nhanh và ổn định hơn (không bị ngủ), nâng cấp gói trả phí thấp nhất của Render (khoảng 7 USD/tháng).
- **Sao lưu dữ liệu**: sau khi đóng cổng, nên vào trang admin xuất Excel VÀ tải hết file đính kèm về lưu trữ nội bộ ngay, không nên chỉ dựa vào server Render lâu dài.
- Đây là bản dựng nhanh phục vụ 1 đợt mua sắm - trước khi dùng cho gói thầu có giá trị lớn/tính chất pháp lý cao, nên nhờ bộ phận CNTT/pháp chế của bệnh viện rà soát thêm.

---

## 8. Chạy thử trên máy tính cá nhân (không bắt buộc, chỉ để kiểm tra trước khi deploy)

```bash
pip install -r requirements.txt
set SUBMISSION_OPEN_AT=2020-01-01T00:00:00      (Windows: dùng "set", Mac/Linux: dùng "export")
set SUBMISSION_CLOSE_AT=2099-01-01T00:00:00
set ADMIN_PASSWORD=admin123
python app.py
```
Mở trình duyệt vào `http://127.0.0.1:5000`.

---

## 9. Cấu trúc code (cho người muốn tuỳ biến thêm)

- `app.py` - toàn bộ route Flask (đăng ký, form, upload, khoá thời gian, admin)
- `db.py` - schema SQLite (vendors, quote_items, maintenance_items, files)
- `categories.py` - danh sách 20 danh mục YCBG (đã sửa đúng số lượng TB02=18, TB17=1 theo bản scan gốc)
- `export_excel.py` - sinh file Excel tổng hợp đúng cấu trúc đang dùng
- `templates/` - giao diện HTML (Bootstrap 5 qua CDN, không cần build gì thêm)
