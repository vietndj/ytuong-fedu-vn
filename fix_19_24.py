import json

with open("master_classifications.json", "r", encoding="utf-8") as f:
    master = json.load(f)

# #19: Phương án 2
vid19 = "IG_@𝐂𝐢𝐧𝐝𝐲🌼_DcgQDZ_JNIr_Video_by_clarissaacindy"
if vid19 in master:
    master[vid19]["shooting_style"] = {"id": "walk-and-talk", "name": "Walk and Talk", "icon": "🚶"}
    master[vid19]["industries"] = [
        {"id": "du-lich", "name": "Du lịch", "icon": "✈️"},
        {"id": "ky-thuat-quay", "name": "Bố cục", "icon": "🎯"}
    ]
    master[vid19]["x_factors"] = []

# #20: Xóa khỏi hệ thống
vid20 = "IG_@Jackson_Sword_DdU4rBeMXZt_Video_by_byjacksonsword"
if vid20 in master:
    del master[vid20]
    print(f"Deleted {vid20}")

# #22: Phương án 1
vid22 = "IG_@Pascal_Blaurock_DdT9CF7tGzn_Video_by_pascal_blaurock"
if vid22 in master:
    master[vid22]["shooting_style"] = {"id": "dien-anh", "name": "Chỉn Chu", "icon": "🎬"}
    master[vid22]["industries"] = [
        {"id": "ky-thuat-quay", "name": "Bố cục", "icon": "🎯"}
    ]
    master[vid22]["x_factors"] = ["Thủ thuật sáng tạo", "Setup Studio"]

# #23: Phương án 1
vid23 = "IG_@Megan_Tan_DdT4EOzveQL_Video_by_megantanhweewen"
if vid23 in master:
    master[vid23]["shooting_style"] = {"id": "storytelling", "name": "Kể Chuyện", "icon": "📖"}
    master[vid23]["industries"] = [
        {"id": "cong-nghe", "name": "Công nghệ", "icon": "📱"},
        {"id": "ugc", "name": "UGC", "icon": "📱"}
    ]
    master[vid23]["x_factors"] = ["Góc máy trên cao", "Không khí Sit-com"]

# #24: Phương án 1
vid24 = "IG_@신_유은_yueun_shin_DdQwL3Ahci1_Video_by_yuuxeun"
if vid24 in master:
    master[vid24]["shooting_style"] = {"id": "dien-anh", "name": "Chỉn Chu", "icon": "🎬"}
    master[vid24]["industries"] = [
        {"id": "thoi-trang", "name": "Thời trang", "icon": "👔"},
        {"id": "du-lich", "name": "Du lịch", "icon": "✈️"}
    ]
    master[vid24]["x_factors"] = ["Nhan sắc", "Thần thái tự nhiên"]

with open("master_classifications.json", "w", encoding="utf-8") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)
