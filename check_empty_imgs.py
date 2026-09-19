import os
import glob
from bs4 import BeautifulSoup

report_dir = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports"
html_files = glob.glob(os.path.join(report_dir, "*.html"))

bad_imgs = []
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    imgs = soup.find_all('img')
    for img in imgs:
        src = img.get('src')
        # Skip lightbox imgs
        if img.get('id') in ['lightboxImg', 'lightboxLargeImg', 'lightboxImage'] or 'lightbox' in img.get('class', []):
            continue
            
        if not src or src == "" or src == "null" or src == "undefined":
            bad_imgs.append(f"{os.path.basename(file)}: {img}")

if bad_imgs:
    print(f"Found {len(bad_imgs)} bad images:")
    for b in bad_imgs[:50]:
        print(b)
else:
    print("No bad images found.")
