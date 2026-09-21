import json, os, re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_PATH = os.path.join(BASE_DIR, "master_classifications.json")

with open(MASTER_PATH, "r", encoding="utf-8") as f:
    master = json.load(f)

# Define full rich data for the 10 missing items
missing_data = [
    {
        "id": "IG_@tsangtastic_DaB-gO6hvPX_Tory_Burch_Summer_Unboxing",
        "shortcode": "DaB-gO6hvPX",
        "creator": "@tsangtastic",
        "creator_name": "Jenny Tsang",
        "title": "Jenny Tsang • Nghệ Thuật Mở Hộp Rương Mùa Hè Tory Burch & Phối Đồ Điện Ảnh",
        "shots_count": 22,
        "duration": "90s",
        "shooting_style": {
            "id": "dien-anh",
            "name": "Điện Ảnh (Cinematic)",
            "icon": "🎬"
        },
        "industry": {
            "id": "thoi-trang",
            "name": "Thời Trang & Phụ Kiện",
            "icon": "👔"
        },
        "country": {
            "id": "asia_other",
            "name": "Châu Á Khác",
            "en_name": "Other Asia",
            "flag": "🌏",
            "badge_color": "sky"
        },
        "purpose": "Mở hộp bộ sưu tập mùa hè Tory Burch kết hợp phối đồ Lookbook cao cấp",
        "tech_tags": [
            "Chuyển cảnh Level 1",
            "Cinematic Unboxing",
            "High-End Fashion Grading",
            "Macro Texture Shot",
            "Dynamic Whip Pan Transition",
            "Natural Ambient Lighting"
        ],
        "transition_level": "Chuyển cảnh Level 1",
        "is_ad_bot": False,
        "logic_explanation": "Jenny Tsang kết hợp mở hộp rương quà tặng thủ công với các nhịp dạo phố, cầm máy selfie chuyển động xoay người và gật đầu đổi góc nhìn thời trang thanh lịch.",
        "quick_takeaway": "Nghệ thuật đập hộp thời trang cao cấp kết hợp dạo phố Lookbook: Sự hòa quyện giữa macro chi tiết da thuộc, chuyển động cơ thể nhẹ nhàng và tone màu điện ảnh ấm áp.",
        "video_url": "https://media.fedu.vn/v/BAACAgUAAxkDAAMCar...",
        "report_url": "reports/IG_@tsangtastic_DaB-gO6hvPX_Tory_Burch_Summer_Unboxing.html",
        "fedu_optimization": {
            "key_optimization_point": "⚡ Chuyển cảnh Level 1: Cầm tay selfie Lookbook thời trang, chuyển cảnh bằng cử động đầu và xoay máy nhẹ nhàng",
            "practice_focus": "Bài tập mở hộp thời trang: Quay cận cảnh mở hộp trên bàn, sau đó cầm máy dạo bước selfie qua góc phố, kết thúc shot bằng cú gật đầu dứt khoát đổi set đồ.",
            "ig_seeding_hook": "Follow @tsangtastic để thuật toán Instagram liên tục cập nhật phong cách thời trang Hong Kong / New York, kỹ thuật unboxing đồ hiệu tinh tế.",
            "course_industry_mapping": "Thời Trang & Lookbook Phụ Kiện Cao Cấp"
        }
    },
    {
        "id": "IG_@shogentle_DdCRQnBI4ny_Fast_Food_Outsells_Restaurant",
        "shortcode": "DdCRQnBI4ny",
        "creator": "@shogentle",
        "creator_name": "AL (Shogentle)",
        "title": "Triết Lý Fast Food Outsells Restaurant: Ẩn Dụ Thị Giác & Giữ Chân Khán Giả",
        "shots_count": 16,
        "duration": "32s",
        "shooting_style": {
            "id": "storytelling",
            "name": "Storytelling",
            "icon": "📖"
        },
        "industry": {
            "id": "thuong-hieu",
            "name": "Thương Hiệu Cá Nhân & Dịch Vụ",
            "icon": "💼"
        },
        "country": {
            "id": "japan",
            "name": "Nhật Bản",
            "en_name": "Japan",
            "flag": "🇯🇵",
            "badge_color": "rose"
        },
        "purpose": "Phân tích tư duy sáng tạo nội dung: Ẩn dụ thức ăn nhanh vs nhà hàng cao cấp",
        "tech_tags": [
            "Visual Metaphor",
            "Chiaroscuro Light",
            "Match Action Cut",
            "Storytelling Pacing",
            "Split Screen Narrative"
        ],
        "transition_level": None,
        "is_ad_bot": False,
        "logic_explanation": "Sử dụng ẩn dụ bánh burger và đĩa steak để lý giải vì sao nội dung ngắn gọn, dễ tiêu hóa lại tiếp cận hàng triệu khán giả dễ hơn nội dung quá hàn lâm.",
        "quick_takeaway": "Nghệ thuật truyền tải bài học kinh doanh qua hình ảnh ẩn dụ: Ánh sáng Chiaroscuro tương phản sâu, nhịp cắt đanh thép và thông điệp thực chiến chạm trần nhận thức.",
        "video_url": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DdCRQnBI4ny.mp4",
        "report_url": "reports/IG_@shogentle_DdCRQnBI4ny_Fast_Food_Outsells_Restaurant.html",
        "fedu_optimization": {
            "key_optimization_point": "Tối ưu cho Xây Kênh & Storytelling: Ẩn dụ thị giác (Visual Metaphor) kết hợp ánh sáng điện ảnh tương phản",
            "practice_focus": "Bài tập Talking Head & B-Roll ẩn dụ: Chọn 1 đồ vật quen thuộc (ly nước, đồng hồ) để giải thích một khái niệm phức tạp trong 30 giây.",
            "ig_seeding_hook": "Follow @shogentle để feed Instagram xuất hiện đều đặn các video tư duy điện ảnh, màu phim Nhật Bản hoài niệm và triết lý sống tối giản.",
            "course_industry_mapping": "Thương Hiệu Cá Nhân, Đào Tạo & Kể Chuyện Thương Mại"
        }
    },
    {
        "id": "IG_@aidana_adilkassym_DcQy-eEOIHc_Tornado_Kick_Martial_Arts_Kinetic_Hook",
        "shortcode": "DcQy-eEOIHc",
        "creator": "@aidana_adilkassym",
        "creator_name": "Aidana Adilkassym",
        "title": "Aidana • Tornado Kick Martial Arts Kinetic Hook & Match Action Chân Máy",
        "shots_count": 7,
        "duration": "14s",
        "shooting_style": {
            "id": "chuyen-canh",
            "name": "Chuyển Cảnh (Transition)",
            "icon": "⚡"
        },
        "industry": {
            "id": "the-thao",
            "name": "Thể Thao & Năng Động",
            "icon": "🏃"
        },
        "country": {
            "id": "asia_other",
            "name": "Châu Á Khác",
            "en_name": "Other Asia",
            "flag": "🌏",
            "badge_color": "sky"
        },
        "purpose": "Hook động lực học 3s đầu bằng cú đá xoay Tornado Kick nối cảnh chân máy",
        "tech_tags": [
            "Chuyển cảnh Level 2",
            "Momentum Match Cut",
            "Tornado Kick Hook",
            "Tripod Fixed Framing",
            "Fabric Physics Motion",
            "Kinetic Visual Impact"
        ],
        "transition_level": "Chuyển cảnh Level 2",
        "is_ad_bot": False,
        "logic_explanation": "Điện thoại cố định trên tripod, nhân vật tung cú đá xoay người dứt khoát; nhát cắt thứ hai tiếp nối chính xác ở góc máy khác cùng quán tính xoay tạo ra cú chuyển cảnh bùng nổ.",
        "quick_takeaway": "Mẫu chuyển cảnh Level 2 chuẩn mực: Điện thoại đặt chân máy cố định, lặp lại cú đá xoay 2 lần ở 2 bối cảnh khác nhau tạo thành cú Match Cut giật gân triệu view.",
        "video_url": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Tornado%20Kick%20Martial%20Arts%20Kinetic%20Hook%20-%20%40aidana_adilkassym.mp4",
        "report_url": "reports/Tornado Kick Martial Arts Kinetic Hook - @aidana_adilkassym.html",
        "fedu_optimization": {
            "key_optimization_point": "⚡ Chuyển cảnh Level 2: Đặt máy lên chân máy (tripod), hành động cơ thể vung chân đá lặp lại 2 lần nối quán tính (Momentum Match Cut)",
            "practice_focus": "Bài tập Chuyển cảnh Level 2: Đặt điện thoại lên chân máy ngang tầm thắt lưng, tung một động tác dứt khoát (vung tay hoặc đá chân) 2 lần tại 2 vị trí khác nhau để cắt nối.",
            "ig_seeding_hook": "Follow @aidana_adilkassym để thuật toán Instagram liên tục đề xuất các video võ thuật, chuyển động kinetic và kỹ xảo match cut đỉnh cao.",
            "course_industry_mapping": "Thể Thao, Võ Thuật, Fitness & Quán Tính Điện Ảnh (Khóa học video.fedu.vn)"
        }
    },
    {
        "id": "IG_@critos_pro_DcxwKHYoBFv_The_Art_of_Consistency",
        "shortcode": "DcxwKHYoBFv",
        "creator": "@critos_pro",
        "creator_name": "Critos Pro",
        "title": "Critos Pro • The Art of Consistency: Bàn Làm Việc Công Nghệ & Match Cut Cố Định",
        "shots_count": 17,
        "duration": "10s",
        "shooting_style": {
            "id": "chuyen-canh",
            "name": "Chuyển Cảnh (Transition)",
            "icon": "⚡"
        },
        "industry": {
            "id": "cong-nghe",
            "name": "Công Nghệ & Thiết Bị",
            "icon": "📱"
        },
        "country": {
            "id": "us_eu",
            "name": "Âu Mỹ",
            "en_name": "US & Europe",
            "flag": "🇺🇸/🇪🇺",
            "badge_color": "purple"
        },
        "purpose": "Trình diễn quy trình làm việc kỷ luật tại bàn làm việc với match cut đồ vật",
        "tech_tags": [
            "Chuyển cảnh Level 2",
            "Desk Setup B-Roll",
            "Object Placement Match Cut",
            "Top-Down POV",
            "Micro-Beats Editing"
        ],
        "transition_level": "Chuyển cảnh Level 2",
        "is_ad_bot": False,
        "logic_explanation": "Chân máy cố định góc nhìn từ trên xuống (Top-Down POV), các thao tác tay đặt chuột, gõ bàn phím và đặt tách trà được lặp lại nhịp nhàng tạo chuỗi chuyển cảnh mượt như nhung.",
        "quick_takeaway": "Nghệ thuật dựng video bàn làm việc công nghệ: Đặt điện thoại cố định trên chân máy, cắt cảnh theo từng cú chạm tay dứt khoát 15 micro-beats.",
        "video_url": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcxwKHYoBFv.mp4",
        "report_url": "reports/The Art of Consistency - @critos_pro.html",
        "fedu_optimization": {
            "key_optimization_point": "⚡ Chuyển cảnh Level 2: Đặt máy cố định trên bàn làm việc, thao tác tay đặt đồ vật lặp lại 2 lần",
            "practice_focus": "Bài tập quay Desk Setup: Đặt máy chân máy cố định cạnh bàn, thực hiện động tác mở laptop và bấm phím lặp lại ở ánh sáng ban ngày và ban đêm để nối cảnh.",
            "ig_seeding_hook": "Follow @critos_pro để Instagram gợi ý các góc máy setup bàn làm việc tối giản, góc quay gear công nghệ đẹp mắt.",
            "course_industry_mapping": "Công Nghệ, Thiết Bị Văn Phòng & Kỷ Luật Creator"
        }
    },
    {
        "id": "IG_@jamison.lange_DawDiT2M1p8_Coffee_Outfit_Match_Cut_Fashion",
        "shortcode": "DawDiT2M1p8",
        "creator": "@jamison.lange",
        "creator_name": "Jamison Lange",
        "title": "Jamison Lange • Coffee + Outfit Match Cut Transition: Biến Hình Thời Trang Chân Máy",
        "shots_count": 22,
        "duration": "44s",
        "shooting_style": {
            "id": "chuyen-canh",
            "name": "Chuyển Cảnh (Transition)",
            "icon": "⚡"
        },
        "industry": {
            "id": "thoi-trang",
            "name": "Thời Trang & Phụ Kiện",
            "icon": "👔"
        },
        "country": {
            "id": "us_eu",
            "name": "Âu Mỹ",
            "en_name": "US & Europe",
            "flag": "🇺🇸/🇪🇺",
            "badge_color": "purple"
        },
        "purpose": "Chuyển cảnh biến hình outfit bằng hành động nâng ly cà phê và dậm chân",
        "tech_tags": [
            "Chuyển cảnh Level 2",
            "Outfit Change Transition",
            "Coffee Cup Wipe",
            "Fixed Tripod Match Cut",
            "Streetwear Color Blocking"
        ],
        "transition_level": "Chuyển cảnh Level 2",
        "is_ad_bot": False,
        "logic_explanation": "Điện thoại cố định trên chân máy, Jamison thực hiện động tác nâng ly cà phê che ống kính hoặc dậm gót giày 2 lần ở 2 bộ trang phục khác nhau để chuyển cảnh mượt mà.",
        "quick_takeaway": "Bài tập kinh điển của khóa học video.fedu.vn: Điện thoại để chân máy, nâng ly cà phê hoặc dậm chân 2 lần thành chuyển cảnh biến hình thời trang triệu view.",
        "video_url": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DawDiT2M1p8.mp4",
        "report_url": "reports/Coffee + Outfit Match Cut Transition - @jamison.lange.html",
        "fedu_optimization": {
            "key_optimization_point": "⚡ Chuyển cảnh Level 2: Đặt máy lên chân máy (tripod), dùng hành động nâng cốc cà phê / dậm chân lặp lại 2 lần để đổi trang phục",
            "practice_focus": "Bài tập Chuyển cảnh Level 2 biến hình: Để điện thoại lên chân máy tại nhà, mặc bộ đồ 1 nâng ly cafe lên trước ngực; thay bộ đồ 2 đứng đúng vị trí hạ ly cafe xuống.",
            "ig_seeding_hook": "Follow @jamison.lange để thuật toán Instagram liên tục đổ về các ý tưởng chuyển cảnh biến hình thời trang nam, phối đồ đường phố sành điệu.",
            "course_industry_mapping": "Thời Trang Nam, Đồ Uống Cafe & Chuyển Cảnh Biến Hình (Khóa học video.fedu.vn)"
        }
    },
    {
        "id": "IG_@주서방_DcvmVl2hbuY_Video_by_ju_seobang",
        "shortcode": "DcvmVl2hbuY",
        "creator": "@주서방",
        "creator_name": "Ju Seobang",
        "title": "Ju Seobang • Vlog Đời Thường Hàn Quốc & Nhịp Sống Chữa Lành Yên Bình",
        "shots_count": 8,
        "duration": "16s",
        "shooting_style": {
            "id": "storytelling",
            "name": "Storytelling",
            "icon": "📖"
        },
        "industry": {
            "id": "kien-truc",
            "name": "Kiến Trúc & Không Gian Sống",
            "icon": "🏛️"
        },
        "country": {
            "id": "korea",
            "name": "Hàn Quốc",
            "en_name": "South Korea",
            "flag": "🇰🇷",
            "badge_color": "pink"
        },
        "purpose": "Ghi lại nhịp sống thường nhật thư thái chuẩn thẩm mỹ chữa lành Hàn Quốc",
        "tech_tags": [
            "Korean Healing Vlog",
            "Clean Framing",
            "Soft Natural Light",
            "Slow Living Rhythm"
        ],
        "transition_level": None,
        "is_ad_bot": False,
        "logic_explanation": "Khung hình trong trẻo, nhịp sống đời thường chậm rãi, ánh sáng tự nhiên mềm mại.",
        "quick_takeaway": "Nghệ thuật quay Daily Vlog Hàn Quốc: Khung hình sạch sẽ, nhịp thở bình dị tôn vinh vẻ đẹp của không gian sống gia đình ấm áp.",
        "video_url": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcvmVl2hbuY.mp4",
        "report_url": "reports/IG_@주서방_DcvmVl2hbuY_Video_by_ju_seobang.html",
        "fedu_optimization": {
            "key_optimization_point": "Tối ưu cho Không Gian Sống & Daily Vlog: Bố cục tĩnh, ánh sáng tự nhiên mềm và màu sắc trong trẻo chuẩn Hàn Quốc",
            "practice_focus": "Bài tập quay góc rộng trong nhà: Đặt máy ở góc phòng, bắt trọn khoảnh khắc pha trà hoặc đọc sách buổi sáng.",
            "ig_seeding_hook": "Follow @ju_seobang để Instagram gợi ý các video đời sống gia đình chữa lành và màu phim pastel ấm áp.",
            "course_industry_mapping": "Đời Sống, Kiến Trúc Nhà Ở & Thẩm Mỹ Chữa Lành"
        }
    },
    {
        "id": "IG_@layton_video_DbILcfyxZot_6_Shots_in_60_Seconds",
        "shortcode": "DbILcfyxZot",
        "creator": "@layton_video",
        "creator_name": "Layton",
        "title": "Layton • 6 Góc Máy Trong 60 Giây: Thao Lược B-Roll Thần Tốc Cầu Đi Bộ",
        "shots_count": 6,
        "duration": "12s",
        "shooting_style": {
            "id": "chuyen-canh",
            "name": "Chuyển Cảnh (Transition)",
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
        "purpose": "Hướng dẫn 6 góc máy B-roll siêu nhanh tại một địa điểm duy nhất",
        "tech_tags": [
            "Chuyển cảnh Level 2",
            "6 Shots Formula",
            "Focal Length Variety",
            "Foreground Wipe",
            "Quick Sequence"
        ],
        "transition_level": "Chuyển cảnh Level 2",
        "is_ad_bot": False,
        "logic_explanation": "Chỉ đứng tại một cây cầu đi bộ, sử dụng chân máy và góc máy thay đổi tiêu cự nhanh (toàn - trung - cận) để tạo chuỗi B-roll điện ảnh sống động.",
        "quick_takeaway": "Công thức 6 góc máy thần tốc: Thay đổi tiêu cự từ Macro đến Ultra-wide để tối ưu hóa địa điểm quay trong thời gian ngắn nhất.",
        "video_url": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DbILcfyxZot.mp4",
        "report_url": "reports/IG_@layton_video_DbILcfyxZot_6_Shots_in_60_Seconds.html",
        "fedu_optimization": {
            "key_optimization_point": "⚡ Chuyển cảnh Level 2: Công thức 6 góc máy chân máy thần tốc (Toàn - Trung - Cận - Chi tiết)",
            "practice_focus": "Bài tập quay B-roll 1 địa điểm: Đứng tại 1 vị trí (công viên, cầu thang), quay 6 shot chỉ bằng cách đổi góc máy và động tác chân máy.",
            "ig_seeding_hook": "Follow @layton_video để feed Instagram nạp các tip quay video bằng điện thoại nhanh gọn, thực chiến.",
            "course_industry_mapping": "Kỹ Thuật B-Roll Thực Chiến Cho Mọi Ngành Hàng (Khóa học video.fedu.vn)"
        }
    }
]

for item in missing_data:
    vid_id = item["id"]
    code = item["shortcode"]
    master[vid_id] = item
    master[code] = item
    print(f"Added missing item to master: {vid_id} (code: {code})")

with open(MASTER_PATH, "w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=2)

print(f"\n✓ Successfully updated master_classifications.json! Total keys: {len(master)}")
