import json
import re
import os

BASE_DIR = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn"
MASTER_PATH = os.path.join(BASE_DIR, "master_classifications.json")
SCENE_PATH = os.path.join(BASE_DIR, "scene.html")
CURATION_PATH = os.path.join(BASE_DIR, "curation_config.json")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_portal_data():
    with open(SCENE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'const portalData\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if not m:
        raise ValueError("Could not extract portalData from scene.html")
    return json.loads(m.group(1))

def main():
    master = load_json(MASTER_PATH)
    portal_data = load_portal_data()
    curation = load_json(CURATION_PATH)
    
    portal_ids = {item.get("id"): item for item in portal_data if "id" in item}
    excluded_ids = set(curation.get("excluded_ids", []))
    
    missing_in_scene = []
    alias_mismatches = []
    
    # 1. Check missing in scene
    for master_id, master_item in master.items():
        if master_id not in portal_ids and master_id not in excluded_ids:
            # wait, is_personal items are not supposed to be in scene.html either
            is_personal = False
            for p in ["@vietmac", "practice_cinematic", "self_practice", "broll_plan", "@local", "vietnd"]:
                if p in master_id.lower():
                    is_personal = True
                    break
            if not is_personal:
                missing_in_scene.append(master_id)
            
    # 2. Check alias mismatches
    for master_id, master_item in master.items():
        if master_id in portal_ids:
            p_item = portal_ids[master_id]
            p_creator = p_item.get("creator", "").strip()
            
            m_handle = master_item.get("creator", "").strip()
            
            if p_creator and m_handle and p_creator != m_handle:
                alias_mismatches.append((master_id, p_creator, m_handle))
                    
    # 3. Check erroneous exclusions
    erroneous_exclusions = []
    for m_id in master:
        if m_id in excluded_ids:
            is_personal = False
            for p in ["@vietmac", "practice_cinematic", "self_practice", "broll_plan", "@local", "vietnd"]:
                if p in m_id.lower():
                    is_personal = True
                    break
            if not is_personal:
                erroneous_exclusions.append(m_id)
    
    print(f"Total master items: {len(master)}")
    print(f"Total portal items: {len(portal_data)}")
    print(f"Missing in scene.html: {len(missing_in_scene)}")
    if missing_in_scene:
        print(f"Sample missing: {missing_in_scene[:5]}")
        
    print(f"Alias mismatches: {len(alias_mismatches)}")
    if alias_mismatches:
        print(f"Sample aliases: {alias_mismatches[:5]}")
        
    print(f"Erroneous exclusions: {len(erroneous_exclusions)}")
    if erroneous_exclusions:
        print(f"Sample exclusions: {erroneous_exclusions[:5]}")

if __name__ == "__main__":
    main()
