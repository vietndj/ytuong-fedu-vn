import json
import re

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = ({.*});', content, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    for idea in data.get('ideas', []):
        if idea.get('id') == 'Hong_Kong_Urban_Transitions_@withyuee':
            print(json.dumps(idea.get('media', {}), indent=2))
