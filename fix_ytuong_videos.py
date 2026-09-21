import json
import re
import os

with open("/Users/vietmac/drive_links.json", "r") as f:
    drive_links = json.load(f)

# Fix master_classifications.json
with open("master_classifications.json", "r") as f:
    mc = json.load(f)

for k, v in mc.items():
    if not isinstance(v, dict):
        continue
    url = v.get("video_url", "")
    if url and ".mp4" in url and "videos_preview" not in url:
        # Extract filename
        basename = url.split("/")[-1].replace(".mp4", "")
        # Remove trailing underscore if exists (bug fix)
        if basename.endswith("_"):
            basename = basename[:-1]
        
        orig_filename = f"{basename}.mp4"
        if orig_filename in drive_links:
            v["video_url_original"] = drive_links[orig_filename]
            
        new_url = f"https://media.fedu.vn/videos_preview/{basename}_preview.mp4"
        v["video_url"] = new_url

with open("master_classifications.json", "w") as f:
    json.dump(mc, f, indent=4, ensure_ascii=False)

# Fix scene.html
with open("scene.html", "r") as f:
    scene_html = f.read()

def fix_url(match):
    full_str = match.group(0)
    url = match.group(1)
    if ".mp4" in url and "videos_preview" not in url:
        basename = url.split("/")[-1].replace(".mp4", "")
        if basename.endswith("_"):
            basename = basename[:-1]
        new_url = f"https://media.fedu.vn/videos_preview/{basename}_preview.mp4"
        return full_str.replace(url, new_url)
    return full_str

scene_html = re.sub(r'"(?:main_vid_rel|root_vid_rel)":\s*"([^"]+)"', fix_url, scene_html)

with open("scene.html", "w") as f:
    f.write(scene_html)
