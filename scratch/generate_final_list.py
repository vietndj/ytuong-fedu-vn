import json

with open('scratch/precise_results.json') as f:
    res = json.load(f)

with open('scratch/deep_audit_results.json') as f:
    deep = {x['id']: x for x in json.load(f)}

both = [x for x in res if x['hook_code'] != 200 and x['key_code'] != 200]
key_only = [x for x in res if x['hook_code'] == 200 and x['key_code'] != 200]

print(f"Total: {len(both) + len(key_only)}")
print(f"Both broken: {len(both)}")
print(f"Key broken: {len(key_only)}")

final_data = {
    'both': both,
    'key_only': key_only
}

with open('scratch/final_classified.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

