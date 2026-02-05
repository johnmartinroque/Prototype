from flask import Flask, jsonify
import requests
import random
import threading
import time

app = Flask(__name__)

TARGET_URL = "http://127.0.0.1:5000/data"  # your main Flask server
SEND_INTERVAL = 2  # seconds

latest_sent = {
    "gsr_value": None,
    "status": None
}

def send_random_gsr():
    global latest_sent
    while True:
        gsr_value = round(random.uniform(2.0, 7.0), 2)

        payload = {
            "gsr_value": gsr_value
        }

        try:
            response = requests.post(TARGET_URL, json=payload, timeout=5)
            latest_sent = {
                "gsr_value": gsr_value,
                "status": response.status_code
            }
            print(f"📤 Sent GSR: {gsr_value} → {response.status_code}")
        except Exception as e:
            latest_sent = {
                "gsr_value": gsr_value,
                "status": "error"
            }
            print("❌ Failed to send:", e)

        time.sleep(SEND_INTERVAL)

# ---------- API ----------
@app.route("/status", methods=["GET"])
def status():
    return jsonify(latest_sent)

# ---------- Run ----------
if __name__ == "__main__":
    print("🚀 GSR Simulator Flask Server running...")
    threading.Thread(target=send_random_gsr, daemon=True).start()
    app.run(host="0.0.0.0", port=6000)
