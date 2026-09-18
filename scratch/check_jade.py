import json

with open("master_classifications.json", "r") as f:
    master = json.load(f)

for k, v in master.items():
    if "jade" in str(v.get("creator", "")).lower() or "jade" in str(v.get("title", "")).lower() or "jade" in k.lower():
        print(f"ID: {k}")
        print(f"Creator: {v.get('creator')}")
        print(f"Title: {v.get('title')}")
        print(f"Excluded: {v.get('is_excluded')}")
        print(f"Missing fedu_optimization?: {'fedu_optimization' not in v}")
        print("---")
