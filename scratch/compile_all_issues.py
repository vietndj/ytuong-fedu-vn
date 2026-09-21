import re
import json
import os
import urllib.parse

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'var FEDU_IDEAS_DATABASE\s*=\s*(\{[\s\S]*\});?\s*$', content)
db = json.loads(m.group(1))
ideas = db.get('ideas', [])
active = [i for i in ideas if not i.get('is_excluded')]

with open('scratch/precise_results.json') as f:
    img_res = {x['id']: x for x in json.load(f)}

# All reports on disk
reports_dir = 'reports'
all_reports = os.listdir(reports_dir)

def count_shots_in_html(fname):
    path = os.path.join(reports_dir, fname)
    if not os.path.exists(path):
        return 0
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
            txt = fp.read()
        nums = set(int(m.group(1)) for m in re.finditer(r'(?:SHOT|Shot|Phân cảnh)\s+(\d+)', txt))
        if nums:
            return max(nums)
        # try slide
        slides = set(int(m.group(1)) for m in re.finditer(r'(?:SLIDE|Slide)\s+(\d+)', txt))
        if slides:
            return max(slides)
        # try card count
        cards = len(re.findall(r'class="[^"]*(?:shot-card|shot-item|storyboard-card)[^"]*"', txt))
        return cards
    except:
        return 0

# Match reports to ideas
mapped_reports = {}
for r in all_reports:
    # try extract shortcode
    m = re.search(r'([A-Za-z0-9_-]{11})', r)
    if m:
        mapped_reports[m.group(1)] = r

# Map special known names
known_mapping = {
    "DYKO1v3g3U2": "The_Art_of_Noticing_Hong_Kong - @withyuee.html",
    "DXbzOkygG0v": "Gough_Street_Central_Hong_Kong - @withyuee.html",
    "Dbk4X4tjJ8A": "London Cinematic Video Postcards - @daiki.shino.html",
    "DctVSroI3UB": "Creative phone video ideas - @valenti_k41.html",
    "DYcM_9FPr7I": "Hong_Kong_Coffee_Morning_Routine - @jazziesillona.html",
    "DXoss18j011": "Tai_Hang_Hong_Kong_Street - @jazziesillona.html",
    "DUS5DYCEgyg": "Mat_Chuoc_x_Pho_Hong_Kong - @jazziesillona.html",
    "DZVAYFwvo4y": "IG_@Jazzie_DZVAYFwvo4y_Video_by_jazziesillona.html",
    "Dc6Cxf-QRWh": "IG_@jazziesillona_Dc6Cxf-QRWh.html",
    "Db7zNC0jPwV": "Tokyo_Slow_Life_Magic_Moments - @ioana_iftode.html",
    "DXWKIztktTN": "Saigon, Vietnam - @qfroost.html",
    "HocVien_Phuong_Ban_Linh_Hay_Vo_Duyen": "Bao_Cao_Phan_Tich_HocVien_Phuong.html"
}

# 1. ISSUE CATEGORY 1: REPORT NOT OPENING
# Ideas where clicking does NOT open a valid report
no_report_list = []
# Ideas where report exists on disk but report_url was empty/missing in database
recoverable_reports = []

# 2. ISSUE CATEGORY 2: SHOTS COUNT ISSUES
zero_shots_list = []
mismatched_shots_list = []

# 3. ISSUE CATEGORY 3: THUMBNAIL ISSUES
thumb_issues_both = []
thumb_issues_key = []

for item in active:
    iid = item['id']
    title = item.get('title_vi') or item.get('title') or ''
    creator = item.get('creator', {}).get('name') or ''
    media = item.get('media', {})
    rep_url = media.get('report_url', '') or ''
    recorded_shots = media.get('shots_count', 0)
    
    # Check disk report
    matched_file = None
    if rep_url:
        bname = os.path.basename(urllib.parse.unquote(rep_url))
        if os.path.exists(os.path.join(reports_dir, bname)):
            matched_file = bname
            
    if not matched_file:
        # Check known mapping
        sc = item.get('shortcode') or ''
        if not sc:
            m = re.search(r'([A-Za-z0-9_-]{11})', iid)
            if m: sc = m.group(1)
        if iid in known_mapping:
            matched_file = known_mapping[iid]
        elif sc in known_mapping:
            matched_file = known_mapping[sc]
        elif sc in mapped_reports:
            matched_file = mapped_reports[sc]
            
    actual_shots_in_disk = count_shots_in_html(matched_file) if matched_file else 0

    # 1. Report click issues
    if not rep_url:
        if matched_file:
            recoverable_reports.append({
                'id': iid,
                'creator': creator,
                'title': title,
                'available_report': matched_file,
                'actual_shots': actual_shots_in_disk,
                'status': 'CÓ BÁO CÁO NHƯNG BỊ BỎ TRỐNG LINK'
            })
        else:
            no_report_list.append({
                'id': iid,
                'creator': creator,
                'title': title,
                'status': 'CHƯA CÓ FILE BÁO CÁO (Chỉ có video/modal video)'
            })
            
    # 2. Shots count issues
    if recorded_shots == 0:
        zero_shots_list.append({
            'id': iid,
            'creator': creator,
            'title': title,
            'recorded_shots': 0,
            'actual_shots': actual_shots_in_disk if actual_shots_in_disk > 0 else "Chưa bóc tách",
            'has_report': bool(matched_file)
        })
    elif actual_shots_in_disk > 0 and recorded_shots != actual_shots_in_disk:
        mismatched_shots_list.append({
            'id': iid,
            'creator': creator,
            'title': title,
            'recorded_shots': recorded_shots,
            'actual_shots': actual_shots_in_disk,
            'report_file': matched_file
        })

    # 3. Thumb issues
    img_stat = img_res.get(iid)
    if img_stat:
        if img_stat['hook_code'] != 200 and img_stat['key_code'] != 200:
            thumb_issues_both.append({
                'id': iid,
                'creator': creator,
                'title': title,
                'hook_code': img_stat['hook_code'],
                'key_code': img_stat['key_code']
            })
        elif img_stat['hook_code'] == 200 and img_stat['key_code'] != 200:
            thumb_issues_key.append({
                'id': iid,
                'creator': creator,
                'title': title,
                'hook_code': img_stat['hook_code'],
                'key_code': img_stat['key_code']
            })

all_issues_summary = {
    'recoverable_reports': recoverable_reports,
    'no_report_list': no_report_list,
    'zero_shots_list': zero_shots_list,
    'mismatched_shots_list': mismatched_shots_list,
    'thumb_issues_both': thumb_issues_both,
    'thumb_issues_key': thumb_issues_key
}

with open('scratch/all_issues_summary.json', 'w', encoding='utf-8') as out:
    json.dump(all_issues_summary, out, ensure_ascii=False, indent=2)

print(f"=== TỔNG KẾT RÀ SOÁT TOÀN DIỆN ===")
print(f"1. Ý tưởng có file báo cáo sẵn nhưng click không ra do thiếu link: {len(recoverable_reports)}")
print(f"2. Ý tưởng hoàn toàn chưa có file báo cáo (chỉ có video): {len(no_report_list)}")
print(f"3. Ý tưởng bị ghi '0 shots' trên giao diện: {len(zero_shots_list)}")
print(f"4. Ý tưởng bị lệch số shot (ghi X shot nhưng báo cáo có Y shot): {len(mismatched_shots_list)}")
print(f"5. Ý tưởng lỗi cả 2 thumbnail: {len(thumb_issues_both)}")
print(f"6. Ý tưởng lỗi 1 thumbnail (Key shot): {len(thumb_issues_key)}")

