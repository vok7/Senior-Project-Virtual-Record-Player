import RPi.GPIO as GPIO
import signal
from time import sleep
import spotipy
import MFRC522

# --- GPIO Setup ---
GPIO.setmode(GPIO.BOARD)  # or GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# --- Configuration ---
ACCESS_TOKEN = "BQBzVwLUTbARK98FVfpodkGfUWPA2Q51_YMz9BFicqqkFwNJrzSRaTIQos9dN-Km7ANLGuUjYDZeaNFt6v_MR5gtWVhK7rfj0Bj4pVGEi-6OoQEdu_ZDuVAyzJHrrP2UthW3mEU401Hp9u-fUDl8HsZQ-RSXgZ5eAhCVavt05KuXekm7EfiN7vbxp-E1AsEvB6wOM0SDEnI2gsk-xt7tKc5zUehD"
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
    main()
