# emotion server.py problem: data different calibration?
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for React or other frontends

# Load trained emotion model and scaler
try:
    model = joblib.load("best_model_emotion.pkl")
    scaler = joblib.load("scaler_emotion.pkl")
    print("✅ Loaded trained emotion model and scaler successfully.")
except Exception as e:
    print(f"❌ Failed to load model or scaler: {e}")
    model = None
    scaler = None

# Store latest reading globally
latest_reading = {"gsr_value": None, "prediction": None, "confidence": None, "timestamp": None}

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_reading
    data = request.get_json()
    
    if data and 'gsr_value' in data:
        try:
            gsr_value = float(data['gsr_value'])
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if model is not None and scaler is not None:
                # Prepare input: expand single GSR to match model input
                input_data = np.array([[gsr_value]])
                input_scaled = scaler.transform(input_data)

                # Predict
                prediction_val = model.predict(input_scaled)[0]
                pred_label = prediction_val  # Calm or Stressed

                # Confidence
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(input_scaled)[0]
                    class_index = list(model.classes_).index(prediction_val)
                    confidence_val = proba[class_index] * 100
                else:
                    confidence_val = None

                # Save latest reading
                latest_reading = {
                    "gsr_value": gsr_value,
                    "prediction": pred_label,
                    "confidence": confidence_val,
                    "timestamp": timestamp
                }

                # Print nicely to console
                if confidence_val:
                    print(f"[{timestamp}] 📡 GSR: {gsr_value:.3f} → 🧠 {pred_label} ({confidence_val:.1f}%)")
                else:
                    print(f"[{timestamp}] 📡 GSR: {gsr_value:.3f} → 🧠 {pred_label}")

                return jsonify(latest_reading), 200
            else:
                return jsonify({"status": "error", "message": "Model or scaler not loaded"}), 500

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Invalid or missing data"}), 400

@app.route('/latest', methods=['GET'])
def get_latest():
    if latest_reading["gsr_value"] is None:
        return jsonify({"status": "error", "message": "No data yet"}), 404
    return jsonify(latest_reading), 200

if __name__ == '__main__':
    print("🚀 Flask server running... waiting for GSR data.")
    app.run(host='0.0.0.0', port=5000)
