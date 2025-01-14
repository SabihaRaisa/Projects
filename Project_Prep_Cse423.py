from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

W_Width, W_Height = 750, 750
speed = 2
ball_size = 2
r, g, b, a = 0, 0, 0, 0


class Egg:
    def __init__(self, egg_type, x, y):
        self.egg_type = egg_type
        self.x = x
        self.y = y
        self.state = 'falling'  # 'falling', 'cracked', 'exploded'
        self.explosion_timer = 0  # Initialize explosion_timer with 0
        self.cracked_timer = 20  # Initialize cracked_timer for cracked state State of the egg (falling, caught, exploded)


def is_bomb(self):
    return self.egg_type == 'BOMB'


def draw_eggs():
    for egg in eggs:
        egg.draw()


import math

normal_egg_points = 1
golden_egg_points = 5
bomb_egg_points = -1

eggs = []
lives = 2

NORMAL = 'normal'
GOLDEN = 'golden'
BOMB = 'bomb'


def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def MidPointLine(x1, y1, x2, y2):
    store = []
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    pE = 2 * dy
    pNE = 2 * dy - 2 * dx
    x = x1
    y = y1
    for i in range(x, x2 + 1):
        store += [[i, y]]
        if d > 0:
            d += pNE
            y += 1
        else:
            d += pE
    return store


def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx > 0 and dy >= 0:
        if abs(dx) > abs(dy):
            return 0
        else:
            return 1
    elif dx <= 0 and dy >= 0:
        if abs(dx) > abs(dy):
            return 3
        else:
            return 2
    elif dx < 0 and dy < 0:
        if abs(dx) > abs(dy):
            return 4
        else:
            return 5
    elif dx >= 0 and dy < 0:
        if abs(dx) > abs(dy):
            return 7
        else:
            return 6


def convertToZone0(zone, x1, y1, x2, y2):
    if zone == 1:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    elif zone == 2:
        x1, y1 = y1, -x1
        x2, y2 = y2, -x2
    elif zone == 3:
        x1, y1 = -x1, y1
        x2, y2 = -x2, y2
    elif zone == 4:
        x1, y1 = -x1, -y1
        x2, y2 = -x2, -y2
    elif zone == 5:
        x1, y1 = -y1, -x1
        x2, y2 = -y2, -x2
    elif zone == 6:
        x1, y1 = -y1, x1
        x2, y2 = -y2, x2
    elif zone == 7:
        x1, y1 = x1, -y1
        x2, y2 = x2, -y2
    return x1, y1, x2, y2


def convertToZoneM(color, zone, points):
    s = 2
    glColor3f(color[0], color[1], color[2])
    if zone == 0:
        for x, y in points:
            draw_points(x, y, s)
    elif zone == 1:
        for x, y in points:
            draw_points(y, x, s)
    elif zone == 2:
        for x, y in points:
            draw_points(-y, x, s)
    elif zone == 3:
        for x, y in points:
            draw_points(-x, y, s)
    elif zone == 4:
        for x, y in points:
            draw_points(-x, -y, s)
    elif zone == 5:
        for x, y in points:
            draw_points(-y, -x, s)
    elif zone == 6:
        for x, y in points:
            draw_points(y, -x, s)
    elif zone == 7:
        for x, y in points:
            draw_points(x, -y, s)


def drawLines(color, x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    x1, y1, x2, y2 = convertToZone0(zone, x1, y1, x2, y2)
    points = MidPointLine(x1, y1, x2, y2)
    convertToZoneM(color, zone, points)


def draw_circle(X, Y, r):
    x, y = 0, r
    d = 1 - r
    numZone = 8
    while x < y:
        for i in range(numZone):
            x0, y0 = zoneConversion(x, y, i)
            draw_points(x0 + X, y0 + Y, 1)
        if d > 0:
            d += 2 * x - 2 * y + 5
            x += 1
            y -= 1
        else:
            d += 2 * x + 3
            x += 1


def zoneConversion(x, y, zone):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y


def specialKeyListener(key, x, y):
    global gb1, gb2, gb3, gb4
    speedCount = 20
    if key == GLUT_KEY_RIGHT:
        if gb1[2] >= 240:
            pass
        else:
            if pause == False:
                gb1[0] += speedCount
                gb1[2] += speedCount
                gb2[0] += speedCount
                gb2[2] += speedCount
                gb3[0] += speedCount
                gb3[2] += speedCount
                gb4[0] += speedCount
                gb4[2] += speedCount
    if key == GLUT_KEY_LEFT:
        if gb1[0] <= -250:
            pass
        else:
            if pause == False:
                gb1[0] -= speedCount
                gb1[2] -= speedCount
                gb2[0] -= speedCount
                gb2[2] -= speedCount
                gb3[0] -= speedCount
                gb3[2] -= speedCount
                gb4[0] -= speedCount
                gb4[2] -= speedCount
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global ballx, bally, new, initY, gameInfo, pause, bColor, miss
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):
            if x >= 6 and x <= 50 and y >= 10 and y <= 45:
                initY = 140
                print('Starting Over!')
                gameInfo = 0
                pause = False
                miss = 0
                bColor = [1, 1, 1]
                lives = 3  # Reset lives
                eggs.clear()  # Clear existing eggs
                init_eggs()  # Initialize eggs
    glutPostRedisplay()


