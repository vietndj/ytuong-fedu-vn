import json
with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js', 'r') as f:
    text = f.read()
jstr = text.split('var FEDU_IDEAS_DATABASE = ')[1].split(';')[0]
data = json.loads(jstr)
for idea in data['ideas']:
    if idea['id'] == 'IG_@Saro_Deele_DXjRnwCISNU_Video_by_sarodeele':
        print(json.dumps(idea, indent=2))
        break
