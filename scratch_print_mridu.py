import json

with open('master_classifications.json', 'r') as f:
    data = json.load(f)

for k, v in data.items():
    creator = str(v.get('creator', '')).lower()
    if 'mridupawasharma' in creator:
        print(k)
        print(v.get('folder_name'))
        print(v.get('main_html_rel'))
        print(v.get('main_vid_rel'))
        print(v.get('thumbs'))
        print('---')
