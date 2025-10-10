#include <WiFi.h>
#include <HTTPClient.h>

// ---------- Wi-Fi Setup ----------
const char* ssid = "*";
const char* password = "*";

// ---------- Server ----------
const char* serverName = "*/data"; // replace with your PC IP

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Send single detection POST
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"status\": \"connected\", \"ip\": \"" + WiFi.localIP().toString() + "\"}";
    int httpResponseCode = http.POST(jsonData);

    Serial.print("Server response code: ");
    Serial.println(httpResponseCode);

    http.end();
  }
}

void loop() {
  // Nothing here; detection happens only in setup
}
