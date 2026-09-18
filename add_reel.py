import json

with open("master_classifications.json", "r", encoding="utf-8") as f:
    data = json.load(f)

new_id = "IG_@marcoandredasilva_DZp2Sres0SD_Chuyen_Canh_Cap_2"

if new_id not in data:
    # try to figure out highest index
    highest_index = max([v.get("index", 0) for v in data.values()]) if data else 0
    
    data[new_id] = {
        "id": new_id,
        "index": highest_index + 1,
        "creator": "@marcoandredasilva",
        "creator_name": "Marco Andre Da Silva",
        "title": "Chuyển Cảnh Cấp 2 - @marcoandredasilva",
        "shots_count": 5,
        "duration": "15s",
        "shooting_style": {
            "id": "chuyen-canh",
            "name": "Chuyển Cảnh",
            "icon": "⚡"
        },
        "industry": {
            "id": "ky-thuat-quay",
            "name": "Kỹ Thuật Quay Dựng & Điện Ảnh",
            "icon": "🎬"
        },
        "purpose": "Trình diễn chuyển cảnh mượt mà",
        "tech_tags": [
            "Chuyển cảnh cấp 2"
        ],
        "logic_explanation": "Kỹ thuật chuyển cảnh cấp 2 tinh tế và mượt mà.",
        "is_excluded": False,
        "quick_takeaway": "Điểm nhấn: chuyển cảnh cấp 2",
        "country": {
            "id": "us_eu",
            "name": "Âu Mỹ",
            "en_name": "US & Europe",
            "flag": "🇺🇸/🇪🇺",
            "badge_color": "purple"
        },
        "transition_level": "Chuyển Cảnh Cấp 2",
        "is_ad_bot": False,
        "fedu_optimization": {
            "key_optimization_point": "Điểm nhấn: chuyển cảnh cấp 2"
        },
        "url": "https://www.instagram.com/marcoandredasilva/reel/DZp2Sres0SD/"
    }
    
    with open("master_classifications.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Added successfully!")
else:
    print("Already exists.")
