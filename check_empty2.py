import json
import re

file_path = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = (\{.*\});?', content, re.DOTALL)
json_str = match.group(1)
data = json.loads(json_str)

empty_thumbs = 0
for idea in data.get('ideas', []):
    media = idea.get('media', {})
    thumb = media.get('thumb_hook', '')
    if not thumb or thumb.strip() == '' or 'placehold' in thumb:
        empty_thumbs += 1

print("Empty or placeholder thumbs:", empty_thumbs)
