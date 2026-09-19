import json, re

with open("ideas_data.js", "r") as f:
    match = re.search(r"var FEDU_IDEAS_DATABASE = (\{.*?\});", f.read(), re.DOTALL)
    data = json.loads(match.group(1))

missing = []
for i in data.get("ideas", []):
    if not i.get("media", {}).get("video_url") and not i.get("is_excluded"):
        missing.append(i.get("id"))

print("Missing video_urls for:", missing)
