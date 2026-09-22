import json, re

with open('gdrive_folders.json') as f:
    gdrive_data = json.load(f)

mapping = {}
for item in gdrive_data:
    url = item['url']
    path = item['path']
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if match:
        mapping[path] = f"https://ytuong.fedu.vn/api/video?id={match.group(1)}"

with open('live_ideas.js') as f:
    js_content = f.read()
    
# thumb_hook and thumb_key usually look like:
# "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/IG_%40..._DcLwG_mKyKM_.../shot_01_mid.jpg"
# We need to map them. Since R2 paths are URL-encoded, we should unquote them to match gdrive paths?
import urllib.parse
match = re.search(r'"thumb_hook":\s*"(.*?)"', js_content)
if match:
    old_url = match.group(1)
    # Extract just the folder and file name
    # e.g. IG_@.../shot_01_mid.jpg
    parts = old_url.split('/images/')
    if len(parts) > 1:
        suffix = urllib.parse.unquote(parts[1])
        # In gdrive_folders.json, the path is "Folder/extracted_shots/shot_01_mid.jpg"
        # Wait, the suffix from r2 is "Folder/shot_01_mid.jpg"
        # Let's check gdrive paths
        print("Suffix from JS:", suffix)
        
