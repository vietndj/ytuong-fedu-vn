#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload Missing Videos to R2 — Batch download from Google Drive via rclone → upload to R2
Sử dụng rclone gdrive: để tải video gốc → nén preview → upload R2
"""

import os
import re
import json
import subprocess
import sys
import urllib.parse

IDEAS_JS = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js"
DRIVE_LINKS = "/Users/vietmac/drive_links.json"
TMP_DIR = "/tmp/r2_batch_upload"

def check_r2_exists(filename):
    """Check if file exists on R2"""
    result = subprocess.run(
        ['rclone', 'ls', f'r2:vietndjmedia/videos/{filename}'],
        capture_output=True, text=True, timeout=15
    )
    return bool(result.stdout.strip())

def check_r2_preview_exists(filename):
    """Check if preview exists on R2"""
    result = subprocess.run(
        ['rclone', 'ls', f'r2:vietndjmedia/videos_preview/{filename}'],
        capture_output=True, text=True, timeout=15
    )
    return bool(result.stdout.strip())

def download_from_drive_rclone(gdrive_path, local_path):
    """Download file from Google Drive via rclone"""
    result = subprocess.run(
        ['rclone', 'copy', gdrive_path, os.path.dirname(local_path), '-v'],
        capture_output=True, text=True, timeout=600
    )
    return result.returncode == 0

def create_preview(input_path, output_path):
    """Create preview video ≤3MB"""
    # Get duration
    probe = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', input_path],
        capture_output=True, text=True
    )
    duration = float(probe.stdout.strip()) if probe.stdout.strip() else 30.0
    target_br = max(int((3.0 * 8 * 1024) / duration), 300)
    
    result = subprocess.run([
        'ffmpeg', '-y', '-i', input_path,
        '-vf', 'scale=720:-2',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '28',
        '-c:a', 'aac', '-b:a', '64k',
        '-movflags', '+faststart',
        output_path
    ], capture_output=True, text=True, timeout=300)
    return result.returncode == 0

def upload_to_r2(local_path, r2_path):
    """Upload to R2"""
    result = subprocess.run(
        ['rclone', 'copy', local_path, r2_path, '-v'],
        capture_output=True, text=True, timeout=120
    )
    return result.returncode == 0

def main():
    os.makedirs(TMP_DIR, exist_ok=True)
    
    # Load drive_links: filename → drive download URL
    with open(DRIVE_LINKS, 'r') as f:
        drive_links = json.load(f)
    
    # Get list of ALL videos currently on R2
    r2_result = subprocess.run(
        ['rclone', 'ls', 'r2:vietndjmedia/videos/'],
        capture_output=True, text=True, timeout=30
    )
    r2_videos = set()
    for line in r2_result.stdout.strip().split('\n'):
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            r2_videos.add(parts[1].strip())
    
    r2_preview_result = subprocess.run(
        ['rclone', 'ls', 'r2:vietndjmedia/videos_preview/'],
        capture_output=True, text=True, timeout=30
    )
    r2_previews = set()
    for line in r2_preview_result.stdout.strip().split('\n'):
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            r2_previews.add(parts[1].strip())
    
    print(f"R2 videos: {len(r2_videos)}, R2 previews: {len(r2_previews)}")
    print(f"Drive links: {len(drive_links)}")
    
    # Find videos in drive_links that are NOT on R2
    missing_originals = []
    missing_previews = []
    
    for fname, drive_url in drive_links.items():
        if fname not in r2_videos:
            missing_originals.append((fname, drive_url))
        preview_name = os.path.splitext(fname)[0] + "_preview.mp4"
        if preview_name not in r2_previews:
            missing_previews.append((fname, preview_name, drive_url))
    
    print(f"\nMissing originals on R2: {len(missing_originals)}")
    print(f"Missing previews on R2: {len(missing_previews)}")
    
    # Process missing originals (download from Drive → upload to R2 → create preview)
    uploaded = 0
    failed = 0
    
    for i, (fname, drive_url) in enumerate(missing_originals):
        print(f"\n[{i+1}/{len(missing_originals)}] Processing: {fname}")
        local_path = os.path.join(TMP_DIR, fname)
        
        # Download from Drive using curl (drive_url is direct download link)
        print(f"  ⬇️ Downloading from Drive...")
        dl_result = subprocess.run(
            ['curl', '-L', '-o', local_path, '-m', '300', drive_url],
            capture_output=True, text=True, timeout=360
        )
        
        if dl_result.returncode != 0 or not os.path.exists(local_path) or os.path.getsize(local_path) < 10000:
            print(f"  ❌ Download failed")
            failed += 1
            if os.path.exists(local_path):
                os.remove(local_path)
            continue
        
        file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
        print(f"  ✅ Downloaded: {file_size_mb:.1f}MB")
        
        # Upload original to R2
        print(f"  📤 Uploading original to R2...")
        if upload_to_r2(local_path, 'r2:vietndjmedia/videos/'):
            print(f"  ✅ Original uploaded")
        else:
            print(f"  ❌ Original upload failed")
        
        # Create and upload preview
        preview_name = os.path.splitext(fname)[0] + "_preview.mp4"
        preview_path = os.path.join(TMP_DIR, preview_name)
        
        if preview_name not in r2_previews:
            print(f"  🎬 Creating preview...")
            if create_preview(local_path, preview_path):
                preview_size = os.path.getsize(preview_path) / (1024 * 1024)
                print(f"  ✅ Preview created: {preview_size:.1f}MB")
                
                if upload_to_r2(preview_path, 'r2:vietndjmedia/videos_preview/'):
                    print(f"  ✅ Preview uploaded")
                else:
                    print(f"  ❌ Preview upload failed")
                
                os.remove(preview_path)
            else:
                print(f"  ❌ Preview creation failed")
        
        # Cleanup
        os.remove(local_path)
        uploaded += 1
    
    print(f"\n{'='*60}")
    print(f"📊 RESULTS:")
    print(f"  ✅ Uploaded: {uploaded}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📋 Total missing: {len(missing_originals)}")

if __name__ == "__main__":
    main()
