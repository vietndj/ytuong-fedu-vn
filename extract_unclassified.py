import json
import re

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js', 'r') as f:
    content = f.read()

json_str = re.search(r'var FEDU_IDEAS_DATABASE = (\{.*?\});', content, re.DOTALL).group(1)
data = json.loads(json_str)

unclassified = []
for idea in data['ideas']:
    tags = idea.get('tags', [])
    if len(tags) <= 2: 
        unclassified.append(idea)
    if len(unclassified) >= 10:
        break

for i, item in enumerate(unclassified, 1):
    print(f"{i}. {item.get('title_vi', 'N/A')} (@{item.get('creator', {}).get('handle')})")
    url = f"https://ytuong.fedu.vn/?id={item.get('id')}"
    print(f"👉 Link xem: {url}")
