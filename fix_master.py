import json
import os

path = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/master_classifications.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for k in list(data.keys()):
    if "Dcbn7Bix-X-" in k:
        entry = data[k]
        entry["title"] = "Kỹ thuật Match Cut & VFX Dịch chuyển không gian"
        entry["shooting_style"] = {
            "id": "chuyen-canh",
            "name": "Chuyển Cảnh & Hiệu Ứng",
            "icon": "🎬"
        }
        entry["industry"] = {
            "id": "du-lich",
            "name": "Du Lịch & Hàng Không",
            "icon": "✈️"
        }
        entry["purpose"] = "Phân tích cú Match Cut không gian ấn tượng của Caleb Natale"
        entry["tech_tags"] = [
            "Match Cut",
            "VFX Transition",
            "In-Camera Effects",
            "Wipe Transition"
        ]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated master_classifications.json")
