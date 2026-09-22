import re

html_path = "./reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html"
drive_url = "https://drive.google.com/uc?id=1H30Z9tsLBPa3HVlKTclDhlVIlGM1KMba&export=download"
proxy_url = "/api/video?id=1H30Z9tsLBPa3HVlKTclDhlVIlGM1KMba"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(drive_url, proxy_url)
content = content.replace('href="' + proxy_url + '"', 'href="' + drive_url + '"') # keep download link as drive_url!

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated HTML file to use proxy.")
