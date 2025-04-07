#!/usr/bin/env python3
import sys
import signal
import subprocess
from time import sleep

# Replace RPi.GPIO with gpiozero for general GPIO handling (if needed in future)
from gpiozero import Device
from gpiozero.pins.native import NativeFactory
Device.pin_factory = NativeFactory()

sys.path.append("./mfrc522")  # Ensure the MFRC522 module is in your path
import MFRC522

# Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- Configuration ---
ACCESS_TOKEN = "your_access_token_here"
DEVICE_ID = "your_device_id_here"

# --- Spotify Client ---
sp = spotipy.Spotify(auth=ACCESS_TOKEN)

# --- RFID to Spotify Mapping ---
RFID_TO_SPOTIFY = {
    '115,117,158,34,186': {'track_uri': 'spotify:track:2X485T9Z5Ly0xyaghN73ed'},
    '211,99,123,49,250': {'track_uri': 'spotify:track:5hmv0zcBcIX8OIVG98imHa'},
    '211,237,26,50,22': {'track_uri': 'spotify:track:2KnMG7ROpc76hMKobBiocK'},
    '162,71,184,3,94': {'playlist_uri': 'spotify:playlist:1OO2Fp9PsnaayiekeXuGJX'},
    '203,81,184,3,33': {'track_uri': 'spotify:track:6vuPZX9fWESg5js2JFTQRJ'},
    '185,28,185,3,31': {'track_uri': 'spotify:track:5TRPicyLGbAF2LGBFbHGvO'}
}

# --- RFID Reader ---
continue_reading = True
MIFAREReader = MFRC522.MFRC522()

# --- Signal Handler ---
def end_read(signal, frame):
    global continue_reading
    print("\nStopped by user.")
    continue_reading = False
    Device.close()  # Cleanup GPIO safely using gpiozero

signal.signal(signal.SIGINT, end_read)

# --- Spotify Playback ---
def play_media(media_uri):
    try:
        sp.start_playback(device_id=DEVICE_ID, uris=[media_uri])
        print(f"Now playing: {media_uri}")
    except Exception as e:
        print(f"Error playing media: {e}")

# --- Main Loop ---
def main():
    print("Waiting for RFID scan...")
    last_card_status = False
    while continue_reading:
        status, TagType = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            print("Card detected!")
            status, uid = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                card_id = ','.join(map(str, uid))
                print(f"Card UID: {card_id}")
                if card_id in RFID_TO_SPOTIFY:
                    track_info = RFID_TO_SPOTIFY[card_id]
                    if 'track_uri' in track_info:
                        print(f"Playing track: {track_info['track_uri']}")
                        play_media(track_info['track_uri'])
                    elif 'playlist_uri' in track_info:
                        print(f"Playing playlist: {track_info['playlist_uri']}")
                        sp.start_playback(device_id=DEVICE_ID, context_uri=track_info['playlist_uri'])
                    sleep(2)
                    last_card_status = True
                else:
                    print("Unrecognized card.")
                    last_card_status = True
        else:
            if last_card_status:
                print("No card detected.")
                last_card_status = False
        sleep(0.5)

if __name__ == "__main__":
    main()

