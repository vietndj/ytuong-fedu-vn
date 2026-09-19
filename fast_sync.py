import subprocess
import re
import os
import concurrent.futures

# Get the new IDs from the git commit
out = subprocess.check_output(["git", "show", "ebc91c0a54b161cd7236f378b734799f297b6b86", "--", "master_classifications.json"], text=True)
ids = re.findall(r"^\+\s+\"(IG_[^\"]+|FB_[^\"]+)\":\s*\{", out, re.MULTILINE)

# Some IDs in master_classifications.json might have _Carousel_Analysis appended. We should strip it if needed,
# or we can just try to copy. If the folder is named without _Carousel_Analysis, rclone will fail and we can fallback.
print(f"Found {len(ids)} new IDs.")

def sync_folder(vid_id):
    # Try to sync from extracted_shots to R2 root of that folder
    src = f"gdrive,root_folder_id=1Iu9v2sRTAUYvnkeKx-Tgu-RM_9A54_Qf:/{vid_id}/extracted_shots"
    dest = f"r2:vietndjmedia/images/{vid_id}"
    
    # Run rclone copy
    res = subprocess.run(["rclone", "copy", src, dest, "--include", "*.jpg", "--ignore-existing"], capture_output=True, text=True)
    if res.returncode != 0:
        # Maybe the folder in Gdrive doesn't have _Carousel_Analysis
        if "_Carousel_Analysis" in vid_id:
            clean_id = vid_id.replace("_Carousel_Analysis", "")
            src2 = f"gdrive,root_folder_id=1Iu9v2sRTAUYvnkeKx-Tgu-RM_9A54_Qf:/{clean_id}/extracted_shots"
            dest2 = f"r2:vietndjmedia/images/{vid_id}"
            subprocess.run(["rclone", "copy", src2, dest2, "--include", "*.jpg", "--ignore-existing"], capture_output=True)
            return f"Synced {vid_id} (fallback clean)"
        return f"Failed {vid_id}"
    
    return f"Synced {vid_id}"

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(sync_folder, ids))

for r in results:
    print(r)
print("Done!")
