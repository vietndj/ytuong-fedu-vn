import os
import sys
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

def get_authenticated_service():
    credentials_path = '/Users/vietmac/Documents/CODE/videoOffline/token.pickle'
    creds = None
    if os.path.exists(credentials_path):
        with open(credentials_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(credentials_path, 'wb') as token:
                pickle.dump(creds, token)
        else:
            print("ERROR_AUTH", file=sys.stderr)
            sys.exit(1)
    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, file_path, title):
    body = {
        'snippet': {
            'title': title,
            'description': 'Uploaded via script'
        },
        'status': {
            'privacyStatus': 'unlisted'
        }
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}...", file=sys.stderr)
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            if 'quotaExceeded' in str(e):
                print("ERROR_QUOTA", file=sys.stderr)
            sys.exit(1)
            
    print(response.get('id'))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python upload_yt.py <file_path> <title>", file=sys.stderr)
        sys.exit(1)
    youtube = get_authenticated_service()
    upload_video(youtube, sys.argv[1], sys.argv[2])
