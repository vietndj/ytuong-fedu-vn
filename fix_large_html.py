import os
import re
import base64

files = [
    "reports/Ulanzi LA30 30W RGB Air Tube Light - @ulanzi.global.html",
    "reports/The_Next_Station_Is_Vietnam - @madisonkjan.html",
    "reports/DJI Mic 3 ASMR Cinematic - @valenti_k41.html",
    "reports/Hong_Kong_Cinematic_Cityscape - @withyuee.html"
]

os.makedirs("reports/assets", exist_ok=True)

pattern = re.compile(r'data:(image|video)/([^;]+);base64,([a-zA-Z0-9+/=]+)')

for filepath in files:
    if not os.path.exists(filepath): continue
    print(f"Processing {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    count = 0
    def replacer(match):
        global count
        m_type = match.group(1) # image or video
        m_ext = match.group(2)
        b64_data = match.group(3)
        
        # Avoid extracting tiny things (e.g. less than 100KB base64 string ~ 133KB)
        if len(b64_data) < 133000:
            return match.group(0)
            
        count += 1
        base_name = os.path.basename(filepath).replace(".html", "").replace(" ", "_").replace("@", "")
        filename = f"{base_name}_{count}.{m_ext}"
        asset_path = f"reports/assets/{filename}"
        
        try:
            with open(asset_path, "wb") as af:
                af.write(base64.b64decode(b64_data))
            return f"assets/{filename}"
        except Exception as e:
            print("Error decoding:", e)
            return match.group(0)
            
    new_content = pattern.sub(replacer, content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Replaced {count} large base64 assets in {filepath}")

