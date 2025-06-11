import time
import requests
import geocoder
import uuid

API_TOKEN = "supersecrettoken123"
SERVER_URL = "http://127.0.0.1:5000/update_location"

# Generate a pseudo-IMEI (or use any other unique identifier)
DEVICE_ID = str(uuid.uuid4())

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_current_location():
    g = geocoder.ip('me')
    if g.ok:
        return g.latlng  # [lat, lon]
    else:
        print("Failed to get location")
        return None, None

def send_location(lat, lon):
    payload = {
        "imei": DEVICE_ID,
        "latitude": lat,
        "longitude": lon
    }
    try:
        response = requests.post(SERVER_URL, json=payload, headers=headers)
        print(f"Sent location: {lat}, {lon} => {response.status_code}")
    except Exception as e:
        print(f"Error sending location: {e}")

# Send real-time location every 5 seconds
while True:
    latitude, longitude = get_current_location()
    if latitude is not None and longitude is not None:
        send_location(latitude, longitude)
    time.sleep(5)
