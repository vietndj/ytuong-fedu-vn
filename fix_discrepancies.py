import json
import re
import os
import urllib.parse

BASE_DIR = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn"
MASTER_PATH = os.path.join(BASE_DIR, "master_classifications.json")
SCENE_PATH = os.path.join(BASE_DIR, "scene.html")
CURATION_PATH = os.path.join(BASE_DIR, "curation_config.json")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_shortcode(vid_id):
    # Same as build_ideas_bank.py
    m_code = re.search(r"_(D[A-Za-z0-9_-]{10})(?:_|$)", vid_id)
    if m_code:
        return m_code.group(1).strip().rstrip("_")
    m_code2 = re.search(r"_(D[A-Za-z0-9_-]{9,11})", vid_id)
    if m_code2:
        return m_code2.group(1).strip().rstrip("_")
    return vid_id.strip()

def fix_all():
    master = load_json(MASTER_PATH)
    
    with open(SCENE_PATH, "r", encoding="utf-8") as f:
        scene_content = f.read()
    m = re.search(r'const portalData\s*=\s*(\[.*?\]);', scene_content, re.DOTALL)
    if not m:
        raise ValueError("Could not extract portalData from scene.html")
    portal_data = json.loads(m.group(1))
    
    curation = load_json(CURATION_PATH)
    excluded_ids = set(curation.get("excluded_ids", []))
    
    portal_ids = {item.get("id"): item for item in portal_data if "id" in item}
    
    # 1. Alias mismatches
    fixed_aliases = 0
    for p_item in portal_data:
        m_id = p_item.get("id")
        if m_id in master:
            m_creator = master[m_id].get("creator", "").strip()
            p_creator = p_item.get("creator", "").strip()
            if m_creator and p_creator and m_creator != p_creator:
                p_item["creator"] = m_creator
                fixed_aliases += 1

    # 2. Add missing items
    added_count = 0
    for m_id, m_item in master.items():
        is_personal = False
        for p in ["@vietmac", "practice_cinematic", "self_practice", "broll_plan", "@local", "vietnd"]:
            if p in m_id.lower():
                is_personal = True
                break
                
        if m_id not in portal_ids and not is_personal and m_id not in excluded_ids:
            code = extract_shortcode(m_id)
            new_item = {
                "id": m_id,
                "folder_name": m_id,
                "title_vi": m_item.get("title", ""),
                "creator": m_item.get("creator", ""),
                "desc_vi": m_item.get("quick_takeaway", ""),
                "key_tech": ", ".join(m_item.get("tech_tags", [])),
                "ig_url": "",
                "main_vid_rel": f"https://media.fedu.vn/videos/{code}.mp4",
                "shots_count": m_item.get("shots_count", 0),
                "thumbnails": [
                    f"https://media.fedu.vn/images/{urllib.parse.quote(m_id, safe='')}/shot_01_mid.jpg",
                    f"https://media.fedu.vn/images/{urllib.parse.quote(m_id, safe='')}/shot_03_mid.jpg"
                ]
            }
            portal_data.append(new_item)
            added_count += 1
            
    # 3. Erroneous exclusions
    removed_exclusions = 0
    new_excluded = []
    for ex_id in curation.get("excluded_ids", []):
        if ex_id in master:
            is_personal = False
            for p in ["@vietmac", "practice_cinematic", "self_practice", "broll_plan", "@local", "vietnd"]:
                if p in ex_id.lower():
                    is_personal = True
                    break
            if not is_personal:
                # Erroneous exclusion
                removed_exclusions += 1
                continue
        new_excluded.append(ex_id)
        
    curation["excluded_ids"] = new_excluded
    
    # Save curation
    with open(CURATION_PATH, "w", encoding="utf-8") as f:
        json.dump(curation, f, indent=4, ensure_ascii=False)
        
    # Save scene
    new_portal_str = json.dumps(portal_data, indent=2, ensure_ascii=False)
    # The portalData array might have lines that are very long. json.dumps is fine.
    
    # Replace in scene.html
    new_scene_content = scene_content[:m.start()] + "const portalData = " + new_portal_str + ";" + scene_content[m.end():]
    with open(SCENE_PATH, "w", encoding="utf-8") as f:
        f.write(new_scene_content)
        
    print(f"Fixed alias mismatches: {fixed_aliases}")
    print(f"Added missing items: {added_count}")
    print(f"Removed erroneous exclusions: {removed_exclusions}")

if __name__ == "__main__":
    fix_all()
