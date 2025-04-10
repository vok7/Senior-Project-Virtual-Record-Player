#!/usr/bin/env python3
from gpiozero import OutputDevice
from signal import signal, SIGINT
from time import sleep
import spotipy
import MFRC522_gpiozero as MFRC522  

#Configuration
ACCESS_TOKEN = "ACCESS_TOKEN"
DEVICE_ID = "DEVICE_ID"

#Initialize Spotify Client
sp = spotipy.Spotify(auth=ACCESS_TOKEN)

#RFID to Spotify Mapping
RFID_TO_SPOTIFY = {
    #Tracks
    '211,237,26,50,22': {'track_uri': 'spotify:track:2KnMG7ROpc76hMKobBiocK'},
    '115,117,158,34,186': {'track_uri': 'spotify:track:2X485T9Z5Ly0xyaghN73ed'},
    '211,99,123,49,250': {'track_uri': 'spotify:track:5hmv0zcBcIX8OIVG98imHa'},

    #Playlists
    '185,28,185,3,31': {'playlist_uri': 'spotify:playlist:0qu2tGOCixqaV6V0Aym72x'},
    '203,81,184,3,33': {'playlist_uri': 'spotify:playlist:7KPmjjagSk6VUzVlWDjWTJ'},
    '162,71,184,3,94': {'playlist_uri': 'spotify:playlist:3v8Fm0PyOMRuQ2rehEvgok'},

    #Albums
    '154,124,75,246,91': {'album_uri': 'spotify:album:5tXZfxvr2VaWibD74nw8VL'},  # Earth Wind & Fire
    '42,114,77,246,227': {'album_uri': 'spotify:album:3DGQ1iZ9XKUQxAUWjfC34w'},  # Kendrick Lamar
    '170,49,75,246,38': {'album_uri': 'spotify:album:34LxHI9x14qXUOS8AWRrYD'},   # De La Soul
    '106,36,73,246,241': {'album_uri': 'spotify:album:3ywVzrwMQ3Kq43N9zBdBQm'},  # Funkadelic
    '218,85,73,246,48': {'album_uri': 'spotify:album:7Cw4LObzgnVqSlkuIyywtI'},    # Baby Keem
    '138,69,75,246,114': {'album_uri': 'spotify:album:6rsQnwaoJHxXJRCDBPkBRw'},  # Arctic Monkeys
    '26,244,79,246,87': {'album_uri': 'spotify:album:79dL7FLiJFOO0EoehUHQBv'},   # Tame Impala
    '234,181,77,246,228': {'album_uri': 'spotify:album:6nfJMRoIjyRwk3ZTHNm0PY'}, # Westside Gunn
    '42,169,79,246,58': {'album_uri': 'spotify:album:1hxraaWEf3wFnJxADf8Dge'},   # Panic at the Disco
    '26,134,77,246,39': {'album_uri': 'spotify:album:127CLXCibn1ARC1CGExGav'}    # Rufus
}

# --- Initialize MFRC522 (RFID Reader) ---
continue_reading = True
MIFAREReader = MFRC522.MFRC522()

# --- Signal Handler ---
def end_read(signal, frame):
    global continue_reading
    print("\n🛑 Stopped by user.")
    continue_reading = False
    MIFAREReader.cleanup()

signal(SIGINT, end_read)

# --- Function to Play Media ---
def play_media(media_uri):
    try:
        if "track:" in media_uri:
            sp.start_playback(device_id=DEVICE_ID, uris=[media_uri])
        else:
            sp.start_playback(device_id=DEVICE_ID, context_uri=media_uri)
        print(f"🎶 Now playing: {media_uri}")
    except Exception as e:
        print(f"⚠️ Error playing media: {e}")

# --- Main Loop ---
def main():
    print("📡 Waiting for RFID scan...")
    last_card_status = False
    while continue_reading:
        status, TagType = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            print("✅ Card detected!")
            status, uid = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                card_id = ','.join(map(str, uid))
                print(f"✅ UID: {card_id}")
                track_info = RFID_TO_SPOTIFY.get(card_id)
                if track_info:
                    uri = track_info.get("track_uri") or track_info.get("playlist_uri") or track_info.get("album_uri")
                    if uri:
                        play_media(uri)
                    else:
                        print("⚠️ URI not defined.")
                else:
                    print("❌ Unknown card.")
                sleep(2)
                last_card_status = True
        else:
            if last_card_status:
                print("🔍 No card detected.")
                last_card_status = False
        sleep(0.5)

if __name__ == "__main__":
    main()
