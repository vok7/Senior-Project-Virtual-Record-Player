 #!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Spotify Credentials
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8080"
SCOPE = "user-read-playback-state"

#Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE))

#Display Avaliable Devices
devices = sp.devices()
if devices['devices']:
    for device in devices['devices']:
        print(f"Device Name: {device['name']}, Device ID: {device['id']}")
else:
    print("No devices found.")
