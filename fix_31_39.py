import json

with open("master_classifications.json", "r", encoding="utf-8") as f:
    master = json.load(f)

# Define new style
style_nhac = {"id": "theo-nhip-nhac", "name": "Theo nhịp nhạc", "icon": "🎵"}

# 31 - 1
vid31 = "IG_@cushygarden_DdL6pHDSKRc"
if vid31 in master:
    master[vid31]["shooting_style"] = {"id": "dien-anh", "name": "Chỉn Chu", "icon": "🎬"}
    master[vid31]["industries"] = [{"id": "kien-truc", "name": "Góc nhà đẹp", "icon": "🏛️"}]
    master[vid31]["x_factors"] = ["Bầu không khí chữa lành", "Đặc tả Macro"]
    master[vid31]["purpose"] = "Thưởng thức"

# 32 - 2, kiểu: Theo nhịp nhạc
vid32 = "IG_@dev_zero_Db-S8i1hXwF"
if vid32 in master:
    master[vid32]["shooting_style"] = style_nhac
    master[vid32]["industries"] = [{"id": "thuong-hieu", "name": "Xây kênh", "icon": "💼"}]
    master[vid32]["x_factors"] = []
    master[vid32]["purpose"] = "VLog"

# 33 - 2, kiểu: Theo nhịp nhạc, vlog
vid33 = "IG_@nagisa.decor_Dco_DevvUla"
if vid33 in master:
    master[vid33]["shooting_style"] = style_nhac
    master[vid33]["industries"] = [{"id": "kien-truc", "name": "Góc nhà đẹp", "icon": "🏛️"}]
    master[vid33]["x_factors"] = []
    master[vid33]["purpose"] = "VLog"

# 34 - 1
vid34 = "IG_@yuto_creator_DdBlAWRO1Hl"
if vid34 in master:
    master[vid34]["shooting_style"] = {"id": "dien-anh", "name": "Chỉn Chu", "icon": "🎬"}
    master[vid34]["industries"] = [
        {"id": "du-lich", "name": "Du lịch", "icon": "✈️"},
        {"id": "ky-thuat-quay", "name": "Bố cục", "icon": "🎯"}
    ]
    master[vid34]["x_factors"] = ["Màu sắc điện ảnh", "Moody vibe"]
    master[vid34]["purpose"] = "Thưởng thức"

# 35 - 1 kiểu: theo nhịp nhạc
vid35 = "IG_@beixin_DdRGd8evPK-"
if vid35 in master:
    master[vid35]["shooting_style"] = style_nhac
    master[vid35]["industries"] = [
        {"id": "du-lich", "name": "Du lịch", "icon": "✈️"},
        {"id": "ky-thuat-quay", "name": "Bố cục", "icon": "🎯"}
    ]
    master[vid35]["x_factors"] = ["Minh họa trực quan", "Setup điện thoại"]
    master[vid35]["purpose"] = "Mẹo"

# 36 - 1
vid36 = "IG_@layton_video_DdKGq2TMhf4"
if vid36 in master:
    master[vid36]["shooting_style"] = {"id": "talking-head", "name": "Nói Trực Diện", "icon": "🗣️"}
    master[vid36]["industries"] = [{"id": "thuong-hieu", "name": "Xây kênh", "icon": "💼"}]
    master[vid36]["x_factors"] = ["Góc nhìn chân thật", "Kịch tính"]
    master[vid36]["purpose"] = "Tạo động lực"

with open("master_classifications.json", "w", encoding="utf-8") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

# Check 37, 38, 39
vid37 = "IG_@kienobifilms_DdPLvUpBwCl"
vid38 = "IG_@aki_japan_DaDFH_TSii8"
vid39 = "IG_@nathanael.lct_DdRg_ybtlKI"

for vid, label in zip([vid37, vid38, vid39], ["37", "38", "39"]):
    if vid in master:
        data = master[vid]
        style = data.get("shooting_style", {}).get("name", "Chưa có")
        inds = ", ".join([i.get("name", "") for i in data.get("industries", [])])
        x = ", ".join(data.get("x_factors", []))
        p = data.get("purpose", "Chưa có")
        print(f"#{label} - Kiểu: {style} | Ngành: {inds} | Mục đích: {p} | X-Factor: {x}")
    else:
        print(f"#{label} not found")

