from flask import Flask, request, jsonify
from datetime import datetime
import joblib
import numpy as np

app = Flask(__name__)

# Load saved model and scaler
try:
    model = joblib.load("datasets/gsr/best_gsr_model.pkl")
    scaler = joblib.load("datasets/gsr/best_gsr_scaler.pkl")
    print("✅ Loaded trained GSR model and scaler successfully.")
except Exception as e:
    print(f"❌ Failed to load model/scaler: {e}")
    model = None
    scaler = None

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data and 'gsr_value' in data:
        gsr_value = float(data['gsr_value'])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- Predict MWL if model is loaded ---
        if model is not None:
            # Here we assume GSR value represents mean; we expand it to match model input shape
            input_data = np.array([[gsr_value] * model.n_features_in_])
            try:
                if scaler:
                    scaled_input = scaler.transform(input_data)
                else:
                    scaled_input = input_data

                prediction = model.predict(scaled_input)[0]
                label = "High MWL" if prediction == 1 else "Low MWL"

                print(f"[{timestamp}] 📡 GSR Received: {gsr_value:.2f} → 🧠 Prediction: {label}")

                return jsonify({
                    "status": "success",
                    "prediction": label,
                    "gsr_value": gsr_value
                }), 200
            except Exception as e:
                print(f"⚠️ Prediction error: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500
        else:
            print(f"[{timestamp}] GSR Value: {gsr_value:.2f} (Model not loaded)")
            return jsonify({"status": "error", "message": "Model not loaded"}), 500
    else:
        return jsonify({"status": "error", "message": "Invalid or missing data"}), 400

if __name__ == '__main__':
    print("🚀 Flask server running... waiting for ESP32 data every 5s.")
    app.run(host='0.0.0.0', port=5000)
