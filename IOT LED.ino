#include <WiFi.h>
#include <ThingSpeak.h>

// =====================================
// Wi-Fi
// =====================================

const char* ssid = "GalaxyS25A";
const char* password = "12345678";

// =====================================
// ThingSpeak
// =====================================

unsigned long channelNumber = 3440946;

const char* writeAPIKey = "J932SGRAB8UB85N1";
const char* readAPIKey  = "BO4EE879LOVZW8AF";

// =====================================
// LED
// =====================================

#define LED_PIN 4

WiFiClient client;

// =====================================
// Setup
// =====================================

void setup() {

  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);

  // Start with LED OFF
  digitalWrite(LED_PIN, LOW);

  // Connect to Wi-Fi
  Serial.println();
  Serial.print("Connecting to Wi-Fi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");

  }

  Serial.println();
  Serial.println("Wi-Fi connected!");

  Serial.print("ESP32-S3 IP Address: ");
  Serial.println(WiFi.localIP());

  // Start ThingSpeak
  ThingSpeak.begin(client);

  Serial.println("ThingSpeak connected!");
}

// =====================================
// Loop
// =====================================

void loop() {

  // Make sure Wi-Fi is connected
  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("Wi-Fi disconnected. Reconnecting...");

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {

      delay(500);
      Serial.print(".");

    }

    Serial.println();
    Serial.println("Wi-Fi reconnected!");
  }

  // ===================================
  // Read Field 1 from ThingSpeak
  // ===================================

  int ledStatus = ThingSpeak.readIntField(
    channelNumber,
    1,
    readAPIKey
  );

  int statusCode = ThingSpeak.getLastReadStatus();

  Serial.print("ThingSpeak Field 1: ");
  Serial.println(ledStatus);

  Serial.print("Read status: ");
  Serial.println(statusCode);

  // ===================================
  // Control LED
  // ===================================

  if (statusCode == 200) {

    if (ledStatus == 1) {

      digitalWrite(LED_PIN, HIGH);

      Serial.println("RED LED: ON");

    }

    else if (ledStatus == 0) {

      digitalWrite(LED_PIN, LOW);

      Serial.println("RED LED: OFF");

    }

    else {

      Serial.println("Invalid value. Use 0 or 1.");

    }
  }

  else {

    Serial.println("Failed to read ThingSpeak!");

  }

  // Check ThingSpeak every 5 seconds
  delay(5000);
}
