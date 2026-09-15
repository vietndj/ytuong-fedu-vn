import re

html_path = 'reports/IG_@dev_zero_Db-S8i1hXwF.html'
with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Title
text = re.sub(r'Zero Dev • Routine Sau Giờ Làm: Tự Học Code, Đàn Guitar & Kỷ Luật Bản Thân', 'Zero Dev • Vlog Kỷ Luật: Tan làm, Đàn Guitar, Code Đêm & Ăn Dưa Hấu', text)
text = re.sub(r'Mẫu video thương hiệu cá nhân kỷ luật: Kể chuyện bằng chuỗi thói quen buổi tối không cần lời thoại.', 'Không cần lời thoại, việc ghép các hoạt động với text thời gian đủ tạo nên storytelling mạnh mẽ, thân mật.', text)
text = re.sub(r'Kể chuyện một buổi tối không dùng lời: Từ bàn phím cơ gõ code, chuyển sang ngón tay gảy đàn guitar, rồi xỏ giày chạy bộ. Mỗi hành động đại diện cho 1 mảnh ghép phát triển bản thân.', 'Xây dựng nhịp điệu sinh hoạt qua 5 bối cảnh đời thường. Các góc máy tĩnh tôn vinh sự thư giãn, kết hợp âm thanh mộc (foley) và text time-stamp để định hình dòng thời gian chân thực.', text)
text = re.sub(r'Xây dựng thương hiệu chuyên gia không nhất thiết phải thuyết giảng. Đôi khi chỉ cần quay một chuỗi hành động kỷ luật trong không gian làm việc sạch sẽ là đủ tạo niềm tin.', 'Không cần lời thoại, việc ghép các hoạt động (chọn giày, đàn, code, đi dạo, ăn) với text thời gian (06:10 pm -> 10:00 pm) đủ tạo storytelling mạnh mẽ.', text)

# Shot 1
text = re.sub(r'Cú lia máy hẹp từ bàn phím cơ sang màn hình đen, báo hiệu sự tập trung tuyệt đối.', 'Góc máy ngang tủ giày: Bắt đầu hành trình chuyển đổi trạng thái', text)
text = re.sub(r'Góc máy cận cảnh \(Macro\), ánh sáng màn hình hắt lên bàn phím tạo độ tương phản ngầm.', 'Chọn đôi sneaker, text 06:10 pm (tan làm). Hành động kéo giày ra khỏi tủ tạo động lực đi về.', text)
text = re.sub(r'Âm thanh gõ phím ASMR tạo cảm giác nhập tâm và chuyên nghiệp.', 'Bố cục ngang tĩnh tại, để lộ chi tiết đôi giày Samba, thể hiện gu thẩm mỹ lifestyle sạch sẽ.', text)
text = re.sub(r'Khung hình hơi tối, nếu thêm đèn ven (rim light) xanh dương sẽ có chiều sâu hơn.', 'Ánh sáng hơi bết vùng tối ở tủ giày, chưa làm nổi bật được chủ thể.', text)
text = re.sub(r'Dùng chi tiết nhỏ \(bàn phím, con chuột\) để kể chuyện về một "người thợ" công nghệ.', 'Quay POV hành động sinh hoạt đời thường là cách dễ nhất báo hiệu bắt đầu chuỗi vlog.', text)

# Shot 2
text = re.sub(r'Đổi nhịp: Bàn tay gảy nốt nhạc đầu tiên, phá vỡ sự im lặng của code.', 'Cận cảnh thùng đàn Guitar: Kết nối cảm xúc thính giác', text)
text = re.sub(r'Chuyển cảnh bằng match cut âm thanh \(từ tiếng phím sang tiếng dây đàn\).', 'Đánh đàn acoustic, mốc thời gian 07:20 pm (tập đàn).', text)
text = re.sub(r'Sự đối lập giữa máy móc \(MacBook\) và nghệ thuật mộc mạc \(Guitar\) tạo nên chiều sâu nhân vật.', 'Khung hình ấm áp, ngón tay gảy đàn mộc mạc, âm thanh sống động giúp neo giữ cảm xúc.', text)
text = re.sub(r'Cần có nhịp lơi ra một chút trước khi đàn để khán giả kịp cảm nhận sự tĩnh lặng.', 'Góc máy hơi hẹp, chưa thấy được biểu cảm khuôn mặt.', text)
text = re.sub(r'Muốn chứng minh kỷ luật, hãy quay sự cân bằng. Code là logic, Đàn là cảm xúc.', 'Âm nhạc tự chơi \(instrumental\) tạo sự tin cậy cao hơn hẳn việc lồng BGM có sẵn.', text)

