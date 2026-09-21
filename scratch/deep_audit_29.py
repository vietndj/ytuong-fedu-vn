import json
import os
import re
import ssl
import urllib.request

ctx = ssl._create_unverified_context()

with open('scratch/broken_images_report.json') as f:
    data = json.load(f)

active = data['active_broken']

with open('scratch/r2_image_folders.txt') as f:
    r2_folders = [line.strip().rstrip('/') for line in f if line.strip()]

def check_url(url):
    if not url or not url.startswith('http'):
        return 0
    try:
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
            return resp.status
    except Exception as e:
        return 0

print(f"Deep auditing all {len(active)} items...")

audit_results = []

for item in active:
    iid = item['id']
    title = item['title']
    creator = item['creator']
    hook = item['hook']
    key = item['key']
    h_stat = item['hook_status']
    k_stat = item['key_status']
    
    # Try find actual folder on R2
    shortcode = item.get('shortcode') or ''
    if not shortcode:
        m = re.search(r'([A-Za-z0-9_-]{11})', iid)
        if m: shortcode = m.group(1)
        
    found_r2_folder = None
    if shortcode:
        for f in r2_folders:
            if shortcode in f:
                found_r2_folder = f
                break
                
    # Check if files can be found
    working_hook = None
    working_key = None
    
    # Candidates for hook/key
    folders_to_check = []
    if found_r2_folder:
        folders_to_check.append(found_r2_folder)
        
    # Extract folder from current hook
    m_f = re.search(r'/images/([^/]+)/', hook)
    if m_f:
        folders_to_check.append(urllib.parse.unquote(m_f.group(1)))
        
    # Test possible filenames
    for folder in set(folders_to_check):
        quoted = urllib.parse.quote(folder)
        patterns = [
            f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{quoted}/shot_01_mid.webp",
            f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{quoted}/shot_01_mid.jpg",
            f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{quoted}/slide_01_mid.webp",
            f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{quoted}/slide_01_mid.jpg",
            f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{quoted}/carousel_slides/slide_01_mid.webp",
            f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{quoted}/extracted_shots/shot_01_mid.webp",
            f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{quoted}/img_001_mid.webp",
            f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{quoted}/img_001_38273934.webp", # withyuee #4
            f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{quoted}/img_001_61880809.webp", # withyuee #5
        ]
        for p in patterns:
            if check_url(p) == 200:
                working_hook = p
                break
        if working_hook: break
        
    audit_results.append({
        'id': iid,
        'shortcode': shortcode,
        'creator': creator,
        'title': title,
        'hook_status': h_stat,
        'key_status': k_stat,
        'hook_url': hook,
        'key_url': key,
        'r2_folder': found_r2_folder,
        'working_hook': working_hook
    })

with open('scratch/deep_audit_results.json', 'w') as out:
    json.dump(audit_results, out, indent=2, ensure_ascii=False)

print("Saved scratch/deep_audit_results.json")
