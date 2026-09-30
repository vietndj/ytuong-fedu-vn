# Phân tích và Kế hoạch Tối ưu Kho Tag

## 1. Phân tích nguyên nhân "Lộn xộn" của Tag

Dựa vào mã nguồn của `build_ideas_bank.py` và dữ liệu trong `master_classifications.json`, nguyên nhân dẫn đến tình trạng các tag bị rác và lộn xộn bao gồm:

1. **Cơ chế thêm Tag Động (Dynamic Tag Append):** Trong `build_ideas_bank.py`, khi phân tích dữ liệu từ `master_classifications.json`, nếu phát hiện một ID tag chưa có trong danh sách chuẩn (7 kiểu quay gốc), hệ thống sẽ **tự động thêm tag đó vào danh sách hiển thị** trên UI.
2. **Dữ liệu thô từ AI/Người dùng bị phân mảnh:** Dữ liệu trong `master_classifications.json` chứa rất nhiều biến thể văn bản tự do (Free-text) cho cùng một ý nghĩa. Ví dụ:
   - `Điện Ảnh (Cinematic)`, `Chỉn Chu`, `dien-anh`, `Cinematic B-Roll`, `Cinematic Vlog`, `B-Roll Điện Ảnh`... (có đến hơn 20 biến thể khác nhau).
   - `Chuyển Cảnh (Transition)`, `chuyen-canh`, `Chuyển Cảnh Thời Trang (OOTD Transition)`, `bien-hinh`...
3. **Nhầm lẫn giữa Trục Nội dung và Trục Kiểu quay:** Một số tag như `Solo Creator Setup`, `BTS / Hậu Trường Sáng Tạo`, `Lookbook Thực Chiến` mang ý nghĩa về *Chủ đề/Ngành (Industry/Purpose)* nhưng lại bị lưu nhầm vào trường `shooting_style` (Kiểu quay).

## 2. Kế hoạch Tối ưu & Dọn dẹp (Tag Cleanup Plan)

Để giải quyết dứt điểm, chúng ta cần thực hiện quy trình 3 bước chuẩn hóa (ETL):

### Bước 1: Xây dựng Từ điển Chuẩn hóa (Mapping Dictionary)
Nhóm toàn bộ 60+ biến thể rác thành 7-8 nhóm chuẩn.
- **Điện Ảnh / Chỉn Chu:** Gom toàn bộ `Cinematic Vlog`, `B-Roll`, `Chỉn Chu`...
- **Chuyển Cảnh:** Gom `Transition`, `bien-hinh`, `OOTD Transition`...
- **Nói Trực Diện:** Gom `Talking Head`, `Talking Head & Hướng Dẫn`...
- **Kể Chuyện:** Gom `Storytelling`, `Đời thường & Chữa lành`...
- **Walk & Talk:** Gom `POV`, `Campus Tour`, `Walk and Talk`...
- **Hậu Trường & Setup:** (Tạo riêng một tag chuẩn mới cho `BTS / Setup Solo` vì lượng video dạng này khá nhiều và có giá trị cao).

### Bước 2: Chạy Script Chuẩn hóa Data gốc
- Viết một script Python tên `clean_tags.py`.
- Script này sẽ đọc `master_classifications.json`, quét qua toàn bộ thuộc tính `shooting_style`, đối chiếu với từ điển và **ghi đè lại bằng chuẩn ID thống nhất**.

### Bước 3: Build lại UI và Khớp Data
- Cập nhật file `build_ideas_bank.py` để bổ sung ID `bts` (Hậu trường) vào mảng `SHOOTING_STYLES` gốc nhằm đảm bảo UI render đẹp và có icon phù hợp.
- Chạy lại lệnh `python3 build_ideas_bank.py` để xuất ra `ideas_data.js` sạch sẽ.
- Kiểm tra lại các file giao diện (UI) xem đã gom nhóm chuẩn xác chưa.
