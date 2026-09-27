import os
import pickle
import sys
import subprocess
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

def get_authenticated_service():
    token_path = '/Users/vietmac/Documents/CODE/videoOffline/token.pickle'
    if not os.path.exists(token_path):
        token_path = '/Users/vietmac/.config/youtube_full_token.pickle'
    with open(token_path, 'rb') as token:
        credentials = pickle.load(token)
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    return build('youtube', 'v3', credentials=credentials)

def upload_video(youtube, file_path, index):
    body = {
        'snippet': {
            'title': f'Chibuzor Carousel Slide {index}',
            'description': 'AI Analysis B-Roll Video.',
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'unlisted'
        }
    }
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
    return response['id']

if __name__ == '__main__':
    # Download
    print("Downloading IG...")
    subprocess.run(["yt-dlp", "https://www.instagram.com/p/DdRGMalgl4E/", "-o", "chibuzor_%(autonumber)s.%(ext)s"], check=True)
    
    yt = get_authenticated_service()
    ids = []
    for i in range(1, 8):
        file_path = f"chibuzor_0000{i}.mp4"
        if os.path.exists(file_path):
            print(f"Uploading {file_path}...")
            vid_id = upload_video(yt, file_path, i)
            ids.append(vid_id)
            os.remove(file_path)
    
    print("YT_IDS=" + ",".join(ids))
