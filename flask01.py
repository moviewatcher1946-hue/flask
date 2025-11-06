from flask01 import Flask, request, jsonify

app = Flask(__name__)

latest_command = None
dog_detected = False  # for example

@app.route('/send', methods=['POST'])
def send():
    global latest_command
    data = request.get_json()
    if not data or 'command' not in data:
        return jsonify({'error': 'No command received'}), 400
    latest_command = data['command']
    print(f"Received command: {latest_command}")
    return jsonify({'status': 'ok'})

@app.route('/get', methods=['GET'])
def get():
    """ESP32 calls this to get the latest command"""
    global latest_command
    if latest_command is None:
        return jsonify({'command': 'none'})
    cmd = latest_command
    latest_command = None  # reset after sending
    return jsonify({'command': cmd})

@app.route('/dog', methods=['POST'])
def dog_status():
    """ESP32 updates whether a dog is detected"""
    global dog_detected
    data = request.get_json()
    if not data or 'dog' not in data:
        return jsonify({'error': 'No dog status sent'}), 400
    dog_detected = data['dog']
    print(f"Dog detected: {dog_detected}")
    return jsonify({'status': 'ok'})

@app.route('/status', methods=['GET'])
def status():
    """For the website or check: show if dog is detected"""
    if not dog_detected:
        return "no dog"
    return "dog detected"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
