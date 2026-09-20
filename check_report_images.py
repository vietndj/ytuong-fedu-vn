import glob
import re

reports = glob.glob('dist/reports/*.html')
broken = []
for report in reports:
    with open(report, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Check for empty src=""
        if re.search(r'<img[^>]*src=["\']\s*["\']', content):
            broken.append(f"{report}: Empty src")
        
        # Check for 404 images from fedu (not doing network request, just check if it's there)
        # Actually earlier the user said "các bài viết không có đủ ảnh" (articles don't have enough images)
        # Wait, some articles have images that 404. Let's find images that have broken relative links.

print(f"Total reports checked: {len(reports)}")
print(f"Broken reports found: {len(broken)}")
if broken:
    for b in broken:
        print(b)
