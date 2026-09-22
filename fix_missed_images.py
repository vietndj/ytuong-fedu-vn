import os, re

files = [
    './reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html',
    './dist/reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace any leftover drive.google.com/uc?id= inside <img> src with proxy
    def replacer(match):
        drive_id = match.group(1)
        return f"https://ytuong.fedu.vn/api/video?id={drive_id}"

    new_content = re.sub(r'https://drive\.google\.com/uc\?id=([a-zA-Z0-9_-]+)', replacer, content)
    
    with open(filepath, 'w') as f:
        f.write(new_content)

print("Done replacing.")
