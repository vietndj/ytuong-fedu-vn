import json
import os
from datetime import datetime

base_dir = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn'
master_file = os.path.join(base_dir, 'master_classifications.json')
learned_file = os.path.join(base_dir, 'LEARNED_PATTERNS.json')
output_file = os.path.join(base_dir, 'training_data.js')

with open(master_file, 'r', encoding='utf-8') as f:
    master_data = json.load(f)

with open(learned_file, 'r', encoding='utf-8') as f:
    learned_data = json.load(f)

stats = learned_data.get('stats', {})
corrections = learned_data.get('learning_history_logs', [])
rules = learned_data.get('distilled_rules', [])

# Parse all classifications
all_classifications = []
for video_id, data in master_data.items():
    if data.get('is_excluded', False):
        continue
    
    style = data.get('shooting_style', {})
    industry = data.get('industry', {})
    if isinstance(industry, list):
        if industry:
            ind = industry[0]
            if isinstance(ind, dict):
                industry = ind
            else:
                industry = {"id": ind, "name": ind}
        else:
            industry = {}
            
    if isinstance(style, str):
        style = {"id": style, "name": style}
        
    all_classifications.append({
        "id": video_id,
        "title": data.get('title', ''),
        "creator": data.get('creator', ''),
        "shooting_style": style,
        "industry": industry,
        "purpose": data.get('purpose', ''),
        "logic_explanation": data.get('logic_explanation', ''),
        "report_url": data.get('report_url', ''),
        "has_correction": any(c.get('video_id') == video_id for c in corrections),
        "correction_summary": next((c.get('reason_distilled') for c in corrections if c.get('video_id') == video_id), "")
    })

training_data = {
    "generated_at": datetime.now().isoformat(),
    "stats": {
        "total_videos": len(all_classifications),
        "total_corrections": len(corrections),
        "alignment_score": stats.get('alignment_score', 0),
        "target_score": stats.get('target_score', 98.0),
        "rules_count": len(rules),
        "most_common_errors": stats.get('most_common_errors', [])
    },
    "corrections": corrections,
    "rules": rules,
    "all_classifications": all_classifications
}

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('var TRAINING_DATA = ' + json.dumps(training_data, indent=2, ensure_ascii=False) + ';')

print(f"Generated {output_file} with {len(all_classifications)} classifications and {len(corrections)} corrections.")

import shutil
dist_dir = os.path.join(base_dir, "dist")
if os.path.exists(dist_dir):
    # Copy training_data.js
    shutil.copy2(output_file, os.path.join(dist_dir, "training_data.js"))
    # Copy training/ folder
    training_src = os.path.join(base_dir, "training")
    training_dist = os.path.join(dist_dir, "training")
    if os.path.exists(training_src):
        shutil.copytree(training_src, training_dist, dirs_exist_ok=True)
    print("Copied training data and training/ directory to dist/")
