import re

with open("build_ideas_bank.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if '"ig_url": item.get("ig_url", "") or c_info["profile_url"],' in line:
        new_lines.append('            "ig_url": f"https://www.instagram.com/reel/{code}/" if code and len(code) == 11 else (c_info["profile_url"] if c_info.get("profile_url") else ""),\n')
    else:
        new_lines.append(line)

with open("build_ideas_bank.py", "w") as f:
    f.writelines(new_lines)
