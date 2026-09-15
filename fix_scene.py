import re
import os

path = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/scene.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace title
content = re.sub(r'"title_vi":\s*"@Caleb Natale Dcbn7Bix-X- Video by calebnatale"', '"title_vi": "Kỹ thuật Match Cut & VFX Dịch chuyển không gian (Caleb Natale)"', content)
content = re.sub(r'"title_vi":\s*"@Caleb_Natale - Video by calebnatale"', '"title_vi": "Kỹ thuật Match Cut & VFX Dịch chuyển không gian (Caleb Natale)"', content)

# Replace desc
content = re.sub(r'"desc_vi":\s*"Báo cáo phân tích chuyên sâu ngôn ngữ điện ảnh[^"]+"', '"desc_vi": "Phân tích cú Match Cut không gian ấn tượng, chuyển tiếp mượt mà từ phòng khách lên máy bay Turkish Airlines."', content)

# Replace key_tech
content = re.sub(r'"key_tech":\s*"Establishing Hook Shot • Close-Up / Macro Detail Shot • Low-key Lighting"', '"key_tech": "Match Cut • VFX Transition • In-Camera Effects • Wipe Transition"', content)


with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated scene.html")
