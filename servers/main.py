from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib
import numpy as np
import traceback
import requests  # <-- for n8n

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

# ---------------- n8n Webhook ----------------
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/119c6b94-4113-4370-8aca-4172fa7c423e"

# ---------------- Latest Reading ----------------
latest_reading = {
    "gsr_value": None,
    "emotion": {"prediction": None, "confidence": None, "all_percentages": None, "timestamp": None},
    "mwl": {"prediction": None, "confidence": None, "all_percentages": None, "timestamp": None}
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
        emotion_result = {
            "prediction": None,
            "confidence": None,
            "all_percentages": None,
            "timestamp": timestamp
        }

        if emotion_model and emotion_scaler:
            input_data = np.array([[gsr_value]])
            try:
                input_scaled = emotion_scaler.transform(input_data)
            except:
                expected_features = getattr(emotion_scaler, 'n_features_in_', 1)
                input_data = np.array([[gsr_value] * expected_features])
                input_scaled = emotion_scaler.transform(input_data)

            pred_val = emotion_model.predict(input_scaled)[0]
            pred_label = str(pred_val)

            all_percentages = None
            confidence_val = None

            if hasattr(emotion_model, "predict_proba"):
                proba = emotion_model.predict_proba(input_scaled)[0]
                all_percentages = {
                    str(cls): round(p * 100, 1)
                    for cls, p in zip(emotion_model.classes_, proba)
                }
                confidence_val = max(proba) * 100

            emotion_result.update({
                "prediction": pred_label,
                "confidence": round(confidence_val, 1) if confidence_val else None,
                "all_percentages": all_percentages
            })

        # ---------- MWL Prediction ----------
        mwl_result = {
            "prediction": None,
            "confidence": None,
            "all_percentages": None,
            "timestamp": timestamp
        }

        if mwl_model:
            input_data = np.array([[gsr_value] * mwl_model.n_features_in_])
            pred_val = mwl_model.predict(input_data)[0]
            pred_label = "High MWL" if pred_val == 1 else "Low MWL"

            all_percentages = None
            confidence_val = None

            if hasattr(mwl_model, "predict_proba"):
                proba = mwl_model.predict_proba(input_data)[0]
                all_percentages = {
                    "Low MWL": round(proba[0] * 100, 1),
                    "High MWL": round(proba[1] * 100, 1)
                }
                confidence_val = all_percentages[pred_label]

            mwl_result.update({
                "prediction": pred_label,
                "confidence": confidence_val,
                "all_percentages": all_percentages
            })

        # ---------- Save Latest ----------
        latest_reading = {
            "gsr_value": gsr_value,
            "emotion": emotion_result,
            "mwl": mwl_result
        }

        # ---------- Send to n8n ----------
        try:
            payload = {
                "timestamp": timestamp,
                "gsr_value": gsr_value,
                "emotion_prediction": emotion_result["prediction"],
                "emotion_confidence": emotion_result["confidence"],
                "mwl_prediction": mwl_result["prediction"],
                "mwl_confidence": mwl_result["confidence"]
            }

            requests.post(N8N_WEBHOOK_URL, json=payload, timeout=3)
            print("📤 Sent data to n8n")

        except Exception as e:
            print("⚠️ Failed to send to n8n:", e)

        # ---------- Log ----------
        print(f"[{timestamp}] 📡 GSR: {gsr_value:.3f}")
        if emotion_result["all_percentages"]:
            print("🧠 Emotion:", emotion_result["all_percentages"])
        if mwl_result["all_percentages"]:
            print("💼 MWL:", mwl_result["all_percentages"])

        return jsonify(latest_reading), 200

    except Exception as e:
        print("⚠️ Server Error:\n", traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500


# ---------------- Latest Endpoint ----------------
@app.route('/latest', methods=['GET'])
def get_latest():
    if latest_reading["gsr_value"] is None:
        return jsonify({"status": "error", "message": "No data yet"}), 404
    return jsonify(latest_reading), 200


# ---------------- Run Server ----------------
if __name__ == '__main__':
    print("🚀 Flask server running on http://localhost:5000/data")
    app.run(host='0.0.0.0', port=5000, debug=True)
