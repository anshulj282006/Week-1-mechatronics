#include <Adafruit_NeoPixel.h>

#define LED_PIN 6
#define NUM_LEDS 1

Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.setBrightness(80);
  strip.show();
}

void loop() {
  // Rainbow colours
  strip.setPixelColor(0, strip.Color(255, 0, 0)); // Red
  strip.show();
  delay(500);

  strip.setPixelColor(0, strip.Color(0, 255, 0)); // Green
  strip.show();
  delay(500);

  strip.setPixelColor(0, strip.Color(0, 0, 255)); // Blue
  strip.show();
  delay(500);
}
