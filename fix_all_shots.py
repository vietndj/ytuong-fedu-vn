import re

html_path = 'reports/IG_@dev_zero_Db-S8i1hXwF.html'
with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

shots_data = [
    {
        "title": "Góc máy ngang tủ giày: Bắt đầu hành trình chuyển đổi trạng thái",
        "desc": "Chọn đôi sneaker, text '06:10 pm 퇴근' (tan làm). Hành động kéo giày ra khỏi tủ tạo động lực đi về.",
        "pro": "Bố cục ngang tĩnh tại, để lộ chi tiết đôi giày Samba kinh điển, thể hiện gu thẩm mỹ lifestyle sạch sẽ.",
        "con": "Ánh sáng hơi bết vùng tối ở tủ giày, chưa làm nổi bật được chủ thể.",
        "lesson": "Quay POV hành động sinh hoạt đời thường là cách dễ nhất báo hiệu bắt đầu chuỗi vlog."
    },
    {
        "title": "Cận cảnh thùng đàn Guitar: Kết nối cảm xúc thính giác",
        "desc": "Đánh đàn acoustic, mốc thời gian '07:20 pm 기타 연습' (tập đàn).",
        "pro": "Khung hình ấm áp, ngón tay gảy đàn mộc mạc, âm thanh sống động (Foley) giúp neo giữ cảm xúc.",
        "con": "Góc máy hơi hẹp, chưa thấy được biểu cảm khuôn mặt.",
        "lesson": "Âm nhạc tự chơi (instrumental) tạo sự tin cậy cao hơn hẳn việc lồng BGM có sẵn."
    },
    {
        "title": "Pomodoro Timer & Thiết lập bàn làm việc",
        "desc": "Thiết lập đồng hồ Pomodoro (nelna) và chuẩn bị làm việc.",
        "pro": "Quay cận cảnh núm vặn đồng hồ (xúc giác). Text 'Great things take time' truyền cảm hứng tinh tế.",
        "con": "Không gian hơi hẹp, chưa lột tả được hết sự tập trung.",
        "lesson": "Lồng ghép công cụ vật lý (đồng hồ) thay vì app trên màn hình tạo cảm giác nghiêm túc và chân thực hơn."
    },
    {
        "title": "Cảnh gõ code ban đêm trước màn hình MacBook",
        "desc": "Time-lapse quá trình gõ code tập trung.",
        "pro": "Góc máy time-lapse ổn định, kết hợp đồng hồ Pomodoro tạo điểm tựa thị giác thời gian trôi.",
        "con": "Không gian màn hình hơi nhiễu do code text quá nhỏ, focus hơi nhảy nhẹ.",
        "lesson": "Góc máy tĩnh rất phù hợp cho time-lapse, nhấn mạnh sự kiên trì trong thời gian dài."
    },
    {
        "title": "POV đổ bóng đi bộ: Nhịp thở giữa các phiên làm việc",
        "desc": "Bước đi ngoài đường, bóng đổ dài trên mặt đường nhựa, mốc '09:30 pm'.",
        "pro": "Đổi không khí ngột ngạt trong nhà ra ngoài trời. Bước chân tạo nhịp điệu (rhythm).",
        "con": "Hơi rung lắc (shaky) khi cầm tay quay POV.",
        "lesson": "Đừng dán mắt 100% vào màn hình, một shot đi dạo outdoor làm cân bằng lại năng lượng toàn bộ vlog."
    },
    {
        "title": "Thưởng thức dưa hấu đêm: Tương tác qua caption dài",
        "desc": "Ăn dưa hấu găm dĩa (10:00 pm), kèm bảng text tiếng Hàn giải thích cách nhận biết dưa hấu hỏng.",
        "pro": "Chi tiết bất ngờ, màu đỏ tươi của dưa hấu tương phản mạnh, kích thích thị giác. Khối text dài giữ chân người xem phải pause đọc.",
        "con": "Font chữ text khối khá bé, hơi chìm trên nền dưa hấu mọng nước.",
        "lesson": "Dùng một kiến thức vặt đời thường (mẹo chọn dưa) chèn vào cuối vlog để giữ chân người xem lâu hơn (tăng Watch Time)."
    }
]

# We need to replace the content of each shot block.
# Let's split by '<article class="shot-card"'
parts = text.split('<article class="shot-card"')
for i in range(1, 7): # shots 1 to 6
    if i <= len(parts) - 1:
        shot_text = parts[i]
        
        # Replace headline
        shot_text = re.sub(r'<h2 class="shot-headline">.*?</h2>', f'<h2 class="shot-headline">Phân Cảnh 0{i} • {shots_data[i-1]["title"]}</h2>', shot_text)
        
        # Replace desc
        shot_text = re.sub(r'<div class="block-text">.*?</div>', f'<div class="block-text">{shots_data[i-1]["desc"]}</div>', shot_text)
        
        # Replace pro
        shot_text = re.sub(r'<div class="side-content">Điểm sáng thị giác.*?</div>', f'<div class="side-content">{shots_data[i-1]["pro"]}</div>', shot_text)
        
        # Replace con
        shot_text = re.sub(r'<div class="side-content">Lưu ý: Kiểm soát nhịp thở.*?</div>', f'<div class="side-content">{shots_data[i-1]["con"]}</div>', shot_text)
        
        # Replace lesson
        shot_text = re.sub(r'<div class="takeaway-body">.*?</div>', f'<div class="takeaway-body">{shots_data[i-1]["lesson"]}</div>', shot_text)
        
        parts[i] = shot_text

new_text = '<article class="shot-card"'.join(parts)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated shots in HTML.")
