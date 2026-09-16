import json

with open("master_classifications.json", "r") as f:
    data = json.load(f)

for k, v in data.items():
    if k != v.get("id"): continue
    qk = v.get("quick_takeaway", "")
    k1 = v.get("fedu_optimization", {}).get("key_optimization_point", "")
    k2 = v.get("fedu_optimization", {}).get("practice_focus", "")
    
    if "Tác phẩm điện ảnh ngắn" in qk or "Tác phẩm điện ảnh ngắn" in k1 or "Tác phẩm điện ảnh ngắn" in k2:
        print(f"ID: {k}")
        print(f"TAGS: {v.get('tech_tags')}")
