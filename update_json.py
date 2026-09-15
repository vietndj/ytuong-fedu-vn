import json

paths = [
    '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/master_classifications.json',
    '/Users/vietmac/Documents/CODE/vietndj.github.io/master_classifications.json'
]

for path in paths:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if "IG_@layton_video_DdKGq2TMhf4" in data:
        obj = data["IG_@layton_video_DdKGq2TMhf4"]
        obj["title"] = "Layton • Sự Thật Khắc Nghiệt Khi Làm Creator: Cứ Làm Đi Thay Vì Dạy Đời"
        obj["shots_count"] = 6
        obj["duration"] = "15.0s"
        obj["purpose"] = "Kịch bản cảnh tỉnh cho các nhà sáng tạo nội dung mới: Không cần cố gắng hoàn hảo hay dạy người khác cách làm, chỉ cần bắt tay vào thực hiện trong một khoảng thời gian nhất định."
        obj["logic_explanation"] = "Hook trực diện 'Sự thật khắc nghiệt khi làm creator'. Sự luân phiên giữa cảnh ngồi nói chuyện tại bàn (talking head) và cảnh B-roll (outside/tripod) tạo nhịp điệu. Nhấn mạnh việc thực hành thay vì chỉ lên kế hoạch."
        obj["quick_takeaway"] = "Không cần cố gắng đóng vai chuyên gia ngay từ đầu. Hãy cứ làm, sai và sửa trong một khoảng thời gian đủ dài, ý tưởng sẽ tự động xuất hiện."
        obj["fedu_optimization"]["key_optimization_point"] = "⚡ Không cần cố gắng đóng vai chuyên gia ngay từ đầu. Hãy cứ làm, sai và sửa trong một khoảng thời gian đủ dài, ý tưởng sẽ tự động xuất hiện."
        obj["fedu_optimization"]["practice_focus"] = "Thực hành: Hook trực diện 'Sự thật khắc nghiệt khi làm creator'. Sự luân phiên giữa cảnh ngồi nói chuyện tại bàn và cảnh B-roll tạo nhịp điệu."
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
