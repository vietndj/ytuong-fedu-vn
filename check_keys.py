import json
import re

file_path = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = (\{.*\});?', content, re.DOTALL)
json_str = match.group(1)
data = json.loads(json_str)

for i, idea in enumerate(data.get('ideas', [])[:5]):
    print(f"Idea {i} keys: {list(idea.keys())}")
    print(f"Idea {i} media keys: {list(idea.get('media', {}).keys())}")
    if 'thumbnail' in idea: print("has thumbnail")
    if 'cover_image' in idea: print("has cover_image")
