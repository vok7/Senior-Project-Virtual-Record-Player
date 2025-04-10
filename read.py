#!/usr/bin/env python3
import sys
import signal
import RPi.GPIO as GPIO
from time import sleep

import spotipy
from spotipy.oauth2 import SpotifyOAuth

ACCESS_TOKEN = "ACCESS_TOKEN"
DEVICE_ID = "DEVICE_ID"

#Spotify Client
sp = spotipy.Spotify(auth=ACCESS_TOKEN)

#MFRC522
sys.path.append("./mfrc522")
import MFRC522

continue_reading = True
MIFAREReader = MFRC522.MFRC522()
last_card_status = False

#Signal 
def end_read(signal, frame):
    global continue_reading
    print("\n🛑 Stopped by user.")
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)

#Play Media
def play_media_for_card(card_id):
    """If a specific RFID card is detected, play the corresponding track."""
    if card_id == '115,117,158,34,186':
        media_uri = 'spotify:track:2X485T9Z5Ly0xyaghN73ed'
        try:
            sp.start_playback(device_id=DEVICE_ID, uris=[media_uri])
            print(f"🎶 Now playing: {media_uri}")
        except Exception as e:
            print(f"⚠️ Error playing media: {e}")

#Main Loop
def main():
    global last_card_status
    print("📡 Waiting for you to scan an RFID sticker/card...")
    while continue_reading:
        status, TagType = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            print("✅ Card detected!")
            status, uid = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                card_id = ','.join(map(str, uid))
                print(f"✅ Card UID: {card_id}")
                play_media_for_card(card_id)
                last_card_status = True
        else:
            if last_card_status:
                print("🔍 No card detected. Try again.")
            last_card_status = False
        sleep(0.5)

if __name__ == "__main__":
    main()


