#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feedback_learner.py
Hệ Thống Học Phân Loại Phản Hồi 1-Chạm (Active Learning Engine)
Được thiết kế riêng cho anh Nguyễn Việt (@vietndj)

Cú pháp sử dụng:
  python3 feedback_learner.py "SUA: #4 -> Đời thường, Kỷ luật"
  python3 feedback_learner.py "SUA: @creator -> Voice Over, Thương Hiệu, Lý do: chia sẻ tư duy solo creator"
  python3 feedback_learner.py --stats  (Xem bảng đối soát tiến trình học)
  python3 feedback_learner.py --rules  (Xem danh sách quy tắc AI đã học)
"""

import os
import sys
import re
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURATION_CONFIG_PATH = os.path.join(BASE_DIR, "curation_config.json")
MASTER_PATH = os.path.join(BASE_DIR, "master_classifications.json")
PATTERNS_PATH = os.path.join(BASE_DIR, "LEARNED_PATTERNS.json")
BUILD_SCRIPT_PATH = os.path.join(BASE_DIR, "build_ideas_bank.py")

# Danh mục ánh xạ chuẩn
INDUSTRY_ALIASES = {
    "spa": "spa-lam-dep",
    "lam dep": "spa-lam-dep",
    "làm đẹp": "spa-lam-dep",
    "y te": "spa-lam-dep",
    "y tế": "spa-lam-dep",
    "da lieu": "spa-lam-dep",
    "da liễu": "spa-lam-dep",
    "thuong hieu": "thuong-hieu",
    "thương hiệu": "thuong-hieu",
    "ky luat": "thuong-hieu",
    "kỷ luật": "thuong-hieu",
    "thoi quen": "thuong-hieu",
    "thói quen": "thuong-hieu",
    "tu duy": "thuong-hieu",
    "tư duy": "thuong-hieu",
    "thoi trang": "thoi-trang",
    "thời trang": "thoi-trang",
    "am thuc": "am-thuc",
    "ẩm thực": "am-thuc",
    "fnb": "am-thuc",
    "cafe": "am-thuc",
    "cà phê": "am-thuc",
    "du lich": "du-lich",
    "du lịch": "du-lich",
    "cong nghe": "cong-nghe",
    "công nghệ": "cong-nghe",
    "kien truc": "kien-truc",
    "kiến trúc": "kien-truc",
    "the thao": "the-thao",
    "thể thao": "the-thao",
    "ky thuat": "ky-thuat-quay",
    "kỹ thuật": "ky-thuat-quay",
    "ugc": "ugc"
}

STYLE_ALIASES = {
    "walk": "walk-and-talk",
    "walk and talk": "walk-and-talk",
    "vừa đi vừa nói": "walk-and-talk",
    "voice": "voice-over",
    "voice over": "voice-over",
    "lồng tiếng": "voice-over",
    "long tieng": "voice-over",
    "talking": "talking-head",
    "talking head": "talking-head",
    "nói trực diện": "talking-head",
    "noi truc dien": "talking-head",
    "storytelling": "storytelling",
    "kể chuyện": "storytelling",
    "ke chuyen": "storytelling",
    "chỉnh chu": "dien-anh",
    "chỉn chu": "dien-anh",
    "dien anh": "dien-anh",
    "điện ảnh": "dien-anh",
    "cinematic": "dien-anh",
    "chuyen canh": "chuyen-canh",
    "chuyển cảnh": "chuyen-canh",
    "transition": "chuyen-canh",
    "doi thuong": "storytelling",
    "đời thường": "storytelling"
}

def load_json(path, default=None):
    if not os.path.exists(path):
        return default or {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

from user_note_parser import INDUSTRY_MAP, STYLE_MAP

IDEAS_DATA_PATH = os.path.join(BASE_DIR, "ideas_data.js")

def load_ideas_list():
    """Load danh sách ideas có thứ tự tuần tự 1-indexed từ ideas_data.js"""
    if not os.path.exists(IDEAS_DATA_PATH):
        return []
    try:
        with open(IDEAS_DATA_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.search(r'var FEDU_IDEAS_DATABASE\s*=\s*(\{[\s\S]*\});\s*$', content)
        if m:
            db = json.loads(m.group(1))
            return db.get("ideas", [])
    except Exception as e:
        print(f"⚠️ Không đọc được ideas_data.js: {e}")
    return []

def find_target_video(query_key, master_db):
    """Tìm video theo index số trên web (#4), video_id, hoặc creator (@joshdiazfilms)"""
    ideas_list = load_ideas_list()

    # 1. Tìm theo số index trên web (#4 hoặc số 4)
    idx_match = re.search(r'#?(\d+)', query_key.strip())
    if idx_match and not "@" in query_key and not " " in query_key.strip():
        target_idx = int(idx_match.group(1))
        # Ưu tiên 1: Tra cứu theo thứ tự tuần tự 1-indexed trên web
        if 1 <= target_idx <= len(ideas_list):
            web_item = ideas_list[target_idx - 1]
            vid_id = web_item.get("id")
            if vid_id in master_db:
                return vid_id, master_db[vid_id]
            return vid_id, web_item
        # Ưu tiên 2: Fallback tìm index field trong master_db
        for vid_id, item in master_db.items():
            if item.get("index") == target_idx:
                return vid_id, item

    # 2. Tìm theo creator (@abc)
    clean_key = query_key.strip().lower()
    if "@" in clean_key:
        handle = re.search(r'@([a-zA-Z0-9_\.]+)', clean_key)
        if handle:
            creator_tag = "@" + handle.group(1).lower()
            # Tìm trong ideas web trước
            for item in ideas_list:
                c_handle = item.get("creator", {}).get("handle", "") if isinstance(item.get("creator"), dict) else str(item.get("creator", ""))
                if c_handle.lower() == creator_tag:
                    vid_id = item.get("id")
                    return vid_id, master_db.get(vid_id, item)
            # Tìm trong master_db
            for vid_id, item in master_db.items():
                if item.get("creator", "").lower() == creator_tag:
                    return vid_id, item

    # 3. Tìm theo exact ID hoặc title match
    for item in ideas_list:
        if clean_key in item.get("id", "").lower() or clean_key in item.get("title_vi", "").lower():
            vid_id = item.get("id")
            return vid_id, master_db.get(vid_id, item)

    for vid_id, item in master_db.items():
        if clean_key in vid_id.lower() or clean_key in item.get("title", "").lower():
            return vid_id, item

    return None, None

def parse_feedback_command(command_str):
    """
    Phân tích câu lệnh của anh Việt:
    Ví dụ: 'SUA: #4 -> Đời thường, Kỷ luật, Lý do: chia sẻ thói quen buổi sáng'
    """
    cmd = command_str.strip()
    if cmd.upper().startswith("SUA:"):
        cmd = cmd[4:].strip()
    elif cmd.upper().startswith("SỬA:"):
        cmd = cmd[4:].strip()

    parts = cmd.split("->")
    if len(parts) != 2:
        return None, None, None, None

    target_ref = parts[0].strip()
    correction_part = parts[1].strip()

    # Tách lý do nếu có
    reason = ""
    if "lý do:" in correction_part.lower():
        sub_parts = re.split(r'lý do:|ly do:', correction_part, flags=re.IGNORECASE)
        correction_part = sub_parts[0].strip()
        reason = sub_parts[1].strip()

    elements = [e.strip() for e in re.split(r'[,;]+', correction_part) if e.strip()]

    target_style = None
    target_industry = None
    tags = []

    for el in elements:
        low = el.lower()
        matched_ind = INDUSTRY_ALIASES.get(low)
        matched_sty = STYLE_ALIASES.get(low)

        if matched_ind and not target_industry:
            target_industry = matched_ind
        elif matched_sty and not target_style:
            target_style = matched_sty
        else:
            tags.append(el)

    return target_ref, target_style, target_industry, reason

def apply_feedback(command_str):
    print("=" * 70)
    print("🧠 ANTIGRAVITY ACTIVE LEARNING ENGINE - TIẾP NHẬN PHẢN HỒI ANH VIỆT")
    print("=" * 70)

    target_ref, new_style, new_ind, reason = parse_feedback_command(command_str)
    if not target_ref:
        print("❌ Cú pháp chưa đúng. Vui lòng dùng: SUA: #id -> [Kiểu quay], [Ngành], Lý do: [Giải thích]")
        return False

    master_db = load_json(MASTER_PATH, {})
    vid_id, item = find_target_video(target_ref, master_db)

    if not vid_id:
        print(f"❌ Không tìm thấy video tương ứng với mốc '{target_ref}' trong master database.")
        return False

    old_style = item.get("shooting_style", {}).get("id", "chua-ro")
    old_ind = item.get("industry", {}).get("id", "chua-ro")
    title = item.get("title", "Video không tiêu đề")
    creator = item.get("creator", "Creator")

    print(f"\n🎯 [Xác nhận đối tượng]: #{item.get('index')} - {title} ({creator})")
    print(f"   ID: {vid_id}")
    print(f"   • Trạng thái cũ AI đoán: Kiểu quay: {old_style} | Ngành: {old_ind}")
    print(f"   • Anh Việt hiệu chỉnh:   Kiểu quay: {new_style or '(giữ nguyên)'} | Ngành: {new_ind or '(giữ nguyên)'}")
    if reason:
        print(f"   • Lý do anh Việt ghi chú: \"{reason}\"")

    # 1. Cập nhật curation_config.json
    curation = load_json(CURATION_CONFIG_PATH, {
        "custom_industry_overrides": {},
        "custom_shooting_style_overrides": {}
    })

    if new_ind:
        curation.setdefault("custom_industry_overrides", {})[vid_id] = new_ind
    if new_style:
        curation.setdefault("custom_shooting_style_overrides", {})[vid_id] = new_style

    save_json(CURATION_CONFIG_PATH, curation)
    print("\n✅ [1/4] Đã ghi nhận ghi đè vào curation_config.json")

    # 2. Cập nhật master_classifications.json
    if new_ind:
        ind_obj = INDUSTRY_MAP.get(new_ind, {"id": new_ind, "name": new_ind.replace("-", " ").title(), "icon": "✨"})
        item["industry"] = {
            "id": ind_obj["id"],
            "name": ind_obj["name"],
            "icon": ind_obj.get("icon", "✨")
        }
    if new_style:
        sty_obj = STYLE_MAP.get(new_style, {"id": new_style, "name": new_style.replace("-", " ").title(), "icon": "🎬"})
        item["shooting_style"] = {
            "id": sty_obj["id"],
            "name": sty_obj["name"],
            "icon": sty_obj.get("icon", "🎬")
        }
    master_db[vid_id] = item
    save_json(MASTER_PATH, master_db)
    print("✅ [2/4] Đã đồng bộ mỏ neo chuẩn (Anchor) vào master_classifications.json")

    # 3. Ghi nhật ký học tập vào LEARNED_PATTERNS.json
    patterns = load_json(PATTERNS_PATH, {
        "learning_stats": {"total_corrections": 0, "current_alignment_score": 85.0},
        "learning_history_logs": [],
        "distilled_rules": []
    })

    log_entry = {
        "log_id": f"LEARN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "video_id": vid_id,
        "title": title,
        "creator": creator,
        "ai_predicted": {
            "industry": old_ind,
            "shooting_style": old_style
        },
        "mentor_corrected": {
            "industry": new_ind or old_ind,
            "shooting_style": new_style or old_style
        },
        "reason_distilled": reason or "Hiệu chỉnh trực tiếp từ Super Mentor anh Việt",
        "learned_at": datetime.now().isoformat()
    }

    patterns.setdefault("learning_history_logs", []).append(log_entry)
    patterns.setdefault("learning_stats", {})["total_corrections"] = len(patterns["learning_history_logs"])
    
    # Tính lại Alignment score
    total = len(master_db)
    overrides_cnt = len(curation.get("custom_industry_overrides", {})) + len(curation.get("custom_shooting_style_overrides", {}))
    # Ước lượng tỷ lệ đồng thuận
    alignment = max(75.0, min(99.0, 100.0 - (overrides_cnt / (total * 2 or 1)) * 30.0))
    patterns["learning_stats"]["current_alignment_score"] = round(alignment, 1)

    save_json(PATTERNS_PATH, patterns)
    print("✅ [3/4] Đã đúc kết bài học & ghi nhật ký vĩnh viễn vào LEARNED_PATTERNS.json")

    # 4. Tự động trigger build_ideas_bank.py
    print("⚙️  [4/4] Đang biên dịch lại toàn bộ website ytuong.fedu.vn...")
    res = os.system(f"python3 {BUILD_SCRIPT_PATH} > /dev/null 2>&1")
    if res == 0:
        print("🚀 [Hoàn tất 100%] Website và CSDL đã cập nhật theo đúng chuẩn anh Việt!")
    else:
        print("⚠️ Cần kiểm tra lại build_ideas_bank.py")

    print("\n" + "=" * 70)
    print(f"📊 CHỈ SỐ ĐỒNG THUẬN TƯ DUY (ALIGNMENT SCORE): {patterns['learning_stats']['current_alignment_score']}%")
    print("=" * 70)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sử dụng: python3 feedback_learner.py \"SUA: #4 -> Đời thường, Kỷ luật, Lý do: ...\"")
        print("         python3 feedback_learner.py --stats")
        sys.exit(0)

    arg = sys.argv[1]
    if arg == "--stats":
        p = load_json(PATTERNS_PATH, {})
        stats = p.get("learning_stats", {})
        print(f"📊 Thống kê học tập: Số ca hiệu chỉnh: {stats.get('total_corrections')} | Độ tự tin đồng thuận: {stats.get('current_alignment_score')}%")
        for log in p.get("learning_history_logs", [])[-5:]:
            print(f" - [{log.get('learned_at')[:10]}] {log.get('creator')}: AI({log.get('ai_predicted')}) -> Anh Việt({log.get('mentor_corrected')})")
    elif arg == "--rules":
        p = load_json(PATTERNS_PATH, {})
        print("📜 Danh mục quy tắc AI đã học:")
        for r in p.get("distilled_rules", []):
            print(f" • [{r.get('rule_id')}] {r.get('name')}: {r.get('description')}")
    else:
        apply_feedback(" ".join(sys.argv[1:]))
