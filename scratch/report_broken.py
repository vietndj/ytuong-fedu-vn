import json
import re

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = ({.*});', content, re.DOTALL)
if not match: exit(1)
data = json.loads(match.group(1))

# Read the IDs from check_404 output
import sys
broken_ids = set()
with open('/Users/vietmac/.gemini/antigravity/brain/832729d7-7c13-4fc3-b0eb-0c1bea314a89/.system_generated/tasks/task-58.log', 'r') as logf:
    for line in logf:
        if line.startswith('- '):
            broken_ids.add(line[2:].strip())

with open('/Users/vietmac/.gemini/antigravity/brain/832729d7-7c13-4fc3-b0eb-0c1bea314a89/broken_ideas.md', 'w') as out:
    out.write("# Danh Sách Ý Tưởng Bị Lỗi (Thumbnail 404 / Thiếu Video)\n\n")
    out.write(f"Tổng cộng: {len(broken_ids)} ý tưởng bị lỗi.\n\n")
    count = 0
    for idea in data.get('ideas', []):
        if idea.get('id') in broken_ids:
            count += 1
            creator = idea.get('creator', {}).get('name', 'Unknown')
            title = idea.get('title_vi') or idea.get('title', 'No Title')
            out.write(f"{count}. **{creator}**: {title} (`{idea.get('id')}`)\n")
            
