import cv2
import numpy as np
import serial
import time
import random

# ===========================
# High Score
# ===========================

try:
    with open("highscore.txt","r") as f:
        high_score=int(f.read())
except:
    high_score=0


def save_highscore():

    with open("highscore.txt","w") as f:
        f.write(str(high_score))

# ===========================
# Arduino Configuration
# ===========================

PORT = "COM8"          # <-- Change if your Arduino uses another COM port
BAUD = 9600

try:
    ser = serial.Serial(PORT, BAUD)
    time.sleep(2)
    print("Arduino Connected")
except:
    print("Arduino Not Connected")
    ser = None


# ===========================
# Window Settings
# ===========================

WIDTH = 900
HEIGHT = 600

GROUND_HEIGHT = 80

SKY = (255,220,120)
GROUND = (70,170,70)

bird_x = 180
bird_y = 250

bird_radius = 18

bird_velocity = 0

target_y = bird_y

SMOOTHNESS = 0.12


# ===========================
# Read Potentiometer
# ===========================

def read_pot():

    global target_y

    if ser is None:
        return

    if ser.in_waiting:

        try:

            value = int(ser.readline().decode().strip())

            value = max(0,min(1023,value))

            target_y = np.interp(value,[0,1023],[520,60])

        except:
            pass


# ===========================
wing = 0

def draw_bird(img, x, y):

    global wing

    wing += 0.4

    flap = int(np.sin(wing) * 10)

    # Body
    cv2.circle(img, (x, y), 18, (0,255,255), -1)

    # Wing
    cv2.ellipse(
        img,
        (x-5, y+flap),
        (13,8),
        20,
        0,
        360,
        (0,220,220),
        -1
    )

    # Eye
    cv2.circle(img,(x+6,y-6),4,(255,255,255),-1)
    cv2.circle(img,(x+7,y-6),2,(0,0,0),-1)

    # Beak
    pts=np.array([
        [x+18,y],
        [x+30,y-4],
        [x+18,y+5]
    ])

    cv2.fillPoly(img,[pts],(0,150,255))
# ===========================

wing = 0

def draw_bird(img,x,y):

    global wing

    wing += 0.35

    wing_offset = int(6*np.sin(wing))

    # Body
    cv2.circle(img,(x,y),18,(0,255,255),-1)

    # Wing
    cv2.ellipse(img,
                (x-5,y+wing_offset),
                (12,8),
                0,
                0,
                360,
                (0,220,220),
                -1)

    # Eye
    cv2.circle(img,(x+6,y-6),3,(255,255,255),-1)
    cv2.circle(img,(x+7,y-6),1,(0,0,0),-1)

    # Beak
    pts=np.array([[x+18,y],[x+28,y-3],[x+18,y+4]])

    cv2.fillPoly(img,[pts],(0,140,255))


# ===========================
cloud_offset = 0

def draw_background(img):

    global cloud_offset

    # Gradient Sky
    for y in range(HEIGHT):
        blue = 255 - int(y * 0.15)
        green = 220 - int(y * 0.10)
        img[y, :] = (blue, green, 120)

    # Sun
    cv2.circle(img, (760, 90), 45, (0, 255, 255), -1)

    # Clouds
    cloud_offset -= 2

    if cloud_offset < -220:
        cloud_offset = 0

    for i in range(6):

        x = i * 220 + cloud_offset

        cv2.circle(img, (x, 90), 22, (255,255,255), -1)
        cv2.circle(img, (x+25,75), 28, (255,255,255), -1)
        cv2.circle(img, (x+55,90), 22, (255,255,255), -1)

    # Ground

    cv2.rectangle(
        img,
        (0, HEIGHT-GROUND_HEIGHT),
        (WIDTH, HEIGHT),
        (80,180,70),
        -1
    )

    # Grass

    for x in range(0, WIDTH, 18):

        cv2.line(
            img,
            (x, HEIGHT-GROUND_HEIGHT),
            (x+5, HEIGHT-GROUND_HEIGHT-10),
            (20,120,20),
            2
        )
# ===========================

ground_offset = 0

def draw_background(img):

    update_pipes()
    draw_pipes(frame)

    global ground_offset

    img[:] = SKY

    # Clouds
    for i in range(5):

        cx = (i*220 + ground_offset)%1100 -100

        cv2.circle(img,(cx,80),22,(255,255,255),-1)
        cv2.circle(img,(cx+20,70),28,(255,255,255),-1)
        cv2.circle(img,(cx+42,82),22,(255,255,255),-1)

    # Ground

    cv2.rectangle(img,
                  (0,HEIGHT-GROUND_HEIGHT),
                  (WIDTH,HEIGHT),
                  GROUND,
                  -1)

    # Moving grass

    ground_offset -= 4

    if ground_offset<-220:
        ground_offset=0

    for x in range(-220,WIDTH+220,40):

        xx=x+ground_offset

        cv2.line(img,
                 (xx,HEIGHT-GROUND_HEIGHT),
                 (xx+20,HEIGHT),
                 (20,120,20),
                 2)
# ===========================
def draw_pipes(img):

    for pipe in pipes:

        x = int(pipe["x"])
        h = pipe["height"]

        # Top Pipe
        cv2.rectangle(
            img,
            (x,0),
            (x+PIPE_WIDTH,h),
            (40,170,40),
            -1
        )

        cv2.rectangle(
            img,
            (x,h-18),
            (x+PIPE_WIDTH,h),
            (20,120,20),
            -1
        )

        # Highlight
        cv2.line(
            img,
            (x+10,0),
            (x+10,h),
            (120,255,120),
            3
        )

        y2 = h + PIPE_GAP

        # Bottom Pipe
        cv2.rectangle(
            img,
            (x,y2),
            (x+PIPE_WIDTH,HEIGHT-GROUND_HEIGHT),
            (40,170,40),
            -1
        )

        cv2.rectangle(
            img,
            (x,y2),
            (x+PIPE_WIDTH,y2+18),
            (20,120,20),
            -1
        )

        cv2.line(
            img,
            (x+10,y2),
            (x+10,HEIGHT-GROUND_HEIGHT),
            (120,255,120),
            3
        )
