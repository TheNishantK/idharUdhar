import cv2

# Replace with your ESP32-CAM stream URL
ESP32_STREAM_URL = "http://<ESP32-IP>/"

# Initialize the OpenCV QR code detector
qr_detector = cv2.QRCodeDetector()

# Open the video stream from ESP32-CAM
cap = cv2.VideoCapture(ESP32_STREAM_URL)

if not cap.isOpened():
    print("❌ Error: Unable to open ESP32-CAM stream")
    exit()

print("📷 Streaming started. Bring a QR code in front of the camera...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Failed to grab frame")
        continue

    # Detect and decode the QR code
    qr_data, bbox, _ = qr_detector.detectAndDecode(frame)

    if bbox is not None and qr_data:
        # Draw a bounding box around the QR code
        for point in bbox:
            cv2.polylines(frame, [point.astype(int)], True, (0, 255, 0), 2)
        cv2.putText(frame, qr_data, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        print(f"✅ QR Code Detected: {qr_data}")

    # Show the grayscale video stream
    cv2.imshow("ESP32-CAM QR Scanner", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


