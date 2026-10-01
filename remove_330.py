import json
import os

files_to_update = ['broll_data.json', 'dist/broll_data.json']

for file_path in files_to_update:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Filter out item 330
        initial_len = len(data)
        data = [item for item in data if str(item.get('id')) != '330']
        final_len = len(data)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Updated {file_path}: {initial_len} -> {final_len} items")
