import json
import subprocess
import re

with open('scratch/deep_audit_results.json') as f:
    items = json.load(f)

def curl_status(url):
    if not url or not url.startswith('http'):
        return 0
    cmd = ['curl', '-s', '-I', '-o', '/dev/null', '-w', '%{http_code}', '--connect-timeout', '10', '--max-time', '15', url]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        code = res.stdout.strip()
        return int(code) if code.isdigit() else 0
    except:
        return 0

results = []
for idx, it in enumerate(items, 1):
    iid = it['id']
    title = it['title']
    creator = it['creator']
    hook = it['hook_url']
    key = it['key_url']
    
    code_h = curl_status(hook)
    code_k = curl_status(key)
    
    results.append({
        'id': iid,
        'creator': creator,
        'title': title,
        'hook_url': hook,
        'key_url': key,
        'hook_code': code_h,
        'key_code': code_k
    })
    print(f"[{idx:2d}/{len(items)}] {creator[:18]} | Hook: {code_h} | Key: {code_k} | {title[:45]}")

with open('scratch/precise_results.json', 'w') as out:
    json.dump(results, out, indent=2, ensure_ascii=False)

