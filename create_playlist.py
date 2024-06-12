import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()
# Nếu bạn đã có token, hãy tải nó
# Nếu chưa có, bạn sẽ phải xác thực lại và lưu token
SCOPES = [os.getenv('SCOPES')]
CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRETS_FILE')
VIDEO_IDS_FILE = os.getenv('VIDEO_IDS_FILE')  # File chứa các ID video

def get_authenticated_service():
    creds = None
    # File token.json lưu trữ token của người dùng
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Nếu chưa có token hoặc token đã hết hạn
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Lưu token để lần sau không phải xác thực lại
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('youtube', 'v3', credentials=creds)

def create_playlist(service, title, description):
    request = service.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    response = request.execute()
    print(f"Playlist created: {response['id']}")
    return response['id']

def update_playlist(service, playlist_id, new_title=None, new_description=None):
    # Lấy thông tin hiện tại của playlist
    request = service.playlists().list(
        part="snippet",
        id=playlist_id
    )
    response = request.execute()
    
    # Cập nhật thông tin
    snippet = response['items'][0]['snippet']
    if new_title:
        snippet['title'] = new_title
    if new_description:
        snippet['description'] = new_description
    
    request = service.playlists().update(
        part="snippet",
        body={
            "id": playlist_id,
            "snippet": snippet
        }
    )
    response = request.execute()
    print(f"Playlist updated: {response['id']}")
    return response['id']

def add_video_to_playlist(service, playlist_id, video_id):
    request = service.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    print(f"Added video to playlist: {response['id']}")

def read_video_ids_from_file(file_path):
    with open(file_path, 'r') as file:
        video_ids = file.read().splitlines()
    return video_ids

if __name__ == "__main__":
    service = get_authenticated_service()
    playlist_id = create_playlist(service, "My New Playlist", "This is a test playlist created by API")
    video_ids = read_video_ids_from_file(VIDEO_IDS_FILE)
    
    for video_id in video_ids:
        add_video_to_playlist(service, playlist_id, video_id)
    
    print(f"Created playlist with ID: {playlist_id} and added videos from {VIDEO_IDS_FILE}")
    
    # Cập nhật tên và mô tả của playlist
    updated_playlist_id = update_playlist(service, playlist_id, new_title="Updated Playlist Title", new_description="Updated description for the playlist")
    print(f"Updated playlist with ID: {updated_playlist_id}")
