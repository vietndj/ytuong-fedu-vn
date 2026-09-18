import re

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/build_ideas_bank.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("top_ind = ind_counts.most_common(1)[0][0]", 'top_ind = ind_counts.most_common(1)[0][0] if ind_counts else "Unknown"')

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/build_ideas_bank.py', 'w', encoding='utf-8') as f:
    f.write(content)
