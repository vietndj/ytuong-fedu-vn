import json
import glob

with open("audit_queue.json", "r") as f:
    queue = json.load(f)

reports = glob.glob("reports/*.html")

ghosts_in_queue = []
for item in queue:
    vid = item["id"]
    found = False
    for r in reports:
        if vid in r:
            found = True
            break
    if not found:
        ghosts_in_queue.append(vid)

print(f"Ghosts in queue: {len(ghosts_in_queue)} / {len(queue)}")