# Shot 3
text = re.sub(r'Màn hình nháy code chạy tự động, phản chiếu trong ánh mắt tĩnh lặng.', 'Pomodoro Timer: Xác lập biểu tượng kỷ luật', text)
text = re.sub(r'Mốc thời gian 10:00 PM chìm trong góc, thông báo sự kiên trì.', 'Thiết lập đồng hồ Pomodoro \(nelna\) và cảnh gõ code ban đêm trước màn hình MacBook.', text)
text = re.sub(r'Nhấn mạnh vào kết quả \(code chạy\) chứ không phải quá trình gian khổ.', 'Quay cận cảnh núm vặn đồng hồ \(xúc giác\) và góc rộng time-lapse. Text Great things take time truyền cảm hứng.', text)
text = re.sub(r'Thiếu một điểm nhấn sáng ở đồng hồ đếm ngược để định lượng thời gian.', 'Không gian màn hình hơi nhiễu do code text quá nhỏ, focus hơi bị nhảy nhẹ.', text)
text = re.sub(r'Sử dụng screen glow \(ánh sáng màn hình\) làm key light là một kỹ thuật quay ban đêm cực mạnh.', 'Lồng ghép công cụ vật lý \(đồng hồ\) thay vì app trên màn hình tạo cảm giác nghiêm túc và chân thực.', text)

# Shot 4
text = re.sub(r'Cận cảnh xỏ dây giày chạy bộ phản quang.', 'Cảnh đánh máy với đồng hồ Pomodoro (Wide)', text)
text = re.sub(r'Hành động quyết liệt, bẻ góc máy thấp \(low angle\) tăng tính động học.', 'Time-lapse quá trình ngồi làm việc với đồng hồ đếm ngược kế bên.', text)
text = re.sub(r'Thể hiện rõ ràng triết lý: "Trí óc minh mẫn trong một cơ thể cường tráng".', 'Sự xuất hiện của đồng hồ Pomodoro tạo điểm tựa thị giác cho time-lapse trôi qua nhanh.', text)
text = re.sub(r'Chuyển cảnh từ ghế ngồi xuống sàn hơi gắt, cần chèn 1 frame bước chân trung gian.', 'Góc máy ngang tầm mắt, nhưng thiếu ánh sáng ven cho chủ thể.', text)
text = re.sub(r'Cuối chuỗi thói quen tĩnh phải là một hành động động \(kinetic\) để đẩy năng lượng lên đỉnh.', 'Góc máy tĩnh rất phù hợp cho time-lapse, nhấn mạnh sự tập trung thời gian dài.', text)

# Shot 5
text = re.sub(r'Bước chân chạy trên mặt đường ướt sương đêm.', 'POV đổ bóng đi bộ: Nhịp thở giữa các phiên làm việc', text)
text = re.sub(r'Slow-motion 60fps giảm tốc độ, nhịp điệu thở đều đặn.', 'Bước đi ngoài đường, bóng đổ dài trên mặt đường nhựa, mốc 09:30 pm.', text)
text = re.sub(r'Tạo cảm giác "Afterglow" - sự thỏa mãn sau khi hoàn thành mục tiêu kỷ luật.', 'Đổi không khí ngột ngạt trong nhà ra ngoài trời. Bước chân tạo nhịp điệu \(rhythm\).', text)
text = re.sub(r'Nên có ánh đèn đường vàng hắt ngược để phân tách bóng đêm.', 'Hơi rung lắc khi cầm tay quay POV.', text)
text = re.sub(r'Đừng bao giờ quay mặt bạn khi đang thở dốc, hãy quay đôi chân đang tiến về phía trước.', 'Đừng dán mắt 100% vào màn hình, một shot đi dạo outdoor làm cân bằng lại năng lượng toàn bộ vlog.', text)

# Shot 6
text = re.sub(r'Gấp laptop lại, tiếng click dứt khoát kết thúc ngày.', 'Thưởng thức dưa hấu đêm: Tương tác qua caption dài', text)
text = re.sub(r'Màn hình phụ tắt lịm, chỉ còn đèn bàn vàng dịu.', 'Ăn dưa hấu găm dĩa \(10:00 pm\), kèm theo bảng text tiếng Hàn giải thích cách nhận biết dưa hấu hỏng.', text)
text = re.sub(r'Đây là "Call To Action" ngầm: Hãy đứng dậy và làm việc như tôi.', 'Chi tiết bất ngờ, màu đỏ tươi của dưa hấu tương phản mạnh, kích thích thị giác vị giác. Khối text dài giữ chân người xem vì họ phải pause để đọc.', text)
text = re.sub(r'Chưa lưu lại được hình ảnh tổng quan toàn bộ không gian setup.', 'Font chữ text khối khá bé, hơi chìm trên nền dưa hấu mọng nước.', text)
text = re.sub(r'Kết thúc bằng sự kết thúc vật lý \(đóng nắp máy, tắt đèn\) tạo điểm dừng tâm lý hoàn hảo.', 'Dùng một kiến thức vặt đời thường \(mẹo chọn dưa\) chèn vào cuối vlog để giữ chân người xem lâu hơn \(tăng Watch Time\).', text)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(text)

