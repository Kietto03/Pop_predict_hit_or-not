import os
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ---------------------------- CONFIG ----------------------------
SPOTIFY_CLIENT_ID = "35efb7bc89cb411693d023536f82ecdc"
SPOTIFY_CLIENT_SECRET = "9902d3b088594d16bf3c281340c50a54"

folders = {
    "Trendy": [
        "https://www.youtube.com/playlist?list=PLeqTkIUlrZXk5eNKqIGK5M2RIpa6hmXQZ",
        "https://open.spotify.com/playlist/34NbomaTu7YuOYnky8nLXL?si=a6b45c36c21d4bb8"
    ],
    "Mid": [
        "https://music.youtube.com/playlist?list=PLiQI_et-bZcfwJyek3Zev4MZZ3-GyQ7oQ",
        "https://open.spotify.com/playlist/2ue0e4tzF3nZ0slH7uWQmr?si=33a37c93da75408d",
        "https://open.spotify.com/playlist/56wO2plyv8BFjODdAnBbdB?si=56617b0244d3492b"
    ],
    "Flop": [
        "https://music.youtube.com/watch?v=C5T9tDubYRQ&list=PLXYC_akHsObFQx5Fnb9xfM3YUEofc_AcK",
        "https://open.spotify.com/playlist/1tcckJyZvsGJ51kThIqfV2?si=2a71df622dae4761"
    ]
}

# ------------------------ SETUP & HELPERS ------------------------
def create_folders():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def download_youtube_audio(link, folder):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{folder}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav'
            }],
            'quiet': True,
            'nooverwrites': True,
            'noplaylist': False,
            'ignoreerrors': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except Exception as e:
        print(f"    [Error] Skipping due to error: {e}")

def search_and_download_from_youtube(song_name, folder):
    # Skip if file already exists (approx match)
    base_name = song_name.replace('/', '').replace('\\', '')[:60]  # limit name length
    if any(base_name.lower() in file.lower() for file in os.listdir(folder)):
        print(f"    [Skip] Already exists: {song_name}")
        return
    search_query = f"ytsearch1:{song_name} official audio"
    download_youtube_audio(search_query, folder)

def get_spotify_tracks(playlist_url):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))
        playlist_id = playlist_url.split("playlist/")[-1].split("?")[0]
        results = sp.playlist_tracks(playlist_id)
        track_names = []
        for item in results['items']:
            track = item['track']
            if track:
                name = track['name']
                artists = ", ".join([a['name'] for a in track['artists']])
                track_names.append(f"{name} by {artists}")
        return track_names
    except Exception as e:
        print(f"    [Error] Failed to fetch Spotify playlist: {e}")
        return []

# -------------------------- MAIN FLOW ---------------------------
def main():
    create_folders()
    
    for folder, links in folders.items():
        print(f"\nProcessing folder: {folder}")
        for link in links:
            if 'youtube.com' in link or 'youtu.be' in link:
                print(f"  → Downloading from YouTube: {link}")
                download_youtube_audio(link, folder)
            elif 'spotify.com' in link:
                print(f"  → Fetching Spotify playlist: {link}")
                track_names = get_spotify_tracks(link)
                for track in track_names:
                    print(f"    → Downloading: {track}")
                    try:
                        search_and_download_from_youtube(track, folder)
                    except Exception as e:
                        print(f"    [Error] Skipping {track}: {e}")

if __name__ == "__main__":
    main()