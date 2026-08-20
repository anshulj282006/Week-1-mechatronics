#define TRIG_PIN 3
#define ECHO_PIN 4
#define BUZZER_PIN 7

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  long duration;
  float distance;

  // Measure distance
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);

  distance = duration * 0.034 / 2;

  // Play notes as distance decreases
  if (distance <= 50 && distance > 40) {
    tone(BUZZER_PIN, 261); // Sa
  }
  else if (distance <= 40 && distance > 30) {
    tone(BUZZER_PIN, 294); // Re
  }
  else if (distance <= 30 && distance > 20) {
    tone(BUZZER_PIN, 330); // Ga
  }
  else if (distance <= 20 && distance > 10) {
    tone(BUZZER_PIN, 349); // Ma
  }
  else if (distance <= 10) {
    tone(BUZZER_PIN, 392); // Pa
  }
  else {
    noTone(BUZZER_PIN);
  }

  delay(100);
}
