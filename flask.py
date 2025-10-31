from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Store the latest command to send to ESP32
latest_command = {}

@app.route('/send', methods=['POST'])
def send():
    """
    Laptop posts a command to this endpoint
    """
    global latest_command
    data = request.json  # JSON from laptop
    latest_command = data
    print("Command received:", data)
    return jsonify({"status": "ok", "stored": latest_command})

@app.route('/get_command', methods=['GET'])
def get_command():
    """
    ESP32 fetches the latest command
    """
    return jsonify(latest_command)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
