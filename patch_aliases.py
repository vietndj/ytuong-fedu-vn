import re
with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/feedback_learner.py', 'r', encoding='utf-8') as f:
    c = f.read()
    
c = c.replace('"ugc": "ugc"', '"ugc": "ugc",\n    "bố cục": "ky-thuat-quay",\n    "bo cuc": "ky-thuat-quay",\n    "xây kênh": "thuong-hieu",\n    "xay kenh": "thuong-hieu"')
with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/feedback_learner.py', 'w', encoding='utf-8') as f:
    f.write(c)
