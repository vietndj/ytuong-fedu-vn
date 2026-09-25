import json

with open("master_classifications.json", "r") as f:
    master = json.load(f)

with open("audit_queue.json", "r") as f:
    queue = json.load(f)

# Collect all IDs in queue
queue_ids = {item["id"] for item in queue}

fixed_count = 0
for k, v in master.items():
    if not isinstance(v, dict):
        continue
    
    # We only care about items that are actually videos (not raw post_id aliases)
    if "creator" not in v or "title" not in v:
        continue
        
    creator = v["creator"]
    title = v["title"]
    
    # Check if creator is in title
    if creator not in title and creator.replace('@','') not in title.lower():
        # Clean title first
        clean_title = title.strip()
        if clean_title.endswith("-"):
            clean_title = clean_title[:-1].strip()
        
        # Append creator
        new_title = f"{clean_title} - {creator}"
        master[k]["title"] = new_title
        fixed_count += 1

with open("master_classifications.json", "w") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Healed {fixed_count} titles in master_classifications.json")

# Also run training_data_builder.py to update dist/ideas_data.js
import subprocess
try:
    subprocess.run(["python3", "training_data_builder.py"], check=True)
    print("Rebuilt ideas_data.js successfully.")
except Exception as e:
    print(f"Error rebuilding data: {e}")
