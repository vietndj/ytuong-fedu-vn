import json
import re

with open("ideas_data.js", "r") as f:
    content = f.read()
    match = re.search(r"var FEDU_IDEAS_DATABASE = (\{.*?\});", content, re.DOTALL)
    data = json.loads(match.group(1))

missing_images = []
missing_reports = []
missing_videos = []
empty_shots = []

for i in data.get("ideas", []):
    if i.get("is_excluded"): continue
    id = i.get("id")
    m = i.get("media", {})
    if not m.get("cover_image") and not m.get("thumb_hook"):
        missing_images.append(id)
    if not m.get("video_url"):
        missing_videos.append(id)
    rep = m.get("report_url", "")
    if rep:
        import urllib.parse
        import os
        clean_rep = rep.replace("./", "")
        if not clean_rep.startswith("http"):
            decoded_path = urllib.parse.unquote(clean_rep)
            full_path = os.path.join('/Users/vietmac/Documents/CODE/ytuong-fedu-vn', decoded_path)
            if not os.path.exists(full_path):
                missing_reports.append({'id': id, 'path': rep})

print(f"Missing images (cover/thumb): {len(missing_images)}")
if missing_images:
    print("Example missing images:", missing_images[:5])
print(f"Missing videos: {len(missing_videos)}")
print(f"Missing reports: {len(missing_reports)}")
if missing_reports:
    print("Missing reports:", missing_reports[:10])
print(f"Empty shots: {len(empty_shots)}")
