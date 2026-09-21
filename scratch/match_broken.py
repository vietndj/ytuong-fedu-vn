import json
import os
import re

with open('scratch/broken_images_report.json') as f:
    rep = json.load(f)

active_broken = rep['active_broken']

with open('scratch/r2_image_folders.txt') as f:
    r2_folders = [line.strip().rstrip('/') for line in f if line.strip()]

reports = os.listdir('reports')

print(f"Analyzing {len(active_broken)} broken ideas against {len(r2_folders)} R2 folders and {len(reports)} reports...")

matches = {}

for item in active_broken:
    item_id = item['id']
    shortcode = item.get('shortcode') or ''
    # extract shortcode from id if not set
    if not shortcode:
        m = re.search(r'([A-Za-z0-9_-]{11})', item_id)
        if m:
            shortcode = m.group(1)
            
    creator = item.get('creator', '').lower().replace(' ', '').replace('@', '')
    title = item.get('title', '')
    
    # Check matching r2 folders
    matched_r2 = []
    for f in r2_folders:
        f_lower = f.lower()
        if shortcode and shortcode.lower() in f_lower:
            matched_r2.append(f)
        elif creator and len(creator) > 3 and creator in f_lower:
            matched_r2.append(f)
            
    # Check matching reports
    matched_rep = []
    for r in reports:
        r_lower = r.lower()
        if shortcode and shortcode.lower() in r_lower:
            matched_rep.append(r)
        elif creator and len(creator) > 3 and creator in r_lower:
            matched_rep.append(r)
            
    matches[item_id] = {
        'id': item_id,
        'shortcode': shortcode,
        'creator': item['creator'],
        'title': title,
        'hook_status': item['hook_status'],
        'key_status': item['key_status'],
        'hook': item['hook'],
        'key': item['key'],
        'matched_r2': matched_r2,
        'matched_rep': matched_rep
    }

for idx, m in enumerate(matches.values(), 1):
    print(f"\n{idx}. [{m['id']}] {m['creator']} | SC: {m['shortcode']}")
    print(f"   Title: {m['title'][:60]}")
    print(f"   Hook ({m['hook_status']}): {m['hook']}")
    print(f"   Key  ({m['key_status']}): {m['key']}")
    print(f"   R2 matches: {m['matched_r2']}")
    print(f"   Report matches: {m['matched_rep']}")

with open('scratch/matched_broken.json', 'w') as out:
    json.dump(matches, out, indent=2, ensure_ascii=False)

