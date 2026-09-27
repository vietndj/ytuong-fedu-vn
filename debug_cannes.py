import re
import subprocess

filename = "Cannes Street Fit Check - @vicgaibar.html"
filepath = f"reports/{filename}"

git_cmd = f'git show 3a30a0d^:"{filepath}"'
result = subprocess.run(git_cmd, shell=True, capture_output=True, text=True)
old_content = result.stdout

with open(filepath, 'r') as f:
    new_content = f.read()

old_urls = re.findall(r'(https://media\.fedu\.vn/images/[^\'"\s>]+)', old_content)

new_matches = list(re.finditer(r'(https://ytuong\.fedu\.vn/api/video\?id=[^\'"\s>]+)', new_content))
new_urls = []
for m in new_matches:
    start_idx = m.start()
    prefix = new_content[max(0, start_idx - 30):start_idx]
    if 'rawVideoSrc' not in prefix:
        new_urls.append(m.group(1))

print(f"Old URLs ({len(old_urls)}):")
print(old_urls[:5])
print("...")
print(old_urls[-5:])

print(f"New URLs ({len(new_urls)}):")
print(new_urls[:5])
print("...")
print(new_urls[-5:])
