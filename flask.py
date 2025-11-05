from flask import Flask, request, jsonify, send_file
import io, time, os

app = Flask(__name__)


latest_command = {}

@app.route('/send', methods=['POST'])
def send():
    """Laptop cmd"""
    global latest_command, last_detection_time
    data = request.json
    latest_command = data
    print("Command received:", data)
#if laptop send "dog"
    if data.get("dog"):
        last_detection_time = time.time()

    return jsonify({"status": "ok", "stored": latest_command})

@app.route('/get_command', methods=['GET'])
def get_command():
    """ESP32 fetches the latest command"""
    return jsonify(latest_command)


#cam with flask integration

latest_frame = None
last_detection_time = 0
DOG_TIMEOUT = 120  # seconds before /check resets

@app.route("/upload", methods=["POST"])
def upload():
    """ESP32-CAM uploads its latest frame"""
    global latest_frame
    if 'image' not in request.files:
        return "No image uploaded", 400
    latest_frame = request.files['image'].read()
    print("📸 Received a frame")
    return "OK", 200

@app.route("/latest", methods=["GET"])
def latest():
    """Laptop fetches latest frame for YOLO"""
    if not latest_frame:
        return "No frame yet", 404
    return send_file(io.BytesIO(latest_frame), mimetype='image/jpeg')

@app.route("/check", methods=["GET"])
def check():
    """Feeder ESP32 checks if dog detected recently"""
    if time.time() - last_detection_time < DOG_TIMEOUT:
        return jsonify({"dog": True})
    else:
        return jsonify({"dog": False})


# ===== Start server ===== 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
