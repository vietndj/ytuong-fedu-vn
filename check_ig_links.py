import json
import re
import urllib.request
import urllib.error
import time

print("Bắt đầu quét link Instagram...")
with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
    
match = re.search(r'var FEDU_IDEAS_DATABASE = ({.*});', content, re.DOTALL)
if not match:
    exit(1)

db = json.loads(match.group(1))
ideas = db.get("ideas", [])

count_404 = 0
for i, item in enumerate(ideas):
    ig_url = item.get("ig_url")
    if ig_url and ig_url.startswith("http"):
        try:
            req = urllib.request.Request(ig_url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=5)
            # 200 OK
        except urllib.error.HTTPError as e:
            if e.code == 404:
                item["ig_url"] = "" # Ẩn nút follow
                count_404 += 1
        except Exception:
            pass # Lỗi timeout, ssl, ... tạm thời bỏ qua
        time.sleep(0.1) # Tránh bị block

new_db_json = json.dumps(db, ensure_ascii=False, indent=4)
new_content = content[:match.start()] + "var FEDU_IDEAS_DATABASE = " + new_db_json + ";" + content[match.end():]
with open('ideas_data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print(f"Đã kiểm tra xong. Phát hiện và xử lý {count_404} deadlinks 404.")
