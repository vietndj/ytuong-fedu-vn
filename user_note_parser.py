#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
user_note_parser.py
Module phân tích ghi chú tự nhiên từ người dùng (User Note Parser)
Hỗ trợ bóc tách đa trục:
- Ngành nghề / Chủ đề (9 ngành chuẩn YTUONG HUB + UGC)
- Kiểu quay (6 Shooting Styles)
- Danh sách Tags chuyên sâu (từ khóa, #hashtag, sau tiền tố tag:/thẻ:)
"""

import re

# 1. Danh mục 9 Ngành Nghề & UGC chuẩn YTUONG HUB
INDUSTRIES = [
    {
        "id": "spa-lam-dep",
        "name": "Làm đẹp",
        "icon": "💆",
        "keywords": [
            "spa làm đẹp", "spa lam dep", "viện thẩm mỹ", "vien tham my", "chăm sóc da",
            "cham soc da", "nặn mụn", "nan mun", "trị mụn", "tri mun", "y khoa", "y tế",
            "da liễu", "da lieu", "thẩm mỹ", "tham my", "phẫu thuật", "phau thuat",
            "nha khoa", "răng", "rang", "filler", "botox", "laser", "gội đầu dưỡng sinh",
            "dưỡng sinh", "skincare", "clinic", "bác sĩ da liễu", "bác sĩ thẩm mỹ", "spa", "làm đẹp", "lam dep"
        ]
    },
    {
        "id": "thuong-hieu",
        "name": "Xây kênh",
        "icon": "💼",
        "keywords": [
            "thương hiệu cá nhân", "thuong hieu ca nhan", "xây kênh", "xay kenh", "personal brand", "xây kênh", "xay kenh",
            "solo creator", "bán khóa học", "ban khoa hoc", "khóa học", "khoa hoc", "coaching",
            "dịch vụ", "dich vu", "tư duy", "tu duy", "thương hiệu", "thuong hieu", "cá nhân", "ca nhan"
        ]
    },
    {
        "id": "thoi-trang",
        "name": "Thời trang",
        "icon": "👔",
        "keywords": [
            "thời trang", "thoi trang", "phụ kiện", "phu kien", "lookbook", "outfit", "phối đồ",
            "phoi do", "quần áo", "quan ao", "váy vóc", "váy", "vay", "túi xách", "tui xach",
            "giày dép", "giày", "sneaker", "streetwear", "fashion", "trang phục", "style", "model"
        ]
    },
    {
        "id": "am-thuc",
        "name": "F&B",
        "icon": "🍜",
        "keywords": [
            "ẩm thực", "am thuc", "fnb", "f&b", "quán cafe", "quan cafe", "cà phê", "ca phe", "cafe",
            "nhà hàng", "nha hang", "quán ăn", "quan an", "nấu ăn", "nau an", "nấu nướng", "đồ ăn",
            "do an", "món ăn", "mon an", "bếp củi", "bep cui", "asmr nấu", "đồ uống", "do uong",
            "trà sữa", "tra sua", "bar", "pha chế", "food", "beverage", "cooking"
        ]
    },
    {
        "id": "du-lich",
        "name": "Du lịch",
        "icon": "✈️",
        "keywords": [
            "du lịch", "du lich", "văn hóa", "van hoa", "travel", "khám phá", "kham pha", "phong cảnh",
            "phong canh", "phượt", "phuot", "nghỉ dưỡng", "nghi duong", "khách sạn", "khach san",
            "resort", "tour", "phố cổ", "pho co", "checkin", "đà lạt", "tây bắc", "biển", "núi"
        ]
    },
    {
        "id": "cong-nghe",
        "name": "Đồ công nghệ",
        "icon": "📱",
        "keywords": [
            "công nghệ", "cong nghe", "thiết bị", "đồ công nghệ", "do cong nghe", "thiet bi", "tech", "unboxing", "mở hộp", "mo hop",
            "máy ảnh", "may anh", "camera", "gear", "điện thoại", "dien thoai", "iphone", "gimbal",
            "micro", "mic", "lens", "ống kính", "ong kinh", "gadget", "tai nghe", "setup", "đèn ulanzi", "ulanzi"
        ]
    },
    {
        "id": "kien-truc",
        "name": "Góc nhà đẹp",
        "icon": "🏛️",
        "keywords": [
            "kiến trúc", "góc nhà đẹp", "goc nha dep", "kien truc", "không gian sống", "khong gian song", "không gian", "khong gian",
            "nhà đẹp", "nha dep", "nội thất", "noi that", "thiết kế nội thất", "nhà gỗ", "nha go",
            "villa", "decor", "căn hộ", "can ho", "thiết kế nhà", "architecture", "interior"
        ]
    },
    {
        "id": "the-thao",
        "name": "Thể thao",
        "icon": "🏃",
        "keywords": [
            "thể thao", "the thao", "gym", "chạy bộ", "chay bo", "running", "tập gym", "thể hình",
            "the hinh", "workout", "fitness", "bơi lội", "bóng rổ", "cầu lông", "yoga", "pilates", "boxing", "sport"
        ]
    },
    {
        "id": "ky-thuat-quay",
        "name": "Bố cục",
        "icon": "🎯",
        "keywords": [
            "kỹ thuật quay", "ky thuat quay", "quay dựng", "quay dung", "góc máy", "bố cục", "bo cuc", "goc may", "cú máy",
            "cu may", "lighting", "bố cục", "bo cuc", "phân cảnh", "phan canh", "storyboard", "camera movement",
            "4 cuts", "tips quay", "mẹo quay", "meo quay", "hướng dẫn quay", "filmmaking", "broll tutorial", "đạo diễn"
        ]
    },
    {
        "id": "ugc",
        "name": "UGC",
        "icon": "📱",
        "keywords": [
            "ugc", "quảng cáo sàn", "quảng cáo shopee", "quảng cáo tiktok", "tiktok shop", "shopee",
            "affiliate", "video bán hàng", "aida", "ads", "review sản phẩm", "quảng cáo"
        ]
    }
]

# 2. Danh mục 6 Kiểu Quay chuẩn YTUONG HUB
SHOOTING_STYLES = [
    {
        "id": "walk-and-talk",
        "name": "Walk and Talk",
        "icon": "🚶",
        "keywords": [
            "walk and talk", "walk & talk", "walkandtalk", "vừa đi vừa nói", "vua di vua noi",
            "di chuyển vừa nói", "vừa đi vừa quay", "theo bước chân"
        ]
    },
    {
        "id": "voice-over",
        "name": "Voice Over",
        "icon": "🎙️",
        "keywords": [
            "voice over", "voice-over", "voiceover", "lồng tiếng", "long tieng", "thuyết minh",
            "thuyet minh", "b-roll lồng tiếng", "đọc thuyết minh", "podcast voice"
        ]
    },
    {
        "id": "talking-head",
        "name": "Talking Head",
        "icon": "🗣️",
        "keywords": [
            "talking head", "talking-head", "talkinghead", "nói trực diện", "noi truc dien",
            "ngồi nói", "ngoi noi", "chia sẻ trước máy", "trước camera", "đối diện ống kính"
        ]
    },
    {
        "id": "storytelling",
        "name": "Storytelling",
        "icon": "📖",
        "keywords": [
            "storytelling", "kể chuyện", "ke chuyen", "tự sự", "tu su", "câu chuyện",
            "cau chuyen", "hành trình", "hanh trinh", "tâm sự"
        ]
    },
    {
        "id": "dien-anh",
        "name": "Chỉn Chu",
        "icon": "🎬",
        "keywords": [
            "chỉn chu", "chỉnh chu", "chin chu", "điện ảnh", "dien anh", "cinematic", "khung hình tĩnh", "khung hinh tinh",
            "thước phim", "phim ngắn", "aesthetic"
        ]
    },
    {
        "id": "chuyen-canh",
        "name": "Chuyển Cảnh (Transition)",
        "icon": "⚡",
        "keywords": [
            "chuyển cảnh", "chuyen canh", "transition", "match cut", "whip pan", "zoom in",
            "kinetic", "cắt cảnh", "nối cảnh", "biến hình"
        ]
    }
]

# 3. Danh mục từ khóa chi tiết (Sub-keywords) tự động trích xuất thành Tags
SUB_KEYWORDS = {
    "spa-lam-dep": [
        "trị mụn", "nặn mụn", "chăm sóc da", "lăn kim", "laser", "da liễu", "skincare",
        "gội đầu dưỡng sinh", "nha khoa", "răng", "răng sứ", "filler", "botox", "before after", "trẻ hóa", "tế bào gốc"
    ],
    "thoi-trang": [
        "outfit", "lookbook", "phối đồ", "streetwear", "váy vóc", "túi xách", "giày", "sneaker", "dạo phố", "thời trang thu đông", "thời trang hè"
    ],
    "am-thuc": [
        "cafe", "cà phê", "quán cafe", "quán ăn", "nhà hàng", "nấu ăn", "nấu nướng", "bếp củi",
        "asmr", "pha chế", "món ngon", "street food", "ẩm thực đường phố", "cafe trứng"
    ],
    "du-lich": [
        "phong cảnh", "phượt", "khám phá", "nghỉ dưỡng", "resort", "khách sạn", "đà lạt", "tây bắc", "phố cổ", "checkin", "du lịch trải nghiệm"
    ],
    "cong-nghe": [
        "unboxing", "mở hộp", "máy ảnh", "camera", "gear", "gimbal", "iphone", "lens", "ống kính", "setup bàn làm việc", "đèn", "ulanzi", "sony"
    ],
    "kien-truc": [
        "không gian", "nội thất", "nhà đẹp", "nhà gỗ", "villa", "decor", "căn hộ", "slow living", "minimal", "rustic", "nhà phố"
    ],
    "the-thao": [
        "gym", "chạy bộ", "running", "thể hình", "workout", "fitness", "bơi lội", "bóng rổ", "yoga", "pilates", "thể thao ngoài trời"
    ],
    "thuong-hieu": [
        "xây kênh", "solo creator", "bán khóa học", "coaching", "tư duy", "kinh doanh", "chia sẻ bài học", "phát triển bản thân"
    ],
    "ky-thuat-quay": [
        "4 cuts", "góc máy", "cú máy", "lighting", "bố cục", "match cut", "whip pan", "slow motion", "speed ramp", "cinematic visual"
    ],
    "ugc": [
        "quảng cáo", "review", "shopee", "tiktok shop", "aida", "affiliate", "review chân thực", "đập hộp review"
    ]
}

INDUSTRY_MAP = {ind["id"]: ind for ind in INDUSTRIES}
STYLE_MAP = {st["id"]: st for st in SHOOTING_STYLES}

def clean_tag(raw: str) -> str:
    """Làm sạch và chuẩn hóa tag"""
    t = re.sub(r"^[#•\-\*\s]+", "", raw)
    t = re.sub(r"[#\s]+$", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    if not t:
        return ""
    words = t.split()
    if len(words) <= 5:
        return " ".join(w.capitalize() if not w.isupper() else w for w in words)
    return t

def normalize_for_search(text: str) -> str:
    """Chuẩn hóa chuỗi để tìm kiếm từ khóa an toàn"""
    clean_chars = []
    for ch in text.lower():
        if ch.isalnum() or ch.isspace() or ch == '_':
            clean_chars.append(ch)
        else:
            clean_chars.append(' ')
    t = "".join(clean_chars)
    return " " + re.sub(r'\s+', ' ', t).strip() + " "

def parse_user_note(raw_text: str) -> dict:
    """
    Phân tích ghi chú từ người dùng (text hoặc caption).
    Trả về dict gồm:
    - raw_note: Chuỗi gốc
    - matched_industry: Dict ngành nghề hoặc None
    - matched_style: Dict kiểu quay hoặc None
    - user_tags: Danh sách các tag người dùng chỉ định
    - cleaned_note: Nội dung ghi chú đã bóc tách
    """
    if not raw_text or not isinstance(raw_text, str):
        return {
            "raw_note": "",
            "matched_industry": None,
            "matched_style": None,
            "user_tags": [],
            "cleaned_note": ""
        }

    text = raw_text.strip()
    extracted_tags = []
    
    # 1. Bóc tách hashtag trước
    hashtags = re.findall(r"#([A-Za-z0-9_À-ỹ]+)", text)
    extracted_tags.extend([clean_tag(h.replace("_", " ")) for h in hashtags if clean_tag(h)])

    # 2. Bóc tách các mệnh đề chỉ định rõ ràng: mục / ngành / kiểu / tag
    explicit_ind_str = ""
    m_ind = re.search(r'(?:mục|ngành|chủ đề|thể loại|cho vào mục|cho vào)[\s:]+([^;\r\n\.]*?)(?=(?:\s+(?:tags?|thẻ|kiểu|style)[\s:]|$))', text, re.IGNORECASE)
    if m_ind:
        explicit_ind_str = m_ind.group(1).strip()
        
    explicit_style_str = ""
    m_sty = re.search(r'(?:kiểu|style|kiểu quay|thể loại quay)[\s:]+([^;\r\n\.]*?)(?=(?:\s+(?:tags?|thẻ|mục|ngành|chủ đề)[\s:]|$))', text, re.IGNORECASE)
    if m_sty:
        explicit_style_str = m_sty.group(1).strip()

    m_tag = re.search(r'(?:tags?|thẻ|gắn tag|gán tag|tag là|thẻ là)[\s:]+([^;\r\n\.]*?)(?=(?:\s+(?:mục|ngành|chủ đề|kiểu|style|thể loại)[\s:]|$))', text, re.IGNORECASE)
    if m_tag:
        raw_tag_str = m_tag.group(1)
        # Tách riêng hashtag nếu có trong chuỗi tag
        if '#' in raw_tag_str:
            sub_hash = re.findall(r'#([A-Za-z0-9_À-ỹ]+)', raw_tag_str)
            for sh in sub_hash:
                c_sh = clean_tag(sh.replace('_', ' '))
                if c_sh and c_sh.lower() not in [x.lower() for x in extracted_tags]:
                    extracted_tags.append(c_sh)
            raw_tag_str = re.sub(r'#[A-Za-z0-9_À-ỹ]+', '', raw_tag_str)

        parts = re.split(r'[,;/•]+', raw_tag_str)
        for p in parts:
            cleaned = clean_tag(p)
            if cleaned and cleaned.lower() not in [x.lower() for x in extracted_tags] and len(cleaned) > 1:
                extracted_tags.append(cleaned)

    # 3. Nhận diện ngành nghề (Ưu tiên mệnh đề chỉ định rõ trước)
    norm_text = normalize_for_search(text)
    matched_industry = None
    best_ind_score = 0

    if explicit_ind_str:
        norm_exp = normalize_for_search(explicit_ind_str)
        for ind in INDUSTRIES:
            for kw in ind["keywords"]:
                if f" {kw.lower()} " in norm_exp:
                    matched_industry = {
                        "id": ind["id"],
                        "name": ind["name"],
                        "icon": ind["icon"]
                    }
                    best_ind_score = 1000 + len(kw)
                    break
            if matched_industry:
                break

    if not matched_industry:
        for ind in INDUSTRIES:
            for kw in ind["keywords"]:
                search_target = f" {kw.lower()} "
                if search_target in norm_text:
                    score = len(kw)
                    if score > best_ind_score:
                        best_ind_score = score
                        matched_industry = {
                            "id": ind["id"],
                            "name": ind["name"],
                            "icon": ind["icon"]
                        }

    # 4. Nhận diện kiểu quay (Ưu tiên mệnh đề chỉ định rõ trước)
    matched_style = None
    best_style_score = 0

    if explicit_style_str:
        norm_exp = normalize_for_search(explicit_style_str)
        for st in SHOOTING_STYLES:
            for kw in st["keywords"]:
                if f" {kw.lower()} " in norm_exp:
                    matched_style = {
                        "id": st["id"],
                        "name": st["name"],
                        "icon": st["icon"]
                    }
                    best_style_score = 1000 + len(kw)
                    break
            if matched_style:
                break

    if not matched_style:
        for st in SHOOTING_STYLES:
            for kw in st["keywords"]:
                search_target = f" {kw.lower()} "
                if search_target in norm_text:
                    score = len(kw)
                    if score > best_style_score:
                        best_style_score = score
                        matched_style = {
                            "id": st["id"],
                            "name": st["name"],
                            "icon": st["icon"]
                        }

    # 5. Bóc tách các cụm từ cách nhau bởi dấu phẩy / gạch đầu dòng (Chunk extraction)
    text_for_chunks = re.sub(r'https?://[^\s]+', '', text)
    text_for_chunks = re.sub(r'#([A-Za-z0-9_À-ỹ]+)', '', text_for_chunks)
    if m_ind:
        text_for_chunks = text_for_chunks.replace(m_ind.group(0), '')
    if m_sty:
        text_for_chunks = text_for_chunks.replace(m_sty.group(0), '')
    if m_tag:
        text_for_chunks = text_for_chunks.replace(m_tag.group(0), '')

    chunks = re.split(r'[,;•\n]+', text_for_chunks)
    for ch in chunks:
        c = clean_tag(ch)
        if not c or len(c) < 2 or len(c) > 35:
            continue
        c_low = c.lower()
        if any(c_low.startswith(pfx) for pfx in ['mục:', 'mục ', 'ngành:', 'ngành ', 'kiểu:', 'kiểu quay:', 'tag:', 'thẻ:']):
            continue
        # Bỏ nếu trùng với tên ngành nghề hoặc từ khóa nhận diện ngành nghề
        if matched_industry:
            ind_info = INDUSTRY_MAP.get(matched_industry["id"], {})
            ind_kws = [k.lower() for k in ind_info.get("keywords", [])]
            if c_low == matched_industry['name'].lower() or c_low in ind_kws:
                continue
        # Bỏ nếu trùng với tên kiểu quay hoặc từ khóa nhận diện kiểu quay
        if matched_style:
            sty_info = STYLE_MAP.get(matched_style["id"], {})
            sty_kws = [k.lower() for k in sty_info.get("keywords", [])]
            if c_low == matched_style['name'].lower() or c_low in sty_kws:
                continue
        if c_low not in [x.lower() for x in extracted_tags]:
            extracted_tags.append(c)

    # 6. Tự động nhận diện Sub-Keywords (chỉ thêm nếu chưa được bao hàm trong tag dài hơn)
    for cat_id, kws in SUB_KEYWORDS.items():
        for sk in kws:
            search_sk = f" {sk.lower()} "
            if search_sk in norm_text:
                c_sk = clean_tag(sk)
                sk_low = c_sk.lower()
                # Bỏ nếu trùng tên ngành hoặc kiểu quay
                if matched_industry:
                    ind_info = INDUSTRY_MAP.get(matched_industry["id"], {})
                    if sk_low == matched_industry['name'].lower() or sk_low in [k.lower() for k in ind_info.get("keywords", [])]:
                        continue
                if matched_style:
                    sty_info = STYLE_MAP.get(matched_style["id"], {})
                    if sk_low == matched_style['name'].lower() or sk_low in [k.lower() for k in sty_info.get("keywords", [])]:
                        continue
                # Bỏ nếu tag này đã nằm gọn trong một tag dài hơn đã bóc tách
                already_covered = any(sk_low in t.lower() for t in extracted_tags)
                if not already_covered:
                    extracted_tags.append(c_sk)

    # 7. Làm sạch và chuẩn hóa danh sách tag cuối cùng
    final_tags = []
    for t in extracted_tags:
        if t and t.lower() not in [x.lower() for x in final_tags]:
            final_tags.append(t)

    return {
        "raw_note": text,
        "matched_industry": matched_industry,
        "matched_style": matched_style,
        "user_tags": final_tags,
        "cleaned_note": text
    }
