import os
import json

projects = [
    "duyettin-fedu-vn",
    "brollbank-fedu-vn",
    "aioffline-fedu-vn",
    "cms-react",
    "fonthub-fedu-vn",
    "tho-fedu-vn",
    "don-ban-ve-ecopark",
    "aiwork-fedu-vn",
    "khoa-hoc-quay-dung-offline-k30",
    "workshop-edit-video-thuc-chien"
]

base_dir = "/Users/vietmac/Documents/CODE"
results = {}

keywords = ["sepay", "seqpay", "telegram", "webhook", "process.env"]

for proj in projects:
    proj_path = os.path.join(base_dir, proj)
    if not os.path.exists(proj_path):
        results[proj] = {"status": "NOT_FOUND"}
        continue
    
    has_api_dir = False
    api_paths = []
    keyword_hits = []
    
    for root, dirs, files in os.walk(proj_path):
        if '.git' in root or 'node_modules' in root or '.next' in root or 'dist' in root or 'build' in root:
            continue
        
        # Check for api directories
        rel_path = os.path.relpath(root, proj_path)
        if rel_path.endswith('api') or rel_path == 'api':
            has_api_dir = True
            api_paths.append(rel_path)
            
        # Scan files for keywords
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
                    
    # Deduplicate keyword hits
    unique_hits = list(set(keyword_hits))
    
    results[proj] = {
        "status": "FOUND",
        "has_api": has_api_dir,
        "api_paths": api_paths,
        "keyword_hits": unique_hits,
        "is_safe": not has_api_dir and not any('sepay' in h or 'webhook' in h for h in unique_hits)
    }

print(json.dumps(results, indent=2))
