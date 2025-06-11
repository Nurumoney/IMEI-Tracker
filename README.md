# 📍 IMEI Device Tracker (Flask + Android)

A real-time device location tracking system using:
- 🚀 Android app (sends IMEI and GPS data)
- 🌐 Flask backend (REST + WebSocket)
- 🗺️ Web interface to view location updates live

---

## 🔧 How It Works

### 📱 Android App
- Collects the device's IMEI and location.
- Sends location updates via HTTP POST to the Flask server every few seconds.

### 🧠 Flask Backend
- Receives IMEI, latitude, and longitude via `/update_location`.
- Broadcasts real-time location to the web dashboard using **Socket.IO**.
- Renders a live tracking map with device markers.

---

## 🛠 Requirements

- Python 3.8+
- Flask
- Flask-SocketIO
- Eventlet
- Geocoder (for testing)

Install with:
```bash
pip install -r requirements.txt
```

---

## 🚀 Run Locally

```bash
python app.py
```

> Make sure port 5000 is open and accessible.

---

## 📡 Endpoint Info

### `POST /update_location`

**Headers:**
```
Authorization: Bearer supersecrettoken123
Content-Type: application/json
```

**Payload:**
```json
{
  "imei": "device-123",
  "latitude": 37.7749,
  "longitude": -122.4194
}
```

---

## 🧪 Local Device Test Script

Use `send_location.py` to simulate a device:
```bash
python send_location.py
```

---

## 🌍 Render Deployment

This app is ready to deploy on [Render.com](https://render.com):

- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`
- Set `PORT` environment variable (Render does this automatically)
- Deploy from GitHub

> App auto-binds to `0.0.0.0` and uses `os.environ['PORT']`.

---

## 🛡️ Security Note

- The current token is hardcoded: `supersecrettoken123`. Replace it with a secure system in production.
- Consider using HTTPS, IP whitelisting, or JWT tokens for better security.

---

## 📂 Project Structure

```
.
├── app.py               # Flask + SocketIO server
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Live map dashboard
└── send_location.py     # Simulator for testing device updates
```

---

## 👨‍💻 Author

- Developed by **[Ellams Nurudeen Mustapha]**
- Based on an Android + Flask integration concept for device tracking

---racking

---
