from flask import Flask, request
from datasets.gsr import *

app = Flask(__name__)

@app.route('/')
def home():
    return "ESP32 Server running!"

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data:
        print("📡 ESP32 detected:", data)
        return {"status": "success", "message": "ESP32 detected"}, 200
    else:
        return {"status": "error", "message": "No data received"}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
