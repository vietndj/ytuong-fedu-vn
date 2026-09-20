import os
import pickle
import sys
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

def get_authenticated_service():
    token_path = '/Users/vietmac/Documents/CODE/videoOffline/token.pickle'
    if not os.path.exists(token_path):
        token_path = '/Users/vietmac/.config/youtube_full_token.pickle'
        
    if not os.path.exists(token_path):
        print("Không tìm thấy token.")
        sys.exit(1)
        
    with open(token_path, 'rb') as token:
        credentials = pickle.load(token)
        
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        
    return build('youtube', 'v3', credentials=credentials)

def upload_video(youtube, file_path):
    body = {
        'snippet': {
            'title': os.path.basename(file_path).replace('.mp4', ''),
            'description': 'Test upload để kiểm tra bản quyền.',
            'tags': ['test', 'copyright'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'private' # ĐỂ TRẠNG THÁI RIÊNG TƯ
        }
    }

    print(f"Uploading {file_path}...")
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if status:
            print(f"Đã tải lên {int(status.progress() * 100)}%")

    print(f"Hoàn thành! Video ID: {response['id']}")

if __name__ == '__main__':
    videos = [
        'dist/videos/LAZADA_Ulanzi_Đèn_LED_Thanh_Bơm_Hơi_UA20,_.mp4',
        'dist/videos/4 Cu May Sieu Thi Bang Gia Do Ulanzi MA38 MT85 - @hena_film_vlog.mp4',
        'dist/videos/Teaching_Nervous_System_Not_Emergency_-_@kawoon.lee.mp4',
        'dist/videos/LAZADA_Ulanzi_Chân_Đế_Tự_Sướng_Có_Từ_Tính_.mp4'
    ]
    yt = get_authenticated_service()
    for v in videos:
        if os.path.exists(v):
            upload_video(yt, v)
        else:
            print(f"Không tìm thấy: {v}")
