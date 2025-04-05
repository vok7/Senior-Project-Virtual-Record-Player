#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def main():
    reader = SimpleMFRC522()
    try:
        while True:
            print("\n📡 Waiting for you to scan an RFID sticker/card...")
            card_id = reader.read()[0]
            print(f"✅ Card detected! ID: {card_id}")
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
    finally:
        GPIO.cleanup()
        print("🔌 GPIO cleaned up.")

if __name__ == "__main__":
    main()
