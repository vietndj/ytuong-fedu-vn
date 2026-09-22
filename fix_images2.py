import json
import re

html_path = "./reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html"
dist_html_path = "./dist/reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html"

with open("gdrive_folders.json", "r", encoding="utf-8") as f:
    gdrive = json.load(f)

mapping = {}
for item in gdrive:
    path = item['path']
    if "DcVnyJyNWGY" in path and path.endswith(".jpg"):
        filename = path.split("/")[-1]
        # Get the ID from the URL
        url = item['url']
        match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
        if match:
            drive_id = match.group(1)
            mapping[filename] = f"https://ytuong.fedu.vn/api/video?id={drive_id}"

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def replacer(match):
        filename = match.group(1)
        if filename in mapping:
            return mapping[filename]
        return match.group(0)

    # Note: earlier I replaced R2 URLs with Drive URLs, so now I need to replace Drive URLs!
    # Wait, in the previous script I successfully replaced R2 -> Drive.
    # So I need to replace Drive -> Proxy.
    
    # Replace https://drive.google.com/uc?id=XYZ with https://ytuong.fedu.vn/api/video?id=XYZ
    def drive_replacer(match):
        drive_id = match.group(1)
        # Only replace if it's an image id from mapping, but actually ALL uc?id can be replaced?
        # No, wait, if I just replace ALL Google Drive image URLs in the file with the proxy URL:
        return f"https://ytuong.fedu.vn/api/video?id={drive_id}"

    # We match the Drive URLs that were inserted for images (which don't have &export=download because gdrive_folders.json doesn't have it for images)
    # Example: https://drive.google.com/uc?id=1k1YTuE9Fk1fxsOnxNOe2dalxtKtq0uDA
    content = re.sub(r'https://drive\.google\.com/uc\?id=([a-zA-Z0-9_-]+)', drive_replacer, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file(html_path)
fix_file(dist_html_path)

print("Images replaced with Proxy URLs.")
