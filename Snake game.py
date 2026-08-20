import cv2
import numpy as np
import socket
import threading
import random
import time

# ==========================================
# 1. NETWORK SETUP (Talks to the ESP32)
# ==========================================
ESP32_IP = '192.168.4.1'
PORT = 8080
mouth_is_open = False
game_running = True


def receive_sensor_data():
    """Background thread to listen to the ESP32 sensor data"""
    global mouth_is_open, game_running
    while game_running:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect((ESP32_IP, PORT))
                buffer = ""
                while game_running:
                    data = s.recv(1024).decode()
                    if not data: break
                    buffer += data
                    if '\n' in buffer:
                        lines = buffer.split('\n')
                        latest_state = lines[-2]
                        buffer = lines[-1]
                        mouth_is_open = (latest_state == "OPEN")
        except:
            time.sleep(1)  # Retry connection if lost


# Start the network listener in the background
net_thread = threading.Thread(target=receive_sensor_data, daemon=True)
net_thread.start()

# ==========================================
# 2. GAME SETUP & GRAPHICS ENGINE
# ==========================================
WIDTH, HEIGHT = 1920, 700
score = 0
game_over = False
objects = []
spawn_timer = 0

# Note: OpenCV uses BGR (Blue, Green, Red) instead of RGB
COLOR_GREEN = (76, 177, 34)
COLOR_RED = (36, 28, 237)
COLOR_GRAY = (127, 127, 127)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)


def spawn_object():
    """Randomly spawns a fruit or a rock"""
    obj_type = 'fruit' if random.randint(1, 10) <= 7 else 'rock'
    objects.append({'x': WIDTH, 'y': HEIGHT // 2, 'type': obj_type})


def draw_snake_head(frame, x, y, is_open):
    """Draws the snake on the OpenCV frame"""
    # Base head
    cv2.circle(frame, (x, y), 50, COLOR_GREEN, -1)

    # Eye
    cv2.circle(frame, (x, y - 20), 10, COLOR_WHITE, -1)
    cv2.circle(frame, (x, y - 20), 5, COLOR_BLACK, -1)

    if is_open:
        # Draw open mouth (A black triangle polygon)
        pts = np.array([[x, y], [x + 60, y - 30], [x + 60, y + 30]], np.int32)
        cv2.fillPoly(frame, [pts], COLOR_BLACK)
    else:
        # Draw closed mouth (A black line)
        cv2.line(frame, (x, y), (x + 50, y), COLOR_BLACK, 4)


# ==========================================
# 3. MAIN GAME LOOP
# ==========================================
while game_running:
    # Create a blank black canvas
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    if not game_over:
        # Spawn logic
        spawn_timer += 1
        if spawn_timer > 30:  # Spawn a new object approximately every second
            spawn_object()
            spawn_timer = 0

        # Move and draw objects
        for obj in objects[:]:
            obj['x'] -= 10  # Movement speed

            # Collision Detection (Snake head is at x=100)
            if 70 < obj['x'] < 130:
                if mouth_is_open:
                    if obj['type'] == 'fruit':
                        score += 1
                        objects.remove(obj)
                    elif obj['type'] == 'rock':
                        game_over = True
                else:
                    # Mouth closed, item bounces off
                    objects.remove(obj)

            # Remove objects that went off screen
            elif obj['x'] < -50:
                objects.remove(obj)

            # Draw the object if it hasn't been removed
            if obj in objects:
                if obj['type'] == 'fruit':
                    cv2.circle(frame, (obj['x'], obj['y']), 20, COLOR_RED, -1)
                    # Stem
                    cv2.rectangle(frame, (obj['x'] - 2, obj['y'] - 25), (obj['x'] + 2, obj['y'] - 15), COLOR_GREEN, -1)
                else:
                    # Draw a rock polygon
                    pts = np.array([
                        [obj['x'], obj['y'] - 20], [obj['x'] + 25, obj['y']],
                        [obj['x'] + 15, obj['y'] + 20], [obj['x'] - 15, obj['y'] + 20],
                        [obj['x'] - 25, obj['y']]
                    ], np.int32)
                    cv2.fillPoly(frame, [pts], COLOR_GRAY)

        # Draw Snake Head
        draw_snake_head(frame, 100, HEIGHT // 2, mouth_is_open)

        # Draw Score
        cv2.putText(frame, f"Score: {score}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_WHITE, 2)

        if not mouth_is_open and score == 0:
            cv2.putText(frame, "Put hand near sensor to open mouth!", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        COLOR_GRAY, 2)

    else:
        # Game Over Screen
        cv2.putText(frame, "GAME OVER", (WIDTH // 2 - 160, HEIGHT // 2 - 20), cv2.FONT_HERSHEY_DUPLEX, 1.8, COLOR_RED,
                    4)
        cv2.putText(frame, f"Final Score: {score}", (WIDTH // 2 - 90, HEIGHT // 2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    COLOR_WHITE, 2)
        cv2.putText(frame, "Press SPACE to Restart", (WIDTH // 2 - 160, HEIGHT // 2 + 90), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, COLOR_GRAY, 2)

    # Render the frame to the screen
    cv2.imshow("Wi-Fi Ultrasonic Snake (OpenCV)", frame)

    # Handle Keyboard Inputs & Frame Rate
    key = cv2.waitKey(30) & 0xFF  # Controls frame rate (~30 FPS)

    if key == 27:  # Press 'ESC' to quit
        game_running = False
    elif key == ord(' ') and game_over:  # Press 'Spacebar' to restart
        score = 0
        objects.clear()
        game_over = False

# Clean up windows when closed
cv2.destroyAllWindows()
