import json
import re

SCENE_PATH = "scene.html"
MASTER_PATH = "master_classifications.json"

with open(MASTER_PATH, "r", encoding="utf-8") as f:
    master = json.load(f)

with open(SCENE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r'const portalData\s*=\s*(\[.*?\]);', content, re.DOTALL)
if m:
    portal_data = json.loads(m.group(1))
    existing_ids = {item.get('id') for item in portal_data}
    
    missing_codes = ['DaH_rTUTe14', 'DaXdrAVzGcc', 'DbnlAB5Twrw', 'DcGbEVFznin']
    
    added = 0
    for code in missing_codes:
        master_item = master.get(code)
        if not master_item: continue
        
        vid_id = master_item.get('id')
        if vid_id in existing_ids:
            continue
            
        new_item = {
            "id": vid_id,
            "folder_name": vid_id,
            "title_vi": master_item.get('title', ''),
            "creator": master_item.get('creator', ''),
            "desc_vi": master_item.get('quick_takeaway', ''),
            "key_tech": " • ".join(master_item.get('tech_tags', [])),
            "ig_url": f"https://www.instagram.com/reel/{code}/",
            "gdrive_folder": "",
            "gdrive_pdf": "",
            "main_vid_rel": f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/{code}.mp4",
            "main_html_rel": f"reports/{vid_id}.html",
            "main_pdf_rel": "",
            "shots_count": master_item.get('shots_count', 0),
            "root_html_rel": f"reports/{vid_id}.html",
            "root_vid_rel": f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/{code}.mp4",
            "root_pdf_rel": "",
            "all_vids": [
                {
                    "name": "Video Master",
                    "rel_url": f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/{code}.mp4"
                }
            ],
            "thumbnails": [
                f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{vid_id}/shot_01_mid.jpg"
            ]
        }
        portal_data.insert(0, new_item)
        added += 1
        
    if added > 0:
        new_json = json.dumps(portal_data, indent=2, ensure_ascii=False)
        new_content = content[:m.start(1)] + new_json + content[m.end(1):]
        with open(SCENE_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Added {added} items to scene.html")
    else:
        print("No items needed to be added.")
else:
    print("Could not find portalData in scene.html")
