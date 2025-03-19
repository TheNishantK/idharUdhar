#include "esp_camera.h"
#include <WiFi.h>

// Replace with your Wi-Fi credentials
const char* ssid = "KASHEWADI_NOOK_2GH";
const char* password = "Defy@12345";

// Camera Config for AI Thinker ESP32-CAM
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

WiFiServer server(80);

void startCamera() {
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_GRAYSCALE; // Set grayscale mode

    // Set frame size and quality
    config.frame_size = FRAMESIZE_QVGA;  // 320x240
    config.jpeg_quality = 12;            // Low value = better quality
    config.fb_count = 2;

    // Initialize the camera
    if (esp_camera_init(&config) != ESP_OK) {
        Serial.println("Camera init failed!");
        return;
    }
    Serial.println("Camera ready!");
}

void startServer() {
    Serial.println("Starting server...");
    server.begin();
    Serial.println("Server started! Access stream at: http://<ESP32-IP>/");
}

void handleClient(WiFiClient client) {
    String req = client.readStringUntil('\r');
    client.flush();
    
    if (req.indexOf("GET /") >= 0) {
        Serial.println("Client connected!");

        // HTTP Header
        client.println("HTTP/1.1 200 OK");
        client.println("Content-Type: multipart/x-mixed-replace; boundary=frame");
        client.println();

        while (client.connected()) {
            camera_fb_t *fb = esp_camera_fb_get();
            if (!fb) {
                Serial.println("Failed to get frame buffer");
                continue;
            }

            // Convert grayscale to JPEG
            size_t jpg_size;
            uint8_t *jpg_buf;
            bool jpeg_converted = frame2jpg(fb, 80, &jpg_buf, &jpg_size);

            if (jpeg_converted) {
                client.print("--frame\r\n");
                client.print("Content-Type: image/jpeg\r\n\r\n");
                client.write(jpg_buf, jpg_size);
                client.print("\r\n");
                free(jpg_buf);
            }

            esp_camera_fb_return(fb);
            delay(100);  // Adjust frame rate
        }
        Serial.println("Client disconnected");
    }
    client.stop();
}

void setup() {
    Serial.begin(115200);
    Serial.println("\n\nStarting ESP32-CAM Grayscale Streaming...");

    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    // Start camera and server
    startCamera();
    startServer();
}

void loop() {
    WiFiClient client = server.available();
    if (client) {
        handleClient(client);
    }
}
