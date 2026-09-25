import json
import os
import re
import glob

with open("master_classifications.json", "r") as f:
    master = json.load(f)

reports_dir = "reports"
html_files = glob.glob(f"{reports_dir}/*.html")

# Create a map of POST_ID -> current_html_file
post_id_to_file = {}
for hf in html_files:
    basename = os.path.basename(hf)
    # Find 11 or 19 char ID bounded by _ or - or .
    # Actually, a simpler way: just check if the POST_ID is a substring of the filename
    pass

synced_count = 0
renamed_count = 0
missing_count = 0

for vid, v in master.items():
    if not isinstance(v, dict) or "id" not in v:
        continue
    
    vid_id = v["id"]
    title = v.get("title", "")
    creator = v.get("creator", "")
    
    # Extract POST_ID
    post_id = None
    if vid_id.startswith(f"IG_{creator}_"):
        rem = vid_id[len(f"IG_{creator}_"):]
        m = re.match(r'^([A-Za-z0-9_-]{11})(?:_|$)', rem)
        if m: post_id = m.group(1)
    elif vid_id.startswith(f"TT_{creator}_"):
        rem = vid_id[len(f"TT_{creator}_"):]
        m = re.match(r'^([0-9]{19})(?:_|$)', rem)
        if m: post_id = m.group(1)
        
    if not post_id and "_" in vid_id:
        post_id = vid_id.split('_')[-2] if len(vid_id.split('_')) > 2 else vid_id
        
    expected_path = os.path.join(reports_dir, f"{vid_id}.html")
    
    if not os.path.exists(expected_path) and post_id:
        # Try to find a file containing the POST_ID
        candidates = [f for f in html_files if post_id in f]
        if candidates:
            # Rename the first candidate
            old_path = candidates[0]
            os.rename(old_path, expected_path)
            html_files.remove(old_path)
            html_files.append(expected_path)
            renamed_count += 1
        else:
            missing_count += 1
            
    # Now fix the title inside the HTML if it exists
    if os.path.exists(expected_path):
        with open(expected_path, "r", encoding="utf-8") as rf:
            content = rf.read()
        
        # Replace <title>...</title>
        new_content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content)
        
        # Also replace the <h1> title in the body if we can find it
        # The h1 is usually like <h1 class="...">(old title)</h1>
        # We can try to replace the inner text of the h1 that has the main title.
        # But just replacing <title> is safe.
        
        if new_content != content:
            with open(expected_path, "w", encoding="utf-8") as wf:
                wf.write(new_content)
            synced_count += 1

print(f"Renamed {renamed_count} missing report files.")
print(f"Synced {synced_count} report HTML titles to match JSON.")
print(f"Still missing {missing_count} reports completely.")
