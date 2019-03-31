import pygame
import random
import math
import numpy as np
import cv2

pygame.init()

SCREENWIDTH = 1280
SCREENHEIGHT = 800

#frame config
# in mm
WIDTH = 3200
HEIGHT = 2400

# LED pitch in mm (here for 30LEDs / m)
PITCH = 33

# Price per 5m reel
PRICE = 9.75

# LEDs per 5m reel
LEDSPERSTRIP = 150.

DENSITY = 12

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT))

done = False

def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points

totalLEDs = 0

def createStrip(surface, videoframe, start, end):
    pygame.draw.line(surface, (100,100,100), start, end, 10)

    points = get_line(start[0], start[1], end[0], end[1])
    global PITCH
    global totalLEDs
    lastpoint = (0, 0)
    for i in points:
        if math.hypot(lastpoint[0] - i[0], lastpoint[1] - i[1]) > PITCH:
            pygame.draw.circle(surface, tuple(videoframe[(i[1], i[0])]), i, 10)
            totalLEDs = totalLEDs + 1
            lastpoint = i
    #pygame.draw.polygon (display_box, white, [(140, 160), (140, 200), (1060, 200), (1060, 160)])

cap = cv2.VideoCapture('simpson.mp4')

clock = pygame.time.Clock()
seed = random.randint(0, 99999999999999)
random.seed(seed)

printed = False

fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (SCREENHEIGHT, SCREENWIDTH))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    random.seed(seed)

    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (WIDTH+1, HEIGHT+1))

    totalLEDs = 0

    for i in range(DENSITY):
        createStrip(surface, frame, (random.randint(0, WIDTH), 0), (random.randint(0, WIDTH), HEIGHT))
        createStrip(surface, frame, (0, random.randint(0, HEIGHT)), (WIDTH, random.randint(0, HEIGHT)))

        createStrip(surface, frame, (random.randint(0, WIDTH), 0), (0, random.randint(0, HEIGHT)))
        createStrip(surface, frame, (random.randint(0, WIDTH), 0), (WIDTH, random.randint(0, HEIGHT)))

        createStrip(surface, frame, (random.randint(0, WIDTH), HEIGHT), (0, random.randint(0, HEIGHT)))
        createStrip(surface, frame, (random.randint(0, WIDTH), HEIGHT), (WIDTH, random.randint(0, HEIGHT)))

    if printed is False:
        print totalLEDs
        print ((totalLEDs / LEDSPERSTRIP) * PRICE)
    printed = True

    clock.tick(30)

    pygame.transform.scale (surface, (SCREENWIDTH, SCREENHEIGHT), screen)
    pygame.display.flip()

    #x3 = pygame.surfarray.pixels3d(screen)
    #print x3.shape
    #out.write(x3)
