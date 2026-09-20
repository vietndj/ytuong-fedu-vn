import json
import urllib.request

with open('dist/ideas_data.js', 'r') as f:
    content = f.read()

import re
match = re.search(r'var FEDU_IDEAS_DATABASE = ({[\s\S]*?});', content)
db = json.loads(match.group(1))

missing = []
for item in db['ideas']:
    thumb = item.get('media', {}).get('thumb_hook')
    if thumb:
        try:
            req = urllib.request.Request(thumb, method='HEAD')
            urllib.request.urlopen(req, timeout=3)
        except Exception as e:
            missing.append(thumb)

print(f"Total checked: {len(db['ideas'])}")
print(f"Total missing: {len(missing)}")
if missing:
    print("First 5 missing:", missing[:5])
