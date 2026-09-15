import os
import glob
import subprocess
from PIL import Image

def process_favicon(repo_path, prefix, version):
    svg_path = os.path.join(repo_path, 'favicon.svg')
    png_path = os.path.join(repo_path, 'favicon.png')
    ico_path = os.path.join(repo_path, 'favicon.ico')
    
    # 1. Convert SVG to PNG using sips
    print(f"Converting {svg_path} to {png_path}...")
    subprocess.run(['sips', '-s', 'format', 'png', svg_path, '--out', png_path], check=True)
    
    # 2. Convert PNG to ICO using Pillow
    print(f"Converting {png_path} to {ico_path}...")
    img = Image.open(png_path)
    img.save(ico_path, format='ICO', sizes=[(256, 256)]) # specify sizes to make it a valid ico with 256x256
    
    # 3. Inject <link> to HTML files
    html_files = glob.glob(os.path.join(repo_path, '*.html'))
    print(f"Injecting favicon into {len(html_files)} HTML files in {repo_path}...")
    
    link_tag = f'<link rel="icon" type="image/x-icon" href="{prefix}favicon.ico?v={version}">'
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # If it already has our link_tag, skip
        if link_tag in content:
            continue
            
        # If it has an old favicon link, replace it
        if '<link rel="icon"' in content:
            # simple replacement of the line or just append our tag
            # to be safe, append right before </head>
            pass
            
        if '</head>' in content:
            content = content.replace('</head>', f'    {link_tag}\n</head>')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

# Process Ytuong
process_favicon('/Users/vietmac/Documents/CODE/ytuong-fedu-vn', '/', '3')

# Process K
process_favicon('/Users/vietmac/Documents/CODE/k', '/k/', '3')

print("Done!")
