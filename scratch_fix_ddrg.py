import json
import re

# 1. Update master_classifications.json
master_file = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/master_classifications.json"
with open(master_file, "r") as f:
    master_data = json.load(f)

vid_id = "IG_@nathanael.lct_DdRg_ybtlKI"

if vid_id in master_data:
    entry = master_data[vid_id]
    entry["title"] = "Nathanael • Kỹ Thuật Kể Chuyện 'How I Shop vs How I Style' Thu Hút Khách Hàng"
    entry["purpose"] = "Mẫu video UGC thương mại thời trang kết hợp định dạng Storytelling (Mua sắm & Phối đồ)"
    entry["tech_tags"] = ["How I Shop", "How I Style", "Lookbook", "Lifestyle", "Zalando Commercial"]
    entry["logic_explanation"] = "Tạo sự đồng cảm bằng cách chia video làm 2 giai đoạn: Giai đoạn 1 (How I Shop) thể hiện hành vi mua sắm online thực tế (ví, laptop, giỏ hàng). Giai đoạn 2 (How I Style) phô diễn thành quả phối đồ tự tin trên phố."
    entry["quick_takeaway"] = "Đừng chỉ show quần áo, hãy kể câu chuyện quá trình sở hữu nó. Việc thêm phân cảnh 'How I Shop' (thêm vào giỏ hàng) giúp định hướng hành vi mua sắm của người xem một cách tự nhiên."
    entry["fedu_optimization"]["key_optimization_point"] = "⚡ " + entry["quick_takeaway"]
    entry["fedu_optimization"]["practice_focus"] = "Thực hành: Quay 2-3 shot mô tả quá trình lướt web/thêm vào giỏ hàng trước khi chuyển cảnh sang kết quả mặc trên người. Đặt chữ 'How I Shop' và 'How I Style' để neo giữ sự chú ý."
    
with open(master_file, "w") as f:
    json.dump(master_data, f, indent=2, ensure_ascii=False)

# 2. Update scene.html (we can just call build_ideas_bank.py later or update scene.html portalData directly)
scene_file = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/scene.html"
with open(scene_file, "r") as f:
    scene_content = f.read()

# Replace in scene_content (using regex to find the object)
# It's better to just let build_ideas_bank.py handle scene.html if it builds from master? 
# Wait, build_ideas_bank.py builds ideas_data.js FROM scene.html! So scene.html is the source of truth for YTUONG Hub.
