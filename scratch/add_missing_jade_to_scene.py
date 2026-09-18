import json, re

with open("master_classifications.json", "r", encoding="utf-8") as f:
    master = json.load(f)

missing_jade_ids = [
    "IG_@Jade_Sheng_DYXiic5xMeC_Video_by_jade.got.curious",
    "IG_@Jade_Sheng_DZB9Ls3No6p_Video_by_jade.got.curious",
    "IG_@Jade_Sheng_DZa9pzKRsAU_Video_by_jade.got.curious",
    "IG_@Jade_Sheng_DZwO5X6N_MS_Video_by_jade.got.curious",
    "IG_@Jade_Sheng_DcbAqchxJ2t_Video_by_jade.got.curious"
]

SCENE_PATH = "scene.html"
with open(SCENE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r'const portalData\s*=\s*(\[.*?\]);', content, re.DOTALL)
portal_data = json.loads(m.group(1))

existing_ids = set([item.get("id", "") for item in portal_data])

count = 0
for jade_id in missing_jade_ids:
    if jade_id in existing_ids:
        print(f"Skipping {jade_id}, already in scene.html")
        continue

    code_match = re.search(r'_([A-Za-z0-9_-]{11})_', jade_id)
    code = code_match.group(1) if code_match else "unknown"

    item_data = master.get(jade_id) or master.get(code)
    if not item_data:
        print(f"Not found in master: {jade_id} / {code}")
        continue

    tech_tags = item_data.get("tech_tags", [])
    key_tech = " • ".join(tech_tags) if tech_tags else ""

    new_item = {
        "id": jade_id,
        "folder_name": jade_id,
        "title_vi": item_data.get("title", ""),
        "creator": item_data.get("creator", "@jade.got.curious"),
        "desc_vi": item_data.get("logic_explanation", ""),
        "key_tech": key_tech,
        "ig_url": f"https://www.instagram.com/reel/{code}/",
        "gdrive_folder": "",
        "gdrive_pdf": "",
        "main_vid_rel": f"https://media.fedu.vn/videos/{code}.mp4",
        "main_html_rel": f"reports/{jade_id}.html",
        "main_pdf_rel": "",
        "shots_count": item_data.get("shots_count", 0),
        "root_html_rel": f"reports/{jade_id}.html",
        "root_vid_rel": f"https://media.fedu.vn/videos/{code}.mp4",
        "root_pdf_rel": "",
        "all_vids": [
            {
                "name": "Video Master",
                "rel_url": f"https://media.fedu.vn/videos/{code}.mp4"
            }
        ],
        "thumbnails": [
            f"https://media.fedu.vn/images/{jade_id}/shot_01_mid.jpg",
            f"https://media.fedu.vn/images/{jade_id}/shot_03_mid.jpg"
        ]
    }
    portal_data.insert(0, new_item)
    print(f"Added {jade_id}")
    count += 1

if count > 0:
    new_json = json.dumps(portal_data, indent=2, ensure_ascii=False)
    new_content = content[:m.start(1)] + new_json + content[m.end(1):]
    with open(SCENE_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Done updating scene.html")
