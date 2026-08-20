#include <WiFi.h>
#include <WebServer.h>

// =============================
// Wi-Fi
// =============================
const char* ssid = "GalaxyS25A";
const char* password = "12345678";

// =============================
// L298N Motor Driver
// =============================
#define ENA 5
#define IN1 6
#define IN2 7

// GPIO 15 was part of your previous setup.
// It is not required for a single motor.
#define EXTRA_PIN 15

// =============================
// Web Server
// =============================
WebServer server(80);

// Motor speed: 0-255
int motorSpeed = 200;

// =============================
// Motor Functions
// =============================

void motorForward() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  ledcWrite(ENA, motorSpeed);

  Serial.println("Motor: FORWARD");
}

void motorBackward() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  ledcWrite(ENA, motorSpeed);

  Serial.println("Motor: BACKWARD");
}

void motorStop() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  ledcWrite(ENA, 0);

  Serial.println("Motor: STOP");
}

// =============================
// Web Page
// =============================

void handleRoot() {

  String html = R"rawliteral(

<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>ESP32 Motor Control</title>

<style>

body {
  font-family: Arial;
  text-align: center;
  background: #111;
  color: white;
  margin-top: 40px;
}

h1 {
  font-size: 32px;
}

button {
  width: 220px;
  height: 65px;
  margin: 10px;
  font-size: 22px;
  border: none;
  border-radius: 15px;
  color: white;
}

.forward {
  background: #2ecc71;
}

.backward {
  background: #3498db;
}

.stop {
  background: #e74c3c;
}

.speed {
  width: 80%;
  margin: 20px;
}

</style>

</head>

<body>

<h1>ESP32-S3 DC Motor</h1>

<h2>
Speed: <span id="speedValue">200</span>
</h2>

<button class="forward"
onclick="motor('forward')">
FORWARD
</button>

<br>

<button class="stop"
onclick="motor('stop')">
STOP
</button>

<br>

<button class="backward"
onclick="motor('backward')">
BACKWARD
</button>

<br><br>

<input
class="speed"
type="range"
min="0"
max="255"
value="200"
oninput="changeSpeed(this.value)">

<script>

function motor(direction) {

  fetch("/" + direction);

}

function changeSpeed(value) {

  document.getElementById("speedValue").innerHTML = value;

  fetch("/speed?value=" + value);

}

</script>

</body>

</html>

)rawliteral";

  server.send(200, "text/html", html);
}

// =============================
// Web Controls
// =============================

void handleForward() {

  motorForward();

  server.send(200, "text/plain", "Forward");

}

void handleBackward() {

  motorBackward();

  server.send(200, "text/plain", "Backward");

}

void handleStop() {

  motorStop();

  server.send(200, "text/plain", "Stopped");

}

void handleSpeed() {

  if (server.hasArg("value")) {

    motorSpeed = server.arg("value").toInt();

    motorSpeed = constrain(motorSpeed, 0, 255);

    Serial.print("Speed: ");
    Serial.println(motorSpeed);

  }

  server.send(200, "text/plain", "Speed updated");

}

// =============================
// SETUP
// =============================

void setup() {

  Serial.begin(115200);

  // Motor pins
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  // Extra historical GPIO
  pinMode(EXTRA_PIN, OUTPUT);
  digitalWrite(EXTRA_PIN, LOW);

  // ESP32-S3 Arduino LEDC PWM
  ledcAttach(ENA, 30000, 8);

  // Start motor stopped
  motorStop();

  // =========================
  // Connect Wi-Fi
  // =========================

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

  // =========================
  // Web Server Routes
  // =========================

  server.on("/", handleRoot);

  server.on("/forward", handleForward);

  server.on("/backward", handleBackward);

  server.on("/stop", handleStop);

  server.on("/speed", handleSpeed);

  server.begin();

  Serial.println("Web server started!");

}

// =============================
// LOOP
// =============================

void loop() {

  server.handleClient();

}
