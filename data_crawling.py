import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ---------------------------- CONFIG ----------------------------
SPOTIFY_CLIENT_ID = "35efb7bc89cb411693d023536f82ecdc"
SPOTIFY_CLIENT_SECRET = "9902d3b088594d16bf3c281340c50a54"

folders = {
    "Trendy": [  # 🔥 Lot of Trendy Popularity (Highly Popular Genres)
        "https://open.spotify.com/playlist/4yNfFAuHcSgzbcSm6q5QDu?si=b0bdc74fa3c44d40"
    ],
    "Mid": [  # ⚖️ Moderate Amount of Popularity (Niche but Strong Genres)
        "https://open.spotify.com/playlist/37i9dQZF1EIefLxrHQP8p4?si=cfc50d58cd664460",  # Rock
        "https://open.spotify.com/playlist/2obrIajjdAn8043mICYF3L?si=55445e7e325f4688",  # Country
        "https://open.spotify.com/playlist/37i9dQZF1DXchlyaSeZp0q?si=ac268768a28544a9",   # Soul
        "https://open.spotify.com/playlist/3AGYHZ3tqmPv3Nek1dRv1g?si=1eef3a51f24542ed"    # Jazz
    ],
    "Flop": [  # 🧊 Very Least Amount of Popularity (Low Streaming / Niche Appeal Genres)
        "https://open.spotify.com/playlist/1jdYkR6P4UP6etoDImX5fB?si=70c3db0bb88944c4",
        "https://open.spotify.com/playlist/37i9dQZF1EIdcKjz0pIYET?si=f3849ad2319f46b7",
        "https://open.spotify.com/playlist/3J1NtZPnwBlxbhCvObxTgX?si=cc59cff8a3704c8d",
        "https://open.spotify.com/playlist/6zfOVd4uZHkLjenFDnfW21?si=70762c29f06c42ba",
        "https://open.spotify.com/playlist/37i9dQZF1DX9GxQjEBVviW?si=dc0193f2c7574946"
    ]
}

# ------------------------ SETUP & HELPERS ------------------------
def create_folders():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

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
            print(f"  → Fetching Spotify playlist: {link}")
            track_names = get_spotify_tracks(link)
            for track in track_names:
                print(f"    → Found: {track}")

if __name__ == "__main__":
    main()
