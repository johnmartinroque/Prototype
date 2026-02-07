from flask import Flask, Response
from flask_cors import CORS
import cv2
import threading

app = Flask(__name__)
CORS(app)

# ---------------- Camera Setup ----------------
camera = cv2.VideoCapture(0)  # 0 = default webcam
lock = threading.Lock()

# Optional: reduce latency
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 15)

def generate_frames():
    while True:
        with lock:
            success, frame = camera.read()

        if not success:
            break

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame_bytes +
            b'\r\n'
        )

@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# ---------------- Run Server ----------------
if __name__ == '__main__':
    print("🚀 Camera stream running at:")
    print("👉 http://localhost:5000/video_feed")
    app.run(host='0.0.0.0', port=5000, debug=True)
