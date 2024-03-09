import os
from dotenv import load_dotenv
from djitellopy import Tello

# Load variables from .env file
load_dotenv()

WIFI_SSID = os.getenv("WIFI_SSID")
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD")

# Assert that the values are present and not empty
assert (
    WIFI_SSID is not None and WIFI_SSID != ""
), "WIFI_SSID is missing or empty in .env file"
assert (
    WIFI_PASSWORD is not None and WIFI_PASSWORD != ""
), "WIFI_PASSWORD is missing or empty in .env file"

# Create a Tello instance
tello = Tello()

# Connect to Tello
tello.connect()

# Connect to Wi-Fi
tello.connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)
