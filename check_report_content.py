import glob
import re

reports = glob.glob('dist/reports/*.html')
no_images = []
for report in reports:
    with open(report, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Count images that are NOT the lightbox
        images = re.findall(r'<img[^>]*src=["\']([^"\']+)["\']', content)
        valid_images = [img for img in images if img.strip() != ""]
        
        if len(valid_images) == 0:
            no_images.append(report)

print(f"Total reports: {len(reports)}")
print(f"Reports with 0 images: {len(no_images)}")
if no_images:
    for n in no_images[:10]:
        print(n)
