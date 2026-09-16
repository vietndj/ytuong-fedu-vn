import json
import re

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = ({.*});', content, re.DOTALL)
if not match:
    print("Could not find database payload in ideas_data.js")
    exit(1)

data = json.loads(match.group(1))

broken_ideas = []
for idea in data.get('ideas', []):
    broken_reasons = []
    
    media = idea.get('media', {})
    if not media:
        broken_reasons.append("No media object")
    else:
        if not media.get('video_url') and not media.get('cover_image'):
            broken_reasons.append("Both video_url and cover_image are missing/empty")
        
    if broken_reasons:
        broken_ideas.append({
            "id": idea.get('id'),
            "title": idea.get('title'),
            "creator": idea.get('creator'),
            "reasons": broken_reasons
        })

print(f"Total broken ideas: {len(broken_ideas)}")
for b in broken_ideas:
    print(f"- ID: {b['id']} | Title: {b['title']} | Creator: {b['creator']}")
    for r in b['reasons']:
        print(f"  * {r}")
