#include <WiFi.h>
#include <ThingSpeak.h>
#include <DHT.h>

// ==============================
// Wi-Fi
// ==============================

const char* ssid = "GalaxyS25A";
const char* password = "12345678";

// ==============================
// DHT11
// ==============================

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// ==============================
// ThingSpeak
// ==============================

// Enter YOUR DHT11 ThingSpeak channel details here
unsigned long channelID = YOUR_CHANNEL_ID;

const char* writeAPIKey = "YOUR_WRITE_API_KEY";

WiFiClient client;

// ==============================
// Setup
// ==============================

void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println();
  Serial.println("ESP32-S3 DHT11 ThingSpeak IoT");
  Serial.println("--------------------------------");

  // Start DHT11
  dht.begin();

  // Connect Wi-Fi
  WiFi.begin(ssid, password);

  Serial.print("Connecting to Wi-Fi");

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");

  }

  Serial.println();
  Serial.println("Wi-Fi connected!");

  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Start ThingSpeak
  ThingSpeak.begin(client);

  Serial.println("ThingSpeak started!");
}

// ==============================
// Loop
// ==============================

void loop() {

  // Read DHT11
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check sensor
  if (isnan(humidity) || isnan(temperature)) {

    Serial.println("ERROR: Failed to read DHT11!");

    delay(2000);

    return;
  }

  // Display readings
  Serial.println();
  Serial.println("DHT11 Readings");
  Serial.println("----------------");

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  // ============================
  // Send to ThingSpeak
  // ============================

  ThingSpeak.setField(1, temperature);
  ThingSpeak.setField(2, humidity);

  int response = ThingSpeak.writeFields(channelID, writeAPIKey);

  if (response == 200) {

    Serial.println("ThingSpeak update successful!");

  } else {

    Serial.print("ThingSpeak update failed. HTTP error: ");
    Serial.println(response);

  }

  // ThingSpeak requires a minimum interval
  // between channel updates.
  delay(20000);
}
