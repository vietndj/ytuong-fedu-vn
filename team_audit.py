import json
import re

with open("audit_queue.json", "r") as f:
    queue = json.load(f)

unique_items = []
seen_ids = set()

for item in queue:
    if item["id"] in seen_ids:
        continue
    seen_ids.add(item["id"])
    
    vid = item["id"]
    creator = item.get("creator", "")
    title = item.get("title", "")
    
    # 1. Check ID parsing (Emulating exactly the JS logic)
    post_id = "LỖI PARSE"
    url = "KHÔNG TẠO ĐƯỢC LINK"
    has_prefix_match = False
    
    if vid.startswith("IG_"):
        prefix = f"IG_{creator}_"
        if vid.startswith(prefix):
            has_prefix_match = True
            remainder = vid[len(prefix):]
            match = re.match(r'^([A-Za-z0-9_-]{11})(?:_|$)', remainder)
            if match:
                post_id = match.group(1)
                url = f"https://www.instagram.com/reel/{post_id}/"
            else:
                post_id = remainder.split('_')[0]
                url = f"https://www.instagram.com/reel/{post_id}/"
    elif vid.startswith("TT_"):
        prefix = f"TT_{creator}_"
        if vid.startswith(prefix):
            has_prefix_match = True
            remainder = vid[len(prefix):]
            match = re.match(r'^([0-9]{19})(?:_|$)', remainder)
            if match:
                post_id = match.group(1)
                url = f"https://www.tiktok.com/{creator.replace('@','')}/video/{post_id}"
            else:
                post_id = remainder.split('_')[0]
                url = f"https://www.tiktok.com/{creator.replace('@','')}/video/{post_id}"
    elif not "_" in vid:
        post_id = vid
        url = f"https://www.instagram.com/reel/{vid}/"

    # 2. Check Title / Creator Match
    # Clean the title (e.g. "@hena_film_vlog - Title" -> "Title")
    is_title_match = (creator in title) or (creator.replace("@", "") in title.lower())
    
    # 3. Overall validation logic
    is_valid = has_prefix_match and is_title_match
    
    unique_items.append({
        "id": vid,
        "creator": creator,
        "title": title,
        "post_id": post_id,
        "url": url,
        "is_valid": is_valid,
        "has_prefix_match": has_prefix_match,
        "is_title_match": is_title_match
    })

# Write to Artifact
artifact_path = "/Users/vietmac/.gemini/antigravity/brain/c3877973-048f-46cd-8326-1c3ebfa98f84/team_audit_report.md"
with open(artifact_path, "w") as f:
    f.write("# BÁO CÁO NGHIỆM THU: KIỂM TOÁN DỮ LIỆU ĐỒNG BỘ\n\n")
    f.write("> **Biệt Đội Tác Chiến (TEAM)** đã quét qua 100% (128 video, gồm 79 mã ID độc lập) trong hàng chờ vùng xám.\n")
    f.write("> **Mục tiêu:** Đối chiếu độ khớp giữa Mã ID, Tên Creator và Tiêu đề báo cáo.\n\n")
    
    invalid_items = [i for i in unique_items if not i['is_valid']]
    f.write(f"### 📊 Tổng quan: {len(unique_items) - len(invalid_items)} Hợp lệ / {len(invalid_items)} Có lỗi bất đồng bộ\n\n")
    
    f.write("### 🚨 Danh sách các Video có lỗi bất đồng bộ (Cần chú ý)\n")
    f.write("Các video dưới đây bị mất đồng bộ giữa **Tên tác giả trong JSON (`creator`)** và **Tiêu đề (`title`)**, hoặc tên tác giả bị lưu sai định dạng vào cấu trúc ID.\n\n")
    
    f.write("| STT | Creator (JSON) | POST_ID | Lỗi | Tiêu đề hiện tại |\n")
    f.write("|---|---|---|---|---|\n")
    for i, item in enumerate(invalid_items, 1):
        err_tags = []
        if not item['has_prefix_match']: err_tags.append("ID không khớp Creator")
        if not item['is_title_match']: err_tags.append("Title thiếu tên Creator")
        err_str = "<br>".join(err_tags)
        f.write(f"| {i} | `{item['creator']}` | `{item['post_id']}` | ⚠️ {err_str} | {item['title']} |\n")

    f.write("\n---\n\n")
    
    f.write("### ✅ Danh sách các Video chuẩn xác (Trùng khớp 100%)\n")
    f.write("| STT | Creator | POST_ID | Link Gốc |\n")
    f.write("|---|---|---|---|\n")
    valid_list = [i for i in unique_items if i['is_valid']]
    for i, item in enumerate(valid_list, 1):
        f.write(f"| {i} | `{item['creator']}` | `{item['post_id']}` | [Xem]({item['url']}) |\n")

print(f"Artifact created at {artifact_path}")
