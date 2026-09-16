import json

updates = {
    "DdT9CF7tGzn": {
        "opt": "⚡ Dùng hook treo máy thẳng đứng trong studio chặn feed ➔ Chuyển cảnh lật ngược máy lấy bóng nước kết hợp flare anamorphic ngoài trời.",
        "focus": "⚡ Thực chiến: Lắp lens Anamorphic, lật ngược máy cắm sát vũng nước lấy bóng gương, đi lùi để hãm rung."
    },
    "DdT4EOzveQL": {
        "opt": "⚡ Lồng sản phẩm vào lối sống: Khóa máy qua khe cửa, đẩy góc nhìn ra cảnh ngồi thuyền kayak gõ laptop giữa hồ để bán công nghệ.",
        "focus": "⚡ Thực chiến: Cắm tripod lén nhìn qua khe hở (frame-in-frame), để diễn viên tự nhiên dùng sản phẩm giữa bối cảnh thiên nhiên."
    },
    "DdQwL3Ahci1": {
        "opt": "⚡ Tracking đi lùi 1 shot: Lấy chiều sâu tiệm tạp hóa làm nền, bắt nét thẳng vào mắt và cử chỉ vuốt tóc tự nhiên của mẫu.",
        "focus": "⚡ Thực chiến: Tay máy lùi giữ cự ly 3 mét, mẫu tiến lên vừa vuốt tóc vừa nhìn thẳng ống kính giữ nhịp."
    },
    "DctRlh0jZlj": {
        "opt": "⚡ Đồng bộ Carousel Flow và dải màu Color Grading để khách tự vuốt hết 8 mặt slide mà không bị khựng nhịp.",
        "focus": "⚡ Thực chiến: Đóng lưới bố cục cố định ở mọi slide, nối thông tin và hình ảnh tràn viền bằng Storyboard Rhythm."
    },
    "DdTeHleIqkg": {
        "opt": "⚡ Mở bát bằng Establishing Hook góc siêu rộng, ngay lập tức ép sáng Low-key dìm tối phông nền để dồn mắt vào chủ thể.",
        "focus": "⚡ Thực chiến: Băm nhịp luân phiên giữa toàn cảnh sáng rực (High-key) và dí sát chi tiết (Macro) trong bóng tối tạo độ gắt."
    },
    "Dcbn7Bix-X-": {
        "opt": "⚡ Đặt Establishing Hook trong không gian tối, đập đèn ven (Rim Light) mạnh để tách hẳn chủ thể khỏi nền.",
        "focus": "⚡ Thực chiến: Dí sát ống kính (Macro Detail) bắt vân bề mặt, xoay tay máy chậm kết hợp ánh sáng chéo để nổi khối 3D."
    },
    "DOd8XMMjxcH": {
        "opt": "⚡ Mở đầu Establishing Hook rồi lập tức đẩy Medium Tracking đi ngang song song với người dưới ánh sáng Low-key.",
        "focus": "⚡ Thực chiến: Vừa đẩy máy theo bước chân vừa khóa nét mặt, cắt rụp sang góc cận (tay, biểu cảm) để tạo cảm giác có người đi cùng."
    },
    "Dcx7pQpS6zs": {
        "opt": "⚡ Đóng chết 1 góc Establishing Hook tĩnh, ke bố cục chuẩn xác và để chủ thể tự bước vào vùng bắt nét.",
        "focus": "⚡ Thực chiến: Fix cứng máy, để hở khoảng trống và đợi người đi vào khung (frame-in-frame) tạo điểm nhấn dứt khoát."
    },
    "DdSs5rahILb": {
        "opt": "⚡ Dựng luồng ảnh (Visual Rhythm) bằng Cinematic Lighting và Composition Mastery để tạo chiều sâu như cắt ra từ phim.",
        "focus": "⚡ Thực chiến: Xếp ảnh theo thứ tự toàn-trung-cận để khách vuốt ngang Carousel vẫn đọc được câu chuyện liền mạch."
    }
}

with open("master_classifications.json", "r") as f:
    master = json.load(f)

for k, v in master.items():
    vid_code = None
    for code in updates.keys():
        if code in k:
            vid_code = code
            break
            
    if vid_code:
        v["fedu_optimization"]["key_optimization_point"] = updates[vid_code]["opt"]
        v["fedu_optimization"]["practice_focus"] = updates[vid_code]["focus"]
        if "quick_takeaway" in v and "Tác phẩm điện ảnh ngắn" in str(v["quick_takeaway"]):
            v["quick_takeaway"] = updates[vid_code]["opt"]

with open("master_classifications.json", "w") as f:
    json.dump(master, f, ensure_ascii=False, indent=2)
