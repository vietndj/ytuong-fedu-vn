import re
import json

file_path = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except Exception as e:
    print(f"Error reading {file_path}: {e}")
    exit(1)

# Extract JSON from ideas_data.js
# var FEDU_IDEAS_DATABASE = {...};
match = re.search(r'var\s+FEDU_IDEAS_DATABASE\s*=\s*(\{.*?\});\s*$', content, re.DOTALL)
if not match:
    # Try another approach, just find the first { and the last }
    start = content.find('{')
    end = content.rfind('}')
    if start != -1 and end != -1:
        data_str = content[start:end+1]
    else:
        print("Could not find JSON object")
        exit(1)
else:
    data_str = match.group(1)

try:
    data = json.loads(data_str)
except Exception as e:
    print(f"Error parsing JSON: {e}")
    exit(1)

tags_freq = {}
for idea in data.get('ideas', []):
    tags = idea.get('tags', [])
    for tag in tags:
        if tag not in tags_freq:
            tags_freq[tag] = 0
        tags_freq[tag] += 1

unique_tags = list(tags_freq.keys())
print(f"Total unique tags before: {len(unique_tags)}")
print(f"Unique tags: {unique_tags}")

# Generate a more comprehensive mapping based on user instructions
canonical_map = {
    "Food": ["Ẩm Thực & F&B", "am-thuc", "F&B", "Food", "Ẩm thực", "Nấu ăn", "am thuc", "nấu ăn", "cafe", "coffee", "baking", "đồ ăn", "do an"],
    "Fashion": ["Thời Trang", "thoi-trang", "Fashion", "Trang phục", "OOTD", "mix & match", "outfit", "phối đồ", "phoi do"],
    "Travel": ["Du Lịch & Văn Hóa", "du-lich", "Travel", "Du lịch", "Khám phá", "cảnh đẹp", "phong cảnh", "canh dep", "phong canh"],
    "Tech": ["Công Nghệ", "cong-nghe", "Tech", "Thiết bị", "Gadget", "setup", "bàn làm việc", "ban lam viec"],
    "Sport": ["Thể Thao", "the-thao", "Sport", "Gym", "Fitness", "yoga", "chạy bộ"],
    "Beauty": ["Spa & Làm Đẹp", "spa-lam-dep", "Beauty", "Makeup", "Skincare", "làm đẹp", "lam dep", "chăm sóc da"],
    "Branding": ["Thương Hiệu & Dịch Vụ", "thuong-hieu", "Branding", "Doanh nghiệp", "kinh doanh", "doanh nghiep"],
    "UGC": ["UGC - Đánh Giá SP", "ugc", "Review", "đánh giá", "danh gia", "unboxing", "mở hộp", "mo hop"],
    "Life": ["Kiến Trúc & Không Gian Sống", "kien-truc", "Life", "Góc nhà đẹp", "Không gian", "Nhà cửa", "Lifestyle", "Thói quen", "đời sống", "doi song", "daily", "decor", "không gian sống", "nội thất"],
    "Deep Talk": ["Tâm Lý", "Podcast", "Tâm sự", "Deep Talk", "Phát Triển Bản Thân", "phat-trien-ban-than", "tâm lý", "tam ly", "chia sẻ", "chia se", "động lực", "dong luc", "học tập", "hoc tap", "giáo dục", "giao duc"],
    "Framing": ["Kỹ Thuật Quay Dựng & Điện Ảnh", "ky-thuat-quay", "Framing", "Góc quay", "Điện ảnh", "Cinematic", "Cinematic B-Roll", "Cinematic B-roll", "B-Roll Điện Ảnh", "B-roll", "b-roll", "transition", "Chuyển cảnh", "kỹ xảo", "vfx", "edit", "hiệu ứng"],
}

# The user explicitly said: Shooting Style (Walk&Talk, Talking Head...) shouldn't be in tags.
styles_to_remove = ["Chỉn Chu", "Chuyển Cảnh", "Nói Trực Diện", "Kể Chuyện", "Lồng Tiếng", "Walk & Talk", "Theo nhịp nhạc", "Walk-and-Talk", "Tĩnh", "Thong Dong"]
# Also exact matches to the user mentioned tags that are styles
styles_to_remove_lower = [s.lower() for s in styles_to_remove]

merge_map = {}
for tag in unique_tags:
    mapped = False
    for canon, variants in canonical_map.items():
        if tag in variants or tag.lower() in [v.lower() for v in variants]:
            merge_map[tag] = canon
            mapped = True
            break
    
    if not mapped:
        if tag in styles_to_remove or tag.lower() in styles_to_remove_lower:
             merge_map[tag] = "__REMOVE__"
             mapped = True
        else:
             # Try to map to the best one based on string match
             if "b-roll" in tag.lower() or "cinematic" in tag.lower():
                 merge_map[tag] = "Framing"
             elif "talk" in tag.lower() or "podcast" in tag.lower():
                 merge_map[tag] = "Deep Talk"
             elif "nhà" in tag.lower() or "life" in tag.lower():
                 merge_map[tag] = "Life"
             elif "vlog" in tag.lower():
                 merge_map[tag] = "Life"
             elif "hài" in tag.lower() or "fun" in tag.lower():
                 merge_map[tag] = "Entertainment"
             else:
                 merge_map[tag] = "Others"

# Make sure all required mappings are present
for t in unique_tags:
    if t not in merge_map:
        merge_map[t] = "Others"

output = {
    "canonical_tags": list(canonical_map.keys()) + ["Entertainment", "Others"],
    "merge_map": merge_map
}

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/tag_migration_map.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Generated tag_migration_map.json with {len(merge_map)} keys")
