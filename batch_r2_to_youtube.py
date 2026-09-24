import os
import sys
import json
import pickle
import time
import subprocess
import re
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

TOKEN_CANDIDATES = [
    ("/Users/vietmac/Documents/CODE/videoOffline/token_kqc.pickle", "kqc_p2"),
    ("/Users/vietmac/Documents/CODE/videoOffline/token_project_4.pickle", "kqc_p4"),
    ("/Users/vietmac/Documents/CODE/videoOffline/token_sabakiz.pickle", "sabakiz_p1"),
    ("/Users/vietmac/Documents/CODE/videoOffline/token_sabakiz_2.pickle", "sabakiz_p2"),
    ("/Users/vietmac/Documents/CODE/videoOffline/token_full.pickle", "personal_p1"),
]

SABAKIZ_PLAYLISTS = ['PLI7jGRLNGsvY', 'PLONsbnGDa39A']

def log(msg):
    print(f"[R2->YT] {msg}", flush=True)

def refresh_and_get_service(token_path):
    if not os.path.exists(token_path):
        return None
    with open(token_path, 'rb') as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, 'wb') as f:
            pickle.dump(creds, f)
    return build('youtube', 'v3', credentials=creds)

def add_to_sabakiz_playlists(video_id):
    sabakiz_token = '/Users/vietmac/Documents/CODE/videoOffline/token_sabakiz.pickle'
    if not os.path.exists(sabakiz_token):
        return
    try:
        service = refresh_and_get_service(sabakiz_token)
        for pid in SABAKIZ_PLAYLISTS:
            try:
                service.playlistItems().insert(
                    part='snippet',
                    body={
                        'snippet': {
                            'playlistId': pid,
                            'resourceId': {
                                'kind': 'youtube#video',
                                'videoId': video_id
                            }
                        }
                    }
                ).execute()
                log(f"  ✅ Đã thêm vào Sabakiz Playlist {pid}")
            except Exception as e_pl:
                log(f"  ⚠️ Lưu ý thêm playlist {pid}: {e_pl}")
    except Exception as e:
        log(f"  ⚠️ Lỗi kết nối Sabakiz token để add playlist: {e}")

def upload_video(video_path, title, description, tags=None):
    if tags is None:
        tags = ['phan_tich_video', 'storyboard', 'sabakiz', 'review']
    
    # Check vertical 9:16
    try:
        probe = subprocess.check_output(
            f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{video_path}"',
            shell=True
        ).decode().strip().split('x')
        if len(probe) == 2:
            w, h = int(probe[0]), int(probe[1])
            if w > h:
                log(f"  Video NGANG ({w}x{h}), padding về 1080x1920 (9:16)...")
                padded = video_path.replace(".mp4", "_vertical.mp4")
                subprocess.run(
                    f'ffmpeg -y -i "{video_path}" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -preset fast -c:a copy "{padded}" 2>/dev/null',
                    shell=True
                )
                if os.path.exists(padded) and os.path.getsize(padded) > 1000:
                    video_path = padded
    except Exception as e_dim:
        log(f"  Lưu ý check dimension: {e_dim}")

    body = {
        'snippet': {
            'title': title[:100],
            'description': description,
            'tags': tags,
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'unlisted',
            'selfDeclaredMadeForKids': False
        }
    }

    for token_path, tag in TOKEN_CANDIDATES:
        try:
            service = refresh_and_get_service(token_path)
            if not service:
                continue
            media = MediaFileUpload(video_path, chunksize=10*1024*1024, resumable=True)
            req = service.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
            response = None
            retry = 0
            fail = False
            while response is None:
                try:
                    status, response = req.next_chunk()
                    if status:
                        log(f"  Upload ({tag}): {int(status.progress() * 100)}%")
                    retry = 0
                except Exception as e_chunk:
                    err_s = str(e_chunk)
                    if any(k in err_s for k in ["quotaExceeded", "rateLimitExceeded", "uploadLimitExceeded", "429"]):
                        log(f"  ⚠️ Token {tag} bị chặn ({err_s[:90]}). Thử token tiếp theo...")
                        fail = True
                        break
                    retry += 1
                    if retry > 3:
                        log(f"  Lỗi chunk {tag}: {e_chunk}")
                        fail = True
                        break
                    time.sleep(2 ** retry)
            if not fail and response and 'id' in response:
                vid_id = response['id']
                log(f"  🎉 Upload THÀNH CÔNG qua {tag}! ID: {vid_id} | https://youtu.be/{vid_id}")
                add_to_sabakiz_playlists(vid_id)
                return vid_id, tag
        except Exception as e_up:
            err_msg = str(e_up)
            log(f"  Lỗi khi gọi API với token {tag}: {err_msg[:120]}")
            continue
    return None, None

