#include <WiFi.h>
#include <HTTPClient.h>

// ---------- Pin Configuration ----------
#define GSR_PIN 0  // GPIO0 (ADC pin)

// ---------- Constants ----------
const float VCC = 3.3;      // ESP32-C3 supply voltage
const int ADC_MAX = 4095;   // 12-bit ADC resolution
const unsigned long SEND_INTERVAL = 5000; // send every 5 seconds
const int SAMPLE_INTERVAL = 200;          // sample every 200 ms

// ---------- Wi-Fi Setup ----------
const char* ssid = "*";
const char* password = "*";

// ---------- Server ----------
const char* serverName = "*/data";

// ---------- Variables ----------
unsigned long previousMillis = 0;
float sumVoltage = 0.0;
int sampleCount = 0;

// ---------- Setup ----------
void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n📡 Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi connected!");
  Serial.print("📶 IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println("🔹 GSR Sensor Monitoring Started");
}

// ---------- Loop ----------
void loop() {
  // --- Read analog signal ---
  int gsrValue = analogRead(GSR_PIN);
  float voltage = (gsrValue / (float)ADC_MAX) * VCC;

  sumVoltage += voltage;
  sampleCount++;

  unsigned long currentMillis = millis();

  // --- Send average every 5 seconds ---
  if (currentMillis - previousMillis >= SEND_INTERVAL) {
    previousMillis = currentMillis;

    if (sampleCount > 0) {
      float avgVoltage = sumVoltage / sampleCount;
      sumVoltage = 0;
      sampleCount = 0;

      sendToServer(avgVoltage);
    }
  }

  delay(SAMPLE_INTERVAL);
}

// ---------- Send Data to Flask Server ----------
void sendToServer(float avgVoltage) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"gsr_value\": " + String(avgVoltage, 3) + "}";

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      Serial.print("✅ Sent: ");
      Serial.print(avgVoltage, 3);
      Serial.print(" V | Response: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("❌ HTTP POST Error: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("⚠️ WiFi Disconnected. Reconnecting...");
    reconnectWiFi();
  }
}

// ---------- Reconnect WiFi if disconnected ----------
void reconnectWiFi() {
  WiFi.disconnect();
  WiFi.begin(ssid, password);
  unsigned long startAttemptTime = millis();

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 10000) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ Reconnected to WiFi!");
  } else {
    Serial.println("\n❌ Failed to reconnect.");
  }
}
