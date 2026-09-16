import json

with open("master_classifications.json", "r") as f:
    data = json.load(f)

for k, v in data.items():
    if k != v.get("id"): continue
    qk = v.get("quick_takeaway", "")
    if "Tác phẩm điện ảnh ngắn" in qk:
        print(k)
        print("💡:", v.get("fedu_optimization", {}).get("key_optimization_point"))
        print("🎯:", v.get("fedu_optimization", {}).get("practice_focus"))
        print("TAGS:", v.get("tech_tags"))
        print("-" * 20)
