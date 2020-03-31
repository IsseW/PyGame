import pygame
from noise import perlin
import math
import random

pygame.init()

noise = perlin.SimplexNoise()

seed = random.randint(0, 100000)
amplitude = 100

myfont = pygame.font.SysFont('Comic Sans MS', 30)

width = 600
height = 400

smallHeight = height / 4

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
thickness = 4
screen = pygame.display.set_mode((width, height))


def getValue(x):
    return noise.noise2(x / float(200), seed)

def getArray(length, start):
    arr = []
    for i in range(length):
        arr.append(getValue(start))
        start += 1
    return arr, start
        
values, offset = getArray(width, 0)


def getNext(arr, x):
    del arr[0]
    arr.append(getValue(x))
    x += 1
    return arr, x

def minMax(x):
    minY = height / 2  - (values[int(x)] * amplitude + smallHeight / 2)
    maxY = minY + smallHeight
    return minY, maxY
def center(x):
    return height / 2  - (values[int(x)] * amplitude)
def drawValue(x):
    minY, maxY = minMax(x)
    color = int(70 + abs(500 - (offset + x) % 1000) / 6.41)
    pygame.draw.rect(screen, (color, color, color), (x, minY, 1, maxY - minY))
    pygame.draw.rect(screen, BLACK, (x, minY - thickness / 2, 1, thickness))
    pygame.draw.rect(screen, BLACK, (x, maxY - thickness / 2, 1, thickness))

playerX = width / 2
playerY = center(playerX)
playerRadius = 10

def draw():
    screen.fill(RED)
    for i in range(len(values)):
        drawValue(i)
    pygame.draw.circle(screen, WHITE, (int(playerX), int(playerY)), int(playerRadius))
    textsurface = myfont.render(str(int((offset - width) / 10)), False, (0, 0, 0))
    screen.blit(textsurface,(0,0))


def checkCollision():
    for i in range(-int(playerRadius), int(playerRadius)):
        y = math.sqrt(playerRadius * playerRadius - i * i)
        minY, maxY = minMax(playerX + i)
        if playerY - y < minY: return True
        if playerY + y > maxY: return True
    return False

    
done = False
lastTick = 0
tick = 16
speed = 3
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    doTick = pygame.time.get_ticks() - lastTick > tick
    if doTick:
        lastTick = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            playerY -= speed
        elif keys[pygame.K_s]:
            playerY += speed
        if checkCollision():
            seed = random.randint(0, 100000)
            values, offset = getArray(width, 0)
            playerX = width / 2
            playerY = center(playerX)
            tick = 16
            playerRadius = 10
            amplitude = 100
        values, offset = getNext(values, offset)
        draw()
        tick -= 0.0001
        amplitude += 0.01
        pygame.display.flip()
        
    

