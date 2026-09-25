import json
import re

with open("master_classifications.json", "r") as f:
    master = json.load(f)

fixed_count = 0
for k, v in master.items():
    if not isinstance(v, dict) or "creator" not in v:
        continue
    
    vid = v["id"]
    current_creator = v["creator"]
    
    match = re.match(r'^(IG|TT)_(@[a-zA-Z0-9_.]+)', vid)
    if match:
        extracted_creator = match.group(2)
        # Verify it really is the creator by checking if it ends with '_' before post_id
        # Usually it is.
        if extracted_creator != current_creator:
            v["creator"] = extracted_creator
            fixed_count += 1

with open("master_classifications.json", "w") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Healed {fixed_count} creator handles in master_classifications.json")

import subprocess
try:
    subprocess.run(["python3", "training_data_builder.py"], check=True)
    print("Rebuilt ideas_data.js successfully.")
except Exception as e:
    print(f"Error rebuilding data: {e}")
