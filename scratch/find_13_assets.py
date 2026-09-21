import subprocess
import os

items = [
    ("DSKodjDkQYz", "IG_@withyuee_DSKodjDkQYz"),
    ("video_Video", "IG_@creator_video_Video_video"),
    ("DXoss18j011", "IG_@Jazzie_DXoss18j011_Video_by_jazziesillona"),
    ("Db6a3tHoWTS", "IG_@Ben_Db6a3tHoWTS_Video_by_by.bennnj"),
    ("DaSkD6CAHP2", "IG_@Andrew_Yue_DaSkD6CAHP2_Carousel_Analysis"),
    ("DdSs5rahILb", "IG_@creator_DdSs5rahILb_Video_DdSs5rahILb"),
    ("DcgSonjgnkV", "DcgSonjgnkV"),
    ("DO8arRxEZvh", "DO8arRxEZvh"),
    ("DWnsVqWj2XN", "DWnsVqWj2XN"),
    ("DXUG_1TjwJu", "DXUG_1TjwJu"),
    ("DWrDUymD4_a", "DWrDUymD4_a")
]

with open('scratch/r2_image_folders.txt') as f:
    r2_folders = [line.strip().rstrip('/') for line in f if line.strip()]

for sc, name in items:
    print(f"\nSearching for {sc} ({name}):")
    found = [f for f in r2_folders if sc.lower() in f.lower()]
    if not found:
        # try searching partial
        found = [f for f in r2_folders if name.lower() in f.lower()]
    print(f"  Matches in R2: {found}")
    if found:
        for f in found:
            res = subprocess.run(['rclone', 'lsf', f"r2:vietndjmedia/images/{f}/"], capture_output=True, text=True)
            files = res.stdout.strip().split('\n')
            print(f"    In {f}: {files[:6]} (total {len(files)} entries)")
