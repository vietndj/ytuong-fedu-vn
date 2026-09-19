import json

with open('master_classifications.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

for k, v in master.items():
    if 'x_factors' in v:
        if "Basic classification" in v['x_factors']:
            v['x_factors'].remove("Basic classification")

with open('master_classifications.json', 'w', encoding='utf-8') as f:
    json.dump(master, f, ensure_ascii=False, indent=4)