xRandom = -15
initY = 100
gb1 = [-70, -220, 70, -220]
gb2 = [-70, -250, 70, -250]
gb3 = [-70, -250, -80, -180]
gb4 = [70, -250, 80, -180]
pause = False
bColor = [1, 0, 0.5]
R3color = random.random()

ranColor = [R3color, R3color, R3color]

duck_positions = [-200, -100, 0, 100, 200]  # Positions of the ducks

gameInfo = 0
egg_spawn_timer = 0
lives = 3
miss = 0

import random


def draw_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def generate_blast_path(x, y, length, spread=2):
    points = []
    for i in range(length):
        x += random.randint(-1, 1)
        y += random.randint(-spread, spread)
        points.append((x, y))
    return points


def draw_exploded_egg(x, y):
    explosion_color = [1, 0.0, 0.0]
    glColor3f(explosion_color[0], explosion_color[1], explosion_color[2])

    explosion_length = 200000
    main_blast_points = generate_blast_path(x, y, explosion_length)

    for point in main_blast_points:
        draw_point(point[0], point[1])

    for _ in range(3):
        branch_start = random.choice(main_blast_points)
        branch_length = random.randint(10, 20)
        branch_spread = random.randint(2, 4)
        side_blast_points = generate_blast_path(branch_start[0], branch_start[1], branch_length, branch_spread)

        for point in side_blast_points:
            draw_point(point[0], point[1])

    for _ in range(10):
        rand_x = random.randint(x - 50, x + 50)
        rand_y = random.randint(y - 50, y + 50)
        draw_point(rand_x, rand_y)


def draw_crack(x, y):
    explosion_color = [1, 1, 0]
    glColor3f(explosion_color[0], explosion_color[1], explosion_color[2])
    for _ in range(6):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(10, 20)
        x_offset = radius * math.cos(angle)
        y_offset = radius * math.sin(angle)
        draw_circle(x + x_offset, y + y_offset, 5)


def drawHeart(x, y, color):
    glColor3f(*color)
    drawLines(color, x - 10, y + 10, x - 15, y + 20)
    drawLines(color, x - 15, y + 20, x - 20, y + 15)
    drawLines(color, x - 20, y + 15, x - 25, y + 5)
    drawLines(color, x - 10, y + 10, x, y + 20)
    drawLines(color, x, y + 20, x + 5, y + 15)
    drawLines(color, x + 5, y + 15, x + 10, y + 5)
    drawLines(color, x - 25, y + 5, x - 10, y - 10)
    drawLines(color, x + 10, y + 5, x - 10, y - 10)


