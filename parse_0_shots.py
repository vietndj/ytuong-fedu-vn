import re

with open('ideas_data.js', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '"shots_count": 0' in line:
        # scan backwards for id
        for j in range(i, -1, -1):
            if '"id": "IG_' in lines[j]:
                print(lines[j].strip())
                break
