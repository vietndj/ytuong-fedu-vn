import re
import json
import os
import urllib.parse
from bs4 import BeautifulSoup

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'var FEDU_IDEAS_DATABASE\s*=\s*(\{[\s\S]*\});?\s*$', content)
if not m:
    print("Cannot parse ideas_data.js")
    exit(1)

db = json.loads(m.group(1))
ideas = db.get('ideas', [])
active_ideas = [i for i in ideas if not i.get('is_excluded')]

print(f"Total ideas: {len(ideas)}, Active ideas: {len(active_ideas)}")

def count_actual_shots_in_html(report_path):
    if not os.path.exists(report_path):
        return 0, False, "File không tồn tại"
    try:
        with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        if len(html.strip()) < 500:
            return 0, False, "File quá ngắn hoặc rỗng"
        
        # Method 1: regex for shot headers
        shot_nums = set()
        for m in re.finditer(r'(?:SHOT|Shot|Phân cảnh|PHÂN CẢNH)\s+(\d+)', html):
            shot_nums.add(int(m.group(1)))
            
        # Method 2: check shot cards
        card_matches = re.findall(r'class="[^"]*(?:shot-card|shot-item|storyboard-card)[^"]*"', html)
        
        # Method 3: check slide numbers if carousel
        slide_nums = set()
        for m in re.finditer(r'(?:SLIDE|Slide|Slide-video)\s+(\d+)', html):
            slide_nums.add(int(m.group(1)))
            
        count = 0
        if shot_nums:
            count = max(shot_nums)
        elif slide_nums:
            count = max(slide_nums)
        elif card_matches:
            count = len(card_matches)
            
        # Has real content?
        has_content = ("shot" in html.lower() or "phân cảnh" in html.lower() or "báo cáo" in html.lower()) and count > 0
        return count, has_content, "OK"
    except Exception as e:
        return 0, False, str(e)

# Audit each idea
report_issues = []
shots_issues = []

for item in active_ideas:
    iid = item.get('id', '')
    title = item.get('title_vi') or item.get('title') or ''
    creator = item.get('creator', {}).get('name') or item.get('creator', {}).get('raw') or ''
    media = item.get('media', {})
    rep_url = media.get('report_url', '') or ''
    shots_count = media.get('shots_count', 0)
    
    # 1. Check report
    rep_file_exists = False
    actual_shots = 0
    rep_has_content = False
    rep_status = "NO_REPORT_URL"
    
    if rep_url:
        clean_rep = urllib.parse.unquote(rep_url)
        # Check in reports/ and dist/reports/
        cand1 = clean_rep
        cand2 = os.path.join('reports', os.path.basename(clean_rep))
        cand3 = os.path.join('dist', clean_rep)
        
        target_path = None
        for cand in [cand1, cand2, cand3]:
            if os.path.exists(cand):
                target_path = cand
                break
                
        if target_path:
            rep_file_exists = True
            actual_shots, rep_has_content, msg = count_actual_shots_in_html(target_path)
            if rep_has_content:
                rep_status = "VALID_CONTENT"
            else:
                rep_status = f"EMPTY_OR_NO_SHOTS ({msg})"
        else:
            rep_status = "FILE_NOT_FOUND_ON_DISK"
            
    # Record report issues (click vào không ra báo cáo)
    if not rep_url or not rep_file_exists or not rep_has_content:
        report_issues.append({
            'id': iid,
            'creator': creator,
            'title': title,
            'report_url': rep_url,
            'rep_status': rep_status,
            'actual_shots': actual_shots,
            'shots_count': shots_count
        })
        
    # 2. Check shots_count issues (bị 0 shot hoặc sai lệch so với báo cáo)
    if shots_count == 0 or (actual_shots > 0 and shots_count != actual_shots):
        shots_issues.append({
            'id': iid,
            'creator': creator,
            'title': title,
            'recorded_shots': shots_count,
            'actual_shots': actual_shots,
            'report_url': rep_url,
            'reason': "Ghi 0 shot" if shots_count == 0 else f"Sai lệch: ghi {shots_count} shots nhưng báo cáo có {actual_shots} shots"
        })

print(f"\n--- AUDIT SUMMARY ---")
print(f"1. Ý tưởng lỗi báo cáo (ấn vào không ra báo cáo / rỗng): {len(report_issues)}")
print(f"2. Ý tưởng sai số shot (0 shot hoặc lệch so với thực tế): {len(shots_issues)}")

with open('scratch/report_issues.json', 'w', encoding='utf-8') as f:
    json.dump(report_issues, f, ensure_ascii=False, indent=2)

with open('scratch/shots_issues.json', 'w', encoding='utf-8') as f:
    json.dump(shots_issues, f, ensure_ascii=False, indent=2)

