from #!/usr/bin/env python3
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
ACCESS_TOKEN = "BQAkXwBq71nOC789Qs9CKAYJmWAZ3vrivMXliMAYljG0fa-e2jcHnvKLgtREnNSG7-sD6ysFxxs4c3Jhz_Ifme9QIXJM2N3LjEv4LVP3tg8KQO1k4XeEhvLmE-QZ4QgntzCd61E7OPxiNtel_yTWPsulTGEFg4cctzfo1tj-bEey2UJvOfiVDH94bB63RSCwtkW20LuRbS_256ICFIBwsiQ2KZIl"
DEVICE_ID = "d60f59d15c191935fdf1380f83c608305940281c"

# --- Initialize Spotify Client ---
sp = spotipy.Spotify(auth=ACCESS_TOKEN)

# --- RFID to Spotify Mapping ---
RFID_TO_SPOTIFY = {
    '115,117,158,34,186': {
        'track_uri': 'spotify:track:2X485T9Z5Ly0xyaghN73ed'
    },
    '211,99,123,49,250': {
        'track_uri': 'spotify:track:5hmv0zcBcIX8OIVG98imHa'
    },
    '211,237,26,50,22': {
        'track_uri': 'spotify:track:2KnMG7ROpc76hMKobBiocK'
    },
    '162,71,184,3,94': {
        'playlist_uri': 'spotify:playlist:1OO2Fp9PsnaayiekeXuGJX'
    },
    '203,81,184,3,33': {
        'track_uri': 'spotify:track:6vuPZX9fWESg5js2JFTQRJ'
    },
    '185,28,185,3,31': {
        'track_uri': 'spotify:track:5TRPicyLGbAF2LGBFbHGvO'
    }
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
    main()  can i add a feature which allows user to play a playlist and album
