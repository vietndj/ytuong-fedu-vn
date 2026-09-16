#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_ideas_bank.py
Engine tự động phân loại, chuẩn hóa dữ liệu kho ý tưởng theo ma trận đa chiều:
- Trục 1: Kiểu quay (Shooting Format) - Walk and Talk, Voice Over, Talking Head, Storytelling, Điện Ảnh, Chuyển Cảnh
- Trục 2: Ngành nghề & Chủ đề (9 ngành cốt lõi, bao gồm Làm Đẹp & Spa / Y Tế)
- Trục 3: Kỹ thuật quay dựng (Technical tags)
- Trục 4: Mục đích nội dung (Content Purpose)

Tác giả: FEDU Creative Engineering
"""

import os
import re
import json
from collections import defaultdict, Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCENE_PATH = os.path.join(BASE_DIR, "scene.html")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
EXCLUDED_CONFIG_PATH = os.path.join(BASE_DIR, "curation_config.json")
MASTER_CLASSIFICATIONS_PATH = os.path.join(BASE_DIR, "master_classifications.json")
OUTPUT_JS_PATH = os.path.join(BASE_DIR, "ideas_data.js")

# 1. Định nghĩa 6 Kiểu Quay (Shooting Styles) - Bộ lọc ngang chính
SHOOTING_STYLES = [
    {
        "id": "walk-and-talk",
        "name": "Walk & Talk",
        "en_name": "Walk and Talk",
        "icon": "🚶",
        "badge_color": "emerald",
        "desc": "Vừa đi vừa nói, camera di chuyển theo nhân vật, tương tác không gian thực tế."
    },
    {
        "id": "voice-over",
        "name": "Lồng Tiếng",
        "en_name": "Voice Over",
        "icon": "🎙️",
        "badge_color": "purple",
        "desc": "Hình ảnh B-roll điện ảnh kết hợp giọng đọc thuyết minh nền, podcast voice."
    },
    {
        "id": "talking-head",
        "name": "Nói Trực Diện",
        "en_name": "Talking Head",
        "icon": "🗣️",
        "badge_color": "blue",
        "desc": "Nói trực diện trước ống kính chia sẻ chuyên môn, hướng dẫn kỹ năng, review sản phẩm."
    },
    {
        "id": "storytelling",
        "name": "Kể Chuyện",
        "en_name": "Storytelling",
        "icon": "📖",
        "badge_color": "amber",
        "desc": "Kể chuyện tự sự, chuỗi hành trình, bài học cảm xúc & triết lý sâu sắc."
    },
    {
        "id": "dien-anh",
        "name": "Chỉn Chu",
        "en_name": "Cinematic Mastery",
        "icon": "🎬",
        "badge_color": "sky",
        "desc": "Nghệ thuật góc máy điện ảnh, bố cục khung hình tĩnh/chậm, ánh sáng Chiaroscuro."
    },
    {
        "id": "chuyen-canh",
        "name": "Chuyển Cảnh",
        "en_name": "Transitions & Flow",
        "icon": "⚡",
        "badge_color": "rose",
        "desc": "Kỹ thuật cắt cảnh nhịp điệu, match cut, whip pan, zoom transition, kinetic visual loop."
    }
]

# 2. Định nghĩa 9 Ngành Nghề & Chủ Đề (Industries / Niches) - Bộ lọc dọc chính
INDUSTRIES = [
    {
        "id": "spa-lam-dep",
        "name": "Làm đẹp",
        "en_name": "Beauty & Spa",
        "icon": "💆",
        "badge_color": "rose",
        "desc": "Dịch vụ spa, phòng khám thẩm mỹ, da liễu Before/After, phẫu thuật, Flash Sale dịch vụ."
    },
    {
        "id": "thuong-hieu",
        "name": "Xây kênh",
        "en_name": "Personal Brand",
        "icon": "💼",
        "badge_color": "indigo",
        "desc": "Kịch bản bán khóa học, tâm lý creator trước camera, tư duy làm kênh Solo Creator, coaching."
    },
    {
        "id": "thoi-trang",
        "name": "Thời trang",
        "en_name": "Fashion & Style",
        "icon": "👔",
        "badge_color": "pink",
        "desc": "Lookbook biến hóa outfit, mỏ neo món đồ, chuyển động bước chân đổi cảnh, phong cách đường phố."
    },
    {
        "id": "am-thuc",
        "name": "F&B",
        "en_name": "Food & Beverage",
        "icon": "🍜",
        "badge_color": "amber",
        "desc": "Nghệ thuật bếp củi, quán cafe hè, hẻm ẩm thực đêm Yokocho, ASMR nấu nướng, đồ uống."
    },
    {
        "id": "du-lich",
        "name": "Du lịch",
        "en_name": "Travel & Culture",
        "icon": "✈️",
        "badge_color": "sky",
        "desc": "Du ký khám phá, phong cảnh đại ngàn, chân dung bản địa, ánh sáng tự nhiên phố cổ."
    },
    {
        "id": "cong-nghe",
        "name": "Đồ công nghệ",
        "en_name": "Tech & Gear",
        "icon": "📱",
        "badge_color": "purple",
        "desc": "5 nhịp mở hộp unboxing, review gear máy ảnh & phụ kiện, công nghệ AR/AI Spatial."
    },
    {
        "id": "kien-truc",
        "name": "Góc nhà đẹp",
        "en_name": "Architecture & Living",
        "icon": "🏛️",
        "badge_color": "emerald",
        "desc": "Bố cục đối xứng kiến trúc, nghệ thuật nhịp sống ga tàu điện ngầm, không gian gỗ tĩnh lặng (Slow Living)."
    },
    {
        "id": "the-thao",
        "name": "Thể thao",
        "en_name": "Sports & Motion",
        "icon": "🏃",
        "badge_color": "orange",
        "desc": "Gym low-key, chạy bộ kỷ luật, FPV drone tốc độ cao vách tuyết, chuyển động năng động."
    },
    {
        "id": "ky-thuat-quay",
        "name": "Bố cục",
        "en_name": "Filmmaking Mastery",
        "icon": "🎯",
        "badge_color": "blue",
        "desc": "Bóc tách 4 cuts, góc máy điện ảnh, bố cục khung hình, kỹ thuật đánh đèn studio 3 điểm."
    },
    {
        "id": "ugc",
        "name": "UGC",
        "en_name": "UGC & Ads",
        "icon": "📱",
        "badge_color": "amber",
        "desc": "Video quảng cáo UGC sàn TMĐT (Shopee, Lazada...) chuẩn công thức AIDA: Gây chú ý, khơi gợi nhu cầu, thúc đẩy chuyển đổi."
    }
]


# 3. Định nghĩa 6 Khu Vực & Quốc Gia (Countries / Regions)
COUNTRIES = [
    {
        "id": "us_eu",
        "name": "Âu Mỹ",
        "en_name": "US & Europe",
        "flag": "🇺🇸/🇪🇺",
        "badge_color": "purple",
        "desc": "Thước phim phong cách phương Tây, New York, London, Paris, Berlin, tối giản hiện đại."
    },
    {
        "id": "korea",
        "name": "Hàn Quốc",
        "en_name": "South Korea",
        "flag": "🇰🇷",
        "badge_color": "pink",
        "desc": "Tone màu trong trẻo, phong cách Daily Vlog, thẩm mỹ chữa lành, cafe aesthetic Hàn Quốc."
    },
    {
        "id": "india",
        "name": "Ấn Độ",
        "en_name": "India",
        "flag": "🇮🇳",
        "badge_color": "amber",
        "desc": "Kỹ xảo cắt cảnh điêu luyện, Match cut triệu view, kỹ thuật quay dựng đỉnh cao châu Á."
    },
    {
        "id": "japan",
        "name": "Nhật Bản",
        "en_name": "Japan",
        "flag": "🇯🇵",
        "badge_color": "rose",
        "desc": "Mỹ học Wabi-Sabi, khung hình tĩnh (Static Shot), nhịp thở đời thường Kyoto & Tokyo."
    },
    {
        "id": "vietnam",
        "name": "Việt Nam",
        "en_name": "Vietnam",
        "flag": "🇻🇳",
        "badge_color": "emerald",
        "desc": "Mẫu quay bối cảnh Việt Nam thực chiến, đường phố Hà Nội, Sài Gòn, Hải Dương, clip học viên."
    },
    {
        "id": "asia_other",
        "name": "Châu Á Khác",
        "en_name": "Other Asia",
        "flag": "🌏",
        "badge_color": "sky",
        "desc": "Hong Kong, Singapore, Thái Lan, Malaysia, Philippines, không gian đô thị châu Á sống động."
    }
]

def detect_country(creator, title, report_desc=""):
    c = (creator or "").lower()
    t = (title or "").lower()
    r = (report_desc or "").lower()
    combined = f"{c} {t} {r}"

    if any(x in c for x in ['mridu', 'photoknack', 'sajad', 'thomasmathew', 'ayush', 'aayush']) or 'ấn độ' in combined or 'india' in combined:
        return next(x for x in COUNTRIES if x['id'] == 'india')
    if any(x in c for x in ['hena', 'bewoom', 'kyung6', 'nana_ic']) or 'hàn quốc' in combined or 'korea' in combined or 'seoul' in combined:
        return next(x for x in COUNTRIES if x['id'] == 'korea')
    if any(x in c for x in ['shogentle', 'junko', 'kenshoji', 'hana.koni', 'daiki']) or any(x in combined for x in ['tokyo', 'kyoto', 'nhật bản', 'japan', 'yokocho']):
        return next(x for x in COUNTRIES if x['id'] == 'japan')
    if any(x in c for x in ['tinanguyen', 'minhmigoi', 'thodia', 'kopdinh', 'anhsac', 'vietmac', 'startup', 'self_practice']) or any(x in combined for x in ['việt nam', 'vietnam', 'hải dương', 'sài gòn', 'saigon', 'hà nội', 'times city']):
        return next(x for x in COUNTRIES if x['id'] == 'vietnam')
    if any(x in c for x in ['withyuee', 'tsangtastic', 'jazziesillona', 'nicoolalah', 'ariffathul', 'firewood', 'intothethailand', 'jsnhow', 'beixin', 'slaohuairen', 'jeromememe', 'elsaqinn', 'chowyhh', 'gakuyen', 'kerennilan', 'mkxpresar']) or any(x in combined for x in ['bangkok', 'hong kong', 'bhutan', 'thượng hải', 'shanghai', 'malaysia', 'philippines', 'thái lan']):
        return next(x for x in COUNTRIES if x['id'] == 'asia_other')
    return next(x for x in COUNTRIES if x['id'] == 'us_eu')

PERSONAL_IDENTIFIERS = [
    "@vietmac", "practice_cinematic", "self_practice", "broll_plan", "@local", "vietnd"
]

def load_master_classifications():
    if os.path.exists(MASTER_CLASSIFICATIONS_PATH):
        try:
            with open(MASTER_CLASSIFICATIONS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def load_portal_data():
    with open(SCENE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'const portalData\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if not m:
        raise ValueError("Could not extract portalData from scene.html")
    return json.loads(m.group(1))

def load_curation_config():
    if os.path.exists(EXCLUDED_CONFIG_PATH):
        try:
            with open(EXCLUDED_CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "excluded_ids": [],
        "custom_industry_overrides": {},
        "custom_shooting_style_overrides": {},
        "custom_title_overrides": {}
    }

def extract_shortcode(item):
    ig = item.get("ig_url", "")
    m = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_-]+)", ig)
    if m:
        return m.group(1).strip().rstrip("_")
    
    vid_id = item.get("id", "")
    # Ưu tiên mã Instagram chuẩn 11 ký tự dạng D...
    m_code = re.search(r"_(D[A-Za-z0-9_-]{10})(?:_|$)", vid_id)
    if m_code:
        return m_code.group(1).strip().rstrip("_")
        
    m_code2 = re.search(r"_(D[A-Za-z0-9_-]{9,11})", vid_id)
    if m_code2:
        return m_code2.group(1).strip().rstrip("_")
        
    # Thử bóc tách từ tên file video nếu có mã D...
    vurl = item.get("main_vid_rel", "") or item.get("root_vid_rel", "")
    m_v = re.search(r"/([A-Za-z0-9_-]{11})\.mp4", vurl)
    if m_v:
        return m_v.group(1).strip().rstrip("_")
        
    return vid_id.strip()

def clean_creator_info(creator_raw, ig_url="", vid_id="", item=None):
    handle = ""
    name = (creator_raw or "").strip()
    if name == "Unknown":
        name = ""

    # Check item channel/author
    if item:
        if not handle and item.get("channel_tag"):
            handle = item.get("channel_tag")
        if not handle and item.get("author"):
            handle = item.get("author")
        if not name and item.get("channel"):
            name = item.get("channel")
    
    m_by = re.search(r"Video_by_([a-zA-Z0-9._]+)", vid_id)
    if m_by:
        handle = "@" + m_by.group(1)
    elif not handle:
        m = re.search(r"@([a-zA-Z0-9._]+)", creator_raw or "")
        if m:
            handle = "@" + m.group(1)
        else:
            m_id = re.search(r"IG_@([a-zA-Z0-9._]+)_", vid_id)
            if m_id:
                handle = "@" + m_id.group(1)
    
    name_m = re.search(r"\((.*?)\)", creator_raw or "")
    if name_m:
        name = name_m.group(1).strip()
    elif not name and handle:
        name = handle.replace("@", "").title()
    elif not name:
        name = "Creator"
        
    profile_url = ig_url
    if handle:
        raw_h = handle.replace("@", "").strip()
        profile_url = f"https://www.instagram.com/{raw_h}/"
    elif ig_url and "instagram.com" in ig_url:
        m_ig = re.search(r"instagram\.com/([a-zA-Z0-9._]+)/?", ig_url)
        if m_ig and m_ig.group(1) not in ["p", "reel", "tv"]:
            handle = "@" + m_ig.group(1)
            name = handle.replace("@", "").title()
            profile_url = f"https://www.instagram.com/{m_ig.group(1)}/"
            
    return {
        "raw": creator_raw or handle,
        "name": name,
        "handle": handle or "@creator",
        "profile_url": profile_url
    }

def clean_title_and_takeaway(item, title_overrides={}):
    vid_id = item.get("id", "")
    if vid_id in title_overrides:
        clean_title = title_overrides[vid_id]
    else:
        clean_title = (item.get("title_vi") or item.get("title") or item.get("title_en") or "").strip()
        
    desc_vi = (item.get("desc_vi") or item.get("summary") or item.get("desc") or "").strip()
    key_tech = item.get("key_tech", "").strip()
    html_rel = item.get("root_html_rel") or item.get("main_html_rel", "")
    full_html_path = os.path.join(BASE_DIR, html_rel)
    
    report_title = ""
    report_desc = ""
    report_duration = ""
    
    if os.path.exists(full_html_path):
        try:
            with open(full_html_path, "r", encoding="utf-8", errors="ignore") as rf:
                html_head = rf.read(30000)
                
                m_dur = re.search(r"/\s*(\d+(?:\.\d+)?s)\b", html_head)
                if not m_dur:
                    m_dur = re.search(r'class="time-display"[^>]*>.*?/\s*([0-9.]+s)', html_head)
                if not m_dur:
                    m_dur = re.search(r'⏱️\s*([0-9.]+s?)', html_head)
                if m_dur:
                    parsed_d = m_dur.group(1)
                    # Exclude invalid micro CSS transitions like 0.2s
                    try:
                        num_sec = float(parsed_d.replace('s', ''))
                        if num_sec >= 2.0:
                            report_duration = parsed_d
                    except Exception:
                        pass
                
                tm = re.search(r"<title>(.*?)</title>", html_head, re.IGNORECASE)
                if tm:
                    report_title = tm.group(1).strip()
                    
                m_card = re.search(r"<div class=\"overview-card\">.*?<div[^>]*>(.*?)</div>", html_head, re.DOTALL)
                if m_card:
                    report_desc = re.sub(r"<.*?>", "", m_card.group(1)).strip()
                else:
                    sm = re.search(r"<div class=\"synopsis-card\">\s*<div[^>]*>(.*?)</div>", html_head, re.DOTALL)
                    if not sm:
                        sm = re.search(r"<div class=\"overview-desc\">(.*?)</div>", html_head, re.DOTALL)
                    if sm:
                        report_desc = re.sub(r"<.*?>", "", sm.group(1)).strip()
        except Exception:
            pass

    if vid_id not in title_overrides:
        if clean_title.startswith("@") or "DXf1LldT5co" in clean_title or "Video by" in clean_title or "Carousel Analysis" in clean_title:
            if report_title and not report_title.startswith("@creator"):
                cleaned_rt = re.sub(r"^@[a-zA-Z0-9._\s]+[\-–—•]\s*", "", report_title).strip()
                if cleaned_rt and len(cleaned_rt) > 5:
                    clean_title = cleaned_rt
            elif "DXf1LldT5co" in item.get("id", ""):
                clean_title = "Jenny Tsang • Calvin Klein Baggy Jeans Hong Kong Lookbook"

    clean_title = re.sub(r"^[🎬📄📸👤\s]+", "", clean_title).strip()

    takeaway = desc_vi
    if report_desc and len(report_desc) > 30:
        takeaway = report_desc
    elif not takeaway or len(takeaway) < 20:
        takeaway = f"Bóc tách ngôn ngữ điện ảnh và nghệ thuật thị giác: {key_tech}."

    sentences = re.split(r'(?<=[.!?])\s+', takeaway)
    short_takeaway = " ".join(sentences[:2]).strip()
    if len(short_takeaway) > 240:
        short_takeaway = short_takeaway[:237] + "..."

    return clean_title, short_takeaway, report_duration

def get_item_classification(vid_id, code, clean_title, takeaway, key_tech, creator_handle, curation_cfg, master_dict):
    ind_overrides = curation_cfg.get("custom_industry_overrides", {})
    style_overrides = curation_cfg.get("custom_shooting_style_overrides", {})

    master = master_dict.get(vid_id) or master_dict.get(code)
    if master:
        s_id = style_overrides.get(vid_id, master["shooting_style"]["id"])
        i_id = ind_overrides.get(vid_id, master["industry"]["id"])
        style_obj = next((s for s in SHOOTING_STYLES if s["id"] == s_id), SHOOTING_STYLES[4])
        ind_obj = next((i for i in INDUSTRIES if i["id"] == i_id), INDUSTRIES[8])
        purpose = master.get("purpose", "Showcase thị giác & Thẩm mỹ")
        tech_tags = master.get("tech_tags", [key_tech] if key_tech else ["Cinematic Framing"])
        logic = master.get("logic_explanation", "")
        country_obj = master.get("country")
        if not country_obj:
            country_obj = detect_country(creator_handle, clean_title, takeaway)
        return style_obj, ind_obj, country_obj, purpose, tech_tags, logic

    # Fallback for future unknown items
    corpus = f"{vid_id} {clean_title} {takeaway} {key_tech}".lower()
    
    target_style = style_overrides.get(vid_id, "dien-anh")
    if "tinanguyen" in corpus or "medical" in corpus:
        target_style = "walk-and-talk"
    elif any(w in corpus for w in ["talking head", "yap triangle", "nói trước"]):
        target_style = "talking-head"
    elif any(w in corpus for w in ["thuyết minh", "voiceover", "voice over"]):
        target_style = "voice-over"
    elif any(w in corpus for w in ["match cut", "whip pan", "transition", "chuyển cảnh"]):
        target_style = "chuyen-canh"
    elif any(w in corpus for w in ["kể chuyện", "storytelling", "hành trình"]):
        target_style = "storytelling"

    target_ind = ind_overrides.get(vid_id, "ky-thuat-quay")
    if any(w in corpus for w in ["y khoa", "y tế", "spa", "da liễu", "mụn"]):
        target_ind = "spa-lam-dep"
    elif any(w in corpus for w in ["thương hiệu cá nhân", "xây kênh", "bán khóa học"]):
        target_ind = "thuong-hieu"
    elif any(w in corpus for w in ["lookbook", "outfit", "thời trang"]):
        target_ind = "thoi-trang"
    elif any(w in corpus for w in ["ẩm thực", "cafe", "cà phê", "nấu ăn"]):
        target_ind = "am-thuc"
    elif any(w in corpus for w in ["unboxing", "mở hộp", "dji", "mic 3", "gear"]):
        target_ind = "cong-nghe"
    elif any(w in corpus for w in ["kiến trúc", "không gian gỗ", "slow living"]):
        target_ind = "kien-truc"
    elif any(w in corpus for w in ["chạy bộ", "gym", "fitness", "thể thao"]):
        target_ind = "the-thao"
    elif any(w in corpus for w in ["du lịch", "du ký", "bhutan", "porto", "venice"]):
        target_ind = "du-lich"

    style_obj = next((s for s in SHOOTING_STYLES if s["id"] == target_style), SHOOTING_STYLES[4])
    ind_obj = next((i for i in INDUSTRIES if i["id"] == target_ind), INDUSTRIES[8])
    country_obj = detect_country(creator_handle, clean_title, takeaway)
    return style_obj, ind_obj, country_obj, "Showcase thị giác & Thẩm mỹ", [key_tech] if key_tech else ["Cinematic"], ""

def build_database():
    portal_data = load_portal_data()
    curation_cfg = load_curation_config()
    master_dict = load_master_classifications()
    manually_excluded_ids = set(curation_cfg.get("excluded_ids", []))
    deleted_ids = set(curation_cfg.get("deleted_ids", []))
    title_overrides = curation_cfg.get("custom_title_overrides", {})
    
    print(f"Loaded {len(portal_data)} items from scene.html")
    print(f"Loaded {len(master_dict)} items from master_classifications.json")
    print(f"Loaded {len(deleted_ids)} permanently deleted video IDs")

    def calculate_item_quality(it):
        score = 0
        title = it.get("title_vi", "").strip()
        # Ưu tiên tiêu đề tiếng Việt đã chau chuốt, không phải tên raw @handle
        if title:
            score += len(title)
            if not title.startswith("@") and not title.startswith("Video by"):
                score += 80
        # Ưu tiên có báo cáo HTML đầy đủ
        rep = it.get("main_html_rel") or it.get("root_html_rel") or ""
        if rep:
            score += 150
        # Ưu tiên có mô tả phân tích sâu
        desc = it.get("desc_vi") or ""
        if len(desc) > 20:
            score += 50
        # Ưu tiên có thumbnails rõ ràng
        thumbs = it.get("thumbnails") or it.get("thumbs") or []
        if thumbs:
            score += 30
        return score

    unique_items_map = {}
    for idx, item in enumerate(portal_data):
        code = extract_shortcode(item)
        if code in unique_items_map:
            prev = unique_items_map[code]
            cur_score = calculate_item_quality(item)
            prev_score = calculate_item_quality(prev)
            if cur_score > prev_score:
                unique_items_map[code] = item
        else:
            unique_items_map[code] = item

    print(f"Unique master videos: {len(unique_items_map)}")

    processed_ideas = []
    creators_dict = defaultdict(list)

    for code, item in unique_items_map.items():
        vid_id = item.get("id", "")
        # Bỏ qua hoàn toàn các video đã bị xóa khỏi hệ thống
        if (vid_id in deleted_ids) or (code in deleted_ids):
            continue

        creator_raw = item.get("creator") or item.get("author") or item.get("channel_tag") or "Unknown"
        c_info = clean_creator_info(creator_raw, item.get("ig_url", ""), vid_id, item=item)
        master = master_dict.get(vid_id) or master_dict.get(code)
        if master and master.get("creator_name") and (not c_info.get("name") or c_info["name"].startswith("@")):
            c_info["name"] = master["creator_name"]
        elif c_info.get("name", "").startswith("@"):
            c_info["name"] = c_info["name"].replace("@", "").title()
        
        is_personal = False
        check_str = f"{creator_raw} {vid_id}".lower()
        if any(p in check_str for p in PERSONAL_IDENTIFIERS):
            is_personal = True

        is_excluded = is_personal or (vid_id in manually_excluded_ids) or (code in manually_excluded_ids)
        
        clean_title, short_takeaway, rep_dur = clean_title_and_takeaway(item, title_overrides)
        if master and master.get("title") and not master.get("title").startswith("Video by") and not master.get("title").startswith("@"):
            clean_title = master["title"]
        if master and master.get("quick_takeaway") and not master.get("quick_takeaway").startswith("Tác phẩm điện ảnh ngắn gồm"):
            short_takeaway = master["quick_takeaway"]
        style_obj, ind_obj, country_obj, purpose, tech_tags, logic_exp = get_item_classification(
            vid_id, code, clean_title, short_takeaway, item.get("key_tech", ""), c_info["handle"], curation_cfg, master_dict
        )
        
        folder = item.get("folder_name") or vid_id
        thumbs = item.get("thumbnails") or item.get("thumbs") or []
        if not thumbs or len(thumbs) < 2:
            if "Carousel" in folder or "Carousel" in vid_id:
                thumb_hook = f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{folder}/slide_01_mid.jpg"
                thumb_key = f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{folder}/slide_03_mid.jpg"
            else:
                thumb_hook = f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{folder}/shot_01_mid.jpg"
                thumb_key = f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{folder}/shot_03_mid.jpg"
        else:
            thumb_hook = thumbs[0]
            thumb_key = thumbs[1] if len(thumbs) > 1 else thumbs[0]

        # Chuẩn hóa thumbnail URL thành R2 CDN tuyệt đối và an toàn URL encoding
        import urllib.parse
        def normalize_thumb_url(u, fld, default_name):
            if not u:
                return f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{urllib.parse.quote(fld)}/{default_name}"
            if not u.startswith("http"):
                clean = u.lstrip("./")
                if clean.startswith("images/"):
                    clean = clean[7:]
                return f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{urllib.parse.quote(clean, safe='/')}"
            # Encode non-ascii path characters in R2 URLs
            p = urllib.parse.urlsplit(u)
            safe_path = urllib.parse.quote(p.path, safe="/")
            return urllib.parse.urlunsplit((p.scheme, p.netloc, safe_path, p.query, p.fragment))

        thumb_hook = normalize_thumb_url(thumb_hook, folder, "shot_01_mid.jpg")
        thumb_key = normalize_thumb_url(thumb_key, folder, "shot_03_mid.jpg")

        vid_url = item.get("root_vid_rel") or item.get("main_vid_rel") or ""
        if not vid_url and item.get("all_vids"):
            vid_url = item["all_vids"][0].get("rel_url", "")

        # R2 Video URL Mapping Override for guaranteed 200 OK CDN streaming
        R2_OVERRIDE_MAP = {
            "IG_@shogentle_DdCRQnBI4ny_Fast_Food_Outsells_Restaurant": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DdCRQnBI4ny.mp4",
            "IG_@aidana_adilkassym_DcQy-eEOIHc_Tornado_Kick_Martial_Arts_Kinetic_Hook": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Tornado%20Kick%20Martial%20Arts%20Kinetic%20Hook%20-%20%40aidana_adilkassym.mp4",
            "IG_@critos_pro_DcxwKHYoBFv_The_Art_of_Consistency": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcxwKHYoBFv.mp4",
            "IG_@jamison.lange_DawDiT2M1p8_Coffee_Outfit_Match_Cut_Fashion": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DawDiT2M1p8.mp4",
            "IG_@mako__go_DaH7X34NTNX_Palermo_Sicily": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DaH7X34NTNX.mp4",
            "IG_@valenti_k41_DdB_21Yo0Qc_Creative_Phone_Video_Ideas": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Creative%20Phone%20Video%20Ideas%20-%20Routine%20Creator%20-%20%40valenti_k41.mp4",
            "IG_@hey.lirules_DdBDvZph1od_Hoi_An_Natural_Mask_Transitions": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DdBDvZph1od.mp4",
            "IG_@alena.feda_Dc1w07upyNF_Food_Filming_Mastery_From_Scratch": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Food%20Filming%20%26%20Styling%20Mastery%20-%20%40alena.feda.mp4",
            "IG_@ulanzi.global_DcyS2KEm7-v_Ulanzi_LA30_RGB_Air_Tube_Light": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcyS2KEm7-v.mp4",
            "IG_@shogentle_DcyDbGmItDV_One_Lamp_Beats_Five": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcyDbGmItDV.mp4",
            "FB_@AnhSacAnh_1964049564715249_Thuong_Hieu_Ca_Nhan_Sinh_Loi": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Thuong_Hieu_Ca_Nhan_Sinh_Loi_Anh_Sac_Anh.mp4",
            "IG_@tsangtastic_DaB-gO6hvPX_Tory_Burch_Summer_Unboxing": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DaB-gO6hvPX.mp4",
            "IG_@valenti_k41_DctVSroI3UB_Creative_Phone_Video_Ideas": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Creative%20phone%20video%20ideas%20-%20%40valenti_k41.mp4",
            "IG_@jesussropero_Dc9LUXLAHkc_Getting_Ready_Faster_Than_Ever": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Getting%20Ready%20Faster%20Than%20Ever%20-%20%40jesussropero.mp4",
            "IG_@colecoppolino_DcJiRCrTlG1": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcJiRCrTlG1.mp4",
            "IG_@withyuee_DcTk0RGgtBO_Hong_Kong_Cinematic_Cityscape": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcTk0RGgtBO.mp4",
            "IG_@willwfit_DbRak0lsesY_The_Goal_Is_Simple": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DbRak0lsesY.mp4",
            "IG_@iamlukeluquire_DbjCyKgxp8S_Aesthetic_Routine": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DbjCyKgxp8S.mp4",
            "IG_@lifeofriza_DcTqPjitJl1_Y_Tuong_Thanh_Hien_Thuc_Canva": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcTqPjitJl1.mp4",
            "IG_@fabianamsolano_Dc4u6aOhR9r_Yosemite_National_Park_Music_Video_Beat_Match_Cut": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Yosemite%20National%20Park%20Music%20Video%20-%20%40fabianamsolano.mp4",
            "IG_@kawoon.lee_DatbbgJviTV_Teaching_Nervous_System_Not_Emergency": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Teaching_Nervous_System_Not_Emergency_-_%40kawoon.lee.mp4",
            "IG_@hena_film_vlog_Db-mZWEKECo_4_Cu_May_Sieu_Thi_Ulanzi_MA38_MT85": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/4%20Cu%20May%20Sieu%20Thi%20Bang%20Gia%20Do%20Ulanzi%20MA38%20MT85%20-%20%40hena_film_vlog.mp4",
            "IG_@dimasyudhystira_Dc3DUsvpkrP_Gunung_Sumbing_Trekking_Match_Cut": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Gunung%20Sumbing%20Trekking%20Match%20Cut%20-%20%40dimasyudhystira.mp4",
            "IG_@naohasa_DdGp4XftvIn_5_Outfits_Match_Cut_Walk": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DdGp4XftvIn.mp4",
            "IG_@Andrei_Kostromskikh_DctRlh0jZlj_Carousel_Analysis": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/carousel_slides/IG_%40Andrei_Kostromskikh_DctRlh0jZlj_Carousel_Analysis/slide_01.mp4",
            "Visual_Storytelling_Carousel_@withyuee": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/carousel_slides/slide_01.mp4",
            "IG_@treechurchlogan_DcoGfdghNwd_Bring_A_Friend_To_Church_Skit": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcoGfdghNwd.mp4"
        }
        if vid_id in R2_OVERRIDE_MAP:
            vid_url = R2_OVERRIDE_MAP[vid_id]
        elif vid_url and not vid_url.startswith("http"):
            import urllib.parse
            clean_rel = vid_url.lstrip("./")
            vid_url = "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/" + urllib.parse.quote(clean_rel, safe="/")
            
        html_url = item.get("root_html_rel") or item.get("main_html_rel") or ""
        shots_count = item.get("shots_count", 0)
        
        duration_str = item.get("duration", "") or rep_dur or (f"{shots_count * 2}s" if shots_count else "15s")
        if "DaB-gO6hvPX" in vid_id:
            duration_str = "90s"
        
        if shots_count <= 8:
            complexity = {"id": "de", "label": "🟢 Dễ làm theo (3-8 shots)"}
        elif shots_count <= 18:
            complexity = {"id": "trung-binh", "label": "🟡 Trung bình (9-18 shots)"}
        else:
            complexity = {"id": "nang-cao", "label": "🔴 Nâng cao (>18 shots)"}

        transition_level = master.get("transition_level") if master else None
        is_ad_bot = master.get("is_ad_bot", False) if master else False
        if not is_ad_bot and (("LAZADA_" in vid_id) or ("SHOPEE_" in vid_id) or ("UGC, Quảng cáo, AIDA" in str(tech_tags))):
            is_ad_bot = True

        # Video upload từ bot telegram tải quảng cáo (Shopee, Lazada...) -> Xếp vào mục ngành nghề UGC
        if is_ad_bot or "LAZADA_" in vid_id or "SHOPEE_" in vid_id or (master and master.get("industry", {}).get("id") == "ugc"):
            is_ad_bot = True
            ind_obj = next(i for i in INDUSTRIES if i["id"] == "ugc")

        fedu_opt = master.get("fedu_optimization", {}) if master else {}

        idea_obj = {
            "id": vid_id,
            "shortcode": code,
            "title_vi": clean_title,
            "quick_takeaway": short_takeaway,
            "key_tech": item.get("key_tech", ""),
            "shooting_style": {
                "id": style_obj["id"],
                "name": style_obj["name"],
                "en_name": style_obj["en_name"],
                "icon": style_obj["icon"],
                "badge_color": style_obj["badge_color"]
            },
            "industry": {
                "id": ind_obj["id"],
                "name": ind_obj["name"],
                "en_name": ind_obj["en_name"],
                "icon": ind_obj["icon"],
                "badge_color": ind_obj["badge_color"]
            },
            "country": {
                "id": country_obj["id"],
                "name": country_obj["name"],
                "en_name": country_obj["en_name"],
                "flag": country_obj["flag"],
                "badge_color": country_obj["badge_color"]
            },
            "purpose": purpose,
            "tech_tags": tech_tags,
            "transition_level": transition_level,
            "is_ad_bot": is_ad_bot,
            "fedu_optimization": fedu_opt,
            "logic_explanation": logic_exp,
            "creator": c_info,
            "ig_url": item.get("ig_url", "") or c_info["profile_url"],
            "gdrive_folder": item.get("gdrive_folder", ""),
            "media": {
                "thumb_hook": thumb_hook,
                "thumb_key": thumb_key,
                "video_url": vid_url,
                "report_url": html_url,
                "shots_count": shots_count,
                "duration": duration_str,
                "youtube_id": item.get("youtube_id") or (master.get("youtube_id") if master else ""),
                "youtube_embed": item.get("youtube_embed") or (master.get("youtube_embed") if master else ""),
                "youtube_url": item.get("youtube_url") or (master.get("youtube_url") if master else "")
            },
            "complexity": complexity,
            "is_personal": is_personal,
            "is_excluded": is_excluded
        }

        processed_ideas.append(idea_obj)

        if not is_personal and not is_excluded:
            creators_dict[c_info["handle"]].append(idea_obj)

    creators_hub = []
    for handle, vids in sorted(creators_dict.items(), key=lambda x: len(x[1]), reverse=True):
        first_vid = vids[0]
        c_meta = first_vid["creator"]
        ind_counts = Counter(v["industry"]["name"] for v in vids)
        top_ind = ind_counts.most_common(1)[0][0]
        
        creators_hub.append({
            "handle": handle,
            "name": c_meta["name"],
            "profile_url": c_meta["profile_url"],
            "video_count": len(vids),
            "top_industry": top_ind,
            "sample_thumb": first_vid["media"]["thumb_hook"],
            "video_ids": [v["id"] for v in vids]
        })

    active_ideas = [x for x in processed_ideas if not x["is_excluded"]]
    
    industry_stats = {}
    for ind in INDUSTRIES:
        c = sum(1 for x in active_ideas if x["industry"]["id"] == ind["id"])
        industry_stats[ind["id"]] = c

    shooting_style_stats = {}
    for st in SHOOTING_STYLES:
        c = sum(1 for x in active_ideas if x["shooting_style"]["id"] == st["id"])
        shooting_style_stats[st["id"]] = c

    country_stats = {}
    for c_item in COUNTRIES:
        cnt = sum(1 for x in active_ideas if x.get("country", {}).get("id") == c_item["id"])
        country_stats[c_item["id"]] = cnt

    transition_stats = {
        "level_1_count": sum(1 for x in active_ideas if x.get("transition_level") == "Chuyển cảnh Level 1"),
        "level_2_count": sum(1 for x in active_ideas if x.get("transition_level") == "Chuyển cảnh Level 2"),
        "ad_bot_count": sum(1 for x in active_ideas if x.get("is_ad_bot") is True)
    }

    database_payload = {
        "generated_at": "2026-09-13T18:00:00+07:00",
        "total_scene_items": len(portal_data),
        "total_unique_ideas": len(processed_ideas),
        "total_active_ideas": len(active_ideas),
        "total_excluded_ideas": len(processed_ideas) - len(active_ideas),
        "total_creators": len(creators_hub),
        "shooting_styles": SHOOTING_STYLES,
        "shooting_style_stats": shooting_style_stats,
        "industries": INDUSTRIES,
        "industry_stats": industry_stats,
        "countries": COUNTRIES,
        "country_stats": country_stats,
        "transition_stats": transition_stats,
        "deleted_ids": list(deleted_ids),
        "creators_hub": creators_hub,
        "ideas": processed_ideas
    }

    js_content = f"/**\n * FEDU CREATIVE IDEAS BANK DATABASE (Auto-generated)\n * Do not edit manually. Re-run build_ideas_bank.py to update.\n */\nvar FEDU_IDEAS_DATABASE = {json.dumps(database_payload, ensure_ascii=False, indent=2)};\n"

    with open(OUTPUT_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)

    # Automatically sync output files to dist/ for Cloudflare Pages deployment
    import shutil
    dist_dir = os.path.join(BASE_DIR, "dist")
    if os.path.exists(dist_dir):
        shutil.copy2(OUTPUT_JS_PATH, os.path.join(dist_dir, "ideas_data.js"))
        if os.path.exists(MASTER_CLASSIFICATIONS_PATH):
            shutil.copy2(MASTER_CLASSIFICATIONS_PATH, os.path.join(dist_dir, "master_classifications.json"))
        if os.path.exists(EXCLUDED_CONFIG_PATH):
            shutil.copy2(EXCLUDED_CONFIG_PATH, os.path.join(dist_dir, "curation_config.json"))
        index_path = os.path.join(BASE_DIR, "index.html")
        if os.path.exists(index_path):
            shutil.copy2(index_path, os.path.join(dist_dir, "index.html"))
        print("Synchronized all build files to dist/ directory.")

    print(f"Successfully generated {OUTPUT_JS_PATH}")
    print(f"Total active ideas: {len(active_ideas)}")
    print(f"Industry Stats: {industry_stats}")
    print(f"Shooting Style Stats: {shooting_style_stats}")

if __name__ == "__main__":
    build_database()
