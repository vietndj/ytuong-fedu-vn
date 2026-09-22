import json
import os

with open('gdrive_folders.json') as f:
    gdrive_data = json.load(f)

# Track existing paths to avoid duplicates
existing_paths = {item['path'] for item in gdrive_data}

with open('images_db.json') as f:
    images_data = json.load(f)

new_entries = 0
for item in images_data:
    if not item['IsDir'] and item.get('ID'):
        # In images_db.json, the path is like "IG_@german991020_DdiSb5Rp2LB_Lost_in_Seoul/shot_01_mid.jpg"
        # We should map it to the standard format which includes "extracted_shots"
        # Wait! In our fix script, we extract the folder and the filename and match by f"{folder}/{basename}"
        # So as long as we put it in as "Folder/extracted_shots/filename", it will match!
        
        parts = item['Path'].split('/')
        if len(parts) == 2:
            folder, filename = parts
            standard_path = f"{folder}/extracted_shots/{filename}"
            if standard_path not in existing_paths:
                gdrive_data.append({
                    "url": f"https://drive.google.com/uc?id={item['ID']}",
                    "path": standard_path
                })
                existing_paths.add(standard_path)
                new_entries += 1
        else:
            # Maybe already has extracted_shots or something else? Just add it as is
            if item['Path'] not in existing_paths:
                gdrive_data.append({
                    "url": f"https://drive.google.com/uc?id={item['ID']}",
                    "path": item['Path']
                })
                existing_paths.add(item['Path'])
                new_entries += 1

print(f"Added {new_entries} new entries to gdrive_folders.json")

with open('gdrive_folders.json', 'w') as f:
    json.dump(gdrive_data, f, indent=2)

