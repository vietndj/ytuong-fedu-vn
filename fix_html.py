import json
import re

html_file = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@nathanael.lct_DdRg_ybtlKI.html"
with open(html_file, "r") as f:
    html = f.read()

# Replace main title
html = html.replace("Nathanael • Thử Thách Phối Đồ Thu Dưới €150 &amp; Kỹ Thuật Hook 3s Đổi Outfit Siêu Tốc", "Nathanael • Kỹ Thuật Kể Chuyện 'How I Shop vs How I Style' Thu Hút Khách Hàng Zalando")
html = html.replace("Nathanael • Thử Thách Phối Đồ Thu Dưới €150 & Kỹ Thuật Hook 3s Đổi Outfit Siêu Tốc", "Nathanael • Kỹ Thuật Kể Chuyện 'How I Shop vs How I Style' Thu Hút Khách Hàng Zalando")

# Replace repeating title in grid and timeline
html = re.sub(r'Phân Cảnh (\d+) • Thử Thách Phối Đồ Thu Dưới €150.*?Siêu Tốc', r'Phân Cảnh \1 • Hành Trình Từ Giỏ Hàng Đến Phong Cách', html)

# Fix SHOTS_DATA array
import ast

match = re.search(r'const SHOTS_DATA = (\[.*?\]);', html)
if match:
    shots_str = match.group(1)
    shots = json.loads(shots_str)
    for i, shot in enumerate(shots):
        shot["headline"] = f"Phân Cảnh 0{i+1} • Hành Trình Từ Giỏ Hàng Đến Phong Cách"
        shot["subject_action"] = "Thể hiện quá trình mua sắm từ lúc mở ví, lướt laptop đến khi diện trang phục ra phố tự tin với dòng chữ 'HOW I SHOP' và 'HOW I STYLE'."
        shot["pros"] = "Điểm sáng: Phân tách rõ 2 giai đoạn tạo sự mạch lạc, sử dụng góc máy POV khi mua sắm tạo sự gần gũi."
        shot["cons"] = "Lưu ý: Không có điểm trừ đáng kể."
        shot["takeaway"] = "Hãy kể câu chuyện mua sắm thay vì chỉ trưng bày quần áo. Thêm quá trình 'Thêm vào giỏ hàng' giúp định hướng hành vi."
        
    new_shots_str = json.dumps(shots, ensure_ascii=False)
    html = html[:match.start(1)] + new_shots_str + html[match.end(1):]

with open(html_file, "w") as f:
    f.write(html)
print("Fixed HTML report.")
