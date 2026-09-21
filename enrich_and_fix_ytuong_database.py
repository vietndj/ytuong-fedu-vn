#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enrich_and_fix_ytuong_database.py
- Sửa toàn bộ link video và báo cáo lỗi (03-07 và các item khác)
- Phân loại Chuyển cảnh Level 1 (Selfie đông người, đầu gật/lắc x2) & Chuyển cảnh Level 2 (Chân máy, cơ thể cử động rõ ràng x2)
- Đánh dấu is_ad_bot cho các video bot tải quảng cáo để tự ẩn mặc định, chỉ hiện khi vào mục UGC
- Thêm fedu_optimization cho TẤT CẢ các ý tưởng (3 mục đích: thực hành anh Việt, học viên follow creator Instagram, mẫu ngành hàng khóa học)
"""

import os, re, json, urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_PATH = os.path.join(BASE_DIR, "master_classifications.json")
SCENE_PATH = os.path.join(BASE_DIR, "scene.html")

# 1. R2 URL Video Mappings
R2_VID_MAPPINGS = {
    "IG_@shogentle_DdCRQnBI4ny_Fast_Food_Outsells_Restaurant": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DdCRQnBI4ny.mp4",
    "IG_@aidana_adilkassym_DcQy-eEOIHc_Tornado_Kick_Martial_Arts_Kinetic_Hook": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Tornado%20Kick%20Martial%20Arts%20Kinetic%20Hook%20-%20%40aidana_adilkassym.mp4",
    "IG_@critos_pro_DcxwKHYoBFv_The_Art_of_Consistency": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcxwKHYoBFv.mp4",
    "IG_@jamison.lange_DawDiT2M1p8_Coffee_Outfit_Match_Cut_Fashion": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DawDiT2M1p8.mp4",
    "IG_@mako__go_DaH7X34NTNX_Palermo_Sicily": "https://media.fedu.vn/v/BAACAgQAAxkDAANMarC3T52yht7AaZzLgvxfGxltNVgAAmQMAALnfIRR_piJ2SSCqis9BA",
    "IG_@valenti_k41_DdB_21Yo0Qc_Creative_Phone_Video_Ideas": "https://media.fedu.vn/v/BAACAgQAAxkDAAMharC0az9cEO4GN11GdoenWsh1yh0AAlALAAJ3E41RBiKMhmGGTEU9BA",
    "IG_@hey.lirules_DdBDvZph1od_Hoi_An_Natural_Mask_Transitions": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DdBDvZph1od.mp4",
    "IG_@alena.feda_Dc1w07upyNF_Food_Filming_Mastery_From_Scratch": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Food%20Filming%20%26%20Styling%20Mastery%20-%20%40alena.feda.mp4",
    "IG_@ulanzi.global_DcyS2KEm7-v_Ulanzi_LA30_RGB_Air_Tube_Light": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcyS2KEm7-v.mp4",
    "IG_@shogentle_DcyDbGmItDV_One_Lamp_Beats_Five": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DcyDbGmItDV.mp4",
    "FB_@AnhSacAnh_1964049564715249_Thuong_Hieu_Ca_Nhan_Sinh_Loi": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/Thuong_Hieu_Ca_Nhan_Sinh_Loi_Anh_Sac_Anh.mp4",
    "IG_@tsangtastic_DaB-gO6hvPX_Tory_Burch_Summer_Unboxing": "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DaB-gO6hvPX.mp4"
}

# 2. Level 1 vs Level 2 Hand-Curated Ground Truth
# Level 1: Tay cầm điện thoại selfie chỗ đông người, dùng hành động cơ thể đầu gật đầu, lắc đầu lặp lại 2 lần thành chuyển cảnh
LEVEL_1_IDS = {
    "IG_@onethebaha_DcWEp8-swbB_Seamless_Spin_Whip_Pan_Tutorial",
    "IG_@JENNY_TSANG_DXf1LldT5co_Video_by_tsangtastic",
    "IG_@Jazzie_DZzwqWBvfwT_Video_by_jazziesillona",
    "IG_@by.bennnj_DbKauxkoJU_Making_beginner_cameras_look_cinematic",
    "IG_@Jazzie_DUPo66yklxb_Video_by_jazziesillona",
    "IG_@Rilo_Dau0C9AzXc8_Video_by_17th.visuals",
    "IG_@hey.lirules_DdBDvZph1od_Hoi_An_Natural_Mask_Transitions",
    "IG_@Steven_🇻🇳_Vu_DchxEAkJ9Hw_Video_by_steven.vuu",
    "IG_@tinanguyen2004_7673468312290037012_Double_Day_luon_la_dip_de_khach_hang_lua_duoc",
    "Hong_Kong_Urban_Transitions_@withyuee",
    "IG_@Jazzie_DWERTvEjy7k_Video_by_jazziesillona",
    "IG_@Ben_Db6a3tHoWTS_Video_by_by.bennnj"
}

# Level 2: Không cần ở đông người, để điện thoại lên chân máy, bất cứ hành động cơ thể nào làm lại 2 lần rõ ràng thành chuyển cảnh
LEVEL_2_IDS = {
    "IG_@aidana_adilkassym_DcQy-eEOIHc_Tornado_Kick_Martial_Arts_Kinetic_Hook",
    "IG_@jamison.lange_DawDiT2M1p8_Coffee_Outfit_Match_Cut_Fashion",
    "REMAKE_Byjxson_Quang_Cao_Dong_Ho_Bam_Gio",
    "IG_@brandon.dtd_DcTbD0MR-V__Discipline_Motivation_Obsession",
    "IG_@mridupawasharma_Dc0tEcOIdwy_4_Cuts_Mastery",
    "IG_@critos_pro_DcxwKHYoBFv_The_Art_of_Consistency",
    "IG_@omgadrian_DcqzVfno5Al_Travel_Sequence_Formula",
    "IG_@byjxson_Dal3RFpA5nI_Project_100_Day_01",
    "IG_@valenti_k41_DctVSroI3UB_Creative_Phone_Video_Ideas",
    "IG_@valenti_k41_DdB_21Yo0Qc_Creative_Phone_Video_Ideas",
    "IG_@valenti_k41_DcL1W34I6lz_DJI_Mic_3_ASMR",
    "IG_@etaemin_DcgN1bsKUmi_Transition_Into_Running_Mode",
    "IG_@jesussropero_Dc9LUXLAHkc_Getting_Ready_Faster_Than_Ever",
    "IG_@samuelaitken__Da0eP_msVrm_Aesthetic_Routine",
    "IG_@Jazzie_DbLToEpPPzm_Video_by_jazziesillona",
    "IG_@jazziesillona_DXUG_1TjwJu_Carousel_Analysis",
    "IG_@qfroost_Dah8zTnNgq5_Ray_Ban_Meta_System",
    "IG_@layton_video_DbILcfyxZot_6_Shots_in_60_Seconds"
}

# 3. Ad Bot Video IDs (Sẽ tự động ẩn trên trang chủ, chỉ hiện khi vào mục UGC)
AD_BOT_IDS = {
    "LAZADA_Ulanzi_UA20_Đèn_LED_Thanh_Bơm_Hơi_20W_Bi",
    "SHOPEE_ULANZI_MT80_Chân_Máy_Tripod_Cao_213cm_Tả",
    "YT_Ulanzi_UA20_Air_Light_Review",
    "YT_Ulanzi_MT80_Tripod_Review"
}

def load_data():
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        master = json.load(f)
    with open(SCENE_PATH, "r", encoding="utf-8") as f:
        c = f.read()
    portal_data = json.loads(re.search(r'const portalData\s*=\s*(\[.*?\]);', c, re.DOTALL).group(1))
    return master, portal_data, c

def generate_fedu_optimization(item_id, item_title, style_name, ind_name, creator_handle, creator_name, key_tech, t_level, is_bot):
    if is_bot:
        return {
            "key_optimization_point": "Mẫu Video Quảng Cáo TMĐT chuẩn công thức AIDA & Trình diễn tính năng thực tế",
            "practice_focus": "Thực hành dựng video bán hàng sàn TMĐT: 3s đầu đập hộp gây tò mò, 5s tiếp theo test tải trọng thực tế, chốt đơn CTA rõ ràng.",
            "ig_seeding_hook": f"Theo dõi kênh phân phối sản phẩm chính hãng để cập nhật các góc máy review thiết bị quay phim mới nhất.",
            "course_industry_mapping": "Thương Mại Điện Tử, Phụ Kiện Quay Chụp & Đồ Công Nghệ",
            "transition_level": None
        }

    # If Transition Level 1
    if t_level == "Chuyển cảnh Level 1":
        return {
            "key_optimization_point": "⚡ Chuyển cảnh Level 1: Cầm tay selfie chỗ đông người, chuyển cảnh bằng cử động đầu (gật đầu / lắc đầu x2)",
            "practice_focus": "Bài tập thực hành tại phố đi bộ / TTTM: Tay cầm điện thoại selfie, kết thúc shot 1 bằng cú gật đầu dứt khoát; bắt đầu shot 2 tại góc phố khác với cú gật đầu tương tự để nối cảnh liền mạch.",
            "ig_seeding_hook": f"Follow {creator_handle} ({creator_name}) để feed Instagram tự động đẩy các gợi ý video dạo phố, phong cách street vlog tự nhiên và bắt nhịp chuyển động đời thực.",
            "course_industry_mapping": f"{ind_name} • Dạo Phố & Xây Kênh Cá Nhân Ngoài Trời",
            "transition_level": "Chuyển cảnh Level 1"
        }

    # If Transition Level 2
    if t_level == "Chuyển cảnh Level 2":
        return {
            "key_optimization_point": "⚡ Chuyển cảnh Level 2: Đặt máy lên chân máy (tripod), chuyển cảnh bằng hành động cơ thể rõ ràng lặp lại 2 lần",
            "practice_focus": "Bài tập thực hành trong phòng / bối cảnh tĩnh: Cố định điện thoại trên tripod, thực hiện 1 hành động cơ thể rõ nét (vung tay, ném đồ, dậm chân, đổi áo) lặp lại 2 lần để cắt match cut ở đỉnh quán tính.",
            "ig_seeding_hook": f"Follow {creator_handle} ({creator_name}) để thuật toán Instagram liên tục cập nhật các reel biến hình triệu view, match action chuẩn xác và cách kiểm soát nhịp dựng.",
            "course_industry_mapping": f"{ind_name} • Mẫu Biến Hình & Match Action Khóa Học video.fedu.vn",
            "transition_level": "Chuyển cảnh Level 2"
        }

    # Industry / General Optimization
    ind_mapping_str = ind_name
    if "Spa" in ind_name or "Y Tế" in ind_name:
        ind_mapping_str = "Spa Thẩm Mỹ, Phòng Khám Da Liễu & Y Khoa Trị Liệu"
        practice_str = "Bài tập quay quy trình chăm sóc da: Cận cảnh macro dụng cụ y tế, thao tác tay chuyên nghiệp của kỹ thuật viên và biểu cảm thư thái của khách."
        seeding_str = f"Follow {creator_handle} để Instagram gợi ý các video thẩm mỹ viện chuẩn y khoa, ánh sáng sạch và tone màu sang trọng."
    elif "Thời Trang" in ind_name:
        ind_mapping_str = "Thời Trang Lookbook, Phụ Kiện & Phong Cách Cá Nhân"
        practice_str = "Bài tập quay outfit 3 nhịp: Bắt đầu bằng bước chân sải dài, lia máy theo nếp vải chuyển động, kết thúc bằng dáng đứng tự tin trước background kiến trúc."
        seeding_str = f"Follow {creator_handle} để thuật toán Instagram tự động nạp các xu hướng phối đồ tối giản, góc máy thời trang châu Âu/Hàn Quốc vào feed mỗi ngày."
    elif "Ẩm Thực" in ind_name:
        ind_mapping_str = "Ẩm Thực & Nhà Hàng F&B, Quán Cafe, ASMR Nấu Nướng"
        practice_str = "Bài tập quay món ăn: Bắt trọn khói nghi ngút, cận cảnh giọt nước bắn trên chảo, kết hợp âm thanh ASMR chân thực khơi gợi vị giác."
        seeding_str = f"Follow {creator_handle} để feed Instagram liên tục cập nhật nghệ thuật quay B-roll ẩm thực, ánh sáng ấm cúng và cách setup bàn ăn hút mắt."
    elif "Công Nghệ" in ind_name:
        ind_mapping_str = "Review Thiết Bị, Mở Hộp Unboxing Đồ Công Nghệ & Gear"
        practice_str = "Bài tập unboxing 5 nhịp: Cắt xé hộp dứt khoát, quay trượt mượt mà trên bề mặt kim loại, zoom macro chi tiết nút bấm và thử nghiệm tính năng tức thì."
        seeding_str = f"Follow {creator_handle} để học cách trình bày thông số công nghệ hấp dẫn, bố cục bàn làm việc hiện đại và phong cách unboxing cuốn hút."
    elif "Kiến Trúc" in ind_name:
        ind_mapping_str = "Kiến Trúc, Nội Thất, Bất Động Sản & Không Gian Sống Slow Living"
        practice_str = "Bài tập khung hình tĩnh (Static Shot): Để máy yên trên chân máy, đón ánh nắng lọt qua rèm cửa và người lướt qua để tôn vinh đường nét không gian."
        seeding_str = f"Follow {creator_handle} để huấn luyện thuật toán Instagram đề xuất các không gian kiến trúc tối giản wabi-sabi và nhịp sống thanh bình."
    elif "Thể Thao" in ind_name:
        ind_mapping_str = "Thể Thao, Gym, Chạy Bộ Kỷ Luật & Chuyển Động Tốc Độ Cao"
        practice_str = "Bài tập quay chuyển động thể thao: Máy lia ngang theo bước chạy, góc máy thấp sát mặt đất bắt giọt mồ hôi và nhịp thở dồn dập quyết tâm."
        seeding_str = f"Follow {creator_handle} để tiếp cận kho ý tưởng video truyền cảm hứng kỷ luật, nhịp dựng nhạc beat mạnh và góc máy năng động."
    elif "Thương Hiệu" in ind_name:
        ind_mapping_str = "Thương Hiệu Cá Nhân, Chuyên Gia Chia Sẻ, Khóa Học & Coaching"
        practice_str = "Bài tập Talking Head & B-Roll kết hợp: Nói trước ống kính 1 ý tưởng đanh thép, đan xen B-roll làm việc tập trung để củng cố uy tín chuyên môn."
        seeding_str = f"Follow {creator_handle} để cập nhật các kịch bản giữ chân khán giả, cách đặt tiêu đề gây tò mò và phong thái tự tin trước ống kính."
    else:
        ind_mapping_str = f"{ind_name} • Kỹ Thuật Quay Dựng Điện Ảnh Masterclass"
        practice_str = "Bài tập bóc tách ngôn ngữ điện ảnh: Phân tích tỷ lệ khung hình, hướng sáng chính (Key Light), chiều sâu trường ảnh và tiết tấu nhịp cắt."
        seeding_str = f"Follow {creator_handle} để mở rộng tầm nhìn thẩm mỹ thị giác và nâng cao kỹ năng quay dựng chuyên nghiệp mỗi ngày."

    return {
        "key_optimization_point": f"Tối ưu cho {ind_mapping_str}: Phân loại theo cấu trúc {style_name} kết hợp kỹ thuật {key_tech or 'Điện ảnh'}",
        "practice_focus": practice_str,
        "ig_seeding_hook": seeding_str,
        "course_industry_mapping": ind_mapping_str,
        "transition_level": None
    }

def main():
    master, portal_data, scene_raw = load_data()
    print(f"Loaded {len(master)} entries from master_classifications.json")
    print(f"Loaded {len(portal_data)} entries from scene.html")

    # Update master classifications
    updated_count = 0
    l1_count = 0
    l2_count = 0
    bot_count = 0

    for k, v in master.items():
        if not isinstance(v, dict): continue
        vid_id = v.get("id") or k
        
        # Check transition level
        t_level = None
        if vid_id in LEVEL_1_IDS:
            t_level = "Chuyển cảnh Level 1"
            l1_count += 1
        elif vid_id in LEVEL_2_IDS:
            t_level = "Chuyển cảnh Level 2"
            l2_count += 1

        # Check ad bot
        is_bot = (vid_id in AD_BOT_IDS) or ("LAZADA_" in vid_id) or ("SHOPEE_" in vid_id) or ("UGC, Quảng cáo, AIDA" in str(v.get("tech_tags", [])))
        if is_bot:
            bot_count += 1

        # Fix R2 video URL if in mapping
        if vid_id in R2_VID_MAPPINGS:
            v["video_url"] = R2_VID_MAPPINGS[vid_id]
            if "media" in v:
                v["media"]["video_url"] = R2_VID_MAPPINGS[vid_id]

        # Fix duration for Tory Burch
        if "DaB-gO6hvPX" in vid_id:
            v["duration"] = "90s"

        # Generate optimization metadata
        c_handle = v.get("creator") or "@creator"
        c_name = v.get("creator_name") or "Creator"
        style_name = v.get("shooting_style", {}).get("name", "Điện Ảnh")
        ind_name = v.get("industry", {}).get("name", "Kỹ Thuật Quay Dựng")
        key_tech = ", ".join(v.get("tech_tags", []))

        opt = generate_fedu_optimization(vid_id, v.get("title", ""), style_name, ind_name, c_handle, c_name, key_tech, t_level, is_bot)
        
        v["transition_level"] = t_level
        v["is_ad_bot"] = is_bot
        v["fedu_optimization"] = opt

        # Add transition tag to tech_tags if present
        tags = list(v.get("tech_tags", []))
        if t_level and t_level not in tags:
            tags.insert(0, t_level)
            v["tech_tags"] = tags

        updated_count += 1

    # Save master_classifications.json
    with open(MASTER_PATH, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

    print(f"✓ Successfully enriched {updated_count} items in master_classifications.json")
    print(f"  - Chuyển cảnh Level 1: {l1_count} videos")
    print(f"  - Chuyển cảnh Level 2: {l2_count} videos")
    print(f"  - Ad Bot (UGC): {bot_count} videos")

    # Update scene.html video links
    scene_updated = scene_raw
    for vid_id, r2_url in R2_VID_MAPPINGS.items():
        # Match pattern where id is vid_id and update main_vid_rel & root_vid_rel
        pattern = rf'({re.escape(vid_id)}.*?)"(?:main_vid_rel|root_vid_rel)":\s*"[^"]*"'
        # Replace local video paths in scene.html with r2_url
        scene_updated = re.sub(
            rf'("id":\s*"{re.escape(vid_id)}"[^}}]*?"main_vid_rel":\s*")[^"]*(")',
            rf'\g<1>{r2_url}\g<2>',
            scene_updated
        )
        scene_updated = re.sub(
            rf'("id":\s*"{re.escape(vid_id)}"[^}}]*?"root_vid_rel":\s*")[^"]*(")',
            rf'\g<1>{r2_url}\g<2>',
            scene_updated
        )

    with open(SCENE_PATH, "w", encoding="utf-8") as f:
        f.write(scene_updated)

    print("✓ Successfully updated video URLs in scene.html")

if __name__ == "__main__":
    main()
