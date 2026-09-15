import re

html_file = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@nathanael.lct_DdRg_ybtlKI.html"
with open(html_file, "r") as f:
    html = f.read()

# Replace the specific texts
html = re.sub(r'Diễn biến phân cảnh \d+: Đặt ra con số ngân sách cụ thể.*?bằng cú búng tay\.', "Thể hiện quá trình mua sắm từ lúc mở ví, lướt laptop đến khi diện trang phục ra phố tự tin với dòng chữ 'HOW I SHOP' và 'HOW I STYLE'.", html)
html = html.replace("Điểm sáng thị giác: Bố cục cân đối, ánh sáng tự nhiên và chuyển động mượt mà của chủ thể.", "Điểm sáng: Phân tách rõ 2 giai đoạn tạo sự mạch lạc, sử dụng góc máy POV khi mua sắm tạo sự gần gũi.")
html = html.replace("Lưu ý: Cần kiểm soát nhịp cắt để không làm gián đoạn nhịp thở cảm xúc của người xem.", "Lưu ý: Không có điểm trừ đáng kể.")
html = html.replace("Bán hàng thời trang hiệu quả nhất là bọc trong một thử thách có giới hạn (tiền bạc hoặc thời gian): Vừa tạo tính giải trí, vừa xóa tan rào cản giá đắt trong đầu khách.", "Hãy kể câu chuyện mua sắm thay vì chỉ trưng bày quần áo. Thêm quá trình 'Thêm vào giỏ hàng' giúp định hướng hành vi.")
html = html.replace("Thử Thách Phối Đồ Thu Dưới €150 & Kỹ Thuật Ho...", "Hành Trình Từ Giỏ Hàng...")

with open(html_file, "w") as f:
    f.write(html)
