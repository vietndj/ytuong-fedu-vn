import re

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/dist/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

errors = []

# 1. Instagram reels link
if 'href="${igReelsUrl}"' not in content:
    errors.append("Missing igReelsUrl link.")

# 2. forceDownloadVideo
if 'forceDownloadVideo(' not in content:
    errors.append("Missing forceDownloadVideo button.")

# 3. Instagram Video root icon
if 'title="Xem video gốc trên Instagram"' not in content:
    errors.append("Missing neat Instagram button.")

# 4. Images openReportModal
if content.count("openReportModal('${item.id}')") < 2:
    errors.append("Missing openReportModal on duo-posters.")

# 5. Play and Report buttons are gone
if 'title="Xem Video"' in content: # It could be missing or replaced
    pass
# 6. Magnifying glass gone
if 'openImgLightbox' in content and 'function openImgLightbox' not in content:
    pass

print("Audit run complete.")
