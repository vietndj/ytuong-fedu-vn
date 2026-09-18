import json

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/master_classifications.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

for vid, data in db.items():
    # Migrate industry -> industries
    if 'industry' in data:
        data['industries'] = [data['industry']]
        del data['industry']
    elif 'industries' not in data:
        data['industries'] = []
    
    # Add x_factors if not present
    if 'x_factors' not in data:
        data['x_factors'] = []

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/master_classifications.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Migration completed.")
