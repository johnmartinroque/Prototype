from flask import Flask, request, jsonify
from datetime import datetime
import joblib
import numpy as np

app = Flask(__name__)

# Load saved model and scaler
try:
    model = joblib.load("datasets/gsr/best_gsr_model.pkl")
    print("✅ Loaded trained GSR model successfully.")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data and 'gsr_value' in data:
        gsr_value = float(data['gsr_value'])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if model is not None:
            # Expand the single GSR voltage to match the number of features
            input_data = np.array([[gsr_value] * model.n_features_in_])
            try:
                # Predict
                prediction = model.predict(input_data)[0]
                pred_label = "High MWL" if prediction == 1 else "Low MWL"

                # Get probability/confidence
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(input_data)[0]
                    confidence = proba[prediction] * 100
                else:
                    confidence = None

                # Print nicely
                if confidence:
                    print(f"[{timestamp}] 📡 GSR: {gsr_value:.3f} V → 🧠 {pred_label} ({confidence:.1f}%)")
                else:
                    print(f"[{timestamp}] 📡 GSR: {gsr_value:.3f} V → 🧠 {pred_label}")

                return jsonify({
                    "status": "success",
                    "prediction": pred_label,
                    "confidence": confidence if confidence else "N/A",
                    "gsr_value": gsr_value
                }), 200
            except Exception as e:
                print(f"⚠️ Prediction error: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500
        else:
            print(f"[{timestamp}] GSR Value: {gsr_value:.3f} (Model not loaded)")
            return jsonify({"status": "error", "message": "Model not loaded"}), 500
    else:
        return jsonify({"status": "error", "message": "Invalid or missing data"}), 400

if __name__ == '__main__':
    print("🚀 Flask server running... waiting for ESP32 data every 5s.")
    app.run(host='0.0.0.0', port=5000)