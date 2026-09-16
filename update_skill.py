import re

with open("/Users/vietmac/.gemini/config/skills/analyze-video/SKILL.md", "r") as f:
    content = f.read()

new_block = """  - **TỰ ĐỘNG ĐỒNG BỘ VÀO KHO Ý TƯỞNG YTUONG HUB**:
    - **Nguyên tắc bắt buộc**: Đọc và hiểu sâu nội dung video thực tế trước khi phân loại (nếu là spa, thẩm mỹ, y khoa Before/After da mụn -> BẮT BUỘC vào `💆 Làm Đẹp & Spa / Y Tế` + `🚶 Walk and Talk` / `🗣️ Talking Head`, tuyệt đối không để dính bẫy từ khóa hay fallback mù quáng vào Kiến Trúc).
    - Phân loại chuẩn xác theo Ma trận 4 trục:
      1. **Kiểu quay**: Walk and Talk, Voice Over, Talking Head, Storytelling, Điện Ảnh, Chuyển Cảnh.
      2. **Ngành nghề**: 9 ngành cốt lõi (Làm Đẹp & Spa / Y Tế, Thương Hiệu Cá Nhân & Dịch Vụ, Thời Trang, Ẩm Thực, Du Lịch, Công Nghệ, Kiến Trúc, Thể Thao, Kỹ Thuật Quay Dựng, UGC).
      3. **Kỹ thuật & Mục đích**: Xác định rõ mục đích (Bán hàng/Flash Sale, Hướng dẫn/Tips, Kỷ luật/Cảm hứng, Showcase, Vlog) và kỹ thuật nổi bật.
    - **TUYỆT ĐỐI BẮT BUỘC: VIẾT LẠI VĂN PHONG "ĐIỂM HAY NHẤT" (💡) VÀ "THỰC CHIẾN" (🎯)**
      Khi cập nhật `master_classifications.json`, phần `key_optimization_point` (Icon 💡) và `practice_focus` (Icon 🎯) BẮT BUỘC phải tuân thủ chuẩn "văn phong mộc mạc" 1-chạm của anh Việt:
      - **KHÔNG DÙNG TỪ NGỮ AI/FLUFF**: Loại bỏ hoàn toàn các từ sáo rỗng như *cuốn hút, tuyệt đối, đẳng cấp, nghệ thuật, hoàn hảo, sức mạnh, neo giữ*.
      - **💡 Icon Bóng Đèn (`key_optimization_point`)**: Bắt đầu bằng dấu `⚡` + [Hành động kỹ thuật] + [Kết quả thị giác trực tiếp].
        *Ví dụ chuẩn: "⚡ Dùng hook treo máy thẳng đứng trong studio chặn feed ➔ Chuyển cảnh lật ngược máy lấy bóng nước."*
      - **🎯 Icon Hồng Tâm (`practice_focus`)**: Bắt đầu bằng `⚡ Thực chiến:` + [Thao tác tay/Góc máy cụ thể] + [Mục đích].
        *Ví dụ chuẩn: "⚡ Thực chiến: Dí sát ống kính (Macro Detail) bắt vân bề mặt, xoay tay máy chậm kết hợp ánh sáng chéo để nổi khối 3D."*"""

pattern = r"  - \*\*TỰ ĐỘNG ĐỒNG BỘ VÀO KHO Ý TƯỞNG YTUONG HUB\*\*:.*?3\. \*\*Kỹ thuật & Mục đích\*\*: Xác định rõ mục đích \(Bán hàng/Flash Sale, Hướng dẫn/Tips, Kỷ luật/Cảm hứng, Showcase, Vlog\) và kỹ thuật nổi bật\."

content = re.sub(pattern, new_block, content, flags=re.DOTALL)

with open("/Users/vietmac/.gemini/config/skills/analyze-video/SKILL.md", "w") as f:
    f.write(content)

print("Updated SKILL.md successfully.")
