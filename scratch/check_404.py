import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = ({.*});', content, re.DOTALL)
if not match:
    print("Could not find database payload in ideas_data.js")
    exit(1)

data = json.loads(match.group(1))
ideas = data.get('ideas', [])

def check_url(idea):
    media = idea.get('media', {})
    if not media: return None
    
    thumb = media.get('thumb_hook')
    video = media.get('video_url')
    
    broken = []
    
    # Check thumb
    if thumb and thumb.startswith('http'):
        try:
            req = urllib.request.Request(thumb, method='HEAD')
            with urllib.request.urlopen(req, timeout=5) as res:
                if res.status != 200:
                    broken.append(f"Thumb 404: {thumb}")
        except Exception as e:
            broken.append(f"Thumb error: {e}")
            
    # We won't check video_url for now to save time, or maybe just check it too.
    
    if broken:
        return {
            "id": idea.get("id"),
            "title": idea.get("title_vi") or idea.get("title"),
            "broken": broken
        }
    return None

results = []
with ThreadPoolExecutor(max_workers=20) as executor:
    for res in executor.map(check_url, ideas):
        if res:
            results.append(res)

print(f"Total broken ideas (thumb): {len(results)}")
for r in results:
    print(f"- {r['id']}")
