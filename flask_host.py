import cv2
import numpy as np
import requests
import time
from flask import Flask, request, jsonify

ESP32_STREAM_URL = "http://<ESP32-IP>/"
ESP32_POST_URL = "http://<ESP32-IP>/display"

app = Flask(__name__)

def get_qr_name(image):
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(image)
    if data:
        return data
    return None

def capture_qr():
    cap = cv2.VideoCapture(ESP32_STREAM_URL)

    if not cap.isOpened():
        print("Failed to connect to ESP32-CAM stream")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to get frame")
            continue

        name = get_qr_name(frame)
        if name:
            cap.release()
            return name

    cap.release()
    return None

def send_name_to_esp(name):
    try:
        requests.post(ESP32_POST_URL, json={"name": name})
        print(f"Sent name '{name}' to ESP32")
    except Exception as e:
        print("Failed to send name to ESP32:", e)

@app.route('/capture', methods=['GET'])
def handle_capture():
    print("Capturing QR Code...")
    name = capture_qr()
    
    if name:
        send_name_to_esp(name)
        return jsonify({"status": "success", "name": name})
    else:
        return jsonify({"status": "failed", "message": "No QR detected"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
