import json, re

SCENE_PATH = "scene.html"
with open(SCENE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r'const portalData\s*=\s*(\[.*?\]);', content, re.DOTALL)
if m:
    portal_data = json.loads(m.group(1))
    
    new_item = {
        "id": "IG_@sir.ralph_e_DavWS9Islv1_Chuyen_Canh",
        "folder_name": "IG_@sir.ralph_e_DavWS9Islv1_Chuyen_Canh",
        "title_vi": "@sir.ralph_e • Kỹ Thuật Chuyển Cảnh Sáng Tạo",
        "creator": "@sir.ralph_e",
        "desc_vi": "Hướng dẫn chi tiết các mẹo chuyển cảnh biến hình mượt mà bằng match cut.",
        "key_tech": "Match Cut • Chuyển Cảnh (Transition)",
        "ig_url": "https://www.instagram.com/reel/DavWS9Islv1/",
        "gdrive_folder": "",
        "gdrive_pdf": "",
        "main_vid_rel": "https://media.fedu.vn/videos/DavWS9Islv1.mp4",
        "main_html_rel": "reports/IG_@sir.ralph_e_DavWS9Islv1_Chuyen_Canh.html",
        "main_pdf_rel": "",
        "shots_count": 8,
        "root_html_rel": "reports/IG_@sir.ralph_e_DavWS9Islv1_Chuyen_Canh.html",
        "root_vid_rel": "https://media.fedu.vn/videos/DavWS9Islv1.mp4",
        "root_pdf_rel": "",
        "all_vids": [
            {
                "name": "Video Master",
                "rel_url": "https://media.fedu.vn/videos/DavWS9Islv1.mp4"
            }
        ],
        "thumbnails": [
            "https://media.fedu.vn/images/IG_@sir.ralph_e_DavWS9Islv1_Chuyen_Canh/shot_01_mid.jpg",
            "https://media.fedu.vn/images/IG_@sir.ralph_e_DavWS9Islv1_Chuyen_Canh/shot_03_mid.jpg"
        ]
    }
    
    portal_data.insert(0, new_item)
    new_json = json.dumps(portal_data, indent=2, ensure_ascii=False)
    new_content = content[:m.start(1)] + new_json + content[m.end(1):]
    
    with open(SCENE_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("Added to scene.html")
