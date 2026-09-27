import re
with open("dist/reports/IG_@Chibuzor_Ossai_DdRGI36Aj0X_Carousel_Analysis.html", "r") as f:
    html = f.read()
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
with open("test.js", "w") as f:
    for i, s in enumerate(scripts):
        f.write(f"// SCRIPT BLOCK {i}\n")
        f.write(s)
        f.write("\n")
