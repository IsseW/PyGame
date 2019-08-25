import pygame
import math
import pygame.gfxdraw
import copy
import objects

pygame.init()

width = 200
height = 200

windowWidth = 800
windowHeight = 800

xScale = windowWidth / width
xHalf = xScale / 2
yScale = windowHeight / height
yHalf = yScale / 2

TRANSPARENT = (0,0,0,200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((windowWidth, windowHeight))
rect = pygame.Surface((windowWidth,windowHeight), pygame.SRCALPHA, 32)
rect.fill(TRANSPARENT)

world = []
for x in range(width):
    world.append([])
    for y in range(height):
        world[x].append(0)
clean = copy.deepcopy(world)

def getSquare(x, y):
    return math.floor(x / xScale), math.floor(y / yScale)

def drawSquare(x, y, color):
    pygame.draw.rect(screen, color, (x * xScale, y * yScale, xScale, yScale))

def drawWorld():
    screen.blit(rect, (0, 0))
    for x in range(width):
        for y in range(height):
            if world[x][y] > 0:
                drawSquare(x, y, WHITE)

def neighborCount(x, y):
    count = 0
    left = x > 0
    right = x + 1 < width
    up = y > 0
    down = y + 1 < height
    if left and world[x - 1][y] > 0: count+=1
    if right and world[x + 1][y] > 0: count+=1
    if up and world[x][y - 1] > 0: count+=1
    if down and world[x][y + 1] > 0: count+=1
    if left and up and world[x - 1][y - 1]: count+=1
    if right and up and world[x + 1][y - 1]: count+=1
    if left and down and world[x - 1][y + 1]: count+=1
    if right and down and world[x + 1][y + 1]: count+=1
    return count

def simulateWorld(world):
    newWorld = copy.deepcopy(clean)
    for y in range(height):
        for x in range(width):
            count = neighborCount(x, y)
            newWorld[x][y] = world[x][y]
            if world[x][y] == 0 and count == 3:
                newWorld[x][y] = 1
            elif world[x][y] == 1 and (count < 2 or count > 3):
                newWorld[x][y] = 0
    return newWorld


simulate = False
done = False
lastTick = 0
tick = 100
while not done:

    doTick = pygame.time.get_ticks() - lastTick > tick
    if doTick:
        lastTick = pygame.time.get_ticks()

    simulateTick = doTick and simulate

    inside = False
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    x, y = getSquare(pos[0], pos[1])
    if x < width and y < height and x >= 0 and y >= 0:
        inside = True
        if pressed[0] == 1:
            world[x][y] = 1
        elif pressed[2] == 1:
            world[x][y] = 0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                world = copy.deepcopy(clean)
            elif event.key == pygame.K_SPACE:
                simulate = not simulate
            elif event.key == pygame.K_d:
                simulateTick = True
                doTick = True
            elif inside:
                if event.key == pygame.K_1:
                    objects.placeObject(world, objects.GLIDER, x, y)
                if event.key == pygame.K_2:
                    objects.placeObject(world, objects.GLIDERGUN, x, y)

    if doTick:
        if simulateTick:
            world = simulateWorld(world)
        drawWorld()
        pygame.display.flip()


                
