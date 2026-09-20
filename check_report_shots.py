import json
import re
import os

with open('master_classifications.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

missing_images_reports = []

for k, v in master.items():
    shots_count = v.get('shots_count', 0)
    report_file = f"dist/reports/{k}.html"
    
    if os.path.exists(report_file):
        with open(report_file, 'r', encoding='utf-8') as f2:
            content = f2.read()
            images = re.findall(r'<img[^>]*src=["\']([^"\']+)["\']', content)
            valid_images = [img for img in images if img.strip() != ""]
            
            # The lightbox image is always +1. So if valid_images < shots_count, it's missing!
            # Wait, some reports have other images?
            # Let's just check if valid_images <= shots_count
            
            img_count = len(valid_images)
            if img_count < shots_count:
                missing_images_reports.append(f"{k}: Expected {shots_count} shots, found {img_count} images")

print(f"Total master items: {len(master)}")
print(f"Reports with missing images: {len(missing_images_reports)}")
if missing_images_reports:
    for m in missing_images_reports[:20]:
        print(m)
