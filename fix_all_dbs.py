import json
import re
import urllib.parse
import os

with open('gdrive_folders.json') as f:
    gdrive_data = json.load(f)

# Build a mapping from folder+filename_prefix to proxy URL
mapping = {}
for item in gdrive_data:
    url = item['url']
    path = item['path'] # e.g. "IG_@Josh_.../extracted_shots/shot_01_mid.jpg"
    
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if not match: continue
    drive_id = match.group(1)
    
    parts = path.split('/')
    if len(parts) >= 3:
        folder = parts[0]
        filename = parts[-1]
        basename = filename.split('.')[0] # "shot_01_mid"
        key = f"{folder}/{basename}"
        mapping[key] = f"https://ytuong.fedu.vn/api/video?id={drive_id}"

def fix_content(content):
    # Regex to find old R2 or media.fedu.vn image URLs
    # Format: https://media.fedu.vn/images/IG_.../shot_01_mid.webp
    # Or https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/IG_.../shot_01_mid.jpg
    
    def replacer(m):
        full_url = m.group(0)
        folder_encoded = m.group(1)
        filename_full = m.group(2)
        
        folder = urllib.parse.unquote(folder_encoded)
        basename = filename_full.split('.')[0]
        
        key = f"{folder}/{basename}"
        if key in mapping:
            return mapping[key]
        else:
            return full_url

    # pattern to match both media.fedu.vn and pub-447bd
    pattern = r'https://(?:media\.fedu\.vn|pub-447bd44dfdac4938912655c855b8631c\.r2\.dev)/images/([^/]+)/([^"\'\\]+)'
    new_content = re.sub(pattern, replacer, content)
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
    
    new_content = fix_content(content)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
        
    print(f"Fixed {filepath}")

