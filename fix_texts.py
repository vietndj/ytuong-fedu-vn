import json

updates = {
    "DdT9CF7tGzn": {
        "opt": "⚡ Biến iPhone thành máy quay điện ảnh: Dùng hook treo lơ lửng máy trong studio để chặn feed ➔ Cắt sang cảnh lộn ngược bóng nước bắt trọn vệt flare anamorphic ngoài trời.",
        "focus": "⚡ Thực chiến: Lắp lens Anamorphic, lật ngược máy sát mặt vũng nước để lấy hiệu ứng bóng gương (reflection), vừa đi vừa quay lùi để chống rung."
    },
    "DdT4EOzveQL": {
        "opt": "⚡ Bán phong cách sống thay vì bán sản phẩm: Khóa góc máy nhìn qua khe cửa dẫn vào cảnh gõ laptop ngay trên thuyền kayak giữa hồ để quảng cáo công nghệ tự nhiên 100%.",
        "focus": "⚡ Thực chiến: Đặt tripod trên bờ lén nhìn qua khe hở (frame-in-frame), để chủ thể tự nhiên dùng sản phẩm giữa bối cảnh hoang dã trái ngược hoàn toàn với văn phòng."
    },
    "DdQwL3Ahci1": {
        "opt": "⚡ Cú máy tracking đi lùi Lookbook 1 shot: Tận dụng chiều sâu tiệm tạp hóa retro làm nền, khóa chặt ánh mắt giao tiếp và cử chỉ vuốt tóc tự nhiên để giữ chân người xem.",
        "focus": "⚡ Thực chiến: Người cầm máy đi lùi giữ khoảng cách không đổi (3 mét), người mẫu vừa tiến lên vừa vuốt tóc/nhìn thẳng ống kính để tạo nhịp điệu tương tác nhịp nhàng."
    },
    "DctRlh0jZlj": {
        "opt": "⚡ Đẳng cấp mổ xẻ Carousel: Tận dụng luồng Carousel Flow liền mạch kết hợp hệ màu Color Grading điện ảnh để dẫn dắt mắt người xem trượt qua từng khung hình.",
        "focus": "⚡ Thực chiến: Chia lưới bố cục chuẩn trên từng mặt slide, sử dụng Storyboard Rhythm để phân bố thông tin chữ và hình ảnh không bị ngắt quãng giữa các thao tác vuốt."
    },
    "DdTeHleIqkg": {
        "opt": "⚡ Cuốn hút từ giây đầu: Dùng cú máy Establishing Hook góc siêu rộng, ép sáng Low-key tạo mảng tối bí ẩn để khóa sự tập trung của người xem.",
        "focus": "⚡ Thực chiến: Liên tục cắt cảnh luân phiên giữa toàn cảnh sáng rực (High-key) và đặc tả chi tiết (Macro Close-Up) trong bóng tối để nhồi nhét sự tương phản thị giác."
    },
    "Dcbn7Bix-X-": {
        "opt": "⚡ Bí quyết neo giữ ánh nhìn: Thiết lập Establishing Hook bằng không gian tối Low-key, đánh đèn ven sáng sâu (Rim Light) để tách lớp chủ thể khỏi phông nền.",
        "focus": "⚡ Thực chiến: Dí sát ống kính (Macro Detail) bắt trọn chất liệu bề mặt, chuyển động quay tay nhẹ nhàng kết hợp ánh sáng đánh chéo để tạo khối 3D sống động."
    },
    "DOd8XMMjxcH": {
        "opt": "⚡ Nhịp điệu Tracking mượt mà: Mở đầu bằng Establishing Hook, ngay sau đó đẩy Medium Tracking Shot di chuyển song song cùng chủ thể dưới ánh sáng Low-key.",
        "focus": "⚡ Thực chiến: Vừa đẩy máy theo bước chân vừa khóa nét chủ thể, lập tức cắt sang đặc tả Close-Up (bàn tay, biểu cảm) để người xem có cảm giác đồng hành thực sự."
    },
    "Dcx7pQpS6zs": {
        "opt": "⚡ Sức mạnh 1 shot: Gây ấn tượng thị giác tuyệt đối chỉ bằng một cú Establishing Hook Shot tĩnh được căn ke bố cục hoàn hảo đến từng centimet.",
        "focus": "⚡ Thực chiến: Cố định góc máy, để khung cảnh trống tĩnh lặng và đợi chủ thể bước vào khung hình (frame-in-frame) tạo khoảnh khắc đắt giá duy nhất."
    },
    "DdSs5rahILb": {
        "opt": "⚡ Tĩnh mà động: Xếp đặt bộ ảnh bằng kỹ thuật Cinematic Lighting kết hợp Composition Mastery để tạo độ sâu 3D như cắt ra từ một bộ phim thực sự.",
        "focus": "⚡ Thực chiến: Xếp luồng ảnh (Visual Rhythm) khéo léo theo thứ tự toàn-trung-cận để người xem trượt ngang Carousel nhưng vẫn thấy được một câu chuyện liền mạch."
    }
}

with open("master_classifications.json", "r") as f:
    master = json.load(f)

count = 0
for k, v in master.items():
    vid_code = None
    for code in updates.keys():
        if code in k:
            vid_code = code
            break
            
    if vid_code:
        if "fedu_optimization" not in v:
            v["fedu_optimization"] = {}
        v["fedu_optimization"]["key_optimization_point"] = updates[vid_code]["opt"]
        v["fedu_optimization"]["practice_focus"] = updates[vid_code]["focus"]
        # Remove quick_takeaway if it has boilerplate so it doesn't leak
        if "quick_takeaway" in v and "Tác phẩm điện ảnh ngắn" in str(v["quick_takeaway"]):
            v["quick_takeaway"] = updates[vid_code]["opt"]
        count += 1

with open("master_classifications.json", "w") as f:
    json.dump(master, f, ensure_ascii=False, indent=2)

print(f"Updated {count} objects in master_classifications.json")
