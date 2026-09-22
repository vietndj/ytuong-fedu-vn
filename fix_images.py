import json
import re

html_path = "./reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html"
dist_html_path = "./dist/reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html"

with open("gdrive_folders.json", "r", encoding="utf-8") as f:
    gdrive = json.load(f)

mapping = {}
for item in gdrive:
    path = item['path']
    if "DcVnyJyNWGY" in path and path.endswith(".jpg"):
        filename = path.split("/")[-1]
        mapping[filename] = item['url']

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def replacer(match):
        filename = match.group(1)
        if filename in mapping:
            return mapping[filename]
        return match.group(0)

    # Use a non-greedy match for the folder just in case
    content = re.sub(r'https://pub-447bd44dfdac4938912655c855b8631c\.r2\.dev/images/[^"\']*/(shot_\d+_mid\.jpg)', replacer, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file(html_path)
fix_file(dist_html_path)

print("Images replaced.")
