import json
import os
import glob

print("--- TRAINING DATA HEALTH CHECK ---")

# 1. Check Master DB
master_path = "master_classifications.json"
try:
    with open(master_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)
    print(f"Master classifications: {len(master_data)} items")
except Exception as e:
    print(f"Error reading master: {e}")
    master_data = []

# 2. Check Reports
reports = glob.glob("reports/*.html")
print(f"HTML Reports found: {len(reports)} files")

# 3. Check for ghosts (items in master but no report)
ghosts = 0
healthy_items = 0
for vid, data in master_data.items():
    if not isinstance(data, dict): continue
    
    # Check if report exists
    # Naming convention: reports/{id}.html or similar
    # Sometimes it's reports/{title} - @{creator}.html
    # Let's just check if ANY report contains the ID in its filename.
    found = False
    for r in reports:
        if vid in r:
            found = True
            break
    
    if found:
        healthy_items += 1
    else:
        ghosts += 1

print(f"Healthy Items (has report): {healthy_items}")
print(f"Ghost Items (no report): {ghosts}")

# 4. Check Queue
queue_path = "audit_queue.json"
try:
    with open(queue_path, "r", encoding="utf-8") as f:
        queue = json.load(f)
    print(f"Audit Queue: {len(queue)} items pending review")
except Exception as e:
    print(f"Error reading queue: {e}")

