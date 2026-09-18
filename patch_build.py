import re

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/build_ideas_bank.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace master["industry"]["id"] with master.get("industries", [{}])[0].get("id", "ugc")
content = re.sub(r'master\["industry"\]\["id"\]', r'master.get("industries", [{}])[0].get("id", "ugc")', content)

# master.get("industry", {}).get("id") == "ugc"
content = re.sub(r'master and master\.get\("industry", \{\}\)\.get\("id"\) == "ugc"', r'master and any(i.get("id") == "ugc" for i in master.get("industries", []))', content)

# "industry": {
#   "id": master.get("industry", {}).get("id", "ugc"),
#   "name": master.get("industry", {}).get("name", "UGC"),
#   "icon": master.get("industry", {}).get("icon", "📱")
# },
# Change to "industries": master.get("industries", []),
# And add "x_factors": master.get("x_factors", []),
# Wait, let's just find the dictionary construction.

def replace_item_dict(match):
    s = match.group(0)
    s = re.sub(r'"industry": \{\s*"id":.*?\s*"name":.*?\s*"icon":.*?\s*\},', r'"industries": master.get("industries", []),\n            "x_factors": master.get("x_factors", []),', s, flags=re.DOTALL)
    return s
    
# Actually let's just do a string replace for the item dict.
content = re.sub(r'"industry": \{[^}]+\},', r'"industries": master.get("industries", []),\n            "x_factors": master.get("x_factors", []),', content, flags=re.DOTALL)


# Counter(v["industry"]["name"] for v in vids)
content = re.sub(r'v\["industry"\]\["name"\]', r'ind["name"] for ind in v.get("industries", [])', content)
# Wait, Counter(ind["name"] for v in vids for ind in v.get("industries", []))
content = re.sub(r'Counter\(.*?for v in vids\)', r'Counter(ind["name"] for v in vids for ind in v.get("industries", []))', content)

# sum(1 for x in active_ideas if x["industry"]["id"] == ind["id"])
content = re.sub(r'sum\(1 for x in active_ideas if x\["industry"\]\["id"\] == ind\["id"\]\)', r'sum(1 for x in active_ideas if any(i.get("id") == ind["id"] for i in x.get("industries", [])))', content)


with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/build_ideas_bank.py', 'w', encoding='utf-8') as f:
    f.write(content)
