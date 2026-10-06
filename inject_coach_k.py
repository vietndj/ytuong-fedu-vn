import json, re

# Inject to master_classifications.json
with open("master_classifications.json", "r", encoding="utf-8") as f:
    mc = json.load(f)

coach_k_folder = "IG_@MasterClass_nNkE1fK9eQs_Coach_K_Teaches_Values-Driven_Leadership_Offi"
with open(f"/Users/vietmac/Documents/CODE/Quản gia/output_packages/{coach_k_folder}/shot_info.json", "r", encoding="utf-8") as f:
    shots = json.load(f)

mc[coach_k_folder] = {
    "id": coach_k_folder,
    "creator": "@MasterClass",
    "creator_name": "MasterClass",
    "title": "Coach K Teaches Values-Driven Leadership Official Trailer",
    "shots_count": len(shots),
    "shooting_style": {"id": "talking-head", "name": "Talking Head", "icon": "🎬"},
    "industry": {"id": "giao-duc", "name": "Giáo Dục & Chuyên Gia", "icon": "🎯"},
    "tech_tags": ["ngồi nói trực tiếp"],
    "quick_takeaway": "Báo cáo phân tích chuyên sâu ngôn ngữ điện ảnh",
    "country": {"id": "us_eu", "name": "Âu Mỹ"}
}

with open("master_classifications.json", "w", encoding="utf-8") as f:
    json.dump(mc, f, indent=2, ensure_ascii=False)

# Inject to scene.html
with open("scene.html", "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r"const portalData = (\[[\s\S]*?\]);", content)
if m:
    data = json.loads(re.sub(r',\s*([\]\}])', r'\1', m.group(1)))
    new_item = {
        "id": coach_k_folder,
        "folder_name": coach_k_folder,
        "title_vi": "Coach K Teaches Values-Driven Leadership",
        "creator": "@MasterClass",
        "desc_vi": "Báo cáo phân tích chuyên sâu ngôn ngữ điện ảnh",
        "key_tech": "ngồi nói trực tiếp",
        "ig_url": "https://www.youtube.com/watch?v=nNkE1fK9eQs",
        "main_vid_rel": "https://media.fedu.vn/videos/nNkE1fK9eQs.mp4",
        "main_html_rel": f"reports/{coach_k_folder}.html",
        "shots_count": len(shots),
        "root_html_rel": f"reports/{coach_k_folder}.html",
        "root_vid_rel": "https://media.fedu.vn/videos/nNkE1fK9eQs.mp4",
        "all_vids": [{"name": "Video Master", "rel_url": "https://media.fedu.vn/videos/nNkE1fK9eQs.mp4"}]
    }
    data.insert(0, new_item)
    new_json = json.dumps(data, indent=2, ensure_ascii=False)
    content = content[:m.start()] + "const portalData = " + new_json + ";" + content[m.end():]
    with open("scene.html", "w", encoding="utf-8") as f:
        f.write(content)

print("Done injecting Coach K")
