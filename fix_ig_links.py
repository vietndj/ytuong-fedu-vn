import re
import json

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Hàm chuẩn hoá URL Instagram
def clean_ig_url(url):
    if not url: return url
    # Nếu có dạng instagram.com/abc/p/xyz/ -> instagram.com/p/xyz/
    # (Loại bỏ username thừa ở giữa)
    url = re.sub(r'instagram\.com/[^/]+/p/([^/]+)', r'instagram.com/p/\1', url)
    url = re.sub(r'instagram\.com/[^/]+/reel/([^/]+)', r'instagram.com/reel/\1', url)
    # Loại bỏ phần tracking ?igsh=...
    url = url.split('?')[0]
    # Thêm dấu / ở cuối nếu chưa có (ngoại trừ facebook)
    if 'instagram.com' in url and not url.endswith('/'):
        url += '/'
    return url

# Đọc db
match = re.search(r'var FEDU_IDEAS_DATABASE = ({.*});', content, re.DOTALL)
if match:
    db = json.loads(match.group(1))
    fixes = 0
    for item in db.get("ideas", []):
        old_url = item.get("ig_url", "")
        if old_url:
            new_url = clean_ig_url(old_url)
            if new_url != old_url:
                item["ig_url"] = new_url
                fixes += 1

    # Lưu lại
    new_db_json = json.dumps(db, ensure_ascii=False, indent=4)
    new_content = content[:match.start()] + "var FEDU_IDEAS_DATABASE = " + new_db_json + ";" + content[match.end():]
    
    with open('ideas_data.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Đã chuẩn hóa {fixes} đường dẫn Instagram bị lỗi cú pháp.")
else:
    print("Không thể parse DB")
