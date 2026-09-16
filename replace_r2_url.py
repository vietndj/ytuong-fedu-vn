import os

repo_dir = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn"
old_url = "pub-447bd44dfdac4938912655c855b8631c.r2.dev"
new_url = "media.fedu.vn"

count = 0
for root, dirs, files in os.walk(repo_dir):
    if '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith(('.html', '.md', '.js', '.json')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if old_url in content:
                    content = content.replace(old_url, new_url)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
            except Exception as e:
                pass

print(f"Replaced {old_url} with {new_url} in {count} files.")
