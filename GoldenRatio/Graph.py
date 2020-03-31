import pygame
import random
import pygame.gfxdraw
import math

choiceArr = [-1, 1]

x = 1
y = 1


windowWidth = 800
windowHeight = 800

TRANSPARENT = (0,0,0,200)
TRANSPARENTWHITE = (255, 255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def GetNextValue():
    global x, y
    z = x + y * random.choice(choiceArr)
    x = y
    y = z
    return z
    
values = [(0, 1)]
currentViewport = (0, -10, 10, 10)
viewport = [10000.0, 10000.0]

def FitInViewport(value):
    global viewport 
    if value[0] > viewport[0]:
        viewport[0] = value[0]
    if abs(value[1]) > viewport[1]:
        viewport[1] = abs(value[1])

def Transform(value):
    global currentViewport
    return ((value[0] - currentViewport[0]) * (windowWidth / (currentViewport[2] - currentViewport[0])),
            (value[1] - currentViewport[1]) * (windowHeight / (currentViewport[3] - currentViewport[1])))
def InvTransform(value):
    global currentViewport
    return (value[0] * ((currentViewport[2] - currentViewport[0]) / windowWidth) + (currentViewport[0]),
            value[1] * ((currentViewport[3] - currentViewport[1]) / windowHeight) + (currentViewport[1]))
def InsideViewport(value):
    global currentViewport
    return value[0] > currentViewport[0] and value[0] < currentViewport[2] and value[1] > currentViewport[1] and value[1] < currentViewport[3]
def Draw():
    global values, currentViewport
    screen.blit(rect, (0, 0))


    start = math.floor(currentViewport[0])
    if start + 1 > len(values):
        return
    end = math.ceil(currentViewport[2])
    
    p1 = Transform(values[start])
    #print(start, end)
    for i in range(start + 1, min(end, len(values)) - start - 1):
        #print(i)
        p2 = Transform(values[i])
        pygame.draw.line(screen, RED, p1, p2)
        p1 = p2
        
screen = pygame.display.set_mode((windowWidth, windowHeight))
rect = pygame.Surface((windowWidth,windowHeight), pygame.SRCALPHA, 32)
rect.fill(BLACK)


currentValue = 1

toCalc = 10000

lastH = 10.0
done = False
lastTick = 0
tick = 0
useBigViewport = True


selecting = False
startSelect = (0, 0)

while not done:
    doTick = pygame.time.get_ticks() - lastTick > tick
    if doTick:
        lastTick = pygame.time.get_ticks()

    
    pressed = pygame.mouse.get_pressed()

    pos = pygame.mouse.get_pos()
    
    if selecting:
        if not pressed[0] == 1:
            #Stop selecting
            selecting = False
            useBigViewport = False
            start = InvTransform(startSelect)
            end = InvTransform(pos)
            if not start[0] == end[0] and not start[1] == end[1]:
                currentViewport = (start[0], start[1], end[0], end[1])
    elif pressed[0] == 1:
        selecting = True
        startSelect = pos
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                useBigViewport = True
            #if event.key == pygame.K_A:
                #Linear regression
    if doTick:
        if toCalc  > 0:
            toCalc -= 1
        
            v = abs(GetNextValue())
            if v > 0: v = math.log(v)
            elif v < 0: v = -math.log(-v)
            
            value = (currentValue, v)
            currentValue += 1
            #FitInViewport(value)
            values.append(value)
        Draw()
        if selecting:
            pygame.draw.rect(screen, WHITE,(startSelect, (abs(startSelect[0] - pos[0]), abs(startSelect[1] - pos[1]))), 1)
        pygame.display.flip()
        if useBigViewport:
            currentViewport = (0, -viewport[1], viewport[0], viewport[1])
        

    tick -= 0.0001
    
