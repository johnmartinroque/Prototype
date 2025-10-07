#include <WiFi.h>
#include <HTTPClient.h>

#define GSR_PIN 0  // GPIO0 (ADC pin)

// ---------- Wi-Fi Setup ----------
const char* ssid = "HUAWEI-2.4G-eAX8";
const char* password = "pWfm5Aba";

// ---------- Server ----------
const char* serverName = "http://192.168.100.33:5000/data"; // Flask server IP

unsigned long previousMillis = 0;
const unsigned long sendInterval = 5000;  // send every 5 seconds

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("📡 Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println("GSR Sensor Test Start");
}

void loop() {
  static int sampleCount = 0;
  static float sumGSR = 0;

  // --- Read GSR every 200ms ---
  int gsrValue = analogRead(GSR_PIN);
  sumGSR += gsrValue;
  sampleCount++;

  // --- Every 5 seconds, send average to server ---
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= sendInterval) {
    previousMillis = currentMillis;

    if (sampleCount > 0) {
      float avgGSR = sumGSR / sampleCount;
      sumGSR = 0;
      sampleCount = 0;

      sendToServer(avgGSR);
    }
  }

  delay(200);  // sampling interval
}

void sendToServer(float avgGSR) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"gsr_value\": " + String(avgGSR, 2) + "}";
    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      Serial.println("✅ Sent average GSR to server.");
    } else {
      Serial.print("❌ Error sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("⚠️ WiFi not connected!");
  }
}
