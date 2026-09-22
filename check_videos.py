import re
import json

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'var FEDU_IDEAS_DATABASE\s*=\s*(\{[\s\S]*\});?\s*$', content)
db = json.loads(m.group(1))

empty_count = 0
for idea in db.get('ideas', []):
    if idea.get('is_excluded'): continue
    video_url = idea.get('media', {}).get('video_preview', '')
    if not video_url:
        video_url = idea.get('media', {}).get('video_url', '')
    if not video_url:
        video_url = idea.get('video_url', '')
    
    if not video_url:
        empty_count += 1
        # print(f"Empty: {idea['id']}")
print(f"Total active: {len([i for i in db.get('ideas', []) if not i.get('is_excluded')])}")
print(f"Empty video URL count: {empty_count}")
