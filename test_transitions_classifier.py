import json, re

with open('master_classifications.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

# Load scene.html to get full context
with open('scene.html', 'r', encoding='utf-8') as f:
    c = f.read()
portal_data = json.loads(re.search(r'const portalData\s*=\s*(\[.*?\]);', c, re.DOTALL).group(1))
portal_map = {item['id']: item for item in portal_data}

items = {k: v for k, v in master.items() if (k.startswith('IG_') or k.startswith('FB_') or k.startswith('TikTok_') or k.startswith('SHOPEE_') or k.startswith('LAZADA_') or k.startswith('REMAKE_')) and isinstance(v, dict)}

print(f"Total unique master items: {len(items)}")

# Rules for Level 1 vs Level 2 based on Anh Viet's doctrine:
# Level 1: Handheld / Selfie / Chỗ đông người / cử động đầu gật đầu, lắc đầu, quay đầu x2
# Level 2: Chân máy (tripod) / điện thoại cố định / hành động cơ thể rõ ràng x2 (vung tay, đá chân, dậm chân, bước đi, thay đồ, xoay người, match action)

lvl1_keywords = ['selfie', 'gật đầu', 'lắc đầu', 'quay đầu', 'head turn', 'head nod', 'cầm tay', 'đông người', 'dạo phố', 'lia máy theo hướng đi', 'bước chân', 'dạo phố thời trang', 'whip pan tutorial', 'seamless spin']
lvl2_keywords = ['chân máy', 'tripod', 'match cut', 'match action', 'kick', 'tornado', 'thay đồ', 'outfit', 'vung tay', 'dậm chân', 'nhảy', 'tĩnh', 'cố định', 'bàn làm việc', 'đổi cảnh', 'biến hình', 'jump cut', 'routine', 'workout', 'coffee + outfit']

classified_l1 = []
classified_l2 = []

for vid_id, v in items.items():
    p_item = portal_map.get(vid_id, {})
    title = (v.get('title') or p_item.get('title_vi') or '').lower()
    desc = (v.get('quick_takeaway') or p_item.get('desc_vi') or '').lower()
    techs = ' '.join(v.get('tech_tags') or []).lower() + ' ' + (p_item.get('key_tech') or '').lower()
    logic = (v.get('logic_explanation') or '').lower()
    corpus = f"{vid_id} {title} {desc} {techs} {logic}".lower()
    creator = (v.get('creator') or p_item.get('creator') or '').lower()

    # Determine transition level
    t_level = None
    
    # Explicit Level 1 patterns
    if any(k in corpus for k in ['head turn', 'gật đầu', 'lắc đầu', 'selfie']) or \
       ('whip pan' in corpus and ('cầm tay' in corpus or 'spin' in corpus or 'onethebaha' in corpus)) or \
       ('dạo phố' in corpus and ('bước chân' in corpus or 'chuyển cảnh' in corpus or 'lia máy' in corpus)) or \
       ('downtown' in corpus and 'walk' in corpus and 'transition' in corpus) or \
       ('steven.vuu' in creator and ('wake up' in corpus or 'skit' in corpus or 'chuyển cảnh' in corpus)) or \
       ('by.bennnj' in creator and 'camera' in corpus) or \
       ('hey.lirules' in corpus and 'hội an' in corpus):
        # Level 1: Handheld / Selfie / Crowded place head movements
        t_level = "Chuyển cảnh Level 1"
        classified_l1.append((vid_id, v.get('title')))
    
    # Explicit Level 2 patterns (Tripod / Fixed phone / Body action repeated x2)
    elif ('tornado kick' in corpus or 'aidana' in corpus) or \
         ('jamison.lange' in corpus or 'coffee + outfit' in corpus) or \
         ('byjxson' in corpus or 'đồng hồ bấm giờ' in corpus or 'project 100' in corpus) or \
         ('mridupawasharma' in corpus and '4_cuts' in vid_id) or \
         ('critos_pro' in corpus) or \
         ('jesussropero' in corpus or 'getting ready' in corpus) or \
         ('kristinagoose' in corpus or 'bomb outfit transition' in corpus) or \
         ('bysuncan' in corpus or 'smooth criminal punch transition' in corpus) or \
         ('omgadrian' in corpus or 'travel sequence formula' in corpus) or \
         ('dimasyudhystira' in corpus or 'sumbing' in corpus) or \
         ('samuelaitken_' in corpus or 'fitness' in corpus) or \
         ('brandon.dtd' in corpus) or \
         ('valenti_k41' in corpus and 'phone' in corpus) or \
         (v.get('shooting_style', {}).get('id') == 'chuyen-canh' and t_level is None):
        t_level = "Chuyển cảnh Level 2"
        classified_l2.append((vid_id, v.get('title')))

print(f"\n=== LEVEL 1 ({len(classified_l1)} items) ===")
for x in classified_l1:
    print(f"- {x[0]}: {x[1]}")

print(f"\n=== LEVEL 2 ({len(classified_l2)} items) ===")
for x in classified_l2:
    print(f"- {x[0]}: {x[1]}")
