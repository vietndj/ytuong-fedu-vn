import os
import re
import glob
import urllib.parse
import json

def load_gdrive_mapping():
    mapping = {}
    if os.path.exists('./gdrive_folders.json'):
        with open('./gdrive_folders.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                url = item.get('url', '')
                path = item.get('path', '')
                m = re.search(r'id=([a-zA-Z0-9_-]+)', url)
                if m and path:
                    mapping[path] = m.group(1)
                    basename = os.path.basename(path)
                    if basename not in mapping:
                        mapping[basename] = m.group(1)
    return mapping

def process_html_files():
    mapping = load_gdrive_mapping()
    html_files = glob.glob('./reports/*.html') + glob.glob('./dist/reports/*.html')
    table = []
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
            
        original_content = content
        
        # 1. Video
        m_video = re.search(r'(const\s+rawVideoSrc\s*=\s*)["\'](.*?)["\']', content)
        if m_video:
            old_url = m_video.group(2)
            drive_id = ""
            if "id=" in old_url:
                drive_id = old_url.split("id=")[1].split("&")[0]
            elif old_url.endswith(".mp4"):
                drive_id = old_url.split("/")[-1].replace(".mp4", "")
            else:
                drive_id = old_url.split("/")[-1]
                
            # If the extracted drive_id is just an IG ID, lookup the real Drive ID
            lookup_key = f"{drive_id}.mp4"
            if lookup_key in mapping:
                drive_id = mapping[lookup_key]
            elif drive_id in mapping:
                drive_id = mapping[drive_id]
                
            # Wait, if we already replaced it, the `drive_id` extracted might be the short IG ID.
            # E.g. https://ytuong.fedu.vn/api/video?id=DaC90d3tWuV -> drive_id = DaC90d3tWuV
            # We lookup "DaC90d3tWuV.mp4" in mapping -> gets the real Drive ID.
            
            new_url = f"https://ytuong.fedu.vn/api/video?id={drive_id}"
            content = content.replace(m_video.group(0), f'{m_video.group(1)}"{new_url}"')
            
            content = re.sub(r'document\.getElementById\([\'"]directVidLink[\'"]\)\.href\s*=\s*url;', 
                             r'// document.getElementById("directVidLink").href = url;', content)
            
            # Since we might have already put the bad ID in the href, we just replace it again.
            content = re.sub(
                r'(<a[^>]*id=[\'"]directVidLink[\'"][^>]*href=[\'"]).*?([\'"])',
                r'\g<1>https://drive.google.com/file/d/' + drive_id + r'/view\g<2>',
                content
            )

        # images already done
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            table.append(f"| {os.path.basename(filepath)} | Changed | PASS |")
        else:
            table.append(f"| {os.path.basename(filepath)} | No Change | PASS |")

    with open('report1.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(table))

if __name__ == "__main__":
    process_html_files()
