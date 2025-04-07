 #!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your actual Spotify Developer credentials:
CLIENT_ID = "7e96667b625548f88b3ae7ea6fb13481"
CLIENT_SECRET = "285db6e53ebc47998c9d10502d7ff41a"
REDIRECT_URI = "http://localhost:8080"
SCOPE = "user-read-playback-state"

# Initialize the Spotify client with authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE))

# Retrieve and display available devices
devices = sp.devices()
if devices['devices']:
    for device in devices['devices']:
        print(f"Device Name: {device['name']}, Device ID: {device['id']}")
else:
    print("No devices found.")
