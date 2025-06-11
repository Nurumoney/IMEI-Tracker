from flask import Flask, request, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
import time
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

location_db = {}
AUTH_TOKEN = os.environ.get("API_TOKEN", "supersecrettoken123")

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

    location_db[imei] = {"lat": lat, "lon": lon, "timestamp": time.time()}
    socketio.emit('location_update', {"imei": imei, "latitude": lat, "longitude": lon})
    return {"status": "success"}

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
