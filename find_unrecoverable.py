#!/usr/bin/env python3
import json
import re
import subprocess
import urllib.parse
import sys

IDEAS_JS = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js"
DRIVE_LINKS_FILE = "/Users/vietmac/drive_links.json"

def check_url(url):
    if not url or not url.startswith("http"):
        return False
    try:
        res = subprocess.run(
            ['curl', '-sI', '-o', '/dev/null', '-w', '%{http_code}', url],
            capture_output=True, text=True, timeout=10
        )
        return res.stdout.strip() == "200"
    except:
        return False

def check_r2_exists(path):
    res = subprocess.run(
        ['rclone', 'ls', path],
        capture_output=True, text=True, timeout=10
    )
    return bool(res.stdout.strip())

def load_drive_links():
    try:
        with open(DRIVE_LINKS_FILE) as f:
            return json.load(f)
    except:
        return {}

def extract_ideas():
    with open(IDEAS_JS) as f:
        content = f.read()
    match = re.search(r'var FEDU_IDEAS_DATABASE\s*=\s*(\{[\s\S]*\});?\s*$', content)
    if match:
        return json.loads(match.group(1))
    return None

def main():
    db = extract_ideas()
    if not db:
        print("Cannot parse ideas database")
        return
    
    ideas = db.get("ideas", [])
    drive_links = load_drive_links()
    
    broken_ideas = []
    
    print(f"Scanning {len(ideas)} ideas for completely broken ones (no R2, no Drive source)...")
    
    for i, idea in enumerate(ideas):
        vid_url = idea.get("video_url", "")
        orig_url = idea.get("video_url_original", "")
        thumb = idea.get("thumb_hook", "")
        title = idea.get("title", "")
        idea_id = idea.get("id", "")
        
        # 1. Check if we have original video source
        has_source = False
        
        # Is it already on R2?
        if orig_url.startswith("https://media.fedu.vn/videos/"):
            fname = urllib.parse.unquote(orig_url.split("/")[-1])
            if check_r2_exists(f"r2:vietndjmedia/videos/{fname}"):
                has_source = True
        
        # Is it on Drive?
        if not has_source:
            fname = urllib.parse.unquote(vid_url.split("/")[-1]).replace("_preview", "")
            if fname in drive_links:
                has_source = True
                
            # Try fuzzy match in drive_links
            if not has_source:
                fname_lower = fname.lower()
                for k in drive_links.keys():
                    if fname_lower in k.lower() or k.lower() in fname_lower:
                        has_source = True
                        break
        
        # 2. Check if we have thumbnail source
        has_thumb = False
        if thumb.startswith("https://media.fedu.vn/images/"):
            folder = urllib.parse.unquote(thumb.split("/")[4])
            if check_r2_exists(f"r2:vietndjmedia/images/{folder}/"):
                has_thumb = True
        
        if not has_source or not has_thumb:
            broken_ideas.append({
                "id": idea_id,
                "title": title,
                "missing_video": not has_source,
                "missing_thumb": not has_thumb,
                "video_url": vid_url,
                "thumb_hook": thumb
            })
            print(f"  ❌ Broken: {title[:50]}... (ID: {idea_id}) [No Video: {not has_source}, No Thumb: {not has_thumb}]")
            sys.stdout.flush()
    
    print(f"\nFound {len(broken_ideas)} completely unrecoverable ideas.")
    with open("/tmp/broken_ideas_report.json", "w") as f:
        json.dump(broken_ideas, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
