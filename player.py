#!/usr/bin/env python3

import sys
import RPi.GPIO as GPIO
import signal
from time import sleep
import subprocess

# === RFID to Spotify Map ===
RFID_TO_SPOTIFY = {
    '115,117,158,34,186': {
        'track_uri': 'spotify:track:2X485T9Z5Ly0xyaghN73ed'
    },
    # You can add more cards and mappings here as needed
}

# === RFID Reader Setup ===
sys.path.append("./mfrc522")  # Ensure the MFRC522 module is included
import MFRC522

continue_reading = True
MIFAREReader = MFRC522.MFRC522()

# Handle Ctrl+C gracefully to stop reading
def end_read(signal, frame):
    global continue_reading
    print("\n🛑 Stopped by user.")
    continue_reading = False
    GPIO.cleanup()

# Capture SIGINT for cleanup
signal.signal(signal.SIGINT, end_read)

# Function to play media using Raspotify (Spotify Connect)
def play_media(media_uri):
    """Plays track using Raspotify."""
    # Construct the command to play using Spotify Connect (via Raspotify)
    # Use the `dbus` method to control Spotify Connect since we are using Raspotify
    command = f"dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause"
    try:
        # Execute the command to play the selected media via Raspotify
        subprocess.run(command, shell=True, check=True)
        print(f"🎶 Now playing: {media_uri}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error playing media: {e}")

def main():
    """Main function to read RFID and trigger Raspotify actions."""
    print("📡 Waiting for you to scan an RFID sticker/card...")
    
    last_card_status = False  # To track if the card status changed
    while continue_reading:
        # Scan for RFID cards
        status, TagType = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print("✅ Card detected!")

            # Get the UID of the card
            status, uid = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                card_id = ','.join(map(str, uid))  # Format UID as a string
                print(f"✅ Card detected! UID: {card_id}")

                # If the card ID is in the dictionary, play the media
                if card_id in RFID_TO_SPOTIFY:
                    media = RFID_TO_SPOTIFY[card_id]
                    if 'track_uri' in media:
                        print(f"🎶 Playing track: {media['track_uri']}")
                        play_media(media['track_uri'])
                    sleep(2)  # Short delay before next scan
                    last_card_status = True  # Card is now detected
                else:
                    print("❌ Card not recognized. Try again or update your dictionary.")
                    last_card_status = True
        else:
            # Only print the "No card detected" message if the last status was a detected card
            if last_card_status:
                print("🔍 No card detected. Try again.")
                last_card_status = False  # Reset status
        # Sleep to reduce spamming
        sleep(0.5)

if __name__ == "__main__":
    main()

