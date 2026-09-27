import json

with open('tag_migration_map.json', 'r') as f:
    mapping = json.load(f)['merge_map']

with open('master_classifications.json', 'r') as f:
    master = json.load(f)

for k, v in master.items():
    if 'tags' in v:
        new_tags = []
        for t in v['tags']:
            if t in mapping:
                mapped_val = mapping[t]
                if mapped_val != '__REMOVE__' and mapped_val not in new_tags:
                    new_tags.append(mapped_val)
            else:
                new_tags.append(t)
        v['tags'] = new_tags

with open('master_classifications.json', 'w') as f:
    json.dump(master, f, ensure_ascii=False, indent=2)

print("Migrated master_classifications.json")
