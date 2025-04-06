#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

# === Spotify Configuration ===
DEVICE_ID = "2b9f3e49e0f14a2a9c3cb26b67b344a3"
CLIENT_ID = "7e96667b625548f88b3ae7ea6fb13481"
CLIENT_SECRET = "55583bca92a842b9b9bb79200a1f9f04"
REDIRECT_URI = "http://localhost:8080"

# === RFID to Spotify Map ===
RFID_TO_SPOTIFY = {
    'RFID-CARDVALUE-1': {
        'uris': ['spotify:track:2vSLxBSZoK0eha4AuhZlXV']
    },
    'RFID-CARDVALUE-2': {
        'context_uri': 'spotify:album:0JGOiO34nwfUdDrD612dOp'
    },
    # Add more RFID mappings here
}

def setup_spotify():
    """Sets up Spotify authentication."""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-read-playback-state user-modify-playback-state",
        open_browser=False
    ))

def play_media(sp, device_id, media):
    """Play a track or album using Spotify API."""
    if 'uris' in media:
        sp.start_playback(device_id=device_id, uris=media['uris'])
    elif 'context_uri' in media:
        sp.start_playback(device_id=device_id, context_uri=media['context_uri'])
    else:
        print("⚠️ No valid media type found for this card.")

def main():
    reader = SimpleMFRC522()
    sp = setup_spotify()

    try:
        while True:
            print("📡 Waiting for record scan...")
            card_id = str(reader.read()[0])
            print(f"✅ Card scanned: {card_id}")

            if card_id in RFID_TO_SPOTIFY:
                print(f"🎶 Playing content for: {card_id}")
                sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                play_media(sp, DEVICE_ID, RFID_TO_SPOTIFY[card_id])
                sleep(2)
            else:
                print("❌ Unrecognized card.")

    except Exception as e:
        print(f"💥 Error: {e}")

    finally:
        print("🔌 Cleaning up GPIO...")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
