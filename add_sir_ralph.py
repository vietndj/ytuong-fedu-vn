import json, os

MASTER_PATH = "master_classifications.json"

with open(MASTER_PATH, "r", encoding="utf-8") as f:
    master = json.load(f)

item = {
    "id": "IG_@sir.ralph_e_DavWS9Islv1_Chuyen_Canh",
    "shortcode": "DavWS9Islv1",
    "creator": "@sir.ralph_e",
    "creator_name": "Sir Ralph",
    "title": "Kỹ Thuật Chuyển Cảnh Sáng Tạo - @sir.ralph_e",
    "shots_count": 8,
    "duration": "15s",
    "shooting_style": {
        "id": "chuyen-canh",
        "name": "Chuyển Cảnh",
        "icon": "⚡"
    },
    "industry": {
        "id": "ky-thuat-quay",
        "name": "Kỹ Thuật Quay Dựng & Điện Ảnh",
        "icon": "🎯"
    },
    "country": {
        "id": "us_eu",
        "name": "Âu Mỹ",
        "en_name": "US & Europe",
        "flag": "🇺🇸/🇪🇺",
        "badge_color": "purple"
    },
    "purpose": "Hướng dẫn kỹ thuật chuyển cảnh mượt mà",
    "tech_tags": [
        "Chuyển cảnh Level 2",
        "Match Cut",
        "Transition"
    ],
    "transition_level": "Chuyển cảnh Level 2",
    "is_ad_bot": False,
    "logic_explanation": "Thực hiện hành động che ống kính hoặc lặp lại chuyển động để tạo cú nối cảnh.",
    "quick_takeaway": "Bài tập chuyển cảnh: Tận dụng đồ vật hoặc động tác cơ thể để che camera và nối nhịp nhàng sang bối cảnh khác.",
    "video_url": "https://media.fedu.vn/videos/DavWS9Islv1.mp4",
    "report_url": "reports/IG_@sir.ralph_e_DavWS9Islv1_Chuyen_Canh.html",
    "fedu_optimization": {
        "key_optimization_point": "⚡ Chuyển cảnh Level 2: Đặt máy lên chân máy (tripod), chuyển cảnh bằng hành động cơ thể rõ ràng lặp lại 2 lần",
        "practice_focus": "Bài tập Chuyển cảnh Level 2: Đặt máy chân máy cố định, thực hiện động tác vung tay ở hai bối cảnh để tạo match cut.",
        "ig_seeding_hook": "Follow @sir.ralph_e để học thêm các tip chuyển cảnh sáng tạo.",
        "course_industry_mapping": "Kỹ Thuật Chuyển Cảnh (Khóa học video.fedu.vn)"
    }
}

master[item["id"]] = item
master[item["shortcode"]] = item

with open(MASTER_PATH, "w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=2)

print("Added DavWS9Islv1 successfully!")
