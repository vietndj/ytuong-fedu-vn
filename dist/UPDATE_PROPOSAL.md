# Phương án Cập nhật Hệ thống

## 1. Hỗ trợ Nhiều Ngành Nghề (Dual Industry)
- **Kiến trúc DB**: Đổi trường `industry` (Object 1 ngành) thành `industries` (Array nhiều ngành).
- **Core Engine**: Cập nhật `build_ideas_bank.py` để tính toán thống kê song song cho các video có nhiều ngành.
- **AI Learner**: Dạy `feedback_learner.py` cách bóc tách chuỗi ngăn cách bằng dấu phẩy (VD: "Bố cục, Du lịch").
- **Giao diện (UI)**: Thẻ video sẽ hiển thị 2-3 badge ngành kề nhau. Khi lọc "Bố cục" hoặc "Du lịch", video đều sẽ xuất hiện.

## 2. Phân loại "Biểu cảm / Yếu tố ăn điểm" (X-Factor)
- Bổ sung thêm một bộ phân loại hoàn toàn mới: **Vũ khí ăn điểm (X-Factor)**, ngang hàng với "Kiểu quay" và "Mục đích".
- Ứng dụng thực tế: Phân loại Vlog không chỉnh chu nhưng có "Biểu cảm chân thật", "Biểu cảm ngạc nhiên", "Giọng nói điệu đà", "Hook gây sốc".
- Thêm trường `x_factors: []` vào CSDL và UI hiển thị một cụm "Điểm nhấn" riêng biệt ngay dưới kiểu quay.