def display():
    global r, g, b, a, rains
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(r, g, b, a)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    # busket drawing
    global gb1, gb2, gb3, gb4, bColor, ranColor
    z_offset = 0.2
    drawLines(bColor, gb1[0], gb1[1], gb1[2], gb1[3])
    drawLines(bColor, gb2[0], gb2[1], gb2[2], gb2[3])
    drawLines(bColor, gb3[0], gb3[1], gb3[2], gb3[3])
    drawLines(bColor, gb4[0], gb4[1], gb4[2], gb4[3])

    ck = [1, 1, 1]
    ch = [1, 0.6, 0]
    cl = [1, 0, 0]
    cj = [1.0, 0.8, 0.0]
    ct = [1, 0.0, 0.0]

    # ========Duck 1==========
    # Main shape
    drawLines(cl, -230, 150, -170, 150)  # Top horizontal line
    drawLines(cl, -230, 150, -200, 190)  # Left diagonal to top point
    drawLines(cl, -170, 150, -200, 190)  # Right diagonal to top point

    # Decorations
    drawLines(ck, -220, 170, -210, 170)  # Left small horizontal line
    drawLines(ck, -180, 170, -190, 170)  # Right small horizontal line
    drawLines(ch, -210, 160, -190, 160)  # Central horizontal line

    # Extra top detail
    drawLines(cj, -210, 200, -190, 200)  # Topmost horizontal line
    drawLines(cj, -210, 200, -200, 190)  # Left diagonal connecting to the top
    drawLines(cj, -190, 200, -200, 190)  # Right diagonal connecting to the top

    # Adding edges
    drawLines(cl, -230, 150, -230, 110)  # Left vertical edge
    drawLines(cl, -170, 150, -170, 110)  # Right vertical edge
    drawLines(cl, -230, 110, -170, 110)  # Bottom horizontal edge
    drawLines(cl, -200, 190, -200, 150)  # Top vertical edge

    # Adding wings
    # Left wing
    drawLines(ct, -230, 130, -260, 160)  # Left diagonal of left wing
    drawLines(ct, -260, 160, -230, 150)  # Connecting back to shape

    # Right wing
    drawLines(ct, -170, 130, -140, 160)  # Right diagonal of right wing
    drawLines(ct, -140, 160, -170, 150)  # Connecting back to shape

    # Adding legs
    # Left leg
    drawLines(ch, -220, 110, -220, 80)  # Left vertical of left leg
    drawLines(ch, -210, 110, -210, 80)  # Right vertical of left leg
    drawLines(ch, -220, 80, -210, 80)  # Bottom horizontal of left leg

    # Right leg
    drawLines(ch, -190, 110, -190, 80)  # Left vertical of right leg
    drawLines(ch, -180, 110, -180, 80)  # Right vertical of right leg
    drawLines(ch, -190, 80, -180, 80)  # Bottom horizontal of right leg

    # Adding tail
    drawLines(cl, -200, 120, -210, 100)  # Left diagonal of tail
    drawLines(cl, -210, 100, -190, 100)  # Bottom horizontal of tail
    drawLines(cl, -190, 100, -200, 120)  # Right diagonal of tail

    # ==========================    Duck 2    ============================
    ck = [1, 1, 1]
    ch = [1, 0.6, 0]
    cl = [1, 1, 1]
    cj = [0.8, 0.8, 0.8]
    ct = [1, 1, 0.0]
    drawLines(cl, -130, 150, -100, 190)
    drawLines(cl, -70, 150, -100, 190)
    drawLines(cl, -70, 150, -70, 70)
    drawLines(cl, -130, 70, -130, 150)  # Left edge
    drawLines(ck, -120, 170, -110, 170)
    drawLines(ck, -80, 170, -90, 170)
    drawLines(ch, -110, 160, -90, 160)
    drawLines(cl, -70, 70, -130, 70)
    drawLines(ct, -130, 110, -160, 140)  # Diagonal line for left wing
    drawLines(ct, -160, 140, -130, 150)  # Connecting back to the shape

    # Right wing
    drawLines(ct, -70, 110, -40, 140)  # Diagonal line for right wing
    drawLines(ct, -40, 140, -70, 150)
    drawLines(cj, -130, 70, -100, 40)  # Left diagonal of tail
    drawLines(cj, -100, 40, -70, 70)  # Right diagonal of tail

    drawLines(cl, -120, 70, -120, 40)  # Left vertical of left leg
    drawLines(cl, -80, 70, -80, 40)
    # Left leg
    drawLines(ch, -120, 70, -120, 40)  # Left vertical of left leg
    drawLines(ch, -140, 40, -60, 40)
    # Bottom horizontal of left leg

    # Right leg
    drawLines(ch, -80, 70, -80, 40)  # Left vertical of right leg

    drawLines(ch, -100, 40, -60, 40)  # Bottom horizontal of right leg

    # ========Duck 3==========
    ck = [1, 1, 1]
    ch = [1, 0.6, 0]
    cl = [1, 1, 0]
    cj = [1, 1, 0]
    ct = [1, 1, 0.0]
    # Main shape
    drawLines(cl, -30, 150, 30, 150)  # Top horizontal line
    drawLines(cl, -30, 150, 0, 190)  # Left diagonal to the top point
    drawLines(cl, 30, 150, 0, 190)  # Right diagonal to the top point

    # Decorations for the new shape
    drawLines(ck, -20, 170, -10, 170)  # Left small horizontal line
    drawLines(ck, 20, 170, 10, 170)  # Right small horizontal line
    drawLines(ch, -10, 160, 10, 160)  # Central horizontal line

    # Adding left, right, top, and bottom
    drawLines(cl, -30, 150, -30, 110)  # Left vertical line
    drawLines(cl, 30, 150, 30, 110)  # Right vertical line
    drawLines(cl, -30, 110, 30, 110)  # Bottom horizontal line
    drawLines(cl, 0, 190, 0, 150)  # Top vertical line connecting to the middle

    # Adding wings
    # Left wing
    drawLines(ct, -30, 130, -60, 160)  # Left diagonal of the left wing
    drawLines(ct, -60, 160, -30, 150)  # Connecting back to the shape
    # Right wing
    drawLines(ct, 30, 130, 60, 160)  # Right diagonal of the right wing
    drawLines(ct, 60, 160, 30, 150)  # Connecting back to the shape

    # Adding legs
    # Left leg
    drawLines(ch, -20, 110, -20, 80)  # Left vertical of left leg
    drawLines(ch, -10, 110, -10, 80)  # Right vertical of left leg
    drawLines(ch, -20, 80, -10, 80)  # Bottom horizontal of left leg

    # Right leg
    drawLines(ch, 10, 110, 10, 80)  # Left vertical of right leg
    drawLines(ch, 20, 110, 20, 80)  # Right vertical of right leg
    drawLines(ch, 10, 80, 20, 80)  # Bottom horizontal of right leg

    drawLines(cj, -10, 80, 0, 60)  # Left diagonal of the tail
    drawLines(cj, 0, 60, 10, 80)  # Right diagonal of the tail

    # ========Duck 4==========
    ck = [1, 1, 1]
    ch = [1, 0.6, 0]
    cl = [1, 0, 0]
    cj = [1.0, 0.8, 0.0]
    ct = [1, 0.0, 0.0]
    # Main shape
    drawLines(cl, 130, 150, 70, 150)  # Top horizontal line
    drawLines(cl, 130, 150, 100, 190)  # Left diagonal to the top point
    drawLines(cl, 70, 150, 100, 190)  # Right diagonal to the top point

    # Decorations
    drawLines(ck, 120, 170, 110, 170)  # Left small horizontal line
    drawLines(ck, 80, 170, 90, 170)  # Right small horizontal line
    drawLines(ch, 110, 160, 90, 160)  # Central horizontal line

    # Extra top detail
    drawLines(cj, 110, 200, 90, 200)  # Topmost horizontal line
    drawLines(cj, 110, 200, 100, 190)  # Left diagonal connecting to the top
    drawLines(cj, 90, 200, 100, 190)  # Right diagonal connecting to the top

    # Adding edges
    drawLines(cl, 130, 150, 130, 110)  # Left vertical edge
    drawLines(cl, 70, 150, 70, 110)  # Right vertical edge
    drawLines(cl, 130, 110, 70, 110)  # Bottom horizontal edge
    drawLines(cl, 100, 190, 100, 150)  # Top vertical edge

    # Adding wings
    # Left wing
    drawLines(ct, 130, 130, 160, 160)  # Left diagonal of the left wing
    drawLines(ct, 160, 160, 130, 150)  # Connecting back to shape

    # Right wing
    drawLines(ct, 70, 130, 40, 160)  # Right diagonal of the right wing
    drawLines(ct, 40, 160, 70, 150)  # Connecting back to shape

    # Adding legs
    # Left leg
    drawLines(ch, 120, 110, 120, 80)  # Left vertical of left leg
    drawLines(ch, 110, 110, 110, 80)  # Right vertical of left leg
    drawLines(ch, 120, 80, 110, 80)  # Bottom horizontal of left leg

    # Right leg
    drawLines(ch, 90, 110, 90, 80)  # Left vertical of right leg
    drawLines(ch, 80, 110, 80, 80)  # Right vertical of right leg
    drawLines(ch, 90, 80, 80, 80)  # Bottom horizontal of right leg

    # Adding tail
    drawLines(cj, 100, 120, 110, 100)  # Left diagonal of tail
    drawLines(cj, 110, 100, 90, 100)  # Bottom horizontal of tail
    drawLines(cj, 90, 100, 100, 120)  # Right diagonal of tail

    # ========Duck 5==========
    # Main shape
    ck = [1, 1, 1]
    ch = [1, 0.6, 0]
    cl = [1, 1, 1]
    cj = [0.8, 0.8, 0.8]
    ct = [1, 1, 0.0]
    drawLines(cl, 230, 150, 200, 190)
    drawLines(cl, 170, 150, 200, 190)
    drawLines(ck, 220, 170, 210, 170)
    drawLines(ck, 180, 170, 190, 170)
    drawLines(ch, 210, 160, 190, 160)
    drawLines(ct, 230, 70, 260, 150)  # Left diagonal of left wing (starting from the bottom edge)

    # Right Wing
    drawLines(ct, 170, 70, 140, 150)  # Right diagonal of right wing (starting from the bottom edge)

    # Adding edges
    drawLines(cl, 230, 150, 230, 70)  # Left vertical edge (longer)
    drawLines(cl, 170, 150, 170, 70)  # Right vertical edge (longer)
    drawLines(cl, 230, 70, 170, 70)  # Bottom horizontal edge (longer)

    drawLines(ct, 230, 70, 280, 100)  # Left diagonal of left wing (starting from top edge)
    drawLines(ct, 280, 100, 230, 90)  # Connecting back to the shape
    # Adding Left Triangle on the side
    drawLines(ct, 230, 70, 260, 90)  # Left diagonal of left triangle
    drawLines(ct, 260, 90, 230, 90)  # Top horizontal of left triangle
    drawLines(ct, 230, 90, 230, 70)  # Right vertical of left triangle

    # Adding Right Triangle on the side
    drawLines(ct, 170, 70, 140, 90)  # Right diagonal of right triangle
    drawLines(ct, 140, 90, 170, 90)  # Top horizontal of right triangle
    drawLines(ct, 170, 90, 170, 70)  # Left vertical of right triangle

    # Right Wing (Starting from top edge)
    drawLines(ct, 170, 70, 120, 100)  # Right diagonal of right wing (starting from top edge)
    drawLines(ct, 120, 100, 170, 90)  # Connecting back to the shape

    drawLines(ch, 210, 70, 210, 40)  # Right vertical of left leg
    drawLines(ch, 220, 40, 210, 40)  # Bottom horizontal of left leg

    # Right Leg
    drawLines(ch, 180, 70, 180, 40)  # Left vertical of right leg

    drawLines(ch, 180, 40, 170, 40)  # Bottom horizontal of right leg
    color = [0, 1, 1]  # Exit button creation

    color = [1, 0, 0]  # Restart mechanism
    drawLines(color, -200, 225, -240, 225)
    drawLines(color, -218, 240, -240, 225)
    drawLines(color, -218, 210, -240, 225)

    # Drawing the letter "G"
    # Drawing the letter "E" starting at (5, 240)
    drawLines(color, 5, 240, 5, 210)  # Vertical line for "E"
    drawLines(color, 5, 210, 35, 210)  # Top horizontal line of "E"
    drawLines(color, 35, 210, 35, 225)  # Vertical middle line of "E"
    # drawLines(color, 5, 225, 35, 225)  # Horizontal middle line of "E"
    drawLines(color, 5, 240, 35, 240)  # Bottom horizontal line of "E"

    drawLines(color, 55, 240, 45, 210)  # Left diagonal line (to form "^")
    drawLines(color, 55, 240, 75, 240)
    drawLines(color, 65, 210, 75, 240)  # Right diagonal line (to form "^")
    drawLines(color, 50, 225, 70, 225)  # Horizontal bar in the middle of "A"
    # Drawing the letter "M"
    drawLines(color, 85, 240, 85, 210)  # Left vertical line of "M"
    drawLines(color, 85, 240, 105, 225)  # Left diagonal line of "M"
    drawLines(color, 105, 225, 125, 240)  # Right diagonal line of "M"
    drawLines(color, 125, 240, 125, 210)  # Right vertical line of "M"

    # Drawing the letter "E"
    drawLines(color, 145, 240, 145, 210)  # Vertical line for "E"
    drawLines(color, 145, 210, 175, 210)  # Top horizontal line of "E"

    drawLines(color, 145, 225, 175, 225)  # Horizontal middle line of "E"
    drawLines(color, 145, 240, 175, 240)  # Bottom horizontal line of "E"

    heart_color = [0, 1, 1]  # cyan hearts
    heart_positions = [(-100, 210), (-140, 210), (-180, 210)]  # Positions for 3 hearts

    for i in range(lives):
        drawHeart(*heart_positions[i], heart_color)
    for egg in eggs:
        if egg.state == 'falling':
            if egg.egg_type == NORMAL:
                color = [1, 1, 1]  # White for normal eggs
            elif egg.egg_type == GOLDEN:
                color = [1, 0.84, 0]  # Gold for golden eggs
            elif egg.egg_type == BOMB:
                color = [1, 0, 0]  # Black for bombs

            drawLines(color, egg.x, egg.y, egg.x + 10, egg.y + 5)
            drawLines(color, egg.x + 10, egg.y + 5, egg.x + 15, egg.y + 10)
            drawLines(color, egg.x + 15, egg.y + 10, egg.x + 10, egg.y + 15)
            drawLines(color, egg.x + 10, egg.y + 15, egg.x, egg.y + 20)
            drawLines(color, egg.x, egg.y + 20, egg.x - 10, egg.y + 15)
            drawLines(color, egg.x - 10, egg.y + 15, egg.x - 15, egg.y + 10)
            drawLines(color, egg.x - 15, egg.y + 10, egg.x - 10, egg.y + 5)
            drawLines(color, egg.x - 10, egg.y + 5, egg.x, egg.y)

        elif egg.state == 'exploded':
            draw_exploded_egg(egg.x, egg.y)

        elif egg.state == 'cracked':
            draw_crack(egg.x, egg.y)

    glutSwapBuffers()


