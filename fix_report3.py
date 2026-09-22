import re

html_path = "./reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html"
proxy_url = "/api/video?id=1H30Z9tsLBPa3HVlKTclDhlVIlGM1KMba"
full_proxy_url = "https://ytuong.fedu.vn/api/video?id=1H30Z9tsLBPa3HVlKTclDhlVIlGM1KMba"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"' + proxy_url + '"', '"' + full_proxy_url + '"')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated HTML file to use absolute proxy url.")