def update_html_report(report_path, video_id):
    if not os.path.exists(report_path):
        return False
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    iframe_tag = f'<iframe id="mainPlayer" src="https://www.youtube.com/embed/{video_id}?enablejsapi=1&rel=0&modestbranding=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="width:100%;aspect-ratio:9/16;border-radius:12px;"></iframe>'
    
    # Replace <video id="mainPlayer" ...>...</video>
    content = re.sub(
        r'<video\s+id=[\'"]mainPlayer[\'"][^>]*>.*?</video>',
        iframe_tag,
        content,
        flags=re.DOTALL
    )
    # Also handle self-closing if any
    content = re.sub(
        r'<video\s+id=[\'"]mainPlayer[\'"][^>]*/>',
        iframe_tag,
        content
    )
    
    # Replace directVidLink href
    content = re.sub(
        r'href=[\'"]https://media\.fedu\.vn/videos/[^\'"]+[\'"]\s+target=[\'"]_blank[\'"]\s+style=[\'"]([^\'"]*)[\'"]>Tệp gốc ↗</a>',
        f'href="https://youtu.be/{video_id}" target="_blank" style="\\1">Xem YouTube ↗</a>',
        content
    )

    if content != orig:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        log(f"  ✅ Updated HTML: {os.path.basename(report_path)}")
        return True
    else:
        log(f"  ⚠️ HTML unchanged: {os.path.basename(report_path)}")
        return False

def update_master_classifications(shortcode, video_id):
    p = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/master_classifications.json'
    if not os.path.exists(p):
        return
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated = 0
    if isinstance(data, dict):
        for k, v in data.items():
            if shortcode in k or (isinstance(v, dict) and shortcode in str(v)):
                if isinstance(v, dict):
                    v['youtube_id'] = video_id
                    v['youtube_url'] = f"https://youtu.be/{video_id}"
                    updated += 1
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if shortcode in str(item):
                    item['youtube_id'] = video_id
                    item['youtube_url'] = f"https://youtu.be/{video_id}"
                    updated += 1
                    
    if updated > 0:
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        log(f"  ✅ Updated {updated} entries in master_classifications.json")

def delete_from_r2(r2_path):
    cmd = f'rclone delete "r2:vietndjmedia/videos/{r2_path}"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        log(f"  🗑️ Đã xóa video khỏi R2: {r2_path}")
        return True
    else:
        log(f"  ⚠️ Lỗi xóa R2: {res.stderr.strip()}")
        return False

