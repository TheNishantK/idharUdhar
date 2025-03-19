import cv2
import numpy as np
import requests
from pyzbar.pyzbar import decode

ESP32_CAM_URL = "http://192.168.1.36/stream"  # Change this to your ESP32-CAM IP

def convert_rgb565_to_bgr888(rgb565_img):
    """ Convert RGB565 image to OpenCV BGR format """
    img = np.frombuffer(rgb565_img, dtype=np.uint16)
    r = ((img >> 11) & 0x1F) * 255 // 31
    g = ((img >> 5) & 0x3F) * 255 // 63
    b = (img & 0x1F) * 255 // 31
    return cv2.merge((b, g, r))

def get_frame():
    response = requests.get(ESP32_CAM_URL, stream=True)
    if response.status_code == 200:
        img_data = response.raw.read()
        return convert_rgb565_to_bgr888(img_data)
    return None

while True:
    frame = get_frame()
    if frame is not None:
        qr_codes = decode(frame)
        for qr in qr_codes:
            qr_data = qr.data.decode("utf-8")
            print(f"QR Code Detected: {qr_data}")
            x, y, w, h = qr.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("QR Code Scanner", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
