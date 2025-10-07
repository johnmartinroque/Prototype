from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data and 'gsr_value' in data:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] 📡 GSR Data Received: {data['gsr_value']}")
        return jsonify({"status": "success", "message": "Data received"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid or missing data"}), 400

if __name__ == '__main__':
    print("🚀 Flask server running... waiting for ESP32 data every 5s.")
    app.run(host='0.0.0.0', port=5000)
