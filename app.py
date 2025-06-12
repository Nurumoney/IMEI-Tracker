from flask import Flask, request, render_template, send_file
from flask_socketio import SocketIO
from flask_cors import CORS
import time
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

location_db = {}
AUTH_TOKEN = os.environ.get("API_TOKEN", "supersecrettoken123")
LAST_LOG_TIMES = {}
CSV_LOG_PATH = "location_log.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.get_json()
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token != AUTH_TOKEN:
        return {"status": "unauthorized"}, 401

    imei = data.get("imei")
    lat = data.get("latitude")
    lon = data.get("longitude")

    if not imei or lat is None or lon is None:
        return {"status": "bad request"}, 400

    now = time.time()
    location_db[imei] = {"lat": lat, "lon": lon, "timestamp": now}
    socketio.emit('location_update', {"imei": imei, "latitude": lat, "longitude": lon})

    last_log = LAST_LOG_TIMES.get(imei, 0)
    if now - last_log >= 300:
        with open(CSV_LOG_PATH, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.utcnow().isoformat(), imei, lat, lon])
        LAST_LOG_TIMES[imei] = now

    return {"status": "success"}

@app.route('/download_csv')
def download_csv():
    if os.path.exists(CSV_LOG_PATH):
        return send_file(CSV_LOG_PATH, as_attachment=True)
    else:
        return "CSV log not found", 404

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
