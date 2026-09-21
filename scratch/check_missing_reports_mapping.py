import json
import os
import re

with open('scratch/simulated_click_audit.json') as f:
    audit = json.load(f)

no_reports = [x for x in audit if x['click_status'] != 'OPENS_REPORT_MODAL']
reports_in_folder = os.listdir('reports')

print(f"Total ideas without report modal: {len(no_reports)}")

found_match = []
not_found_match = []

for item in no_reports:
    iid = item['id']
    title = item['title']
    creator = item['creator']
    
    # Try find by shortcode or keyword
    sc = ""
    m = re.search(r'([A-Za-z0-9_-]{11})', iid)
    if m: sc = m.group(1)
    
    matched_rep = None
    for r in reports_in_folder:
        if sc and sc.lower() in r.lower():
            matched_rep = r
            break
        # Also check title keywords
        if not matched_rep:
            # check distinctive words
            words = [w for w in re.split(r'[\s\-_,.:;]+', title) if len(w) > 4 and w.lower() not in ['video', 'nghệ', 'thuật', 'phân', 'tích', 'báo', 'cáo', 'chuỗi', 'kịch', 'bản']]
            if words:
                matches_count = sum(1 for w in words if w.lower() in r.lower())
                if matches_count >= 2:
                    matched_rep = r
                    break

    if matched_rep:
        found_match.append({
            'id': iid,
            'creator': creator,
            'title': title,
            'matched_report': matched_rep
        })
    else:
        not_found_match.append({
            'id': iid,
            'creator': creator,
            'title': title
        })

print(f"\n1. Found matching report file in reports/ ({len(found_match)} items):")
for f in found_match:
    print(f"  [{f['id']}] {f['creator']} -> reports/{f['matched_report']}")

print(f"\n2. Truly missing report file ({len(not_found_match)} items):")
for nf in not_found_match:
    print(f"  [{nf['id']}] {nf['creator']} - {nf['title'][:50]}")

