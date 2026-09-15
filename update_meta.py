import json

# Update master_classifications.json
with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/master_classifications.json', 'r') as f:
    master_data = json.load(f)

vid_id = "IG_@AL,_The_Creator_Videography_Reels_DdTeHleIqkg_Video_by_shogentle"
vid_id2 = "DdTeHleIqkg"
new_title = "@shogentle - Bí quyết Set up Ánh sáng Cinematic: Biến hóa không gian với đèn màu và Rim Light"
new_purpose = "Phân tích kỹ thuật đánh sáng điện ảnh (Lighting Setup) và cách sử dụng màu sắc (Color Gel/RGB) để tạo chiều sâu không gian."
new_takeaway = "Sử dụng độ tương phản cao (High Contrast) và nguồn sáng ven (Rim Light) để tách chủ thể khỏi nền, kết hợp đèn màu (Red/Teal) để tạo mood kịch tính ngay cả trong không gian hẹp."

if vid_id in master_data:
    master_data[vid_id]['title'] = new_title
    master_data[vid_id]['purpose'] = new_purpose
    master_data[vid_id]['quick_takeaway'] = new_takeaway
    master_data[vid_id]['industry'] = {"id": "ky-thuat-quay", "name": "Kỹ Thuật Quay Dựng", "icon": "🎥"}
if vid_id2 in master_data:
    master_data[vid_id2]['title'] = new_title
    master_data[vid_id2]['purpose'] = new_purpose
    master_data[vid_id2]['quick_takeaway'] = new_takeaway
    master_data[vid_id2]['industry'] = {"id": "ky-thuat-quay", "name": "Kỹ Thuật Quay Dựng", "icon": "🎥"}

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/master_classifications.json', 'w') as f:
    json.dump(master_data, f, indent=2, ensure_ascii=False)

# Update scene.html portalData
scene_path = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/scene.html'
with open(scene_path, 'r') as f:
    scene_html = f.read()

import re
# Regex to replace the title_vi
scene_html = re.sub(r'("id":\s*"IG_@AL,_The_Creator_Videography_Reels_DdTeHleIqkg_Video_by_shogentle",\s*"folder_name":\s*"[^"]+",\s*"title_vi":\s*")[^"]+(")', r'\g<1>' + new_title + r'\g<2>', scene_html)

with open(scene_path, 'w') as f:
    f.write(scene_html)

print("Updated master_classifications.json and scene.html")
