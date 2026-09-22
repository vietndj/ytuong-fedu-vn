import json
import re
import urllib.parse
import os

print("Loading all gdrive files...")
with open('/tmp/all_gdrive_files.json') as f:
    all_files = json.load(f)

print("Building fast lookup mapping...")
# We want to map something like "IG_@Жамьяна.../shot_01_mid" to its proxy URL
# In all_gdrive_files.json, the path is relative to Work/AI_Video_Analysis
# e.g. "IG_@Жамьяна_Осознанный_стилист_UGC_DdeWMWLsaHA_Video_by_zhamyana/extracted_shots/shot_01_mid.jpg"
# or "images/IG_@german991020_DdiSb5Rp2LB_Lost_in_Seoul/shot_01_mid.jpg"
mapping = {}
for item in all_files:
    if item['IsDir']: continue
    path = item['Path']
    drive_id = item['ID']
    
    # Extract folder name and shot name
    parts = path.split('/')
    if len(parts) >= 2:
        filename = parts[-1]
        basename = filename.split('.')[0]
        
        # The folder name is usually the first or second part
        # if it's in images/ IG_... / shot.jpg -> folder = IG_...
        # if it's IG_... / extracted_shots / shot.jpg -> folder = IG_...
        folder = None
        for p in parts:
            if p.startswith('IG_@') or p.startswith('FB_@') or p.startswith('TikTok_@') or p.startswith('Practice_') or p.startswith('NotebookLM_'):
                folder = p
                break
        
        if folder:
            key = f"{folder}/{basename}"
            mapping[key] = f"https://ytuong.fedu.vn/api/video?id={drive_id}"

print(f"Mapped {len(mapping)} items.")

def fix_content(content):
    # Regex to find old R2 or media.fedu.vn image URLs
    # Pattern to match both media.fedu.vn and pub-447bd
    pattern = r'https://(?:media\.fedu\.vn|pub-447bd44dfdac4938912655c855b8631c\.r2\.dev)/images/([^/]+)/([^"\'\\]+)'
    
    count = 0
    def replacer(m):
        nonlocal count
        full_url = m.group(0)
        folder_encoded = m.group(1)
        filename_full = m.group(2)
        
        folder = urllib.parse.unquote(folder_encoded)
        basename = filename_full.split('.')[0]
        
        key = f"{folder}/{basename}"
        if key in mapping:
            count += 1
            return mapping[key]
        else:
            print(f"NOT FOUND IN DRIVE: {key}")
            return full_url

    new_content = re.sub(pattern, replacer, content)
    print(f"Replaced {count} instances.")
    return new_content

files_to_fix = [
    'scene.html',
    'ideas_data.js',
    'dist/ideas_data.js'
]

for filepath in files_to_fix:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r') as f:
        content = f.read()
    
    print(f"Fixing {filepath}...")
    new_content = fix_content(content)
    
    with open(filepath, 'w') as f:
        f.write(new_content)

