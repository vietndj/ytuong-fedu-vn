import json
import re

json_path = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/master_classifications.json"
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

vid = "IG_@genya_jp_Dc3PgRbBp-m"
if vid in data:
    data[vid]["title"] = "Genya • Food Vlog Cận Cảnh Biểu Cảm Tận Hưởng Ẩm Thực Tự Nhiên & Chân Thực"
    data[vid]["shots_count"] = 6
    data[vid]["duration"] = "18.38s"
    data[vid]["purpose"] = "Showcase ẩm thực tập trung hoàn toàn vào biểu cảm khuôn mặt khi ăn, truyền tải độ ngon qua sự thỏa mãn chân thực"
    data[vid]["tech_tags"] = ["Authentic Eating Expression", "Eye-level Food Review", "Natural Cafe Lighting", "Taste Reaction B-Roll"]
    data[vid]["logic_explanation"] = "Kỹ thuật quay ngang tầm mắt (Eye-level) kết hợp với ánh sáng tự nhiên và trung cảnh (Medium shot). Thay vì quay cận đồ ăn, máy quay khóa chặt vào biểu cảm tận hưởng của người ăn (nhắm mắt, mỉm cười) để kích thích vị giác người xem."
    data[vid]["quick_takeaway"] = "Không cần quay đồ ăn quá cầu kỳ, chính biểu cảm thỏa mãn và chân thực của người ăn mới là thứ thuyết phục người xem nhất."
    data[vid]["fedu_optimization"]["key_optimization_point"] = "⚡ Không cần quay đồ ăn quá cầu kỳ, chính biểu cảm thỏa mãn và chân thực của người ăn mới là thứ thuyết phục người xem nhất."
    data[vid]["fedu_optimization"]["practice_focus"] = "Thực hành: Đặt máy quay ngang tầm mắt, lấy nét vào khuôn mặt người ăn. Yêu cầu diễn viên ăn thật, nhắm mắt cảm nhận và mỉm cười tự nhiên."
    
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated master_classifications.json")

# Update scene.html
scene_path = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/scene.html"
with open(scene_path, 'r', encoding='utf-8') as f:
    scene_text = f.read()

# Replace title, desc, key_tech, thumbnails
scene_text = re.sub(
    r'"title_vi": "Genya • Khám Phá Ẩm Thực Vùng Núi Hakone & Nghệ Thuật Quay Đồ Ăn Xúc Giác Nóng Hổi"',
    r'"title_vi": "Genya • Food Vlog Cận Cảnh Biểu Cảm Tận Hưởng Ẩm Thực Tự Nhiên & Chân Thực"',
    scene_text
)
scene_text = re.sub(
    r'"desc_vi": "Mẫu video ẩm thực xúc giác: Bắt trọn làn khói bốc nghi ngút bằng ánh sáng ngược và cú gắp chậm rãi."',
    r'"desc_vi": "Mẫu video review ẩm thực: Truyền tải độ ngon món ăn thông qua biểu cảm nhắm mắt thỏa mãn và nụ cười chân thực của người trải nghiệm."',
    scene_text
)
scene_text = re.sub(
    r'"key_tech": "Ẩm Thực & F&B • Food Macro Glaze • Steam Capture Lighting • Chopstick Lift Action • Warm Wooden Background"',
    r'"key_tech": "Ẩm Thực & F&B • Authentic Eating Expression • Eye-level Food Review • Natural Cafe Lighting • Taste Reaction B-Roll"',
    scene_text
)
scene_text = re.sub(
    r'"shots_count": 8,',
    r'"shots_count": 6,',
    scene_text
)
scene_text = re.sub(
    r'"duration": "25.0s",',
    r'"duration": "18.38s",',
    scene_text
)

with open(scene_path, 'w', encoding='utf-8') as f:
    f.write(scene_text)

print("Updated scene.html")

