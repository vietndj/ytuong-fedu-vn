import json

with open('/tmp/master_good.json', 'r', encoding='utf-8') as f:
    good = json.load(f)

with open('master_classifications.json', 'r', encoding='utf-8') as f:
    current = json.load(f)

restored_count = 0
for vid_id, data in good.items():
    if 'x_factors' in data:
        if vid_id in current:
            current[vid_id]['x_factors'] = data['x_factors']
            restored_count += 1
        else:
            # Maybe the ID changed? Let's check by title or shortcode
            # The shortcode extraction
            import re
            m = re.search(r'_(D[A-Za-z0-9_-]{9,11})', vid_id)
            if m:
                shortcode = m.group(1).rstrip('_')
                for curr_id, curr_data in current.items():
                    if shortcode in curr_id:
                        curr_data['x_factors'] = data['x_factors']
                        restored_count += 1
                        break

print(f"Restored x_factors for {restored_count} videos.")

with open('master_classifications.json', 'w', encoding='utf-8') as f:
    json.dump(current, f, ensure_ascii=False, indent=4)
