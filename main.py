from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import pickle
import os
import time

# ---- CONFIG ----
CLIENT_SECRETS_FILE = "client_secret.json"  # downloaded from Google Cloud Console
SCOPES = ["https://www.googleapis.com/auth/youtube"]
PLAYLIST_TITLE = "My New Playlist"
PLAYLIST_DESCRIPTION = "Created with Python script"
LAST_ADDED_FILE = "last_added.txt"

# Load songs
with open("cleaned_list.txt", "r", encoding="utf-8") as f:
    SONG_LIST = [line.strip() for line in f if line.strip()]

# Resume logic: check last added song
if os.path.exists(LAST_ADDED_FILE):
    with open(LAST_ADDED_FILE, "r", encoding="utf-8") as f:
        last_added_name = f.read().strip()
    if last_added_name in SONG_LIST:
        start_index = SONG_LIST.index(last_added_name) + 1
    else:
        start_index = 0
else:
    start_index = 0

# Authenticate & build service
def get_youtube_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

# Get existing playlist or create new
def get_or_create_playlist(youtube, title, description):
    request = youtube.playlists().list(
        part="snippet",
        mine=True,
        maxResults=50
    )
    response = request.execute()
    for item in response.get("items", []):
        if item["snippet"]["title"] == title:
            print(f"✅ Found existing playlist: '{title}'")
            return item["id"]

    # Create new playlist if not found
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description},
            "status": {"privacyStatus": "public"}
        }
    )
    response = request.execute()
    print(f"✅ Created new playlist: '{title}'")
    return response["id"]

# Search for a video and return videoId
def search_video(youtube, query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=1
    )
    response = request.execute()
    items = response.get("items", [])
    if items:
        return items[0]["id"]["videoId"]
    return None

# Add video to playlist
def add_video_to_playlist(youtube, playlist_id, video_id):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id}
            }
        }
    ).execute()

if __name__ == "__main__":
    youtube = get_youtube_service()
    playlist_id = get_or_create_playlist(youtube, PLAYLIST_TITLE, PLAYLIST_DESCRIPTION)

    last_added_song = None
    for idx in range(start_index, len(SONG_LIST)):
        song = SONG_LIST[idx]
        try:
            video_id = search_video(youtube, song)
            if video_id:
                add_video_to_playlist(youtube, playlist_id, video_id)
                print(f"Added: {song}")
                last_added_song = song
                with open(LAST_ADDED_FILE, "w", encoding="utf-8") as f:
                    f.write(song)
            else:
                print(f"❌ Not found: {song}")

            # Delay to avoid hitting quota too fast
            time.sleep(1)

        except HttpError as e:
            if "quotaExceeded" in str(e):
                print("🚨 Quota exceeded. Stopping script. Try again tomorrow.")
                break
            else:
                raise

    if last_added_song is not None:
        print(f"✅ Last successfully added song: '{last_added_song}' (line {SONG_LIST.index(last_added_song) + 1})")
    else:
        print("No songs were added this run.")
