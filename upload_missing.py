import json
import glob
import os
import sys

# Import upload_video from batch_r2_to_youtube
sys.path.append('.')
from batch_r2_to_youtube import upload_video, update_master_classifications

with open("audit_queue.json", "r") as f:
    queue = json.load(f)

with open("master_classifications.json", "r") as f:
    master = json.load(f)

unique_queue = {item['id']: item for item in queue}.values()
output_dir = "/Users/vietmac/Documents/CODE/Quản gia/output_packages"

to_upload = []

for item in unique_queue:
    vid = item["id"]
    master_item = master.get(vid, {})
    
    if not master_item.get("youtube_id"):
        # Get post ID
        import re
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
            
        # Find MP4
        search = f"{output_dir}/**/{post_id}.mp4"
        files = glob.glob(search, recursive=True)
        if not files:
            files = glob.glob(f"{output_dir}/*{post_id}*.mp4")
            
        if files:
            to_upload.append({
                "id": vid,
                "post_id": post_id,
                "file": files[0],
                "title": master_item.get("title", f"Video {post_id}")
            })

print(f"Found {len(to_upload)} ready to upload out of missing YT.")

# Upload them
success = 0
for task in to_upload:
    print(f"Uploading {task['post_id']}...")
    desc = f"Video phân tích & bóc tách storyboard tự động.\nShortcode: {task['post_id']}"
    vid_id, tag = upload_video(task['file'], f"[Phân Tích] {task['title']}", desc)
    if vid_id:
        print(f"Success! YouTube ID: {vid_id}")
        update_master_classifications(task['post_id'], vid_id)
        success += 1
    else:
        print(f"Failed to upload {task['post_id']}. Quota likely exceeded.")
        break

print(f"Successfully uploaded {success} videos.")
