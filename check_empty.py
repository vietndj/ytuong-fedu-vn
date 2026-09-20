import json
import re

file_path = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = (\{.*\});?', content, re.DOTALL)
json_str = match.group(1)
data = json.loads(json_str)

empty_thumb_hook = 0
for idea in data.get('ideas', []):
    media = idea.get('media', {})
    if not media.get('thumb_hook'):
        empty_thumb_hook += 1
        
print("Empty thumb_hook:", empty_thumb_hook)
