from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def home():
    return "Arduino Server is running! Use POST /data to send data."

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data:
        print("📡 Received data:", data)
        return {"status": "success", "message": "Data received"}, 200
    else:
        return {"status": "error", "message": "No data received"}, 400

if __name__ == '__main__':
    # 0.0.0.0 allows access from other devices in your Wi-Fi network
    app.run(host='0.0.0.0', port=5000)