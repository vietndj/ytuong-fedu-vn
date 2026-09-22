import os
import glob
import re

reports_dir = 'reports'
html_files = glob.glob(os.path.join(reports_dir, '*.html'))

fixed_count = 0

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to find the section starting with 'let currentEndTime = null;'
    # and ending with 'loadVideoCandidate();'
    
    pattern = r'let currentEndTime = null;[\s\S]*?loadVideoCandidate\(\);'
    
    # Replacement block:
    # let currentEndTime = null;
    # const player = document.getElementById('mainPlayer');
    # player.src = rawVideoSrc;
    # document.getElementById('directVidLink').href = rawVideoSrc.replace('/api/video?id=', 'https://drive.google.com/file/d/') + '/view';
    # player.load();
    
    replacement = """let currentEndTime = null;

const player = document.getElementById('mainPlayer');
if(player) {
    player.src = rawVideoSrc;
    const directLnk = document.getElementById('directVidLink');
    if (directLnk) {
        if (rawVideoSrc.includes('/api/video?id=')) {
            directLnk.href = rawVideoSrc.replace('https://ytuong.fedu.vn/api/video?id=', 'https://drive.google.com/file/d/') + '/view';
        } else {
            directLnk.href = rawVideoSrc;
        }
    }
    player.load();
}"""

    new_content, count = re.subn(pattern, replacement, content)
    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed_count += 1
        
print(f"Fixed {fixed_count} report files.")
