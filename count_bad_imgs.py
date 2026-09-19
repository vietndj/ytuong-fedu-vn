import os
import glob
import re

report_dirs = [
    "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports",
    "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/dist/reports"
]

ignore_ids = ['lightboxImg', 'lightboxLargeImg', 'lightboxImage', 'lightbox-img', 'lbImg', 'modalImg', 'lb-img', 'modal-img']
ignore_classes = ['lightbox-img', 'modal-img', 'lightbox-content', 'img-lightbox-large']

def should_ignore(img_tag_string):
    for idx in ignore_ids:
        if f'id="{idx}"' in img_tag_string or f"id='{idx}'" in img_tag_string:
            return True
    for cls in ignore_classes:
        if cls in img_tag_string:
            return True
    return False

total_bad_imgs = 0
files_with_bad_imgs = []

for report_dir in report_dirs:
    html_files = glob.glob(os.path.join(report_dir, "*.html"))
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all img tags with src="" or src="null" or src="undefined" or empty src
        # Regex to find <img ...>
        imgs = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
        bad_imgs_in_file = 0
        for img in imgs:
            # Check if src is empty or null
            if re.search(r'src=["\'](null|undefined)?["\']', img, re.IGNORECASE) or not re.search(r'src=', img, re.IGNORECASE):
                if not should_ignore(img):
                    bad_imgs_in_file += 1
                    # print(f"Found in {os.path.basename(file)}: {img}")
        
        if bad_imgs_in_file > 0:
            files_with_bad_imgs.append((file, bad_imgs_in_file))
            total_bad_imgs += bad_imgs_in_file

print(f"Total bad images found: {total_bad_imgs}")
for file, count in files_with_bad_imgs:
    print(f"{os.path.basename(file)}: {count} bad images")
