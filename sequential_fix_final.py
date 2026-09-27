import os
import subprocess
import glob
import re

reports_dir = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports'
total_replaced = 0

for filepath in glob.glob(os.path.join(reports_dir, '*.html')):
    filename = os.path.basename(filepath)
    
    git_cmd = f'git show 3a30a0d^:"reports/{filename}"'
    result = subprocess.run(git_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0: 
        continue
        
    old_content = result.stdout
    with open(filepath, 'r') as f:
        new_content = f.read()
        
    old_matches = list(re.finditer(r'(https://media\.fedu\.vn/[^\'"\s>]+)', old_content))
    new_matches = list(re.finditer(r'(https://ytuong\.fedu\.vn/api/video\?id=[^\'"\s>]+)', new_content))
    
    valid_new_matches = []
    for m in new_matches:
        start_idx = m.start()
        prefix = new_content[max(0, start_idx - 30):start_idx]
        if 'rawVideoSrc' not in prefix:
            valid_new_matches.append(m)
            
    if len(old_matches) == len(valid_new_matches) and len(old_matches) > 0:
        offset = 0
        output = ""
        last_end = 0
        
        for i, new_m in enumerate(valid_new_matches):
            old_url = old_matches[i].group(1)
            output += new_content[last_end:new_m.start()]
            output += old_url
            last_end = new_m.end()
            
        output += new_content[last_end:]
        with open(filepath, 'w') as f:
            f.write(output)
        print(f"Fixed {len(old_matches)} links in '{filename}'")
        total_replaced += len(old_matches)
    elif len(valid_new_matches) > 0:
        print(f"Count mismatch in '{filename}': Old={len(old_matches)}, New={len(valid_new_matches)}")

print(f"Total sequentially replaced: {total_replaced}")
