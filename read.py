#!/usr/bin/env python3

import sys
import RPi.GPIO as GPIO
import signal
from time import sleep

# Add the path to the MFRC522 module (if it's in the 'mfrc522' directory)
sys.path.append("./mfrc522")
import MFRC522

continue_reading = True
MIFAREReader = MFRC522.MFRC522()

# Initialize last_card_status outside the main function
last_card_status = False

# Handle Ctrl+C gracefully to stop reading
def end_read(signal, frame):
    global continue_reading
    print("\n🛑 Stopped by user.")
    continue_reading = False
    GPIO.cleanup()

# Capture SIGINT for cleanup
signal.signal(signal.SIGINT, end_read)

def main():
    global last_card_status  # Use the global variable inside the function

    print("📡 Waiting for you to scan an RFID sticker/card...")

    while continue_reading:
        # Scan for RFID cards
        status, TagType = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is detected, proceed to read the UID
        if status == MIFAREReader.MI_OK:
            print("✅ Card detected!")

            # Get the UID of the card
            status, uid = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                card_id = ','.join(map(str, uid))  # Format UID as a string
                print(f"✅ Card detected! UID: {card_id}")
                last_card_status = True  # Update card detection status
        else:
            # Only print the "No card detected" message if the last status was not "No card detected"
            if last_card_status:
                print("🔍 No card detected. Try again.")
            last_card_status = False

        # Sleep for a short period to prevent spamming
        sleep(0.5)

if __name__ == "__main__":
    main()

