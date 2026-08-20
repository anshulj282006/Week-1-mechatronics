const int buttonPin = 2;
const int led1 = 12;
const int led2 = 10;

unsigned long previousMillis = 0;
const long blinkInterval = 250;  // 0.25 seconds

int led2State = LOW;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
}

void loop() {

  // Push button controls LED 1
  if (digitalRead(buttonPin) == LOW) {
    digitalWrite(led1, HIGH);
  } else {
    digitalWrite(led1, LOW);
  }

  // LED 2 blinks every 0.25 seconds
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= blinkInterval) {
    previousMillis = currentMillis;

    if (led2State == LOW) {
      led2State = HIGH;
    } else {
      led2State = LOW;
    }

    digitalWrite(led2, led2State);
  }
}
