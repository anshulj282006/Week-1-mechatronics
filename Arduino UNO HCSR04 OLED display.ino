#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define TRIG_PIN 3
#define ECHO_PIN 4

// Player
int playerX = 20;
int playerY = 50;
const int playerSize = 8;

// Obstacle
int obstacleX = 128;
int obstacleY = 50;
const int obstacleWidth = 6;
const int obstacleHeight = 10;

bool jumping = false;
int jumpVelocity = 0;
const int gravity = 1;

// Score
int score = 0;

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.display();

  randomSeed(analogRead(A0));
}

void loop() {
  // -------- Read ultrasonic sensor --------
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;

  // -------- Jump control --------
  if (distance < 15 && !jumping) {
    jumping = true;
    jumpVelocity = -8;
  }

  // -------- Jump physics --------
  if (jumping) {
    playerY += jumpVelocity;
    jumpVelocity += gravity;

    if (playerY >= 50) {
      playerY = 50;
      jumping = false;
      jumpVelocity = 0;
    }
  }

  // -------- Move obstacle --------
  obstacleX -= 3;

  if (obstacleX < -obstacleWidth) {
    obstacleX = 128;
    score++;
  }

  // -------- Collision detection --------
  bool collision =
    playerX < obstacleX + obstacleWidth &&
    playerX + playerSize > obstacleX &&
    playerY + playerSize > obstacleY;

  // -------- Draw game --------
  display.clearDisplay();

  // Score
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(90, 0);
  display.print(score);

  // Ground
  display.drawLine(0, 58, 128, 58, SSD1306_WHITE);

  // Player square
  display.fillRect(playerX, playerY, playerSize, playerSize, SSD1306_WHITE);

  // Obstacle
  display.fillRect(
    obstacleX,
    obstacleY - obstacleHeight + playerSize,
    obstacleWidth,
    obstacleHeight,
    SSD1306_WHITE
  );

  display.display();

  // -------- Game over --------
  if (collision) {
    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(15, 25);
    display.print("GAME OVER");
    display.display();

    delay(2000);

    // Restart game
    playerY = 50;
    obstacleX = 128;
    score = 0;
  }

  delay(30);
}
