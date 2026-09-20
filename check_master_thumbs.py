import json

with open('master_classifications.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

missing = []
for k, v in master.items():
    media = v.get('media', {})
    thumb_hook = media.get('thumb_hook')
    thumb_key = media.get('thumb_key')
    
    if not thumb_hook or not thumb_key:
        missing.append(k)

print(f"Total missing thumbs: {len(missing)}")
if missing:
    print(missing[:10])
