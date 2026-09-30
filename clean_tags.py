import json
import os

MASTER_PATH = "master_classifications.json"
BACKUP_PATH = "master_classifications.json.bak"

# Từ điển chuẩn hóa
MAPPING = {
    # 1. Điện Ảnh / Chỉn Chu (dien-anh)
    "Điện Ảnh (Cinematic)": "dien-anh",
    "Chỉn Chu": "dien-anh",
    "dien-anh": "dien-anh",
    "Phim Điện Ảnh (Cinematic Stills)": "dien-anh",
    "Cinematic": "dien-anh",
    "Cinematic B-Roll": "dien-anh",
    "B-Roll Điện Ảnh": "dien-anh",
    "Quay B-Roll Quảng Cáo Điện Ảnh": "dien-anh",
    "Cinematic B-roll": "dien-anh",
    "Vlog Lifestyle / B-Roll Điện Ảnh": "dien-anh",
    "Cinematic Vlog": "dien-anh",
    "Cinematic Vlog / Cut On Action": "dien-anh",
    "Cinematic / Đời thường": "dien-anh",
    "Điện Ảnh Đời Thường (Cinematic)": "dien-anh",
    "Điện Ảnh & Chữa Lành (Cinematic Mood / ASMR)": "dien-anh",
    "lifestyle-cinematic": "dien-anh",
    "Vlog": "dien-anh",
    "goc-may-sang-tao": "dien-anh",
    "Chỉn Chu / Bố Cục": "dien-anh",
    "Bố Cục (Framing)": "dien-anh",
    "POV & Aesthetic B-Roll Montage": "dien-anh",

    # 2. Chuyển Cảnh (chuyen-canh)
    "Chuyển Cảnh (Transition)": "chuyen-canh",
    "chuyen-canh": "chuyen-canh",
    "Chuyển Cảnh (In-Camera Transitions)": "chuyen-canh",
    "Chuyển Cảnh Thời Trang (OOTD Transition)": "chuyen-canh",
    "Chuyển Cảnh & Nhịp Dựng Nhanh (Fast-Cut Beat Sync)": "chuyen-canh",
    "chuyen_canh": "chuyen-canh",
    "bien-hinh": "chuyen-canh",
    "Chuyển Cảnh / Biến Hình": "chuyen-canh",
    "Chuyển Cảnh & Diễn Xuất": "chuyen-canh",
    "Chuyển Cảnh (Transitions)": "chuyen-canh",
    "Chuyển Cảnh & Dựng Nhanh (Transition / Speed Ramp)": "chuyen-canh",
    "POV Dynamic / Biến Hình": "chuyen-canh",
    "Vlog 0.5x POV Montage": "chuyen-canh",
    "POV & Fast-Paced Montage": "chuyen-canh",

    # 3. Nói Trực Diện (talking-head)
    "Talking Head": "talking-head",
    "Nói Trực Diện (Talking Head)": "talking-head",
    "Nói Trực Diện": "talking-head",
    "Nói Chuyện Trực Diện (Talking Head & B-roll)": "talking-head",
    "Talking Head & Hướng Dẫn": "talking-head",

    # 4. Kể Chuyện (storytelling)
    "Storytelling": "storytelling",
    "Kể Chuyện (Storytelling)": "storytelling",
    "storytelling": "storytelling",
    "Đời Thường & Chữa Lành": "storytelling",
    "Kể Chuyện": "storytelling",
    "doi-thuong": "storytelling",
    "A Day In The Life (Vlog Không Lời)": "storytelling",
    "Visual Storytelling": "storytelling",

    # 5. Lồng Tiếng (voice-over)
    "Voice Over": "voice-over",
    "Lồng Tiếng (Voice Over)": "voice-over",

    # 6. Walk and Talk (walk-and-talk)
    "Walk and Talk": "walk-and-talk",
    "Walk and Talk Documentary": "walk-and-talk",
    "Walk & Talk / Runway Catwalk (One-Take Plan-Séquence)": "walk-and-talk",
    "Walk & Talk / Phỏng Vấn": "walk-and-talk",
    "Vừa Đi Vừa Nói & Campus Tour (Walk & Talk)": "walk-and-talk",
    "pov": "walk-and-talk",

    # 7. Nhịp nhạc (theo-nhip-nhac)
    "Beat-Match Cut & Vũ Đạo": "theo-nhip-nhac",

    # 8. Hậu Trường / Setup (bts) - Tạo mới!
    "BTS / Hậu Trường Sáng Tạo": "bts",
    "Split Screen / Behind-The-Scenes": "bts",
    "Kỹ Thuật Quay & Setup Solo": "bts",
    "Kỹ Thuật Quay & Dụng Cụ Gá Đỡ": "bts",
    "Solo Creator Setup": "bts",

    # Những cái sai lệch (nên là Industry nhưng đang bị kẹt ở Style) => Tạm map về style phù hợp nhất
    "san-pham": "dien-anh",
    "quang-cao": "dien-anh",
    "Review Sản Phẩm / UGC": "talking-head",
    "UGC Thực Chiến": "walk-and-talk",
    "UGC & Trình Diễn Sản Phẩm": "dien-anh",
    "Lookbook Thực Chiến": "dien-anh"
}

def clean_data():
    if not os.path.exists(MASTER_PATH):
        print(f"Error: {MASTER_PATH} not found.")
        return

    # Backup
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Backed up to {BACKUP_PATH}")

    changes = 0
    for vid_id, item in data.items():
        if "shooting_style" in item:
            style = item["shooting_style"]
            if isinstance(style, dict):
                style_name = style.get("name", "")
            else:
                style_name = str(style)
            
            # Xử lý các case không khớp hoàn toàn
            matched_id = None
            for key, val in MAPPING.items():
                if style_name.strip() == key:
                    matched_id = val
                    break
            
            # Nếu có map, gán lại thành chuỗi ID chuẩn (vd: 'dien-anh') 
            # build_ideas_bank.py có thể xử lý ID dạng chuỗi (dòng 450)
            if matched_id:
                if item["shooting_style"] != matched_id:
                    item["shooting_style"] = matched_id
                    changes += 1
            else:
                # In ra những cái chưa được map
                if style_name not in MAPPING.values():
                    print(f"UNMAPPED: '{style_name}' in {vid_id}")
                    # Chuyển thành lowercase slug-like id
                    slug = style_name.lower().replace(" ", "-").replace("/", "-")
                    # Fallback to dien-anh
                    item["shooting_style"] = "dien-anh"
                    changes += 1

    with open(MASTER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Thành công! Đã cập nhật {changes} tags.")

if __name__ == "__main__":
    clean_data()
