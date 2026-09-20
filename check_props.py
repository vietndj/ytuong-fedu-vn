import json
import re

file_path = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = (\{.*\});?', content, re.DOTALL)
json_str = match.group(1)
data = json.loads(json_str)

has_thumbnail = 0
has_cover = 0
for idea in data.get('ideas', []):
    if 'thumbnail' in idea or 'thumbnail' in idea.get('media', {}):
        has_thumbnail += 1
    if 'cover_image' in idea or 'cover_image' in idea.get('media', {}):
        has_cover += 1
        
print("has_thumbnail:", has_thumbnail)
print("has_cover:", has_cover)
