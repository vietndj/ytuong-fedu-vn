import json
import re

with open("audit_queue.json", "r") as f:
    queue = json.load(f)

mismatches = []
valid_items = []

for item in queue:
    vid = item["id"]
    creator = item.get("creator", "")
    title = item.get("title", "")
    
    # Verify ID structure
    # Try to extract the creator from the ID
    match = re.match(r'^(IG|TT)_(@[a-zA-Z0-9_.]+)', vid)
    extracted_creator = match.group(2) if match else None
    
    # Verify POST_ID
    if extracted_creator and vid.startswith(f"IG_{extracted_creator}_"):
        remainder = vid[len(f"IG_{extracted_creator}_"):]
        post_match = re.match(r'^([A-Za-z0-9_-]{11})(?:_|$)', remainder)
        post_id = post_match.group(1) if post_match else remainder.split('_')[0]
    elif extracted_creator and vid.startswith(f"TT_{extracted_creator}_"):
        remainder = vid[len(f"TT_{extracted_creator}_"):]
        post_match = re.match(r'^([0-9]{19})(?:_|$)', remainder)
        post_id = post_match.group(1) if post_match else remainder.split('_')[0]
    else:
        post_id = vid

    # Check if extracted creator matches JSON creator
    is_creator_match = (extracted_creator == creator)
    # Check if title contains creator
    is_title_match = (creator.replace("@", "") in title or creator in title)
    
    if not is_creator_match or not is_title_match:
        mismatches.append({
            "id": vid,
            "json_creator": creator,
            "extracted_creator": extracted_creator,
            "post_id": post_id,
            "title": title
        })
    else:
        valid_items.append({
            "id": vid,
            "creator": creator,
            "post_id": post_id,
            "title": title
        })

print(f"Total: {len(queue)}")
print(f"Valid: {len(valid_items)}")
print(f"Mismatches: {len(mismatches)}")

with open("audit_mismatches.json", "w") as f:
    json.dump(mismatches, f, indent=2, ensure_ascii=False)

if mismatches:
    print("\nSample mismatches:")
    for m in mismatches[:5]:
        print(f"ID: {m['id']}\nJSON Creator: {m['json_creator']} | ID Creator: {m['extracted_creator']}\nTitle: {m['title']}\n")