gameInfo = 0
miss = 0


def animate():
    glutPostRedisplay()  # Request a redraw of the screen

    global xRandom, initY, gb1, gameInfo, R3color, pause, bColor, ranColor, miss, eggs, egg_spawn_timer, lives, reset_game_state, game_over

    if not pause:  # If the game is not paused
        for egg in eggs:
            if egg.state == 'falling':  # Egg is falling
                egg.y -= speed  # Move the egg down

                if egg.y <= -214:  # Egg has reached the ground level
                    if gb1[0] < egg.x + 20 and gb1[2] > egg.x:  # Egg caught by basket
                        if egg.egg_type == NORMAL:
                            gameInfo += normal_egg_points  # Add points for normal egg
                        elif egg.egg_type == GOLDEN:
                            gameInfo += golden_egg_points  # Add points for golden egg
                        elif egg.egg_type == BOMB:
                            lives = 0  # Decrease lives for bomb
                            egg.state = 'exploded'  # Set egg state to exploded
                            egg.explosion_timer = 20  # Set a timer for explosion
                            if lives <= 0:
                                bColor = [1, 0, 0]  # Game over color
                                print(f'Game Over! Score: {gameInfo}')
                                pause = True  # Pause the game
                        egg.y = 200  # Reset egg position to the top
                        egg.x = random.choice(duck_positions)  # Reset to a random duck position
                        print(f'Score: {gameInfo}')
                    else:  # Egg missed by basket
                        if egg.egg_type == NORMAL or egg.egg_type == GOLDEN or egg.egg_type == BOMB:
                            miss += 1  # Increase miss count
                            egg.state = 'cracked'
                            if miss >= 3:  # Lose a life after 3 misses
                                egg.state = 'cracked'
                                lives -= 1
                                miss = 0  # Reset miss count

                                print(f"You lost a life! Remaining lives: {lives}")
                                if lives <= 0:  # Game over
                                    print(f"Game Over! Score: {gameInfo}")
                                    pause = True  # Pause the game
                            else:
                                egg.state = 'cracked'  # Set egg state to cracked
                                print(f'You missed {miss} egg')
            elif egg.state == 'exploded':  # Egg exploded (bomb)
                egg.explosion_timer -= 1  # Decrease explosion timer
                if egg.explosion_timer > 0:
                    trigger_explosion(egg)  # Trigger explosion animation
                if egg.explosion_timer <= 0:
                    eggs.remove(egg)  # Remove egg after explosion

            elif egg.state == 'cracked':  # Egg cracked
                egg.cracked_timer -= 1  # Decrease cracked timer
                if egg.cracked_timer <= 0:
                    eggs.remove(egg)  # Remove cracked egg

        # Control egg spawning
        egg_spawn_timer += 1  # Increment the spawn timer
        if egg_spawn_timer > 150:  # Adjust this value to control spawn rate
            egg_type = random.choices(
                [NORMAL, GOLDEN, BOMB],
                weights=[70, 20, 10],  # Adjust weights for egg types
                k=1
            )[0]
            eggs.append(Egg(egg_type, random.choice(duck_positions), 200))  # Spawn new egg
            egg_spawn_timer = 0  # Reset spawn timer


def trigger_explosion(egg):
    draw_crack(egg.x, egg.y)


def init_eggs():
    global eggs, duck_positions
    eggs = [Egg(NORMAL, random.choice(duck_positions), 200)]


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)


init_eggs()
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(500, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Chicken Egg Catcher")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()
