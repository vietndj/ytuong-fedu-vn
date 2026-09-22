import re
import json
import os
import urllib.parse
import urllib.request
import ssl

ctx = ssl._create_unverified_context()

# 1. READ SCENE.HTML
with open('scene.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

m = re.search(r'const portalData\s*=\s*(\[[\s\S]*?\]);', html_content)
if not m:
    print("Cannot find portalData in scene.html")
    exit(1)

portal_data = json.loads(m.group(1))

# 2. READ R2 FOLDERS
with open('scratch/r2_image_folders.txt', 'r', encoding='utf-8') as f:
    r2_folders = [line.strip().replace('/', '') for line in f if line.strip()]

def find_best_r2_folder(shortcode, creator, title):
    # Try exact match in r2_folders
    # Common format: IG_@creator_shortcode
    for f in r2_folders:
        if shortcode in f:
            return f
    return None

def count_actual_shots_in_html(report_path):
    if not os.path.exists(report_path):
        return 0
    try:
        with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        shot_nums = set()
        for mm in re.finditer(r'(?:SHOT|Shot|Phân cảnh|PHÂN CẢNH)\s+(\d+)', html):
            shot_nums.add(int(mm.group(1)))
        card_matches = re.findall(r'class="[^"]*(?:shot-card|shot-item|storyboard-card)[^"]*"', html)
        slide_nums = set()
        for mm in re.finditer(r'(?:SLIDE|Slide|Slide-video)\s+(\d+)', html):
            slide_nums.add(int(mm.group(1)))
            
        count = 0
        if shot_nums:
            count = max(shot_nums)
        elif slide_nums:
            count = max(slide_nums)
        elif card_matches:
            count = len(card_matches)
        return count
    except:
        return 0

def get_report_path(rep_url):
    if not rep_url:
        return None
    clean_rep = urllib.parse.unquote(rep_url)
    cand1 = clean_rep
    cand2 = os.path.join('reports', os.path.basename(clean_rep))
    for cand in [cand1, cand2]:
        if os.path.exists(cand):
            return cand
    return None

def extract_shortcode(item):
    code = item.get("id", "")
    code = re.sub(r'^(IG|FB|TIKTOK|YOUTUBE|LAZADA|SHOPEE|TUMI)_', '', code)
    if code.startswith('@'):
        parts = code.split('_')
        if len(parts) >= 2:
            return parts[1]
    return code

# Group items by shortcode
grouped = {}
for item in portal_data:
    sc = extract_shortcode(item)
    if sc not in grouped:
        grouped[sc] = []
    grouped[sc].append(item)

# Merge logic
fixed_data = []

for sc, items in grouped.items():
    # Pick base item: prefer one with longest title or most complete data
    best_item = items[0]
    best_score = -1
    
    merged_shots = 0
    merged_report = ""
    
    for it in items:
        score = len(it.get('title_vi', '')) + len(it.get('desc_vi', ''))
        rep = it.get('main_html_rel') or it.get('root_html_rel') or ""
        if rep:
            score += 100
        if score > best_score:
            best_score = score
            best_item = it
            
        # Accumulate best shots and report
        rep_url = it.get('media', {}).get('report_url', '') or it.get('main_html_rel') or it.get('root_html_rel') or ""
        if rep_url and get_report_path(rep_url):
            merged_report = rep_url
        
        s_cnt = it.get('media', {}).get('shots_count', 0)
        if s_cnt > merged_shots:
            merged_shots = s_cnt
            
    # Also verify actual shots from HTML report
    if merged_report:
        rp = get_report_path(merged_report)
        actual = count_actual_shots_in_html(rp)
        if actual > merged_shots:
            merged_shots = actual
            
    # Update best item
    if 'media' not in best_item:
        best_item['media'] = {}
        
    best_item['media']['shots_count'] = merged_shots
    if merged_report:
        best_item['media']['report_url'] = merged_report
        best_item['main_html_rel'] = merged_report

    # FIX IMAGES
    h_url = best_item['media'].get('thumb_hook', '')
    k_url = best_item['media'].get('thumb_key', '')
    
    # Standardize image URLs
    creator_name = best_item.get('creator', '') if isinstance(best_item.get('creator'), str) else best_item.get('creator', {}).get('name', '')
    r2_folder = find_best_r2_folder(sc, creator_name, best_item.get('title_vi', ''))
    
    if r2_folder:
        base_url = f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{urllib.parse.quote(r2_folder)}"
        
        # Check if existing URL uses carousel_slides or extracted_shots
        if 'carousel_slides' in h_url or 'extracted_shots' in h_url:
            pass # Keep it, but change to webp
        else:
            # Reconstruct
            best_item['media']['thumb_hook'] = f"{base_url}/shot_01_mid.webp"
            best_item['media']['thumb_key'] = f"{base_url}/shot_03_mid.webp"
    else:
        # Just replace .jpg with .webp
        if h_url: best_item['media']['thumb_hook'] = h_url.replace('.jpg', '.webp')
        if k_url: best_item['media']['thumb_key'] = k_url.replace('.jpg', '.webp')
        
    fixed_data.append(best_item)

# 3. WRITE BACK TO SCENE.HTML
new_portal_data_str = json.dumps(fixed_data, indent=2, ensure_ascii=False)
# We need to preserve the wrapping array correctly
new_html = html_content[:m.start(1)] + new_portal_data_str + html_content[m.end(1):]

with open('scene.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Fixed {len(fixed_data)} items and saved to scene.html")

