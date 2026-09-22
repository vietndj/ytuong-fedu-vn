import re

html_path = "./reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html"
dist_html_path = "./dist/reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html"

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the line that overwrites the direct link
    content = content.replace("document.getElementById('directVidLink').href = url;", "// document.getElementById('directVidLink').href = url;")

    # Make sure the href is a Google Drive viewer URL so it has a normal download button
    # From: https://drive.google.com/uc?id=1H30Z9tsLBPa3HVlKTclDhlVIlGM1KMba&export=download
    # To: https://drive.google.com/file/d/1H30Z9tsLBPa3HVlKTclDhlVIlGM1KMba/view
    drive_uc = "https://drive.google.com/uc?id=1H30Z9tsLBPa3HVlKTclDhlVIlGM1KMba&export=download"
    drive_view = "https://drive.google.com/file/d/1H30Z9tsLBPa3HVlKTclDhlVIlGM1KMba/view"
    content = content.replace(drive_uc, drive_view)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file(html_path)
fix_file(dist_html_path)

print("Removed JS overwrite and updated to Drive Viewer URL.")
