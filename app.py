from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import time
from flask_cors import CORS

app = Flask(__name__) # Corrected: '__name__' has double underscores
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# In-memory database for storing IMEI locations
location_db = {}
AUTH_TOKEN = "supersecrettoken123"

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
    timestamp = time.time()

    if not imei or lat is None or lon is None:
        return {"status": "bad request"}, 400

    location_db[imei] = {"lat": lat, "lon": lon, "timestamp": timestamp}

    # Emit new location via WebSocket
    socketio.emit('location_update', {"imei": imei, "lat": lat, "lon": lon})
    return {"status": "success"}, 200

if __name__ == '__main__': # Corrected: '__name__' has double underscores
    socketio.run(app, debug=True)

