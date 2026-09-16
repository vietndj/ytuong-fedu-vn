import json
import os
import glob
from bs4 import BeautifulSoup

with open('master_classifications.json', 'r') as f:
    master = json.load(f)

videos_to_fix = []
for k, v in master.items():
    if v.get('quick_takeaway') and v['quick_takeaway'].startswith('Tác phẩm điện ảnh ngắn'):
        if k == v.get('id'): # avoid duplicates from aliases
            videos_to_fix.append(v)

for v in videos_to_fix:
    vid = v['id']
    html_path = f"reports/{vid}.html"
    if not os.path.exists(html_path):
        # try fallback
        html_path = f"reports/{vid}/index.html"
    
    context = ""
    if os.path.exists(html_path):
        with open(html_path, 'r') as hf:
            soup = BeautifulSoup(hf, 'html.parser')
            # get overview
            overview = soup.select_one('.overview-desc, .overview-card')
            if overview: context += "OVERVIEW: " + overview.text.strip() + "\n"
            
            # get shots
            shots = soup.select('.shot-card')
            if shots:
                context += "SHOTS: "
                for i, s in enumerate(shots[:5]): # first 5 shots
                    desc = s.select_one('.shot-desc')
                    if desc: context += f"[{i+1}] {desc.text.strip()} "
                context += "\n"
                
    print(f"--- ID: {vid} ---")
    print(f"TITLE: {v.get('title')}")
    print(f"CONTEXT: {context[:500]}...") # Limit length
    print()
