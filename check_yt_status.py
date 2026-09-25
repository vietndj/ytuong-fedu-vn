import json
import os
import re

with open("audit_queue.json", "r") as f:
    queue = json.load(f)

with open("master_classifications.json", "r") as f:
    master = json.load(f)

# Deduplicate queue
unique_queue = {item['id']: item for item in queue}.values()

missing_yt = []
has_yt = []

for item in unique_queue:
    vid = item["id"]
    master_item = master.get(vid, {})
    
    yt_id = master_item.get("youtube_id")
    yt_url = master_item.get("youtube_url")
    
    if yt_id or yt_url:
        has_yt.append(vid)
    else:
        # Extract post ID to check if mp4 exists
        creator = item.get("creator", "")
        if vid.startswith(f"IG_{creator}_"):
            remainder = vid[len(f"IG_{creator}_"):]
            match = re.match(r'^([A-Za-z0-9_-]{11})(?:_|$)', remainder)
            post_id = match.group(1) if match else remainder.split('_')[0]
        elif vid.startswith(f"TT_{creator}_"):
            remainder = vid[len(f"TT_{creator}_"):]
            match = re.match(r'^([0-9]{19})(?:_|$)', remainder)
            post_id = match.group(1) if match else remainder.split('_')[0]
        else:
            post_id = vid
            
        missing_yt.append({"id": vid, "post_id": post_id})

print(f"Total Unique Items: {len(unique_queue)}")
print(f"Has YouTube: {len(has_yt)}")
print(f"Missing YouTube: {len(missing_yt)}")

import sys

import glob

output_dir = "/Users/vietmac/Documents/CODE/Quản gia/output_packages"

missing_mp4 = []
found_mp4 = []

for m in missing_yt:
    post_id = m['post_id']
    # Check if {post_id}.mp4 exists anywhere in output_packages or subdirs
    # Also check ytuong-fedu-vn folders
    search_pattern = f"{output_dir}/**/{post_id}.mp4"
    files = glob.glob(search_pattern, recursive=True)
    if not files:
        search_pattern2 = f"{output_dir}/*{post_id}*.mp4"
        files = glob.glob(search_pattern2)
        
    if files:
        found_mp4.append((m['id'], files[0]))
    else:
        missing_mp4.append(m['id'])

print(f"Found MP4: {len(found_mp4)}")
print(f"Missing MP4: {len(missing_mp4)}")
if missing_mp4:
    print("Sample missing:", missing_mp4[:3])
