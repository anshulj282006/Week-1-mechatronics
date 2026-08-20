import cv2
import serial
import numpy as np
import time
import winsound

# --- CONFIGURATION ---
# Change this to your Arduino's port if needed
arduino_port = 'COM8'
baud_rate = 9600

# Try to connect to the Arduino
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=0.01)
    time.sleep(2)
    print("Connected to Arduino!")
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

# --- GAME VARIABLES ---
window_width = 800
window_height = 400

# Dinosaur variables
dino_x = 100
dino_width = 50
standing_height = 80
ducking_height = 25
dino_y_base = 350

# Obstacle variables
obs_width = 60
obs_height = 30
obs_x = window_width
obs_y = 290
obs_speed = 12

# Game state
is_ducking = False
was_ducking_last_frame = False
score = 0

print("Starting game... Press 'q' in the window to quit.")

while True:
    # 1. Read data from Arduino
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line == "DUCK":
            is_ducking = True
        elif line == "STAND":
            is_ducking = False

    # Play beep when ducking starts
    if is_ducking and not was_ducking_last_frame:
        winsound.Beep(600, 150)
    was_ducking_last_frame = is_ducking

    # 2. Update Game Logic
    obs_x -= obs_speed

    # Reset obstacle and increase score
    if obs_x < -obs_width:
        obs_x = window_width
        score += 1
        obs_speed += 0.5

        # Set sizes based on ducking state
    if is_ducking:
        current_h = ducking_height
        current_w = dino_width + 25
    else:
        current_h = standing_height
        current_w = dino_width

    current_y = dino_y_base - current_h

    # 3. Basic Collision Detection (AABB)
    if (dino_x < obs_x + obs_width and
            dino_x + current_w > obs_x and
            current_y < obs_y + obs_height and
            current_y + current_h > obs_y):
        winsound.Beep(200, 500)
        print(f"GAME OVER! Final Score: {score}")
        score = 0
        obs_x = window_width
        obs_speed = 12
        time.sleep(1)

        # 4. Render Graphics using OpenCV
    # Background (Sky Blue)
    frame = np.zeros((window_height, window_width, 3), dtype=np.uint8)
    frame[:] = (235, 206, 135)

    # Sun
    cv2.circle(frame, (700, 60), 40, (0, 221, 255), -1)

    # Ground (Green)
    cv2.rectangle(frame, (0, dino_y_base), (window_width, window_height), (34, 139, 34), -1)

    # Dinosaur (Green body with black eye)
    dino_color = (0, 200, 0)
    cv2.rectangle(frame, (dino_x, current_y), (dino_x + current_w, current_y + current_h), dino_color, -1)
    eye_x = dino_x + current_w - 12
    eye_y = current_y + 12
    cv2.circle(frame, (eye_x, eye_y), 4, (0, 0, 0), -1)

    # Obstacle (Red bird)
    obs_int_x = int(obs_x)
    cv2.rectangle(frame, (obs_int_x, obs_y), (obs_int_x + obs_width, obs_y + obs_height), (0, 0, 180), -1)
    cv2.line(frame, (obs_int_x + 30, obs_y), (obs_int_x + 15, obs_y - 15), (0, 0, 180), 3)
    cv2.line(frame, (obs_int_x + 30, obs_y + obs_height), (obs_int_x + 15, obs_y + obs_height + 15), (0, 0, 180), 3)

    # UI Text
    cv2.putText(frame, f"SCORE: {score}", (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (50, 50, 50), 2)

    if is_ducking:
        cv2.putText(frame, "DUCKING!", (20, 80), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "RUNNING", (20, 80), cv2.FONT_HERSHEY_DUPLEX, 0.8, (70, 70, 70), 2)

    # Display the window
    cv2.imshow("Interactive Dino Game", frame)

    # 5. Handle Window Exit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Cleanup
ser.close()
cv2.destroyAllWindows()
