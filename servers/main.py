from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib
import numpy as np
import traceback
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# ---------------- Load Models & Scalers ----------------
try:
    emotion_model = joblib.load("../datasets/emotion/best_model_emotion.pkl")
    emotion_scaler = joblib.load("../datasets/emotion/scaler_emotion.pkl")
    print("✅ Loaded emotion model and scaler successfully.")
except Exception as e:
    print(f"❌ Failed to load emotion model/scaler: {e}")
    emotion_model = None
    emotion_scaler = None

try:
    mwl_model = joblib.load("../datasets/gsr/best_gsr_model.pkl")
    print("✅ Loaded MWL model successfully.")
except Exception as e:
    print(f"❌ Failed to load MWL model: {e}")
    mwl_model = None

# ---------------- Latest Reading ----------------
latest_reading = {
    "gsr_value": None,
    "emotion": {"prediction": None, "confidence": None, "timestamp": None},
    "mwl": {"prediction": None, "confidence": None, "timestamp": None}
}

# ---------------- Combined Prediction ----------------
@app.route('/data', methods=['POST'])
def predict_data():
    global latest_reading
    try:
        data = request.get_json()
        if not data or 'gsr_value' not in data:
            return jsonify({"status": "error", "message": "Invalid or missing data"}), 400

        gsr_value = float(data['gsr_value'])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ---------- Emotion Prediction ----------
        emotion_result = {"prediction": None, "confidence": None, "timestamp": timestamp}
        if emotion_model and emotion_scaler:
            input_data = np.array([[gsr_value]])
            try:
                input_scaled = emotion_scaler.transform(input_data)
            except:
                expected_features = getattr(emotion_scaler, 'n_features_in_', 1)
                input_data = np.array([[gsr_value]*expected_features])
                input_scaled = emotion_scaler.transform(input_data)

            pred_val = emotion_model.predict(input_scaled)[0]
            pred_label = str(pred_val)
            confidence_val = None
            if hasattr(emotion_model, "predict_proba"):
                proba = emotion_model.predict_proba(input_scaled)[0]
                try:
                    class_index = list(emotion_model.classes_).index(pred_val)
                    confidence_val = proba[class_index] * 100
                except:
                    confidence_val = np.max(proba) * 100

            # ✅ Round confidence to 1 decimal place
            emotion_result.update({
                "prediction": pred_label,
                "confidence": round(confidence_val, 1) if confidence_val is not None else None
            })

        # ---------- MWL Prediction ----------
        mwl_result = {"prediction": None, "confidence": None, "timestamp": timestamp}
        if mwl_model:
            input_data = np.array([[gsr_value]*mwl_model.n_features_in_])
            pred_val = mwl_model.predict(input_data)[0]
            pred_label = "High MWL" if pred_val == 1 else "Low MWL"
            confidence_val = None
            if hasattr(mwl_model, "predict_proba"):
                proba = mwl_model.predict_proba(input_data)[0]
                confidence_val = proba[pred_val] * 100

            # ✅ Round confidence to 1 decimal place
            mwl_result.update({
                "prediction": pred_label,
                "confidence": round(confidence_val, 1) if confidence_val is not None else None
            })

        # ---------- Save Latest ----------
        latest_reading = {
            "gsr_value": gsr_value,
            "emotion": emotion_result,
            "mwl": mwl_result
        }

        # ---------- Log ----------
        print(f"[{timestamp}] 📡 GSR: {gsr_value:.3f} → 🧠 Emotion: {emotion_result['prediction']} ({emotion_result['confidence']}%), MWL: {mwl_result['prediction']} ({mwl_result['confidence']}%)")

        return jsonify(latest_reading), 200

    except Exception as e:
        print("⚠️ Server Error:\n", traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- Latest Endpoint ----------------
@app.route('/latest', methods=['GET'])
def get_latest():
    global last_received_time

    if latest_reading["gsr_value"] is None:
        return jsonify({
            "status": "no_data",
            "message": "No data received yet"
        }), 404

    if last_received_time is None:
        return jsonify(latest_reading), 200

    # ⏱️ Check timeout
    time_diff = datetime.now() - last_received_time
    if time_diff > timedelta(seconds=DATA_TIMEOUT_SECONDS):
        return jsonify({
            **latest_reading,
            "status": "stopped",
            "stopped_at": last_received_time.strftime("%Y-%m-%d %H:%M:%S")
        }), 200

    return jsonify({
        **latest_reading,
        "status": "active"
    }), 200

# ---------------- Run Server ----------------
if __name__ == '__main__':
    print("🚀 Combined Flask server running on /data endpoint.")
    app.run(host='0.0.0.0', port=5000)
