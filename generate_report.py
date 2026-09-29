import json
import random

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/dist/master_classifications.json', 'r') as f:
    data = json.load(f)

# Lọc các bài đã có dữ liệu đầy đủ
enriched = []
for k, v in data.items():
    if v.get('fedu_optimization') and v.get('practice_scenario'):
        if len(v.get('logic_explanation', '')) > 100:
            enriched.append(v)

print(f"Tổng số bài đã được làm giàu: {len(enriched)}/{len(data)}")

# Chọn 2 bài mẫu để làm báo cáo
samples = random.sample(enriched, min(2, len(enriched)))

for i, item in enumerate(samples, 1):
    print(f"\n--- BÀI {i}: {item.get('title', 'No Title')} ---")
    print(f"🎬 Style: {item.get('shooting_style', {}).get('name')} | Ngành: {item.get('industry', {}).get('name')}")
    
    print("\n[1] LOGIC KỊCH BẢN (Nâng cấp):")
    print(f"  {item.get('logic_explanation')}")
    
    fedu = item.get('fedu_optimization', {})
    if isinstance(fedu, dict):
        print("\n[2] TỐI ƯU HÓA (Mới):")
        print(f"  • Điểm cốt lõi: {fedu.get('key_optimization_point')}")
        print(f"  • Bài tập thực hành: {fedu.get('practice_focus')}")
        print(f"  • Câu Hook Seeding IG: {fedu.get('ig_seeding_hook')}")
        
    print("\n[3] TÌNH HUỐNG THỰC TẾ (Mới):")
    print(f"  {item.get('practice_scenario')}")
