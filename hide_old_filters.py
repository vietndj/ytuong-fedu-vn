import re

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html', 'r') as f:
    content = f.read()

# Hide Industry Filter
content = content.replace('<!-- Lọc Theo Ngành Nghề -->\n                <div>', '<!-- Lọc Theo Ngành Nghề -->\n                <div class="hidden">')

# Hide Country Filter
content = content.replace('<!-- Lọc Theo Quốc Gia -->\n                <div>', '<!-- Lọc Theo Quốc Gia -->\n                <div class="hidden">')

# Hide Style Filter (it's in the header actually)
content = content.replace('<div id="shootingStyleTabsContainer"', '<div id="shootingStyleTabsContainer" class="hidden ')

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html', 'w') as f:
    f.write(content)
print("Old filters hidden!")
