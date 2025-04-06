#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

# === Spotify API Credentials ===
DEVICE_ID = "98bb0735e28656bac098d927d410c3138a4b5bca"
CLIENT_ID = "7e96667b625548f88b3ae7ea6fb13481"
CLIENT_SECRET = "55583bca92a842b9b9bb79200a1f9f04"
REDIRECT_URI = "http://localhost:8080"

# === RFID to Spotify Map ===
# Only define one key: 'uris', 'album_uri', or 'playlist_uri' per RFID tag
RFID_TO_SPOTIFY = {
    'RFID-CARDVALUE-1': {
        'uris': ['spotify:track:2vSLxBSZoK0eha4AuhZlXV']
    },
    'RFID-CARDVALUE-2': {
        'album_uri': 'spotify:album:0JGOiO34nwfUdDrD612dOp'
    },
    'RFID-CARDVALUE-3': {
        'playlist_uri': 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'
    }
    # Add more as needed
}

def setup_spotify():
    """Sets up Spotify connection using Spotipy with local token caching."""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-read-playback-state,user-modify-playback-state",
        open_browser=False
    ))

def play_media(sp, device_id, media):
    """Plays track, album, or playlist based on the media dictionary."""
    if 'uris' in media:
        sp.start_playback(device_id=device_id, uris=media['uris'])
    elif 'album_uri' in media:
        sp.start_playback(device_id=device_id, context_uri=media['album_uri'])
    elif 'playlist_uri' in media:
        sp.start_playback(device_id=device_id, context_uri=media['playlist_uri'])
    else:
        print("⚠️ No playable media defined for this card.")

def main():
    reader = SimpleMFRC522()
    sp = setup_spotify()

    try:
        while True:
            print("\n📡 Waiting for record scan...")
            card_id = str(reader.read()[0])
            print(f"✅ Card Scanned: {card_id}")

            if card_id in RFID_TO_SPOTIFY:
                print(f"🎶 Playing media linked to: {card_id}")
                sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                play_media(sp, DEVICE_ID, RFID_TO_SPOTIFY[card_id])
                sleep(2)
            else:
                print("❌ Card not recognized. Try again or update your dictionary.")

    except Exception as e:
        print(f"\n💥 Error occurred: {e}")

    finally:
        print("\n🔌 Cleaning up GPIO...")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
