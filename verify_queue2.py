import json

with open("audit_queue.json", "r") as f:
    queue = json.load(f)

mismatches = []
valid_items = []
seen_ids = set()

for item in queue:
    vid = item["id"]
    creator = item.get("creator", "")
    title = item.get("title", "")
    
    # We know creator is given in json. Let's extract post_id based on creator
    if creator and vid.startswith(f"IG_{creator}_"):
        remainder = vid[len(f"IG_{creator}_"):]
        post_id = remainder.split('_')[0]
    elif creator and vid.startswith(f"TT_{creator}_"):
        remainder = vid[len(f"TT_{creator}_"):]
        post_id = remainder.split('_')[0]
    else:
        post_id = vid

    # Check title match
    is_title_match = (creator in title) or (creator.replace('@','') in title.lower())
    
    # Let's just collect all data
    valid_items.append({
        "id": vid,
        "creator": creator,
        "post_id": post_id,
        "title": title,
        "title_has_creator": is_title_match
    })
    
    if not is_title_match:
        mismatches.append(valid_items[-1])

print(f"Total processed: {len(queue)}")
print(f"Items where Title does NOT contain Creator: {len(mismatches)}")

# Generate a markdown table artifact
import os
artifact_path = "/Users/vietmac/.gemini/antigravity/brain/c3877973-048f-46cd-8326-1c3ebfa98f84/audit_queue_validation.md"
with open(artifact_path, "w") as f:
    f.write("# Bảng Kiểm Tra Hàng Chờ Audit (128 Items)\n\n")
    f.write("| STT | Tên Creator (JSON) | Mã POST_ID (Bóc tách) | Tiêu đề Báo Cáo | Khớp Tên? |\n")
    f.write("|---|---|---|---|---|\n")
    
    # deduplicate for clean table
    unique_items = []
    for item in valid_items:
        if item["id"] not in seen_ids:
            seen_ids.add(item["id"])
            unique_items.append(item)
            
    for i, item in enumerate(unique_items, 1):
        status = "✅" if item["title_has_creator"] else "❌"
        f.write(f"| {i} | `{item['creator']}` | `{item['post_id']}` | {item['title']} | {status} |\n")

print(f"Saved artifact table to {artifact_path} with {len(unique_items)} unique items.")
