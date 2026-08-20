const int buttonPin = 2;
const int greenLED = 12;
const int yellowLED = 10;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);

  pinMode(greenLED, OUTPUT);
  pinMode(yellowLED, OUTPUT);
}

void loop() {
  int buttonState = digitalRead(buttonPin);

  if (buttonState == LOW) {
    // Button pressed
    digitalWrite(greenLED, HIGH);
    digitalWrite(yellowLED, LOW);
  } 
  else {
    // Button released
    digitalWrite(greenLED, LOW);
    digitalWrite(yellowLED, HIGH);
  }
}
