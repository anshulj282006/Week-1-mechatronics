#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define TRIG_PIN 3
#define ECHO_PIN 4

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Ultrasonic");
  lcd.setCursor(0, 1);
  lcd.print("Sensor");
  delay(2000);

  lcd.clear();
}

void loop() {
  long duration;
  float distance;

  // Send ultrasonic pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read echo
  duration = pulseIn(ECHO_PIN, HIGH);

  // Calculate distance in cm
  distance = duration * 0.034 / 2;

  // Display distance
  lcd.setCursor(0, 0);
  lcd.print("Distance: ");

  lcd.setCursor(0, 1);
  lcd.print(distance);
  lcd.print(" cm   ");

  delay(500);
}
