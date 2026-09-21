import re
import json

with open('ideas_data.js', 'r', encoding='utf-8') as f:
    data = f.read()

match = re.search(r'var FEDU_IDEAS_DATABASE = ({.*});', data, re.DOTALL)
if match:
    db = json.loads(match.group(1))
    ideas = db.get("ideas", [])
    
    # 4 video có ở local
    local_videos = [
        "LAZADA_Ulanzi_Đèn_LED_Thanh_Bơm_Hơi_UA20,_.mp4",
        "4 Cu May Sieu Thi Bang Gia Do Ulanzi MA38 MT85 - @hena_film_vlog.mp4",
        "Teaching_Nervous_System_Not_Emergency_-_@kawoon.lee.mp4",
        "LAZADA_Ulanzi_Chân_Đế_Tự_Sướng_Có_Từ_Tính_.mp4"
    ]
    
    markdown_content = "# Báo Cáo 289 Video Đang Khuyết (Chưa Upload Lên R2)\n\n"
    markdown_content += "Anh có thể dùng danh sách này để tìm kiếm trong ổ cứng hoặc sử dụng tool download hàng loạt.\n\n"
    markdown_content += "| STT | Kênh (Creator) | Tiêu Đề Idea | Tên File MP4 Cần Có | Link Bài Gốc (IG) |\n"
    markdown_content += "|---|---|---|---|---|\n"
    
    count = 1
    for item in ideas:
        vid_url = item.get("media", {}).get("video_url", "")
        if not vid_url:
            vid_url = item.get("video_url", "")
            
        if not vid_url:
            continue
            
        file_name = vid_url.split("/")[-1]
        
        # Bỏ qua 4 video đã có local
        if file_name in local_videos:
            continue
            
        creator = item.get("creator", {}).get("handle", "Unknown")
        title = item.get("title_vi", "").replace("|", "-").replace("\n", " ")
        ig_url = item.get("ig_url", "")
        
        markdown_content += f"| {count} | `{creator}` | {title} | `{file_name}` | [Xem Nguồn]({ig_url}) |\n"
        count += 1

    # Lưu thành artifact
    with open('/Users/vietmac/.gemini/antigravity/brain/1266ad06-6736-4892-8a28-40e29db6d0a8/missing_videos_report.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
    print(f"Đã tạo bảng với {count - 1} video khuyết.")
else:
    print("Lỗi parse JSON")
