import json
import re
import os
import subprocess
import time
import urllib.request
import urllib.error

print("=== START BATCH CRAWL & UPLOAD R2 ===")

def check_r2_url(url):
    try:
        req = urllib.request.Request(url, method='HEAD')
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status == 200
    except Exception:
        return False

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = ({.*});', content, re.DOTALL)
if not match:
    exit(1)

db = json.loads(match.group(1))
ideas = db.get("ideas", [])
total = len(ideas)
completed = 0

for item in ideas:
    video_url = item.get("media", {}).get("video_url", "")
    if not video_url:
        video_url = item.get("video_url", "")
        
    if not video_url or "media.fedu.vn/videos" not in video_url:
        continue
        
    filename = video_url.split("/")[-1]
    ig_url = item.get("ig_url", "")
    
    # 1. Curl check R2
    if check_r2_url(video_url):
        completed += 1
        print(f"[{completed}/{total}] {filename} Đã có trên R2. Bỏ qua.")
        continue
        
    print(f"[{completed+1}/{total}] Đang xử lý {filename}...")
    
    if not ig_url or not ig_url.startswith("http"):
        print(f" -> Lỗi: Không có link gốc IG để tải.")
        continue

    # 2. Tải bằng yt-dlp
    temp_file = f"temp_{filename}"
    print(f" -> Tải từ {ig_url}")
    dl_res = subprocess.run(["yt-dlp", ig_url, "-o", temp_file, "--quiet", "--no-warnings"])
    
    if dl_res.returncode != 0 or not os.path.exists(temp_file):
        print(" -> Tải thất bại. (Có thể IG chặn hoặc xóa)")
        # Thử tìm các file trùng tên yt-dlp tạo ra nhưng đuôi .mkv hoặc .webm
        possible_files = [f for f in os.listdir('.') if f.startswith(f"temp_{filename.split('.')[0]}")]
        if possible_files:
            temp_file = possible_files[0]
        else:
            continue
            
    # 3. Upload lên R2
    print(f" -> Upload lên R2 fedu/videos/{filename}")
    up_res = subprocess.run(["wrangler", "r2", "object", "put", f"fedu/videos/{filename}", "--file", temp_file], capture_output=True)
    
    if up_res.returncode == 0:
        print(" -> Upload thành công.")
        completed += 1
    else:
        print(f" -> Lỗi Upload: {up_res.stderr.decode()}")
        
    # Xóa temp
    if os.path.exists(temp_file):
        os.remove(temp_file)
        
    time.sleep(2) # Nghỉ tránh bị limit

print("=== QUÁ TRÌNH HOÀN TẤT ===")
