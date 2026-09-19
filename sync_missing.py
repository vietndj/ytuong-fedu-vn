import json
import re
import subprocess
import os

BASE_DIR = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn"
MASTER_FILE = os.path.join(BASE_DIR, "master_classifications.json")
SCENE_FILE = os.path.join(BASE_DIR, "scene.html")

def get_drive_folders():
    print("Getting list of folders from Google Drive...")
    res = subprocess.run([
        "rclone", "lsf", "--dirs-only", "--drive-root-folder-id", "1Iu9v2sRTAUYvnkeKx-Tgu-RM_9A54_Qf", "gdrive:"
    ], capture_output=True, text=True)
    folders = [f.strip("/") for f in res.stdout.split("\n") if f.strip()]
    return folders

def is_valid_folder(folder_name):
    return not folder_name.startswith("NotebookLM") and not folder_name.startswith("Practice_") and not folder_name.startswith("PRACTICE_")

def extract_id_from_folder(folder_name):
    # Dựa vào folder_name để lấy ra video id hợp lệ
    return folder_name

def extract_shortcode(vid_id):
    m_code = re.search(r"_(D[A-Za-z0-9_-]{10})(?:_|$)", vid_id)
    if m_code:
        code = m_code.group(1).strip().rstrip("_")
        if "Carousel_Analysis" in vid_id:
            code += "_Carousel_Analysis"
        return code
    m_code2 = re.search(r"_(D[A-Za-z0-9_-]{9,11})", vid_id)
    if m_code2:
        code = m_code2.group(1).strip().rstrip("_")
        if "Carousel_Analysis" in vid_id:
            code += "_Carousel_Analysis"
        return code
    return vid_id

def main():
    folders = get_drive_folders()
    valid_folders = [f for f in folders if is_valid_folder(f)]
    print(f"Total valid folders: {len(valid_folders)}")
    
    with open(MASTER_FILE, "r") as f:
        master = json.load(f)
        
    with open(SCENE_FILE, "r") as f:
        scene_content = f.read()
        
    m = re.search(r'const portalData\s*=\s*(\[.*?\]);', scene_content, re.DOTALL)
    if not m:
        print("Cannot find portalData")
        return
    portal_data = json.loads(m.group(1))
    
    # 1. Check missing in master
    missing_in_master = []
    for folder in valid_folders:
        vid_id = extract_id_from_folder(folder)
        shortcode = extract_shortcode(vid_id)
        if vid_id not in master and shortcode not in master:
            missing_in_master.append(folder)
            
    print(f"Missing in master_classifications.json: {len(missing_in_master)}")
    
    for folder in missing_in_master:
        vid_id = extract_id_from_folder(folder)
        creator_name = ""
        m_cr = re.search(r'_(?:@|)([a-zA-Z0-9._]+)_', vid_id)
        if m_cr:
            creator_name = "@" + m_cr.group(1)
            
        master[vid_id] = {
            "title": folder.replace("_", " "),
            "creator_name": creator_name,
            "industry": {"id": "ugc", "name": "UGC & Ads"},
            "shooting_style": {"id": "dien-anh", "name": "Chỉn Chu", "icon": "🎬"},
            "purpose": "Showcase thị giác & Thẩm mỹ",
            "tech_tags": ["Cinematic"],
            "x_factors": ["Basic classification"],
            "country": {"id": "us_eu", "name": "Âu Mỹ", "flag": "🇺🇸/🇪🇺", "badge_color": "purple"}
        }
        
    if missing_in_master:
        with open(MASTER_FILE, "w", encoding="utf-8") as f:
            json.dump(master, f, ensure_ascii=False, indent=4)
        print("Updated master_classifications.json")

    # 2. Check missing in scene.html
    portal_ids = {item.get("id") for item in portal_data}
    portal_codes = {extract_shortcode(item.get("id", "")) for item in portal_data}
    
    missing_in_scene = []
    for folder in valid_folders:
        vid_id = extract_id_from_folder(folder)
        shortcode = extract_shortcode(vid_id)
        if vid_id not in portal_ids and shortcode not in portal_codes:
            missing_in_scene.append(folder)
            
    print(f"Missing in scene.html: {len(missing_in_scene)}")
    
    for folder in missing_in_scene:
        vid_id = extract_id_from_folder(folder)
        creator_name = ""
        m_cr = re.search(r'_(?:@|)([a-zA-Z0-9._]+)_', vid_id)
        if m_cr:
            creator_name = "@" + m_cr.group(1)
            
        # extract shortcode for video url
        m_code = re.search(r"_(D[A-Za-z0-9_-]{9,11})", vid_id)
        short_id = m_code.group(1) if m_code else vid_id
        
        ig_url = ""
        if m_code:
            ig_url = f"https://www.instagram.com/reel/{m_code.group(1)}/"
            
        new_item = {
            "id": vid_id,
            "folder_name": folder,
            "title_vi": folder.replace("_", " "),
            "creator": creator_name,
            "desc_vi": "New imported video.",
            "key_tech": "Cinematic",
            "ig_url": ig_url,
            "gdrive_folder": "",
            "gdrive_pdf": "",
            "main_vid_rel": f"https://media.fedu.vn/videos/{short_id}.mp4",
            "main_html_rel": f"reports/{vid_id}.html",
            "main_pdf_rel": "",
            "shots_count": 0,
            "root_html_rel": f"reports/{vid_id}.html",
            "root_vid_rel": f"https://media.fedu.vn/videos/{short_id}.mp4",
            "root_pdf_rel": "",
            "all_vids": [],
            "all_htmls": [],
            "all_pdfs": [],
            "thumbs": [],
            "thumbnails": []
        }
        portal_data.insert(0, new_item)
        
    if missing_in_scene:
        # replace portalData back in scene.html
        new_portal_str = json.dumps(portal_data, ensure_ascii=False, indent=2)
        new_scene_content = re.sub(r'const portalData\s*=\s*\[.*?\];', f'const portalData = {new_portal_str};', scene_content, flags=re.DOTALL)
        with open(SCENE_FILE, "w", encoding="utf-8") as f:
            f.write(new_scene_content)
        print("Updated scene.html")

if __name__ == "__main__":
    main()
