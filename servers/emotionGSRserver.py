from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib
import numpy as np
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for React or other frontends

# ---------------- Load Model & Scaler ----------------
try:
    model = joblib.load("../datasets/emotion/best_model_emotion.pkl")
    scaler = joblib.load("../datasets/emotion/scaler_emotion.pkl")
    print("✅ Loaded emotion model and scaler successfully.")
except Exception as e:
    print(f"❌ Failed to load model or scaler: {e}")
    model = None
    scaler = None

# ---------------- Latest Reading ----------------
latest_reading = {
    "gsr_value": None,
    "prediction": None,
    "confidence": None,
    "timestamp": None
}

# ---------------- Receive GSR Data ----------------
@app.route('/data', methods=['POST'])
def receive_data():
    global latest_reading

    try:
        data = request.get_json()
        if not data or 'gsr_value' not in data:
            return jsonify({"status": "error", "message": "Invalid or missing data"}), 400

        gsr_value = float(data['gsr_value'])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if model is None or scaler is None:
            return jsonify({"status": "error", "message": "Model or scaler not loaded"}), 500

        # --- Prepare Input ---
        input_data = np.array([[gsr_value]])

        # Check scaler input dimensions
        try:
            input_scaled = scaler.transform(input_data)
        except Exception as e:
            # Auto-fix: if shape mismatch, repeat gsr_value to match scaler feature size
            expected_features = getattr(scaler, 'n_features_in_', 1)
            print(f"⚠️ Input shape mismatch. Expected {expected_features} features, got 1.")
            input_data = np.array([[gsr_value] * expected_features])
            input_scaled = scaler.transform(input_data)

        # --- Prediction ---
        prediction_val = model.predict(input_scaled)[0]
        pred_label = str(prediction_val)  # e.g., Calm, Stressed, Sad, etc.

        # --- Confidence ---
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_scaled)[0]
            try:
                class_index = list(model.classes_).index(prediction_val)
                confidence_val = proba[class_index] * 100
            except:
                confidence_val = np.max(proba) * 100
        else:
            confidence_val = None

        # --- Save Latest Reading ---
        latest_reading = {
            "gsr_value": gsr_value,
            "prediction": pred_label,
            "confidence": confidence_val,
            "timestamp": timestamp
        }

        # --- Print Log ---
        if confidence_val:
            print(f"[{timestamp}] 📡 GSR: {gsr_value:.3f} → 🧠 {pred_label} ({confidence_val:.1f}%)")
        else:
            print(f"[{timestamp}] 📡 GSR: {gsr_value:.3f} → 🧠 {pred_label}")

        return jsonify(latest_reading), 200

    except Exception as e:
        print("⚠️ Server Error:\n", traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- Latest Data Endpoint ----------------
@app.route('/latest', methods=['GET'])
def get_latest():
    if latest_reading["gsr_value"] is None:
        return jsonify({"status": "error", "message": "No data yet"}), 404
    return jsonify(latest_reading), 200

# ---------------- Run Server ----------------
if __name__ == '__main__':
    print("🚀 Emotion Flask server running... waiting for ESP32 data.")
    app.run(host='0.0.0.0', port=5001)
