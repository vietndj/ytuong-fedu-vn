import re
from bs4 import BeautifulSoup
import json
import ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://fedu.vn/brollbank.html"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html_content = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
except Exception as e:
    print("Error fetching:", e)
    html_content = ""

soup = BeautifulSoup(html_content, 'html.parser')
cards = soup.find_all("div", class_=re.compile("glass-card.*"))

broll_data = []

for card in cards:
    card_id = card.get('id', '')
    cat = card.get('data-cat', '')
    orient = card.get('data-orient', '')
    
    title_el = card.find("h3")
    title = title_el.text.strip() if title_el else ""
    
    desc_el = card.find("p", class_=re.compile("text-xs text-slate-400 mt-2.*"))
    desc = desc_el.text.strip() if desc_el else ""
    
    iframe = card.find("iframe")
    youtube_url = iframe.get('src', '') if iframe else ""
    
    yt_id = ""
    if "embed/" in youtube_url:
        yt_id = youtube_url.split("embed/")[1].split("?")[0]
        
    dialogue_el = card.find("p", class_=re.compile("text-\\[11px\\].*italic.*"))
    dialogue = dialogue_el.text.strip() if dialogue_el else ""
    
    broll_data.append({
        "id": card_id.replace("card-", ""),
        "category": cat,
        "orientation": orient,
        "title": title,
        "description": desc,
        "youtube_id": yt_id,
        "dialogue": dialogue
    })

with open("broll_data.json", "w", encoding="utf-8") as f:
    json.dump(broll_data, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(broll_data)} items.")
