import os
import glob
import random

reports_dir = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports'
html_files = sorted(glob.glob(os.path.join(reports_dir, '*.html')))

# Pick 20 files (deterministic but spread out)
sample_files = html_files[10:30] if len(html_files) >= 30 else html_files[:20]

bad_id_1 = "1tgK__fXrXuS4c6KG4C-D2D_EaA98bIr_"
bad_id_2 = "1Q6JimvbKaCtfeHSOWsg4nJL1Mlqlcs8u"

results = []

for filepath in sample_files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_bad_1 = bad_id_1 in content
    has_bad_2 = bad_id_2 in content
    
    # Count valid media.fedu.vn image links
    import re
    valid_links = len(re.findall(r'media\.fedu\.vn/images/[^"]+', content))
    
    status = "✅ FIXED" if not has_bad_1 and not has_bad_2 and valid_links > 0 else "❌ LỖI"
    if valid_links == 0 and not has_bad_1 and not has_bad_2:
        status = "⚠️ NO IMAGES"
        
    results.append(f"| {filename[:40]}... | {has_bad_1 or has_bad_2} | {valid_links} | {status} |")

print("| Tên Báo Cáo (Cắt ngắn) | Còn mã ID ảo? | Số link ảnh media gốc | Trạng thái |")
print("|---|---|---|---|")
for r in results:
    print(r)

