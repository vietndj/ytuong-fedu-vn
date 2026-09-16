import os
import json

base_dir = "/Users/vietmac/Documents/CODE"
folders_to_check = [
    "tho.fedu.vn",
    "aioffline.fedu.vn",
    "CMS",
    "BROLL BANK",
    "fedu-font",
    "font-manager"
]

results = {}
keywords = ["sepay", "seqpay", "telegram", "webhook", "process.env"]

for folder in folders_to_check:
    proj_path = os.path.join(base_dir, folder)
    if not os.path.exists(proj_path):
        results[folder] = {"status": "NOT_FOUND"}
        continue
    
    has_api_dir = False
    api_paths = []
    keyword_hits = []
    
    for root, dirs, files in os.walk(proj_path):
        if '.git' in root or 'node_modules' in root or '.next' in root or 'dist' in root or 'build' in root:
            continue
        
        rel_path = os.path.relpath(root, proj_path)
        if rel_path.endswith('api') or rel_path == 'api':
            has_api_dir = True
            api_paths.append(rel_path)
            
        for file in files:
            if file.endswith(('.js', '.ts', '.jsx', '.tsx', '.html', '.php', '.py')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        for kw in keywords:
                            if kw in content:
                                keyword_hits.append(f"{kw} found in {os.path.relpath(file_path, proj_path)}")
                except:
                    pass
                    
    results[folder] = {
        "status": "FOUND",
        "has_api": has_api_dir,
        "keyword_hits": list(set(keyword_hits))
    }

print(json.dumps(results, indent=2))
