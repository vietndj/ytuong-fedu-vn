import json
import re
import os
import subprocess
import time

print("=== START DEEP VERIFICATION (INSTAGRAM LINKS) ===")

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = ({.*});', content, re.DOTALL)
if not match:
    print("Cannot parse DB")
    exit(1)

db = json.loads(match.group(1))
ideas = db.get("ideas", [])

total = len(ideas)
dead_links_count = 0

for i, item in enumerate(ideas):
    ig_url = item.get("ig_url", "")
    
    # Bỏ qua nếu đã bị excluded hoặc không có link
    if item.get("is_excluded") or not ig_url or not ig_url.startswith("http"):
        continue
        
    print(f"[{i+1}/{total}] Checking: {ig_url}")
    
    # Dùng yt-dlp để extract info (không tải video, chỉ lấy info metadata).
    # Nếu bài viết bị xoá hoặc ẩn riêng tư, yt-dlp sẽ không lấy được video info.
    result = subprocess.run(["yt-dlp", "--dump-json", "--no-warnings", ig_url], capture_output=True, text=True)
    
    if result.returncode != 0 or not result.stdout.strip():
        print(f" -> LỖI: Trang không khả dụng hoặc bị ẩn. Đánh dấu EXCLUDED.")
        item["is_excluded"] = True
        dead_links_count += 1
    else:
        # Check xem có dữ liệu JSON được parse không
        try:
            meta = json.loads(result.stdout.strip().split('\n')[0])
            if "id" in meta:
                print(" -> OK: Link còn sống (Có dữ liệu).")
            else:
                item["is_excluded"] = True
                dead_links_count += 1
                print(" -> LỖI: Không tìm thấy ID video trong metadata.")
        except:
            item["is_excluded"] = True
            dead_links_count += 1
            print(" -> LỖI: Phản hồi không phải JSON hợp lệ.")

    # Ghi DB sau mỗi lần check để không mất dữ liệu nếu bị ngắt
    if dead_links_count > 0:
        new_db_json = json.dumps(db, ensure_ascii=False, indent=4)
        new_content = content[:match.start()] + "var FEDU_IDEAS_DATABASE = " + new_db_json + ";" + content[match.end():]
        with open('ideas_data.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    time.sleep(1) # Tránh Rate Limit của Insta

print(f"=== KẾT THÚC. Đã ẩn {dead_links_count} bài viết hỏng. ===")
