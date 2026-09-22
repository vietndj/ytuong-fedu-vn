import json

# 1. Add Thomas to excluded_ids
with open('curation_config.json', 'r') as f:
    config = json.load(f)

bad_id = "IG_@𝗧𝗵𝗼𝗺𝗮𝘀_𝗠𝗮𝘁𝗵𝗲𝘄_DcgSonjgnkV_Carousel_Analysis"
if bad_id not in config.get("excluded_ids", []):
    config.setdefault("excluded_ids", []).append(bad_id)
    with open('curation_config.json', 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# 2. Fix Lazada broken report_url
with open('scene.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Just a dirty replace for the Lazada one
html = html.replace('"report_url": "reports/Ulanzi UA12 UA20 Inflatable Magnetic Tube Light - @ulanzi.html"', '"report_url": ""')
html = html.replace('"main_html_rel": "reports/Ulanzi UA12 UA20 Inflatable Magnetic Tube Light - @ulanzi.html"', '"main_html_rel": ""')
html = html.replace('"root_html_rel": "reports/Ulanzi UA12 UA20 Inflatable Magnetic Tube Light - @ulanzi.html"', '"root_html_rel": ""')

with open('scene.html', 'w', encoding='utf-8') as f:
    f.write(html)
