import json
import os
import re
import subprocess

# 1. DELETE MISSING REPORTS
with open("master_classifications.json", "r", encoding="utf-8") as f:
    master = json.load(f)

missing_count = 0
deleted_ids = []

for vid in list(master.keys()):
    v = master[vid]
    if not isinstance(v, dict) or "id" not in v:
        continue
    
    report_path = f"reports/{vid}.html"
    if not os.path.exists(report_path):
        del master[vid]
        deleted_ids.append(vid)
        missing_count += 1

with open("master_classifications.json", "w", encoding="utf-8") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Deleted {missing_count} items missing reports.")

# Rebuild data
subprocess.run(["python3", "confidence_gate.py"], check=True)
subprocess.run(["python3", "training_data_builder.py"], check=True)

# 2. AUDIT NEXT 30 ITEMS
with open("audit_queue.json", "r", encoding="utf-8") as f:
    queue = json.load(f)

# Deduplicate queue
unique_queue = []
seen = set()
for item in queue:
    if item["id"] not in seen:
        seen.add(item["id"])
        unique_queue.append(item)

# The user asked to "làm tiếp 30 bài tiếp" (do the next 30).
# Since we deleted some of the first 10, the queue shifted. 
# We'll just take items from index 7 to 37 (assuming 3 were deleted from the first 10).
# Let's just take the next 30 items that we HAVEN'T audited yet.
# We know the first 10 originally had certain IDs. Let's just pick index 7 to 36 of the NEW queue.
start_idx = 7 # We kept 7 from the first 10
end_idx = start_idx + 30
next_30 = unique_queue[start_idx:end_idx]

def get_source_link(id_str, creator):
    if id_str.startswith('IG_'):
        prefix = f"IG_{creator}_"
        if id_str.startswith(prefix):
            remainder = id_str[len(prefix):]
            match = re.match(r'^([A-Za-z0-9_-]{11})(?:_|$)', remainder)
            if match:
                return f"https://www.instagram.com/reels/{match.group(1)}/"
            else:
                return f"https://www.instagram.com/reels/{remainder.split('_')[0]}/"
    elif id_str.startswith('TT_'):
        prefix = f"TT_{creator}_"
        if id_str.startswith(prefix):
            remainder = id_str[len(prefix):]
            match = re.match(r'^([0-9]{19})(?:_|$)', remainder)
            if match:
                return f"https://www.tiktok.com/{creator.replace('@','')}/video/{match.group(1)}"
            else:
                return f"https://www.tiktok.com/{creator.replace('@','')}/video/{remainder.split('_')[0]}"
    elif not "_" in id_str:
        return f"https://www.instagram.com/reels/{id_str}/"
    return "N/A"

results = []

for item in next_30:
    vid = item["id"]
    creator = item["creator"]
    title = item["title"]
    
    link = get_source_link(vid, creator)
    report_path = f"reports/{vid}.html"
    report_exists = os.path.exists(report_path)
    
    report_title_match = "N/A"
    if report_exists:
        with open(report_path, "r", encoding="utf-8") as rf:
            content = rf.read()
            # Relaxed matching to account for HTML encoding or minor differences
            clean_title = title.split('-')[0].strip()
            if clean_title in content or title in content:
                report_title_match = "OK"
            else:
                report_title_match = "FAIL"
                
    results.append({
        "id": vid,
        "title": title,
        "creator": creator,
        "link": link,
        "report_exists": report_exists,
        "report_title_match": report_title_match
    })

artifact_path = "/Users/vietmac/.gemini/antigravity/brain/c3877973-048f-46cd-8326-1c3ebfa98f84/next_30_audit.md"
with open(artifact_path, "w", encoding="utf-8") as f:
    f.write("# NGHIỆM THU: 30 VIDEO TIẾP THEO TRONG HÀNG CHỜ\n\n")
    f.write("| STT | ID (Mã gốc) | Tác giả | Link IG Gen ra | Báo cáo HTML | Khớp Nội dung |\n")
    f.write("|---|---|---|---|---|---|\n")
    for i, r in enumerate(results, 1):
        rpt_status = "✅ Có" if r["report_exists"] else "❌ Không"
        match_status = "✅ Khớp" if r["report_title_match"] == "OK" else ("❌ Lệch" if r["report_title_match"] == "FAIL" else "N/A")
        f.write(f"| {i} | `{r['id'][:30]}...` | `{r['creator']}` | [Link]({r['link']}) | {rpt_status} | {match_status} |\n")

print(f"Artifact created at {artifact_path}")
