import json
from collections import Counter

with open("master_classifications.json", "r") as f:
    data = json.load(f)

f1 = Counter()
f2 = Counter()

for k, v in data.items():
    if k != v.get("id"): continue
    
    k1 = v.get("fedu_optimization", {}).get("key_optimization_point")
    if k1:
        # if it's the "Tác phẩm điện ảnh ngắn gồm X", replace X with a placeholder
        import re
        k1 = re.sub(r"gồm \d+ phân cảnh", "gồm X phân cảnh", k1)
        f1[k1] += 1
        
    k2 = v.get("fedu_optimization", {}).get("practice_focus")
    if k2:
        f2[k2] += 1

print("--- TOP 💡 (key_optimization_point) ---")
for text, count in f1.most_common(10):
    print(f"[{count}] {text}")

print("\n--- TOP 🎯 (practice_focus) ---")
for text, count in f2.most_common(10):
    print(f"[{count}] {text}")
