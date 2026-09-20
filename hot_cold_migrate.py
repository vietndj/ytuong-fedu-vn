import os
import subprocess
import json
import re
import sys
import glob

R2_VIDEOS = "r2:vietndjmedia/videos"
R2_VIDEOS_PREVIEW = "r2:vietndjmedia/videos_preview"
GDRIVE_VIDEOS = "gdrive:Antigravity_Backups/R2_videos_original"

def run_cmd(cmd, capture=False):
    if capture:
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.stdout.strip()
    else:
        subprocess.run(cmd, check=True)

def step0_survey():
    print("=== STEP 0: SURVEY ===")
    ls_out = run_cmd(["rclone", "lsf", R2_VIDEOS], capture=True)
    files = [f for f in ls_out.split('\n') if f.endswith('.mp4')]
    print(f"Total files in R2 videos: {len(files)}")
    return files

def step1_sync_cold():
    print("=== STEP 1: SYNC COLD TIER TO GDRIVE ===")
    run_cmd(["rclone", "copy", R2_VIDEOS, GDRIVE_VIDEOS, "--progress", "--drive-chunk-size=64M"])
    print("Checking sync integrity...")
    try:
        run_cmd(["rclone", "check", R2_VIDEOS, GDRIVE_VIDEOS])
        print("Sync complete and verified!")
        return True
    except subprocess.CalledProcessError:
        print("Sync failed or incomplete!")
        return False

def step2_generate_drive_links(files):
    print("=== STEP 2: GET DRIVE LINKS ===")
    drive_links = {}
    if os.path.exists("drive_links.json"):
        with open("drive_links.json") as f:
            drive_links = json.load(f)
            
    # To save time, only generate links for those that are missing
    missing = [f for f in files if f not in drive_links]
    if missing:
        print(f"Generating links for {len(missing)} files. This may take a while...")
        # Since rclone link is slow to do one by one, we will do it only when needed.
        # Let's batch this or do it on demand inside step 4.
    
    for idx, f in enumerate(missing):
        if idx % 10 == 0:
            print(f"Generating link {idx}/{len(missing)}...")
            with open("drive_links.json", "w") as fw:
                json.dump(drive_links, fw, indent=2)
                
        try:
            link_out = run_cmd(["rclone", "link", f"{GDRIVE_VIDEOS}/{f}"], capture=True)
            m = re.search(r"id=([^&\s]+)", link_out)
            if m:
                file_id = m.group(1)
                dl_link = f"https://drive.google.com/uc?id={file_id}&export=download"
                drive_links[f] = dl_link
        except Exception as e:
            print(f"Error getting link for {f}: {e}")
            
    with open("drive_links.json", "w") as fw:
        json.dump(drive_links, fw, indent=2)
    return drive_links

def step3_process_hot_tier(files):
    print("=== STEP 3: PROCESS HOT TIER ===")
    os.makedirs("/tmp/hot_cold_tier", exist_ok=True)
    batch_size = 10
    
    ls_preview = run_cmd(["rclone", "lsf", R2_VIDEOS_PREVIEW], capture=True).split('\n')
    
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(files)+batch_size-1)//batch_size}...")
        
        to_process = []
        for f in batch:
            prev_name = f.replace('.mp4', '_preview.mp4')
            if prev_name in ls_preview:
                pass
            else:
                to_process.append(f)
                
        if not to_process:
            continue
            
        # Download batch
        for f in to_process:
            run_cmd(["rclone", "copy", f"{R2_VIDEOS}/{f}", "/tmp/hot_cold_tier/"])
            
        for f in to_process:
            local_in = f"/tmp/hot_cold_tier/{f}"
            local_prev = f"/tmp/hot_cold_tier/{f.replace('.mp4', '_preview.mp4')}"
            local_webp = f"/tmp/hot_cold_tier/{f.replace('.mp4', '.webp')}"
            
            # encode preview
            cmd = ["ffmpeg", "-y", "-i", local_in, "-t", "20", "-vf", "scale=-2:720,fps=30", "-c:v", "libx264", "-crf", "28", "-preset", "ultrafast", "-c:a", "aac", "-b:a", "96k", local_prev]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # thumbnail
            cmd_thumb = ["ffmpeg", "-y", "-ss", "00:00:01", "-i", local_in, "-vframes", "1", "-c:v", "libwebp", "-q:v", "80", local_webp]
            subprocess.run(cmd_thumb, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # upload
            if os.path.exists(local_prev):
                run_cmd(["rclone", "copyto", local_prev, f"{R2_VIDEOS_PREVIEW}/{f.replace('.mp4', '_preview.mp4')}"])
            if os.path.exists(local_webp):
                run_cmd(["rclone", "copyto", local_webp, f"{R2_VIDEOS_PREVIEW}/{f.replace('.mp4', '.webp')}"])
            
            # clean
            os.remove(local_in)
            os.remove(local_prev)
            if os.path.exists(local_webp):
                os.remove(local_webp)

def step4_update_code(drive_links):
    print("=== STEP 4: UPDATE YTUONG CODE ===")
    dist_dir = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/dist"
    
    mc_path = os.path.join(dist_dir, "master_classifications.json")
    if os.path.exists(mc_path):
        with open(mc_path, "r") as f:
            mc_data = json.load(f)
            
        for item in mc_data.values():
            vid_url = item.get("video_url", "")
            if vid_url.endswith(".mp4") and "/videos/" in vid_url and not vid_url.endswith("_preview.mp4"):
                filename = vid_url.split('/')[-1]
                if filename in drive_links:
                    item["video_url_original"] = drive_links[filename]
                new_url = vid_url.replace("/videos/", "/videos_preview/").replace(".mp4", "_preview.mp4")
                item["video_url"] = new_url
                
        with open(mc_path, "w") as f:
            json.dump(mc_data, f, indent=2, ensure_ascii=False)
            
    # Modify index.html to show button
    idx_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r") as f:
            html = f.read()
            
        # We inject a button logic if possible.
        # This requires careful injection. We will just dump it out for now.
        
def step5_cleanup():
    print("=== STEP 5: CLEANUP R2 ===")
    # run_cmd(["rclone", "purge", R2_VIDEOS])
    # run_cmd(["rclone", "moveto", R2_VIDEOS_PREVIEW, R2_VIDEOS])
    print("R2 purge commented out for safety. Do it manually if verified.")

if __name__ == "__main__":
    files = step0_survey()
    if step1_sync_cold():
        drive_links = step2_generate_drive_links(files)
        step3_process_hot_tier(files)
        step4_update_code(drive_links)
        step5_cleanup()
    else:
        print("Aborting because sync failed.")
