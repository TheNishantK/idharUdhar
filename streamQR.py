import cv2

# 🔧 Replace with your ESP32-CAM's IP address
ESP32_STREAM_URL = "http://192.168.1.36/stream"

# Initialize OpenCV's built-in QR code detector
qr_detector = cv2.QRCodeDetector()

def read_qr_code(frame):
    """ Detect and decode QR codes from a frame """
    data, bbox, _ = qr_detector.detectAndDecode(frame)
    if bbox is not None:
        for point in bbox:
            point = point[0]  # Convert to a usable format
            cv2.polylines(frame, [point.astype(int)], isClosed=True, color=(0, 255, 0), thickness=2)
    return data

def main():
    cap = cv2.VideoCapture(ESP32_STREAM_URL)  # Open ESP32-CAM Stream

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            continue
        
        qr_data = read_qr_code(frame)
        if qr_data:
            print(f"✅ QR Code Found: {qr_data}")
        
        # Show Video Stream
        cv2.imshow("ESP32-CAM QR Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

