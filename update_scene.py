import json
import re

scene_file = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/scene.html"
with open(scene_file, "r") as f:
    scene_content = f.read()

# Extract portalData array
match = re.search(r'const portalData = (\[.*?\]);\n', scene_content, re.DOTALL)
if match:
    portal_data_str = match.group(1)
    # We can't just json.loads because it might have JS specifics, but it's usually valid JSON.
    try:
        portalData = json.loads(portal_data_str)
        for item in portalData:
            if item.get("id") == "IG_@nathanael.lct_DdRg_ybtlKI":
                item["title"] = "Nathanael • Kỹ Thuật Kể Chuyện 'How I Shop vs How I Style' Thu Hút Khách Hàng"
                item["logic"] = "Tạo sự đồng cảm bằng cách chia video làm 2 giai đoạn: Giai đoạn 1 (How I Shop) thể hiện hành vi mua sắm online thực tế (ví, laptop, giỏ hàng). Giai đoạn 2 (How I Style) phô diễn thành quả phối đồ tự tin trên phố."
                item["lesson"] = "Đừng chỉ show quần áo, hãy kể câu chuyện quá trình sở hữu nó. Việc thêm phân cảnh 'How I Shop' (thêm vào giỏ hàng) giúp định hướng hành vi mua sắm của người xem một cách tự nhiên."
                item["key_tech"] = ["How I Shop", "How I Style", "Lookbook", "Lifestyle", "Zalando Commercial"]
                break
                
        new_portal_data_str = json.dumps(portalData, indent=4, ensure_ascii=False)
        scene_content = scene_content[:match.start(1)] + new_portal_data_str + scene_content[match.end(1):]
        with open(scene_file, "w") as f:
            f.write(scene_content)
        print("Updated scene.html successfully")
    except Exception as e:
        print("Error parsing portalData:", e)
else:
    print("Could not find portalData")

