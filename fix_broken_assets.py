#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Broken Assets: Quét toàn bộ ideas_data.js, tìm video/ảnh 404 trên R2,
tìm nguồn local → upload bổ sung lên R2 CDN.
"""

import os
import re
import json
import subprocess
import sys
import urllib.parse
from pathlib import Path

# === CONFIG ===
IDEAS_JS = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ideas_data.js"
LOCAL_VIDEO_DIR = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn"
WORK_DIR = "/Users/vietmac/Work/AI_Video_Analysis"
R2_VIDEOS = "r2:vietndjmedia/videos"
R2_VIDEOS_PREVIEW = "r2:vietndjmedia/videos_preview"
R2_IMAGES = "r2:vietndjmedia/images"
DRIVE_LINKS_FILE = "/Users/vietmac/drive_links.json"

def load_ideas_data():
    with open(IDEAS_JS, "r") as f:
        content = f.read()
    # Extract JSON from var FEDU_IDEAS_DATABASE = {...};
    match = re.search(r'var FEDU_IDEAS_DATABASE\s*=\s*(\{[\s\S]*\});?\s*$', content)
    if match:
        return json.loads(match.group(1))
    return None

def check_url(url):
    """Return HTTP status code"""
    if not url or not url.startswith("http"):
        return "SKIP"
    try:
        result = subprocess.run(
            ['curl', '-sI', '-o', '/dev/null', '-w', '%{http_code}', url],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except:
        return "ERR"

def find_local_video(filename):
    """Find video file locally"""
    # Search in ytuong repo
    for ext in ['', '.mp4']:
        path = os.path.join(LOCAL_VIDEO_DIR, filename + ext)
        if os.path.exists(path):
            return path
    
    # Search in Work directory
    if os.path.isdir(WORK_DIR):
        for root, dirs, files in os.walk(WORK_DIR):
            for f in files:
                if f == filename or f == filename.replace('_preview', ''):
                    return os.path.join(root, f)
    
    return None

def find_local_images(folder_name):
    """Find local extracted_shots folder"""
    # Check Work dir
    if os.path.isdir(WORK_DIR):
        for root, dirs, files in os.walk(WORK_DIR):
            if os.path.basename(root) == folder_name:
                shots_dir = os.path.join(root, "extracted_shots")
                if os.path.isdir(shots_dir):
                    return shots_dir
                # Maybe images are directly in folder
                if any(f.endswith('.jpg') for f in files):
                    return root
    return None

def upload_to_r2(local_path, r2_dest):
    """Upload file/dir to R2"""
    print(f"  📤 Uploading: {os.path.basename(local_path)} → {r2_dest}")
    result = subprocess.run(
        ['rclone', 'copy', local_path, r2_dest, '-v'],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode == 0:
        print(f"  ✅ Upload thành công")
        return True
    else:
        print(f"  ❌ Upload thất bại: {result.stderr[:200]}")
        return False

def download_from_drive_and_upload_r2(drive_url, r2_dest, filename):
    """Download from Google Drive → Upload to R2"""
    tmp_path = f"/tmp/r2_fix_{filename}"
    print(f"  ⬇️ Downloading from Drive: {filename}")
    
    # Use yt-dlp or curl
    result = subprocess.run(
        ['curl', '-L', '-o', tmp_path, drive_url],
        capture_output=True, text=True, timeout=300
    )
    
    if result.returncode == 0 and os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 10000:
        upload_to_r2(tmp_path, r2_dest)
        os.remove(tmp_path)
        return True
    else:
        print(f"  ❌ Download thất bại từ Drive")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return False

def create_preview_and_upload(video_path, preview_name):
    """Create preview video and upload to R2"""
    tmp_preview = f"/tmp/{preview_name}"
    print(f"  🎬 Tạo preview: {preview_name}")
    
    result = subprocess.run([
        'ffmpeg', '-y', '-i', video_path,
        '-vf', 'scale=720:-2',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '28',
        '-c:a', 'aac', '-b:a', '64k',
        '-movflags', '+faststart',
        tmp_preview
    ], capture_output=True, text=True, timeout=300)
    
    if result.returncode == 0 and os.path.exists(tmp_preview):
        upload_to_r2(tmp_preview, R2_VIDEOS_PREVIEW + "/")
        os.remove(tmp_preview)
        return True
    return False

def main():
    print("=" * 60)
    print("🔍 FIX BROKEN ASSETS — Quét và sửa R2 CDN")
    print("=" * 60)
    
    # Load drive_links fallback
    drive_links = {}
    if os.path.exists(DRIVE_LINKS_FILE):
        with open(DRIVE_LINKS_FILE) as f:
            drive_links = json.load(f)
    
    with open(IDEAS_JS) as f:
        content = f.read()
    
    # Extract all URLs
    thumb_urls = re.findall(r'"thumb_hook":\s*"(https://[^"]+)"', content)
    video_urls = re.findall(r'"video_url":\s*"(https://[^"]+)"', content)
    original_urls = re.findall(r'"video_url_original":\s*"(https://[^"]+)"', content)
    
    all_urls = []
    for u in thumb_urls:
        all_urls.append(("thumb", u))
    for u in video_urls:
        all_urls.append(("video_preview", u))
    for u in original_urls:
        if "media.fedu.vn" in u:  # Only check R2 URLs, not Drive
            all_urls.append(("video_original", u))
    
    print(f"\n📊 Tổng URL cần kiểm tra: {len(all_urls)}")
    print(f"  - Thumbnails: {len(thumb_urls)}")
    print(f"  - Video previews: {len(video_urls)}")
    print(f"  - Video originals (R2): {len([u for u in original_urls if 'media.fedu.vn' in u])}")
    
    broken = []
    fixed = []
    unfixable = []
    
    for url_type, url in all_urls:
        code = check_url(url)
        if code != "200":
            broken.append((url_type, url, code))
    
    print(f"\n🔴 Tổng lỗi 404: {len(broken)}")
    
    for url_type, url, code in broken:
        decoded = urllib.parse.unquote(url)
        print(f"\n--- [{code}] {url_type}: {decoded[:100]}")
        
        if url_type == "video_preview":
            # Try to find original local video → create preview → upload
            fname = urllib.parse.unquote(url.split("/")[-1])
            original_fname = fname.replace("_preview", "")
            
            # Check if original exists on R2
            original_url = url.replace("videos_preview/", "videos/").replace("_preview", "")
            orig_code = check_url(original_url)
            
            if orig_code == "200":
                # Download original, create preview, upload
                tmp = f"/tmp/fix_{original_fname}"
                dl = subprocess.run(
                    ['curl', '-L', '-o', tmp, original_url],
                    capture_output=True, text=True, timeout=300
                )
                if dl.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 10000:
                    if create_preview_and_upload(tmp, fname):
                        fixed.append((url_type, url))
                    else:
                        unfixable.append((url_type, url, "Preview creation failed"))
                    os.remove(tmp)
                else:
                    unfixable.append((url_type, url, "Download original failed"))
                    if os.path.exists(tmp):
                        os.remove(tmp)
            else:
                # Try local
                local = find_local_video(original_fname)
                if local:
                    # Upload original first
                    upload_to_r2(local, R2_VIDEOS + "/")
                    # Then create preview
                    if create_preview_and_upload(local, fname):
                        fixed.append((url_type, url))
                    else:
                        unfixable.append((url_type, url, "Preview creation failed"))
                else:
                    # Try Drive
                    drive_url = drive_links.get(original_fname)
                    if drive_url:
                        tmp = f"/tmp/fix_{original_fname}"
                        if download_from_drive_and_upload_r2(drive_url, R2_VIDEOS + "/", original_fname):
                            if os.path.exists(tmp):
                                create_preview_and_upload(tmp, fname)
                                fixed.append((url_type, url))
                            else:
                                unfixable.append((url_type, url, "No local after Drive download"))
                        else:
                            unfixable.append((url_type, url, "Drive download failed"))
                    else:
                        unfixable.append((url_type, url, "No source found"))
        
        elif url_type == "thumb":
            # Extract folder from URL
            # https://media.fedu.vn/images/FOLDER/shot_01_mid.jpg
            parts = url.replace("https://media.fedu.vn/images/", "").split("/")
            if len(parts) >= 2:
                folder = urllib.parse.unquote(parts[0])
                local_shots = find_local_images(folder)
                if local_shots:
                    upload_to_r2(local_shots, f"{R2_IMAGES}/{urllib.parse.quote(folder, safe='@')}/")
                    fixed.append((url_type, url))
                else:
                    unfixable.append((url_type, url, f"No local images for folder: {folder}"))
            else:
                unfixable.append((url_type, url, "Cannot parse folder"))
        
        elif url_type == "video_original":
            fname = urllib.parse.unquote(url.split("/")[-1])
            local = find_local_video(fname)
            if local:
                upload_to_r2(local, R2_VIDEOS + "/")
                fixed.append((url_type, url))
            else:
                drive_url = drive_links.get(fname)
                if drive_url:
                    download_from_drive_and_upload_r2(drive_url, R2_VIDEOS + "/", fname)
                    fixed.append((url_type, url))
                else:
                    unfixable.append((url_type, url, "No source"))
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 KẾT QUẢ:")
    print(f"  ✅ Đã fix: {len(fixed)}")
    print(f"  ❌ Không fix được: {len(unfixable)}")
    print(f"  📋 Tổng lỗi ban đầu: {len(broken)}")
    
    if unfixable:
        print(f"\n❌ DANH SÁCH KHÔNG FIX ĐƯỢC:")
        for t, u, reason in unfixable:
            print(f"  [{t}] {urllib.parse.unquote(u)[:100]}")
            print(f"    Lý do: {reason}")
    
    return len(unfixable)

if __name__ == "__main__":
    remaining = main()
    sys.exit(0 if remaining == 0 else 1)
