import pygame
import random
import copy
import sys
import math
import pygame.gfxdraw

pygame.init()

width = 100
height = 100

windowWidth = 500
windowHeight = 500

xScale = windowWidth / width
xHalf = xScale / 2
yScale = windowHeight / height
yHalf = yScale / 2

sys.setrecursionlimit(3000)

TRANSPARENT = (0,0,0,50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
POM = [-1, 0, 1]
PO = [0, 1]
OM = [-1 , 0]
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
def drawEllipse(x, y, color):
    pygame.draw.ellipse(screen, color, (x * xScale, y * yScale, xScale, yScale))
def drawTransparentSquare(x, y):
    pygame.gfxdraw.box(screen, (x * xScale, y * yScale, xScale, yScale), TRANSPARENT)
                 
def drawWorld():
    for x in range(width):
        for y in range(height):
            if world[x][y] < 0:
                drawSquare(x, y, WHITE)
            elif world[x][y] > 0:
                drawSquare(x, y, BLUE)
                
def simulateWorld(world):
    newWorld = copy.deepcopy(clean)
    for y in range(height):
        for x in range(width):
            if world[x][y] > 0:
                simulateBlock(x, y, newWorld)
            elif world[x][y] < 0:
                newWorld[x][y] = -1
    return newWorld

#assume x and y is in array
def IsFree(x, y, arr):
    return (arr[x][y] == 0 or arr[x][y] == 5) and (world[x][y] == 0 or world[x][y] == 5)

def simulateBlock(x, y, arr):
    value = world[x][y]
    if value == 5: return
    
    #Free
    down = y + 1 < height and IsFree(x, y + 1, arr)
    up = y - 1 >= 0 and IsFree(x, y - 1, arr)
    right = x + 1 < width and IsFree(x + 1, y, arr)
    left = x - 1 >= 0 and IsFree(x - 1, y, arr)

    downdown = down and y + 2 < height and IsFree(x, y + 2, arr)
    rightright = right and x + 2 < width and IsFree(x + 2, y, arr)
    leftleft = left and x - 2 >= 0 and IsFree(x - 2, y, arr)
    
    close = 0
    if not down: close+=1
    if not up: close+=1
    if not right: close+=1
    if not left: close+=1
    
    if not up and downdown:
        arr[x][y + 1] = 5
        arr[x][y + 2] = 1
    elif down:
        arr[x][y + 1] = 1
    elif (rightright or leftleft) and close >= 2 and random.choice(POM) < close - 2:
        if rightright:
            arr[x + 1][y] = 5
            arr[x + 2][y] = 4
        elif leftleft:
            arr[x - 1][y] = 5
            arr[x - 2][y] = 2
    elif right:
        if left:
            if value == 2:
                arr[x - 1][y] = 2
            elif value == 4:
                arr[x + 1][y] = 4
            else:
                move = random.choice(POM)
                arr[x + move][y] = 3 + move
        else:
            if value == 2:
                arr[x][y] = 3
            else:
                move = random.choice(PO)
                arr[x + move][y] = 3 + move
    elif left:
        if value == 4:
            arr[x][y] = 3
        else:
            move = random.choice(OM)
            arr[x + move][y] = 3 + move
    else:
        arr[x][y] = 3
        
def fill(x, y, value, level=0):
    if level > 2980:
        return
    if world[x][y] == 0:
        world[x][y] = value
        if x + 1 < width:
            fill(x + 1, y, value, level=level+1)
        if x - 1 >= 0:
            fill(x - 1, y, value, level=level+1)
        if y + 1 < height:
            fill(x, y + 1, value, level=level+1)
        if y - 1 >= 0:
            fill(x, y - 1, value, level=level+1)
done = False
last = 0
tick = 10
blitLast = False
while not done:

    value = 0
    
    keys = pygame.key.get_pressed()

    
    
    if keys[pygame.K_LCTRL]:
        value = 1
    else:
        value = -1
    bV = value > 0
    simulate = pygame.time.get_ticks() - last > tick
    inside = False
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    x, y = getSquare(pos[0], pos[1])
    if x < width and y < height and x >= 0 and y >= 0:
        inside = True
        if pressed[0] == 1 and world[x][y] >= 0:
            world[x][y] = value
        elif pressed[2] == 1:
            world[x][y] = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if inside:
                if event.key == pygame.K_f:
                    fill(x, y, value)
                elif event.key == pygame.K_h:
                    for _x in range(width):
                        world[_x][y] = value
                elif event.key == pygame.K_v:
                    for _y in range(height):
                        world[x][_y] = value
                        
            if event.key == pygame.K_r:
                for x in range(width):
                    for y in range(height):
                        if not ((world[x][y] > 0) ^ bV):
                            world[x][y] = 0
    
    
            
    if simulate:
        if keys[pygame.K_SPACE]:
            _x = random.choice(range(width))
            if world[_x][0] == 0:
                world[_x][0] = 1
        last = pygame.time.get_ticks()
        world = simulateWorld(world)
        if not blitLast:
            screen.blit(rect, (0, 0))
            blitLast = True
        else:
            blitLast = False
        drawWorld()
        pygame.display.flip()
        
pygame.display.quit()
pygame.quit()
        
        
    
        
