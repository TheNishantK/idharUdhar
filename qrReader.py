import cv2
import numpy as np
from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    nparr = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if bbox is not None and data:
        print(f"QR Code Found: {data}")
        return data, 200
    else:
        return "No QR Code Found", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
