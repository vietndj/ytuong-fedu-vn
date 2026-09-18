import re

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/feedback_learner.py', 'r', encoding='utf-8') as f:
    content = f.read()

# I want to rewrite parse_feedback_command and apply_feedback entirely.
# Let's find the boundaries of the functions.

start = content.find("def parse_feedback_command(command_str):")
end = content.find("def show_stats():")

if start != -1 and end != -1:
    new_funcs = """def parse_feedback_command(command_str):
    cmd = command_str.strip()
    if cmd.upper().startswith("SUA:"):
        cmd = cmd[4:].strip()
    elif cmd.upper().startswith("SỬA:"):
        cmd = cmd[4:].strip()

    parts = cmd.split("->")
    if len(parts) != 2:
        return None, None, [], [], []

    target_ref = parts[0].strip()
    correction_part = parts[1].strip()

    reason = ""
    if "lý do:" in correction_part.lower():
        sub_parts = re.split(r'lý do:|ly do:', correction_part, flags=re.IGNORECASE)
        correction_part = sub_parts[0].strip()
        reason = sub_parts[1].strip()

    elements = [e.strip() for e in re.split(r'[,;]+', correction_part) if e.strip()]

    target_style = None
    target_industries = []
    x_factors = []
    tags = []

    for el in elements:
        low = el.lower()
        if low.startswith("biểu cảm") or low.startswith("điểm nhấn"):
            x_factors.append(el)
            continue

        matched_ind = INDUSTRY_ALIASES.get(low)
        matched_sty = STYLE_ALIASES.get(low)

        if matched_ind:
            target_industries.append(matched_ind)
        elif matched_sty and not target_style:
            target_style = matched_sty
        elif low in ["giọng nói", "body language", "hook", "giọng nói điệu đà", "kịch tính"]:
            x_factors.append(el)
        else:
            tags.append(el)

    return target_ref, target_style, list(set(target_industries)), x_factors, reason

def apply_feedback(command_str):
    print("=" * 70)
    print("🧠 ANTIGRAVITY ACTIVE LEARNING ENGINE - TIẾP NHẬN PHẢN HỒI ANH VIỆT")
    print("=" * 70)

    target_ref, new_style, new_inds, new_xfactors, reason = parse_feedback_command(command_str)
    if not target_ref:
        print("❌ Cú pháp chưa đúng. Vui lòng dùng: SUA: #id -> [Kiểu quay], [Ngành 1], [Ngành 2], [Biểu cảm...], Lý do: [Giải thích]")
        return False

    master_db = load_json(MASTER_PATH, {})
    vid_id, item = find_target_video(target_ref, master_db)

    if not vid_id:
        print(f"❌ Không tìm thấy video tương ứng với mốc '{target_ref}' trong master database.")
        return False

    old_style = item.get("shooting_style", {}).get("id", "chua-ro")
    old_inds = [i.get("id") for i in item.get("industries", [])]
    old_x = item.get("x_factors", [])
    title = item.get("title", "Video không tiêu đề")
    creator = item.get("creator", "Creator")

    print(f"\\n🎯 [Xác nhận đối tượng]: #{item.get('index')} - {title} ({creator})")
    print(f"   ID: {vid_id}")
    print(f"   • Trạng thái cũ AI đoán: Kiểu quay: {old_style} | Ngành: {old_inds} | X-Factor: {old_x}")
    print(f"   • Anh Việt hiệu chỉnh:   Kiểu quay: {new_style or '(giữ nguyên)'} | Ngành: {new_inds or '(giữ nguyên)'} | X-Factor: {new_xfactors or '(giữ nguyên)'}")
    if reason:
        print(f"   • Lý do anh Việt ghi chú: \\"{reason}\\"")

    # 1. Cập nhật master_classifications.json
    if new_inds:
        item["industries"] = []
        for ind in new_inds:
            ind_obj = INDUSTRY_MAP.get(ind, {"id": ind, "name": ind.replace("-", " ").title(), "icon": "✨"})
            item["industries"].append({
                "id": ind_obj["id"],
                "name": ind_obj["name"],
                "icon": ind_obj.get("icon", "✨")
            })
    if new_style:
        sty_obj = STYLE_MAP.get(new_style, {"id": new_style, "name": new_style.replace("-", " ").title(), "icon": "🎬"})
        item["shooting_style"] = {
            "id": sty_obj["id"],
            "name": sty_obj["name"],
            "icon": sty_obj.get("icon", "🎬")
        }
    if new_xfactors:
        item["x_factors"] = list(set(item.get("x_factors", []) + new_xfactors))
        
    master_db[vid_id] = item
    save_json(MASTER_PATH, master_db)
    print("✅ [1/3] Đã đồng bộ mỏ neo chuẩn (Anchor) vào master_classifications.json")

    # 2. Ghi nhật ký học tập vào LEARNED_PATTERNS.json
    patterns = load_json(PATTERNS_PATH, {
        "learning_stats": {"total_corrections": 0, "current_alignment_score": 85.0},
        "learning_history_logs": []
    })
    
    log_entry = {
        "video_id": vid_id,
        "video_title": title,
        "ai_predicted": {
            "industries": old_inds,
            "shooting_style": old_style,
            "x_factors": old_x
        },
        "mentor_corrected": {
            "industries": new_inds or old_inds,
            "shooting_style": new_style or old_style,
            "x_factors": item["x_factors"]
        },
        "reason_distilled": reason or "Hiệu chỉnh trực tiếp từ Super Mentor anh Việt",
        "learned_at": datetime.now().isoformat()
    }

    patterns.setdefault("learning_history_logs", []).append(log_entry)
    patterns.setdefault("learning_stats", {})["total_corrections"] = len(patterns["learning_history_logs"])
    
    save_json(PATTERNS_PATH, patterns)
    print("✅ [2/3] Đã đúc kết bài học & ghi nhật ký vĩnh viễn vào LEARNED_PATTERNS.json")

    # 3. Tự động trigger build_ideas_bank.py
    print("⏳ [3/3] Đang dịch biên dịch lại hệ thống (build_ideas_bank)...")
    exit_code = os.system(f"python3 {BUILD_SCRIPT_PATH}")
    if exit_code == 0:
        print("✅ Biên dịch UI thành công! F5 trình duyệt để xem kết quả.")
    else:
        print("❌ Lỗi biên dịch. Vui lòng kiểm tra lại build_ideas_bank.py")

"""
    content = content[:start] + new_funcs + content[end:]
    with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/feedback_learner.py', 'w', encoding='utf-8') as f:
        f.write(content)

