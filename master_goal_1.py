import json
import re
import os

print("=== BẮT ĐẦU CHẠY GOAL ===")

# Đọc ideas_data.js
with open('ideas_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
    
match = re.search(r'var FEDU_IDEAS_DATABASE = ({.*});', content, re.DOTALL)
if match:
    db = json.loads(match.group(1))
    ideas = db.get("ideas", [])
    
    # 4. SỬA ẢNH
    print("-> SỬA ẢNH: Đang dọn dẹp ảnh placeholder...")
    for item in ideas:
        if item.get("thumbnail") and "placehold.co" in item["thumbnail"]:
            item["thumbnail"] = ""
        if item.get("cover_image") and "placehold.co" in item["cover_image"]:
            item["cover_image"] = ""
            
    # Lưu lại
    new_db_json = json.dumps(db, ensure_ascii=False, indent=4)
    new_content = content[:match.start()] + "var FEDU_IDEAS_DATABASE = " + new_db_json + ";" + content[match.end():]
    with open('ideas_data.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("-> Đã xóa sạch ảnh placeholder rác.")

# 3. SỬA NÚT TẢI VIDEO & FORCE DOWNLOAD
print("-> SỬA NÚT TẢI: Kiểm tra forceDownloadVideo...")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

blob_script = """
        async function forceDownloadVideo(url, filename) {
            try {
                showToast("Đang tải xuống video, vui lòng đợi...");
                const response = await fetch(url, { mode: 'cors' });
                if (!response.ok) throw new Error('Network response was not ok');
                const blob = await response.blob();
                const blobUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = blobUrl;
                a.download = filename || 'fedu_video.mp4';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(blobUrl);
                document.body.removeChild(a);
                showToast("Tải xuống thành công!");
            } catch (err) {
                console.error(err);
                showToast("Lỗi khi tải video. Vui lòng thử lại.");
            }
        }
"""
if "forceDownloadVideo" not in html:
    html = html.replace('</head>', blob_script + '\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("-> Đã cập nhật hàm tải Blob.")
