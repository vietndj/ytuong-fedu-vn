import json
import re

scene_file = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/scene.html"
with open(scene_file, "r") as f:
    scene_content = f.read()

match = re.search(r'const portalData = (\[.*?\]);\n', scene_content, re.DOTALL)
if match:
    portalData = json.loads(match.group(1))
    for item in portalData:
        if item.get("id") == "IG_@nathanael.lct_DdRg_ybtlKI":
            item["key_tech"] = "How I Shop, How I Style, Lookbook, Lifestyle, Zalando Commercial"
            break
            
    new_portal_data_str = json.dumps(portalData, indent=4, ensure_ascii=False)
    scene_content = scene_content[:match.start(1)] + new_portal_data_str + scene_content[match.end(1):]
    with open(scene_file, "w") as f:
        f.write(scene_content)
    print("Fixed scene.html key_tech successfully")
