import json
import re

# 1. Update master_classifications.json
master_file = 'master_classifications.json'
with open(master_file, 'r', encoding='utf-8') as f:
    master = json.load(f)

vid_id = 'IG_@dev_zero_Db-S8i1hXwF'
if vid_id in master:
    master[vid_id]['title'] = 'Zero Dev • Vlog Kỷ Luật: Tan làm, Đàn Guitar, Code Đêm & Ăn Dưa Hấu'
    master[vid_id]['logic_explanation'] = 'Xây dựng nhịp điệu sinh hoạt qua 5 bối cảnh đời thường. Các góc máy tĩnh tôn vinh sự thư giãn, kết hợp âm thanh mộc (foley) và text time-stamp để định hình dòng thời gian chân thực.'
    master[vid_id]['quick_takeaway'] = 'Không cần lời thoại, việc ghép các hoạt động (chọn giày, đàn, code, đi dạo, ăn) với text thời gian (06:10 pm -> 10:00 pm) đủ tạo storytelling mạnh mẽ.'
    master[vid_id]['fedu_optimization']['key_optimization_point'] = 'Xây dựng nhịp điệu sinh hoạt qua 5 bối cảnh đời thường, kết hợp âm thanh mộc (foley) và text time-stamp để định hình dòng thời gian chân thực.'
    master[vid_id]['fedu_optimization']['practice_focus'] = 'Không cần lời thoại, ghép hoạt động (chọn giày, đàn, code, đi dạo, ăn) với text thời gian (06:10 pm -> 10:00 pm) đủ tạo storytelling.'
    master[vid_id]['industry']['id'] = 'ugc'
    master[vid_id]['industry']['name'] = 'UGC & Đời Sống'
    master[vid_id]['industry']['icon'] = '🤳'

with open(master_file, 'w', encoding='utf-8') as f:
    json.dump(master, f, ensure_ascii=False, indent=2)

print("Updated master_classifications.json")

# 2. Update scene.html
scene_file = 'scene.html'
with open(scene_file, 'r', encoding='utf-8') as f:
    scene_text = f.read()

# Replace title and desc
scene_text = re.sub(
    r'("id":\s*"IG_@dev_zero_Db-S8i1hXwF",[\s\S]*?"title_vi":\s*")[^"]+(")',
    r'\1Zero Dev • Vlog Kỷ Luật: Tan làm, Đàn Guitar, Code Đêm & Ăn Dưa Hấu\2',
    scene_text
)
scene_text = re.sub(
    r'("id":\s*"IG_@dev_zero_Db-S8i1hXwF",[\s\S]*?"desc_vi":\s*")[^"]+(")',
    r'\1Không cần lời thoại, việc ghép các hoạt động với text thời gian đủ tạo nên storytelling mạnh mẽ, thân mật.\2',
    scene_text
)

with open(scene_file, 'w', encoding='utf-8') as f:
    f.write(scene_text)
print("Updated scene.html")

