import json

with open('master_classifications.json', 'r') as f:
    data = json.load(f)

for code in ['DaH_rTUTe14', 'DaXdrAVzGcc', 'DbnlAB5Twrw', 'DcGbEVFznin']:
    print(json.dumps(data.get(code), indent=2, ensure_ascii=False))
