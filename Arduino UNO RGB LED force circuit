const int forceSensor = A0;

const int redPin = 7;
const int greenPin = 8;
const int bluePin = 9;

void setup() {
  Serial.begin(9600);

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  int forceValue = analogRead(forceSensor);

  // Map sensor value to force range 0–150
  int force = map(forceValue, 0, 1023, 0, 150);
  force = constrain(force, 0, 150);

  Serial.print("Force: ");
  Serial.println(force);

  int red, green, blue;

  if (force <= 75) {
    // Gradual transition: Red → Green
    red = map(force, 0, 75, 255, 0);
    green = map(force, 0, 75, 0, 255);
    blue = 0;
  }
  else {
    // Gradual transition: Green → Blue
    red = 0;
    green = map(force, 76, 150, 255, 0);
    blue = map(force, 76, 150, 0, 255);
  }

  // Common Anode RGB LED — values are inverted
  analogWrite(redPin, 255 - red);
  analogWrite(greenPin, 255 - green);
  analogWrite(bluePin, 255 - blue);

  delay(50);
}
