# Seinor Project Virtual Record Player

## Project Overview
Our Virtual Record Player is a Raspberry Pi-based system that simulates the experience of playing a vinyl record using RFID tags. Each RFID tag is mapped to a specific Spotify playlist track, or albumn. Users can place a tag on the reader simulates dropping the needle on a record. This project merges physical interaction with digital music, creating a unique and nostalgic user experience.

This project was built using Python and integrates with the Spotify API using the [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/) library.

---
## File Hierarchy
| Path                          | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `Dockerfile`                  | Docker configuration to contain project                                    |
| `MFRC522.py`                  | Base class for MFRC522 RFID reader                                         |
| `MFRC522_gpiod.py`            | MFRC522 implementation using `gpiod` for GPIO control                      |
| `MFRC522_gpiozero.py`         | MFRC522 implementation using `gpiozero` library                            |
| `README.md`                   | Project documentation                                                      |
| `device.py`                   | Hardware device interface                                                  |
| `player-test.py`              | Main script controls Spotify playback using scanned tags                   |
| `read.py`                     | Test script to read and display scanned RFID tag IDs                       |
| `spotify_auth.py`             | Spotify authorization and token management logic                           |
| `config.py`                   | Contains Spotify API credentials                                           |
---

## Setup and Run Instructions

### Requirements
- Raspberry Pi (Recommend 4)
- Python 3.9+
- Internet connection
- RFID Reader (RC522)
- RFID Tags
- Spotify Premium account
- [Spotify Developer App](https://developer.spotify.com/dashboard/) 


### Installation
### 1. Clone the Repository
```bash
git clone https://github.com/vok7/Senior-Project-Virtual-Record-Player.git
cd Senior-Project-Virtual-Record-Player
```
### 2.Update/Upgrade/Install Python Dependies in Raspi
```bash
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
```
### 3. Install System Libraries (GPIO & SPI Libraries)
```bash
sudo apt install python3-rpi.gpio python3-spidev python3-dev python3-gpiozero python3-libgpiod
```
### 4. Enable SPI on Pi
```bash
sudo raspi-config
```
Select Interface Options
Enable SPI
Exit and Reboot Pi
```bash
sudo reboot
```
## Use Record Player
### 1. Hardware Setup
Connect your RC522 RFID reader to the Raspberry Pi GPIO pins.

### 2. Configure Spotify
Create a Spotify Developer App: https://developer.spotify.com/dashboard/
In config.py or spotify_auth.py, enter your credentials:
```python
CLIENT_ID = "your_spotify_client_id"
CLIENT_SECRET = "your_spotify_client_secret"
REDIRECT_URI = "http://localhost:8888/callback"
```
On the first run, a browser will open to authenticate your account.

### 3. Register RFID Tags
Run the RFID tag scanner:
```bash
python3 read.py
```
Scan a tag. Copy the UID printed to the terminal.
Add it to tag_mapping.json:
```json
{
  "1234567890": "spotify:track:4cOdK2wGLETKBW3PvgPWqT",
  "0987654321": "spotify:playlist:3ZgmfR6lsnCwdffZUan8EA"
}
```
### 4. Start the Virtual Record Player
```bash
python3 player.py
```
Scan a tag to play music from Spotify.

Change tags to play different tracks or playlists.

###How to Exit the Program
To stop any script (like read.py or player.py), press:
```bash
Ctrl + C
