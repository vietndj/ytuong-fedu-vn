import re
import json
import ssl
import concurrent.futures
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError

ctx = ssl._create_unverified_context()

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'var FEDU_IDEAS_DATABASE\s*=\s*(\{[\s\S]*\});?\s*$', content)
if not m:
    print("Failed to parse database")
    exit(1)

db = json.loads(m.group(1))
ideas = db.get('ideas', [])

def check_url(url, timeout=5):
    if not url or not url.startswith('http'):
        return 0, "EMPTY"
    try:
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            return resp.status, "OK"
    except HTTPError as e:
        return e.code, str(e.code)
    except URLError as e:
        return 0, str(e.reason)
    except Exception as e:
        return 0, str(e)

def test_image_with_fallback(url):
    """Test image following browser retry logic:
       1. original
       2. urlencoded
       3. with /extracted_shots/
       4. .webp <-> .jpg swap
    """
    if not url or not url.startswith('http'):
        return False, "EMPTY", url
    
    code, msg = check_url(url)
    if code == 200:
        return True, "200 OK", url
    
    # Try encoded
    try:
        parsed = urllib.parse.urlparse(url)
        encoded_path = '/'.join(urllib.parse.quote(urllib.parse.unquote(p)) for p in parsed.path.split('/'))
        safe_url = urllib.parse.urlunparse(parsed._replace(path=encoded_path))
        if safe_url != url:
            c, _ = check_url(safe_url)
            if c == 200:
                return True, f"200 OK (encoded)", safe_url
    except:
        pass

    # Try extracted_shots
    if "/images/" in url and "/extracted_shots/" not in url:
        parts = url.split("/images/")
        if len(parts) == 2:
            sub = parts[1].split("/")
            if len(sub) >= 2:
                folder = sub[0]
                rest = "/".join(sub[1:])
                alt_url = f"{parts[0]}/images/{folder}/extracted_shots/{rest}"
                c, _ = check_url(alt_url)
                if c == 200:
                    return True, f"200 OK (extracted_shots)", alt_url

    # Try webp / jpg swap
    for ext_from, ext_to in [('.webp', '.jpg'), ('.jpg', '.webp')]:
        if ext_from in url:
            alt_url = url.replace(ext_from, ext_to)
            c, _ = check_url(alt_url)
            if c == 200:
                return True, f"200 OK ({ext_to})", alt_url

    return False, str(code), url

def inspect_idea(item):
    idx = item.get('id', '')
    shortcode = item.get('shortcode', '')
    title = item.get('title_vi') or item.get('title') or ''
    creator_obj = item.get('creator', {})
    creator = creator_obj.get('name') or creator_obj.get('raw') or item.get('creator_name') or ''
    is_excluded = item.get('is_excluded', False)
    
    media = item.get('media', {})
    hook = media.get('thumb_hook', '')
    key = media.get('thumb_key', '')
    
    hook_ok, hook_status, hook_effective = test_image_with_fallback(hook)
    key_ok, key_status, key_effective = test_image_with_fallback(key)
    
    return {
        'id': idx,
        'shortcode': shortcode,
        'creator': creator,
        'title': title,
        'is_excluded': is_excluded,
        'hook': hook,
        'key': key,
        'hook_ok': hook_ok,
        'hook_status': hook_status,
        'hook_effective': hook_effective,
        'key_ok': key_ok,
        'key_status': key_status,
        'key_effective': key_effective
    }

print(f"Checking {len(ideas)} ideas in parallel...")
with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
    results = list(executor.map(inspect_idea, ideas))

broken_ideas = [r for r in results if not r['hook_ok'] or not r['key_ok']]
active_broken = [r for r in broken_ideas if not r['is_excluded']]
excluded_broken = [r for r in broken_ideas if r['is_excluded']]

print(f"\n--- SCAN RESULTS ---")
print(f"Total ideas checked: {len(results)}")
print(f"Total ideas with broken/missing images: {len(broken_ideas)}")
print(f"  - Active ideas with broken images: {len(active_broken)}")
print(f"  - Excluded ideas with broken images: {len(excluded_broken)}")

with open('scratch/broken_images_report.json', 'w', encoding='utf-8') as out:
    json.dump({
        'total': len(results),
        'total_broken': len(broken_ideas),
        'active_broken_count': len(active_broken),
        'excluded_broken_count': len(excluded_broken),
        'active_broken': active_broken,
        'excluded_broken': excluded_broken
    }, out, ensure_ascii=False, indent=2)

print("\n--- ACTIVE BROKEN IDEAS SUMMARY ---")
for i, b in enumerate(active_broken, 1):
    print(f"{i:2d}. [{b['id']}] {b['creator']} | Title: {b['title'][:60]} | Hook: {b['hook_status']} | Key: {b['key_status']}")

