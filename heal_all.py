import json
import re
import subprocess

with open("master_classifications.json", "r") as f:
    master = json.load(f)

fixed_titles = 0
fixed_creators = 0

for k, v in master.items():
    if not isinstance(v, dict):
        continue
    if "creator" not in v or "title" not in v:
        continue
        
    vid = v["id"]
    creator = v["creator"]
    title = v["title"]
    
    # 1. Heal Creator
    # If ID starts with IG_@ or TT_@, extract the string between that and the POST_ID
    # We can use a regex: ^(IG|TT)_(@.+?)_([A-Za-z0-9_-]{11}|[0-9]{19})(?:_|$)
    match = re.match(r'^(IG|TT)_(@.+?)_([A-Za-z0-9_-]{11}|[0-9]{19})(?:_|$)', vid)
    if match:
        extracted_creator = match.group(2)
        if extracted_creator != creator:
            v["creator"] = extracted_creator
            creator = extracted_creator
            fixed_creators += 1

    # 2. Heal Title
    # Check if creator is in title
    if creator not in title and creator.replace('@','') not in title.lower():
        clean_title = title.strip()
        if clean_title.endswith("-"):
            clean_title = clean_title[:-1].strip()
        v["title"] = f"{clean_title} - {creator}"
        fixed_titles += 1

with open("master_classifications.json", "w") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Healed {fixed_creators} creators and {fixed_titles} titles.")
subprocess.run(["python3", "training_data_builder.py"], check=True)
