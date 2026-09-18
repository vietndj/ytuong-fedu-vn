import json

with open("master_classifications.json", "r", encoding="utf-8") as f:
    master = json.load(f)

# 25: PA 2, mục đích thần thái -> Thực ra 'thần thái' hợp với x_factors
vid25 = "IG_@3413882081_Dcx7pQpS6zs_Video_by_syooaann"
if vid25 in master:
    master[vid25]["shooting_style"] = {"id": "dien-anh", "name": "Chỉn Chu", "icon": "🎬"}
    master[vid25]["industries"] = [{"id": "thoi-trang", "name": "Thời trang", "icon": "👔"}]
    master[vid25]["x_factors"] = ["Thần thái"]
    master[vid25]["purpose"] = "VLog"

# 26: storytelling, xây kênh, vlog, thông điệp cảm xúc, chuyển cảnh cấp 2
vid26 = "IG_@Megan_Tan_DOd8XMMjxcH_Video_by_megantanhweewen"
if vid26 in master:
    master[vid26]["shooting_style"] = {"id": "storytelling", "name": "Kể Chuyện", "icon": "📖"}
    master[vid26]["industries"] = [{"id": "thuong-hieu", "name": "Xây kênh", "icon": "💼"}]
    master[vid26]["x_factors"] = ["Thông điệp cảm xúc", "Chuyển cảnh cấp 2"]
    master[vid26]["purpose"] = "VLog"

# 27: PA 1 + chuyển cảnh cấp 2
vid27 = "IG_@Caleb_Natale_Dcbn7Bix-X-_Video_by_calebnatale"
if vid27 in master:
    master[vid27]["shooting_style"] = {"id": "chuyen-canh", "name": "Chuyển Cảnh", "icon": "⚡"}
    master[vid27]["industries"] = [
        {"id": "ky-thuat-quay", "name": "Bố cục", "icon": "🎯"},
        {"id": "du-lich", "name": "Du lịch", "icon": "✈️"}
    ]
    master[vid27]["x_factors"] = ["Kỹ xảo VFX", "Setup thông minh", "Chuyển cảnh cấp 2"]
    master[vid27]["purpose"] = "Mẹo"

# 28: walk and talk, xay kenh, mẹo
vid28 = "IG_@AL,_The_Creator_Videography_Reels_DdTeHleIqkg_Video_by_shogentle"
if vid28 in master:
    master[vid28]["shooting_style"] = {"id": "walk-and-talk", "name": "Walk and Talk", "icon": "🚶"}
    master[vid28]["industries"] = [{"id": "thuong-hieu", "name": "Xây kênh", "icon": "💼"}]
    master[vid28]["x_factors"] = ["Ánh sáng màu kịch tính", "Typography mạnh"]
    master[vid28]["purpose"] = "Mẹo"

# 29: PA 1
vid29 = "IG_@iman.lizi_Dc6qXoKoYKh"
if vid29 in master:
    master[vid29]["shooting_style"] = {"id": "dien-anh", "name": "Chỉn Chu", "icon": "🎬"}
    master[vid29]["industries"] = [
        {"id": "kien-truc", "name": "Góc nhà đẹp", "icon": "🏛️"},
        {"id": "am-thuc", "name": "F&B", "icon": "🍜"}
    ]
    master[vid29]["x_factors"] = ["Bầu không khí chữa lành", "Ánh sáng ấm áp"]
    master[vid29]["purpose"] = "Thưởng thức"

# 30: PA 1
vid30 = "IG_@hayancook_DdSUI9BvhqR"
if vid30 in master:
    master[vid30]["shooting_style"] = {"id": "dien-anh", "name": "Chỉn Chu", "icon": "🎬"}
    master[vid30]["industries"] = [
        {"id": "am-thuc", "name": "F&B", "icon": "🍜"},
        {"id": "ugc", "name": "UGC", "icon": "📱"}
    ]
    master[vid30]["x_factors"] = ["Nhịp cắt nhanh", "Bếp nhà Á Đông"]
    master[vid30]["purpose"] = "Mẹo"

with open("master_classifications.json", "w", encoding="utf-8") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)
