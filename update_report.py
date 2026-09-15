import re

html_path = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@genya_jp_Dc3PgRbBp-m.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Title
content = content.replace("Khám Phá Ẩm Thực Vùng Núi Hakone & Nghệ Thuật Quay Đồ Ăn Xúc Giác Nóng Hổi", "Food Vlog Cận Cảnh Biểu Cảm Tận Hưởng Ẩm Thực Tự Nhiên & Chân Thực")
content = content.replace("Mẫu video ẩm thực xúc giác: Bắt trọn làn khói bốc nghi ngút bằng ánh sáng ngược và cú gắp chậm rãi.", "Showcase ẩm thực tập trung hoàn toàn vào biểu cảm khuôn mặt khi ăn, truyền tải độ ngon qua sự thỏa mãn chân thực")

# Shots data
shots_data = [
    {
        "desc": "Genya ngồi tại bàn gỗ, mỉm cười rạng rỡ nhìn thẳng vào ống kính trước khay đồ ăn Nhật (tonkatsu, cơm).",
        "pro": "Điểm sáng: Giao tiếp bằng mắt (eye-contact) trực tiếp với người xem tạo cảm giác thân thiện, gần gũi như đang ăn cùng bạn.",
        "con": "Lưu ý: Không có",
        "takeaway": "Nụ cười rạng rỡ trước khi ăn thiết lập không khí vui vẻ và kết nối cảm xúc mạnh mẽ với khán giả."
    },
    {
        "desc": "Góc quay ngang tầm mắt, anh gắp miếng tonkatsu đưa vào miệng, nhắm mắt lại để tập trung tận hưởng hương vị.",
        "pro": "Điểm sáng: Biểu cảm nhắm mắt khi đưa thức ăn vào miệng rất tự nhiên, phóng đại được cảm giác ngon miệng.",
        "con": "Lưu ý: Khung hình hơi thiếu sáng ở phần background, nhưng lại giúp chủ thể nổi bật hơn.",
        "takeaway": "Biểu cảm nhắm mắt tận hưởng có sức mạnh kích thích vị giác người xem hơn bất kỳ kỹ xảo hình ảnh nào."
    },
    {
        "desc": "Vẫn giữ khung hình cận cảnh, anh đang nhai thức ăn với vẻ mặt cực kỳ mãn nguyện.",
        "pro": "Điểm sáng: Focus hoàn toàn vào khuôn mặt đang nhai, không bị phân tán bởi các yếu tố khác.",
        "con": "Lưu ý: Chuyển động nhai nếu quá dài có thể làm giảm nhịp độ video.",
        "takeaway": "Hãy để người xem thấy sự thay đổi cảm xúc trên khuôn mặt khi thức ăn tan trong miệng."
    },
    {
        "desc": "Anh tiếp tục gắp cơm trắng đưa lên, chuẩn bị ăn kèm, mắt vẫn lim dim vì ngon.",
        "pro": "Điểm sáng: Hành động gắp cơm liên tục tạo nhịp điệu ăn uống chân thực (food pairing).",
        "con": "Lưu ý: Bát cơm hơi che mất một phần dưới khuôn mặt.",
        "takeaway": "Thể hiện sự liên tục trong hành động ăn uống giúp video không bị đứt gãy mạch cảm xúc."
    },
    {
        "desc": "Chuyển cảnh sang bối cảnh quán cafe nhìn ra rừng cây xanh. Genya mỉm cười dùng thìa xúc món bánh matcha tiramisu.",
        "pro": "Điểm sáng: Sự thay đổi bối cảnh đột ngột (từ trong nhà tối sang không gian mở sáng sủa) làm mới thị giác người xem.",
        "con": "Lưu ý: Match cut chuyển cảnh chưa thực sự mượt về mặt thị giác do khác biệt lớn về màu sắc.",
        "takeaway": "Thay đổi bối cảnh là cách giữ chân người xem tốt nhất khi nội dung chủ đạo chỉ xoay quanh việc ăn uống."
    },
    {
        "desc": "Cận cảnh Genya nhắm nghiền mắt, tận hưởng vị ngọt của món tráng miệng.",
        "pro": "Điểm sáng: Lặp lại công thức thành công: góc máy ngang mắt + biểu cảm nhắm mắt tận hưởng cực độ.",
        "con": "Lưu ý: Không có",
        "takeaway": "Sự đồng nhất về phong cách quay (cận cảnh biểu cảm) tạo nên đặc trưng riêng cho chuỗi video vlog ẩm thực."
    }
]

# We need to replace the blocks sequentially
block_desc_pattern = r'<div class="block-text">.*?</div>'
block_pro_pattern = r'<div class="side-content">Điểm sáng thị giác:.*?</div>'
block_con_pattern = r'<div class="side-content">Lưu ý:.*?</div>'
block_takeaway_pattern = r'<div class="takeaway-text">.*?</div>'

# We'll split the content by '<h2 class="shot-headline">' to process each shot
parts = content.split('<h2 class="shot-headline">')
new_parts = [parts[0]]

for i in range(1, 7): # We have 6 shots
    if i < len(parts):
        part = parts[i]
        shot = shots_data[i-1]
        
        part = re.sub(block_desc_pattern, f'<div class="block-text">{shot["desc"]}</div>', part, count=1)
        part = re.sub(block_pro_pattern, f'<div class="side-content">{shot["pro"]}</div>', part, count=1)
        part = re.sub(block_con_pattern, f'<div class="side-content">{shot["con"]}</div>', part, count=1)
        part = re.sub(block_takeaway_pattern, f'<div class="takeaway-text">{shot["takeaway"]}</div>', part, count=1)
        
        new_parts.append(part)

# If there were extra shots (7 and 8) in the dummy HTML, they will just be appended but we should remove them.
# The HTML structure has <!-- VISUAL GRID VIEW --> after the shots.
content = '<h2 class="shot-headline">'.join(new_parts)

# Let's remove shot 7 and 8 if they exist
# Actually, the file had 8 shots generated before. I should just cut off shot 7 and 8.
# Let's use regex to remove from <h2 class="shot-headline">Phân Cảnh 07 up to the grid view.
content = re.sub(r'<h2 class="shot-headline">Phân Cảnh 07.*?<!-- VISUAL GRID VIEW -->', '<!-- VISUAL GRID VIEW -->', content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated report HTML")