TASKS = [
    {
        'shortcode': 'DajU5I5AKIu',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@˗ˏˋ_celina_ˎˊ˗_DajU5I5AKIu_Video_by_celfstudies/DajU5I5AKIu.mp4',
        'title': '[Phân Tích] @celfstudies - LA VLOG !! (DajU5I5AKIu)',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@celfstudies_DajU5I5AKIu_LA_VLOG_!!_(horizontal_edition🤳).html',
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@˗ˏˋ_celina_ˎˊ˗_DajU5I5AKIu_Video_by_celfstudies.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@celfstudies_DajU5I5AKIu_LA_VLOG_!!_(horizontal_edition🤳).html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@˗ˏˋ_celina_ˎˊ˗_DajU5I5AKIu_Video_by_celfstudies.html',
        ]
    },
    {
        'shortcode': 'Dbd8gmqRAc3',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@cinematic_lee_Dbd8gmqRAc3_It’s_a_constant_struggle_😅/Dbd8gmqRAc3.mp4',
        'title': '[Phân Tích] @cinematic_lee - Constant Struggle (Dbd8gmqRAc3)',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@cinematic_lee_Dbd8gmqRAc3_It’s_a_constant_struggle_😅.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@cinematic_lee_Dbd8gmqRAc3_It’s_a_constant_struggle_😅.html',
        ]
    },
    {
        'shortcode': 'Dblr-88PjlJ',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@ALLYQQ_子涵🐤_Dblr-88PjlJ_Video_by_qaqu_uu/Dblr-88PjlJ.mp4',
        'title': '[Phân Tích] @qaqu_uu - Dblr-88PjlJ',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@qaqu_uu_Dblr-88PjlJ_yelena_belova_would_call_this_small_baby_pota.html',
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@ALLYQQ_子涵🐤_Dblr-88PjlJ_Video_by_qaqu_uu.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@qaqu_uu_Dblr-88PjlJ_yelena_belova_would_call_this_small_baby_pota.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@ALLYQQ_子涵🐤_Dblr-88PjlJ_Video_by_qaqu_uu.html',
        ]
    },
    {
        'shortcode': 'DcYZMc7Sc49',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@31.ioa_DcYZMc7Sc49_Video_by_31.ioa/DcYZMc7Sc49.mp4',
        'title': '[Phân Tích] @31.ioa - DcYZMc7Sc49',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@31.ioa_DcYZMc7Sc49_Video_by_31.ioa.html',
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@Sodam_Kim_DcYZMc7Sc49_Video_by_31.ioa.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@31.ioa_DcYZMc7Sc49_Video_by_31.ioa.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@Sodam_Kim_DcYZMc7Sc49_Video_by_31.ioa.html',
        ]
    },
    {
        'shortcode': 'DcvZ-FowD_A',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@𝙗𝙮𝙨𝙪𝙣𝙘𝙖𝙣_DcvZ-FowD_A_Video_by_bysuncan/DcvZ-FowD_A.mp4',
        'title': '[Phân Tích] @bysuncan - DcvZ-FowD_A',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@𝙗𝙮𝙨𝙪𝙣𝙘𝙖𝙣_DcvZ-FowD_A_Video_by_bysuncan.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@𝙗𝙮𝙨𝙪𝙣𝙘𝙖𝙣_DcvZ-FowD_A_Video_by_bysuncan.html',
        ]
    },
    {
        'shortcode': 'DdESxNlE2Ay',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/DdESxNlE2Ay.mp4',
        'title': '[Phân Tích] @minghan1004 - DdESxNlE2Ay',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@minghan1004_DdESxNlE2Ay_Carousel_Analysis.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@minghan1004_DdESxNlE2Ay_Carousel_Analysis.html',
        ],
        'extra_r2_deletions': ['DdES7VSk4Fc.mp4']
    },
    {
        'shortcode': 'DdGQQL-ih_O',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@createdbyadz_⚡️_DdGQQL-ih_O_Video_by_adz.mov/DdGQQL-ih_O.mp4',
        'title': '[Phân Tích] @adz.mov - Land of Smiles (DdGQQL-ih_O)',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@createdbyadz_⚡️_DdGQQL-ih_O_Video_by_adz.mov.html',
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@adz.mov_DdGQQL-ih_O_the_land_of_smiles_🇹🇭_#thailand_#cinematograp.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@createdbyadz_⚡️_DdGQQL-ih_O_Video_by_adz.mov.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@adz.mov_DdGQQL-ih_O_the_land_of_smiles_🇹🇭_#thailand_#cinematograp.html',
        ]
    },
    {
        'shortcode': 'DdPESzcNS-W',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@AŁEC_RIJKS_DdPESzcNS-W_Video_by_alecrijks/DdPESzcNS-W.mp4',
        'title': '[Phân Tích] @alecrijks - DdPESzcNS-W',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@AŁEC_RIJKS_DdPESzcNS-W_Video_by_alecrijks.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@AŁEC_RIJKS_DdPESzcNS-W_Video_by_alecrijks.html',
        ]
    },
    {
        'shortcode': 'DdYHuz_sXs0',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@KUZYA_монтаж_Reels_DdYHuz_sXs0_Video_by_kuzya.tm/DdYHuz_sXs0.mp4',
        'title': '[Phân Tích] @kuzya.tm - DdYHuz_sXs0',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@KUZYA_монтаж_Reels_DdYHuz_sXs0_Video_by_kuzya.tm.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@KUZYA_монтаж_Reels_DdYHuz_sXs0_Video_by_kuzya.tm.html',
        ]
    },
    {
        'shortcode': 'Ddb6rA7NwQd',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@ELENA_𝗔𝗲𝘀𝘁𝗵𝗲𝘁𝗶𝗰_𝗜𝗻𝘀𝗽𝗶𝗿𝗮𝘁𝗶𝗼𝗻_𝗟𝗶𝗳𝗲𝘀𝘁𝘆𝗹𝗲_Ddb6rA7NwQd_Video_by_elenabuntushak/Ddb6rA7NwQd.mp4',
        'title': '[Phân Tích] @elenabuntushak - Always Ready (Ddb6rA7NwQd)',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@elenabuntushak_Ddb6rA7NwQd_YES,_I’m_always_ready!.html',
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@ELENA_𝗔𝗲𝘀𝘁𝗵𝗲𝘁𝗶𝗰_𝗜𝗻𝘀𝗽𝗶𝗿𝗮𝘁𝗶𝗼𝗻_𝗟𝗶𝗳𝗲𝘀𝘁𝘆𝗹𝗲_Ddb6rA7NwQd_Video_by_elenabuntushak.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@elenabuntushak_Ddb6rA7NwQd_YES,_I’m_always_ready!.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@ELENA_𝗔𝗲𝘀𝘁𝗵𝗲𝘁𝗶𝗰_𝗜𝗻𝘀𝗽𝗶𝗿𝗮𝘁𝗶𝗼𝗻_𝗟𝗶𝗳𝗲𝘀𝘁𝘆𝗹𝗲_Ddb6rA7NwQd_Video_by_elenabuntushak.html',
        ]
    },
    {
        'shortcode': 'DddgEE5R2CW',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@starsinmycam_DddgEE5R2CW_i_blink_and_it’s_night_time/DddgEE5R2CW.mp4',
        'title': '[Phân Tích] @starsinmycam - Night Time (DddgEE5R2CW)',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@starsinmycam_DddgEE5R2CW_i_blink_and_it’s_night_time.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@starsinmycam_DddgEE5R2CW_i_blink_and_it’s_night_time.html',
        ]
    },
    {
        'shortcode': 'DdkHw7gIXLj',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@rubtsov.a_DdkHw7gIXLj_В_библиотеку/DdkHw7gIXLj.mp4',
        'title': '[Phân Tích] @rubtsov.a - Library (DdkHw7gIXLj)',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@Ekaterina_модель_Уфа_,_Питер_DdkHw7gIXLj_Video_by_rubtsov.a.html',
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@rubtsov.a_DdkHw7gIXLj_В_библиотеку.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@Ekaterina_модель_Уфа_,_Питер_DdkHw7gIXLj_Video_by_rubtsov.a.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@rubtsov.a_DdkHw7gIXLj_В_библиотеку.html',
        ]
    },
    {
        'shortcode': 'DdlmRIcBw81',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@Harry_DdlmRIcBw81_Video_by_hdnimedia/DdlmRIcBw81.mp4',
        'title': '[Phân Tích] @hdnimedia - DdlmRIcBw81',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@Harry_DdlmRIcBw81_Video_by_hdnimedia.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@Harry_DdlmRIcBw81_Video_by_hdnimedia.html',
        ]
    },
    {
        'shortcode': 'DdplzLRytOA',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@Flying_DdplzLRytOA_Video_by_loveqinghe/DdplzLRytOA.mp4',
        'title': '[Phân Tích] @loveqinghe - DdplzLRytOA',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@Flying_DdplzLRytOA_Video_by_loveqinghe.html',
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@loveqinghe_DdplzLRytOA_这样拍才好看.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@Flying_DdplzLRytOA_Video_by_loveqinghe.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@loveqinghe_DdplzLRytOA_这样拍才好看.html',
        ]
    },
    {
        'shortcode': 'DdpxcaOMaQS',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@iamaayushswamy_DdpxcaOMaQS_caption_placement/DdpxcaOMaQS.mp4',
        'title': '[Phân Tích] @iamaayushswamy - Caption Placement (DdpxcaOMaQS)',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@iamaayushswamy_DdpxcaOMaQS_caption_placement.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@iamaayushswamy_DdpxcaOMaQS_caption_placement.html',
        ]
    },
    {
        'shortcode': 'Ddqo7-eTI2A',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@lisha_ho_Ddqo7-eTI2A_Wait…_@ralphlauren_+_coffee_at_KLCC_👀/Ddqo7-eTI2A.mp4',
        'title': '[Phân Tích] @lisha_ho - Ralph Lauren Coffee (Ddqo7-eTI2A)',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@lisha_ho_Ddqo7-eTI2A_Wait…_@ralphlauren_+_coffee_at_KLCC_👀.html',
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@Lisha_Ho_Ddqo7-eTI2A_Video_by_lisha_ho.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@lisha_ho_Ddqo7-eTI2A_Wait…_@ralphlauren_+_coffee_at_KLCC_👀.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@Lisha_Ho_Ddqo7-eTI2A_Video_by_lisha_ho.html',
        ]
    },
    {
        'shortcode': 'DdrBPIwIpg-',
        'video_file': '/Users/vietmac/Documents/CODE/Quản gia/output_packages/IG_@Angela_DdrBPIwIpg-_Video_by_aangelazunigaa/DdrBPIwIpg-.mp4',
        'title': '[Phân Tích] @aangelazunigaa - BTS 10 Clips (DdrBPIwIpg-)',
        'reports': [
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@Angela_DdrBPIwIpg-_Video_by_aangelazunigaa.html',
            '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@aangelazunigaa_DdrBPIwIpg-_BTS_from_Day_56_of_Capturing_10_Clips_Until_I.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@Angela_DdrBPIwIpg-_Video_by_aangelazunigaa.html',
            '/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@aangelazunigaa_DdrBPIwIpg-_BTS_from_Day_56_of_Capturing_10_Clips_Until_I.html',
        ]
    }
]

