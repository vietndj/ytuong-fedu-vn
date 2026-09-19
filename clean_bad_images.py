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

def is_bad_image(img_tag_string):
    if should_ignore(img_tag_string):
        return False
    # Check if src is empty, null, undefined, or missing
    has_valid_src = False
    match = re.search(r'src=["\']([^"\']*)["\']', img_tag_string, re.IGNORECASE)
    if match:
        src_val = match.group(1).strip()
        if src_val and src_val not in ["null", "undefined"]:
            has_valid_src = True
    
    return not has_valid_src

total_fixed = 0

for report_dir in report_dirs:
    html_files = glob.glob(os.path.join(report_dir, "*.html"))
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        def replacer(match):
            img_tag = match.group(0)
            if is_bad_image(img_tag):
                print(f"Removing from {os.path.basename(file)}: {img_tag}")
                global total_fixed
                total_fixed += 1
                return "" # Remove the tag
            return img_tag

        new_content = re.sub(r'<img[^>]*>', replacer, content, flags=re.IGNORECASE)
        
        if new_content != content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)

print(f"Total bad images removed: {total_fixed}")
