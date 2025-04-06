import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="7e96667b625548f88b3ae7ea6fb13481",
    client_secret="55583bca92a842b9b9bb79200a1f9f04",
    redirect_uri="http://localhost:8080",
    scope="user-read-playback-state",
    open_browser=False
))

devices = sp.devices()

if devices['devices']:
    print("\n🎧 Available Spotify Devices:\n")
    for device in devices['devices']:
        print(f"🟢 {device['name']} (Type: {device['type']})")
        print(f"    ID: {device['id']}")
        print(f"    Active: {device['is_active']}")
        print(f"    Volume: {device['volume_percent']}%\n")
else:
    print("❌ No devices found. Make sure Spotify is open on your phone or computer and logged into the same account.")

