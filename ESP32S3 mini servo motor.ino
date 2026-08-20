#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

// =========================
// Wi-Fi
// =========================
const char* ssid = "GalaxyS25A";
const char* password = "12345678";

// =========================
// Servo
// =========================
Servo myServo;
const int SERVO_PIN = 7;

// =========================
// Web Server
// =========================
WebServer server(80);

// Current servo angle
int servoAngle = 90;

// =========================
// Web Page
// =========================
void handleRoot() {

  String html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>ESP32 Servo Control</title>

  <style>
    body {
      font-family: Arial;
      text-align: center;
      background: #111;
      color: white;
      margin-top: 50px;
    }

    h1 {
      font-size: 32px;
    }

    .angle {
      font-size: 28px;
      margin: 25px;
    }

    button {
      width: 180px;
      height: 60px;
      margin: 10px;
      font-size: 22px;
      border: none;
      border-radius: 15px;
      cursor: pointer;
    }

    .left {
      background: #3498db;
      color: white;
    }

    .center {
      background: #2ecc71;
      color: white;
    }

    .right {
      background: #e74c3c;
      color: white;
    }
  </style>
</head>

<body>

  <h1>ESP32-S3 Servo Control</h1>

  <div class="angle">
    Servo Angle: <span id="angle">90</span>&deg;
  </div>

  <button class="left" onclick="moveServo(0)">
    0°
  </button>

  <button class="center" onclick="moveServo(90)">
    90°
  </button>

  <button class="right" onclick="moveServo(180)">
    180°
  </button>

  <script>

    function moveServo(angle) {

      fetch("/servo?angle=" + angle)
        .then(response => response.text())
        .then(data => {

          document.getElementById("angle").innerHTML = angle;

        });

    }

  </script>

</body>
</html>
)rawliteral";

  server.send(200, "text/html", html);
}

// =========================
// Servo Control
// =========================
void handleServo() {

  if (server.hasArg("angle")) {

    int angle = server.arg("angle").toInt();

    // Keep angle within safe range
    angle = constrain(angle, 0, 180);

    servoAngle = angle;

    myServo.write(servoAngle);

    Serial.print("Servo angle: ");
    Serial.println(servoAngle);

    server.send(200, "text/plain", "Servo moved");

  } else {

    server.send(400, "text/plain", "Missing angle");

  }
}

// =========================
// Setup
// =========================
void setup() {

  Serial.begin(115200);

  // Attach servo
  myServo.setPeriodHertz(50);
  myServo.attach(SERVO_PIN, 500, 2400);

  // Start at center
  myServo.write(90);

  // Connect Wi-Fi
  WiFi.begin(ssid, password);

  Serial.print("Connecting to Wi-Fi");

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");

  }

  Serial.println();
  Serial.println("Wi-Fi connected!");

  Serial.print("ESP32-S3 IP address: ");
  Serial.println(WiFi.localIP());

  // Web server routes
  server.on("/", handleRoot);
  server.on("/servo", handleServo);

  server.begin();

  Serial.println("Web server started!");
}

// =========================
// Loop
// =========================
void loop() {

  server.handleClient();

}
