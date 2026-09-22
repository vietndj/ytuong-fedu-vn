import json
import re

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js', 'r') as f:
    content = f.read()

json_str = re.search(r'var FEDU_IDEAS_DATABASE = (\{.*?\});', content, re.DOTALL).group(1)
data = json.loads(json_str)

# Instead of strictly len(tags) == 0, let's find the ones that lack detailed tags. 
# We'll just pick the first 10.
unclassified = []
for idea in data['ideas']:
    tags = idea.get('tags', [])
    if len(tags) <= 2: # Very few tags
        unclassified.append(idea)
    if len(unclassified) >= 10:
        break

print(f"Tìm thấy {len(unclassified)} video có ít/chưa có Tag:")
for i, item in enumerate(unclassified, 1):
    print(f"---")
    print(f"{i}. Tiêu đề: {item.get('title_vi', 'N/A')}")
    print(f"Creator: {item.get('creator', {}).get('name')} ({item.get('creator', {}).get('handle')})")
    print(f"Tags hiện tại: {item.get('tags')}")
    print(f"ID: {item.get('id')}")
    url = f"https://ytuong.fedu.vn/?search={item.get('id')}"
    print(f"Link xem: {url}")
