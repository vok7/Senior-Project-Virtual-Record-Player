#!/usr/bin/env python3
import sys
import signal
import subprocess
from time import sleep

# Import GPIO and MFRC522
import RPi.GPIO as GPIO
sys.path.append("./mfrc522")  # Ensure the MFRC522 module is in your path
import MFRC522

# Import Spotipy for Spotify control
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- Configuration ---
# Replace these with your actual values
ACCESS_TOKEN = "BQBTF9HnArLfj8JP_prKlfuDDE4RtEhNZ4urSjWmNHAt3Hir9Y3dxRvV2HWVqUo1C6x9izVpaqHhLe6fuXo1S43LIwIYfP9sVPccyzrUijGGf2QwbDNj9M_K8YgqoqsEki6bN4L2emDfGICgsBzqxhWxcuLKRqKIRH6Xe-xPYVWvUCcAmXQGueiZMatCzq_BvRPl1o0Dk4ufl5_sbjmRBbgk1NPG"
DEVICE_ID = "d60f59d15c191935fdf1380f83c608305940281c"

# --- Initialize Spotify Client ---
sp = spotipy.Spotify(auth=ACCESS_TOKEN)

# --- RFID to Spotify Mapping ---
RFID_TO_SPOTIFY = {
    '115,117,158,34,186': {
        'track_uri': 'spotify:track:2X485T9Z5Ly0xyaghN73ed'
    },
    # Add additional RFID-to-track mappings here
}

# --- Initialize MFRC522 (RFID Reader) ---
continue_reading = True
MIFAREReader = MFRC522.MFRC522()

# --- Signal Handler for Cleanup ---
def end_read(signal, frame):
    global continue_reading
    print("\n🛑 Stopped by user.")
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)

# --- Function to Play Media on Spotify ---
def play_media(media_uri):
    """Starts playback of the given Spotify track URI on the specified device."""
    try:
        sp.start_playback(device_id=DEVICE_ID, uris=[media_uri])
        print(f"🎶 Now playing: {media_uri}")
    except Exception as e:
        print(f"⚠️ Error playing media: {e}")

# --- Main Loop ---
def main():
    print("📡 Waiting for you to scan an RFID sticker/card...")
    last_card_status = False  # Track if a card was detected last time
    while continue_reading:
        status, TagType = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            print("✅ Card detected!")
            status, uid = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                card_id = ','.join(map(str, uid))
                print(f"✅ Card UID: {card_id}")
                if card_id in RFID_TO_SPOTIFY:
                    track_info = RFID_TO_SPOTIFY[card_id]
                    if 'track_uri' in track_info:
                        print(f"🎶 Playing track: {track_info['track_uri']}")
                        play_media(track_info['track_uri'])
                    sleep(2)  # Delay to prevent rapid re-triggering
                    last_card_status = True
                else:
                    print("❌ Card not recognized. Update your mapping.")
                    last_card_status = True
        else:
            if last_card_status:
                print("🔍 No card detected. Try again.")
                last_card_status = False
        sleep(0.5)

if __name__ == "__main__":
    main()