# ===========================

PIPE_WIDTH = 90
PIPE_GAP = 180
PIPE_SPEED = 6

pipes = []

for i in range(4):
    h = random.randint(120, 320)

    pipes.append({
        "x": WIDTH + i * 250,
        "height": h
    })


def update_pipes():

    global pipes

    for pipe in pipes:

        pipe["x"] -= PIPE_SPEED

    # Recycle pipes
    if pipes[0]["x"] < -PIPE_WIDTH:

        pipes.pop(0)

        h = random.randint(120, 320)

        pipes.append({
            "x": pipes[-1]["x"] + 250,
            "height": h
        })


def draw_pipes(img):

    for pipe in pipes:

        x = int(pipe["x"])
        h = pipe["height"]

        # Top Pipe
        cv2.rectangle(
            img,
            (x, 0),
            (x + PIPE_WIDTH, h),
            (0, 180, 0),
            -1
        )

        # Pipe cap
        cv2.rectangle(
            img,
            (x - 5, h - 20),
            (x + PIPE_WIDTH + 5, h),
            (0, 140, 0),
            -1
        )

        # Bottom Pipe
        y2 = h + PIPE_GAP

        cv2.rectangle(
            img,
            (x, y2),
            (x + PIPE_WIDTH, HEIGHT - GROUND_HEIGHT),
            (0, 180, 0),
            -1
        )

        cv2.rectangle(
            img,
            (x - 5, y2),
            (x + PIPE_WIDTH + 5, y2 + 20),
            (0, 140, 0),
            -1
        )
# ===========================
# Game Variables
# ===========================

score = 0
high_score = 0
game_over = False

font = cv2.FONT_HERSHEY_SIMPLEX


def restart_game():

    global pipes
    global score
    global bird_y
    global target_y
    global game_over

    score = 0
    game_over = False

    bird_y = 250
    target_y = 250

    pipes.clear()

    for i in range(4):

        h = random.randint(120,320)

        pipes.append({
            "x": WIDTH+i*250,
            "height": h
        })


def check_collision():

    global game_over

    # Screen boundaries
    if bird_y < 20:
        game_over = True

    if bird_y > HEIGHT-GROUND_HEIGHT-20:
        game_over = True

    # Pipe Collision

    for pipe in pipes:

        x = pipe["x"]
        h = pipe["height"]

        # Bird overlaps pipe in X direction

        if bird_x+18 > x and bird_x-18 < x+PIPE_WIDTH:

            # Hits top pipe
            if bird_y-18 < h:
                game_over = True

            # Hits bottom pipe
            if bird_y+18 > h+PIPE_GAP:
                game_over = True


def update_score():

    global score
    global high_score

    for pipe in pipes:

        if not pipe.get("passed",False):

            if pipe["x"]+PIPE_WIDTH < bird_x:

                pipe["passed"]=True

                score += 1

                if score>high_score:
                    high_score=score


def draw_hud(img):

    cv2.putText(img,
                f"Score : {score}",
                (20,40),
                font,
                1,
                (255,255,255),
                2)

    cv2.putText(img,
                f"Best : {high_score}",
                (20,80),
                font,
                1,
                (255,255,255),
                2)

    if game_over:

        cv2.rectangle(img,
                      (180,180),
                      (720,430),
                      (40,40,40),
                      -1)

        cv2.rectangle(img,
                      (180,180),
                      (720,430),
                      (255,255,255),
                      3)

        cv2.putText(img,
                    "GAME OVER",
                    (260,260),
                    font,
                    1.8,
                    (0,0,255),
                    4)

        cv2.putText(img,
                    f"Score : {score}",
                    (320,320),
                    font,
                    1,
                    (255,255,255),
                    2)

        cv2.putText(img,
                    "Press R to Restart",
                    (250,380),
                    font,
                    1,
                    (0,255,255),
                    2)
coin_spin = 0

def draw_coins(img):

    global score
    global coin_spin

    coin_spin += 0.2

    r = int(10 + 2*np.sin(coin_spin))

    for pipe in pipes:

        cx = int(pipe["x"]+PIPE_WIDTH/2)
        cy = int(pipe["height"]+PIPE_GAP/2)

        cv2.circle(img,(cx,cy),r,(0,215,255),-1)

        if abs(cx-bird_x)<18 and abs(cy-bird_y)<18:

            pipe["passed"]=True

    for pipe in pipes:

        cx = int(pipe["x"] + PIPE_WIDTH/2)
        cy = int(pipe["height"] + PIPE_GAP/2)

        cv2.circle(img,(cx,cy),10,(0,215,255),-1)
        cv2.circle(img,(cx,cy),10,(0,180,220),2)
# ===========================
# Main Loop
# ===========================

while True:

    read_pot()

    frame=np.zeros((HEIGHT,WIDTH,3),dtype=np.uint8)

    draw_background(frame)

    if not game_over:

        bird_y += (target_y-bird_y)*SMOOTHNESS

        update_pipes()

        check_collision()

        update_score()

    draw_pipes(frame)

    draw_bird(frame,bird_x,int(bird_y))

    draw_hud(frame)

    cv2.imshow("Flappy Bird - OpenCV",frame)

    key=cv2.waitKey(20)&0xFF

    if key==27:
        break

    if game_over and key==ord('r'):
        restart_game()
