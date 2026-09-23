import re
import subprocess
import random

with open("ideas_data.js", "r") as f:
    content = f.read()

# count @creator
creator_count = content.count('"handle": "@creator"')

# extract thumb_hook and thumb_key
hooks = re.findall(r'"thumb_hook":\s*"(.*?)"', content)
keys = re.findall(r'"thumb_key":\s*"(.*?)"', content)
urls = set(hooks + keys)
urls = [u for u in urls if u.startswith("http")]

print(f"Ghost @creator active: {creator_count}")

# Get rclone list
try:
    res = subprocess.run(['rclone', 'lsf', 'r2:vietndjmedia/images/', '-R', '--files-only'], capture_output=True, text=True, timeout=60)
    r2_files = set(res.stdout.splitlines())
except Exception as e:
    print(f"Rclone error: {e}")
    r2_files = set()

# check phantom
import urllib.parse
phantom_count = 0
for u in urls:
    # URL format: https://media.fedu.vn/images/...
    if u.startswith("https://media.fedu.vn/images/"):
        path = u.replace("https://media.fedu.vn/images/", "")
        path = urllib.parse.unquote(path)
        if path not in r2_files:
            phantom_count += 1
            # print(f"Phantom: {u} -> {path}")

print(f"Phantom URLs active: {phantom_count}")

# Spot check 3 random
if urls:
    sample = random.sample([u for u in urls if u], min(3, len(urls)))
    for url in sample:
        cmd = ["curl", "-s", "-I", url]
        out = subprocess.check_output(cmd).decode('utf-8')
        status = out.split("\n")[0].strip()
        ctype = ""
        for line in out.split("\n"):
            if line.lower().startswith("content-type:"):
                ctype = line.split(":", 1)[1].strip()
        print(f"HTTP spot-check: {url} -> {status}, Type: {ctype}")