def main():
    log(f"Bắt đầu xử lý {len(TASKS)} video...")
    success_count = 0
    failed_count = 0

    for i, task in enumerate(TASKS, 1):
        sc = task['shortcode']
        vid_file = task['video_file']
        title = task['title']
        desc = f"Video phân tích & bóc tách storyboard tự động.\nShortcode: {sc}"
        
        log(f"\n[{i}/{len(TASKS)}] Đang xử lý: {sc}...")
        if not os.path.exists(vid_file):
            log(f"  ❌ Không tìm thấy file video local: {vid_file}")
            failed_count += 1
            continue

        vid_id, tag = upload_video(vid_file, title, desc)
        if not vid_id:
            log(f"  ❌ Không thể upload {sc}: Tất cả các token YouTube trong Pool đều đã chạm hạn mức/quota hôm nay!")
            failed_count += 1
            break  # If all tokens in pool failed, stop

        success_count += 1
        # Update reports
        for rep in task['reports']:
            update_html_report(rep, vid_id)
            
        update_master_classifications(sc, vid_id)
        
        # Delete from R2
        delete_from_r2(f"{sc}.mp4")
        if 'extra_r2_deletions' in task:
            for extra in task['extra_r2_deletions']:
                delete_from_r2(extra)

        log(f"  🎉 Hoàn thành video {sc} (ID: {vid_id})!")
        time.sleep(1)

    log(f"\n==========================================")
    log(f"KẾT QUẢ: Thành công: {success_count} | Thất bại/Chờ: {failed_count}")
    log(f"==========================================")

if __name__ == '__main__':
    main()
