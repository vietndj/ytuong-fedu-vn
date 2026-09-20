import json
import re

file_path = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the JSON part
match = re.search(r'var FEDU_IDEAS_DATABASE = (\{.*\});?', content, re.DOTALL)
if not match:
    print("Could not find FEDU_IDEAS_DATABASE")
    exit(1)

json_str = match.group(1)
try:
    data = json.loads(json_str)
except Exception as e:
    print("JSON parse error:", e)
    exit(1)

missing_count = 0
for idea in data.get('ideas', []):
    media = idea.get('media', {})
    
    # Let's see what keys are there
    if not media.get('thumb_hook') and not media.get('thumbnail') and not idea.get('thumbnail') and not idea.get('cover_image'):
        missing_count += 1
        print("Missing for:", idea.get('id'), idea.get('title_vi'))

print("Total missing:", missing_count)
