import pygame
import math
import pygame.gfxdraw
import cmath

pygame.init()

def PSqrd(a, b):
    return a * a + b * b

xMin = -5
yMin = -5
xMax = 5
yMax = 5

width = xMax - xMin
height = yMax - yMin
diagonalSqrd = max(PSqrd(xMax, yMax), PSqrd(xMax, yMin), PSqrd(xMin, yMax), PSqrd(xMin, yMin))

windowWidth = 800
windowHeight = 800

xScale = windowWidth / width
xHalf = xScale / 2
yScale = windowHeight / height
yHalf = yScale / 2


xRes = 1
yRes = 1


TRANSPARENT = (0,0,0,200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((windowWidth, windowHeight))

def complexFunction(z):
    if z.real == 0 and z.imag == 0: return complex(0, 0)
    return z*z

def function(x, y):
    z = complex(x, y)
    result = complexFunction(z)
    return result.real, result.imag

def pingpong(v, a, b):
    times = (v - a) // (b - a)
    value = (v - a) % (b - a)
    if times % 2 == 0:
        return a + value
    return b - value

def clamp(v, a, b):
    if v < a: return a
    if v > b: return b
    return v

def remap(v, f, t):
    return (v - f[0]) * (t[1] - t[0]) / (f[1] - f[0]) + t[0]

def getColor(x, y):
    return (pingpong(remap(x, (xMin, xMax), (0, 255)), 0, 255), pingpong(remap(x * x + y * y, (0, diagonalSqrd), (0, 255)), 0, 255), pingpong(remap(y, (yMin, yMax), (0, 255)), 0, 255))

def getSquare(x, y):
    return math.floor(x / xScale), math.floor(y / yScale)

def drawSquare(x, y, color):
    pygame.draw.rect(screen, color, (x, y, xRes, yRes))

def screenToWorld(x, y):
    return x / xScale + xMin, y / yScale + yMin

def worldToScreenX(x):
    return (x - xMin) * xScale
def worldToScreenY(y):
    return (y - yMin) * yScale

def worldToScreen(x, y):
    return worldToScreenX(x), worldToScreeny(y)

def drawWorld():
    for x in range(0, windowWidth, xRes):
        for y in range(0, windowHeight, yRes):
            worldX, worldY = screenToWorld(x, y)
            valueX, valueY = function(worldX, worldY)
            drawSquare(x, y, getColor(valueX, valueY))
    xAxis = worldToScreenY(0)
    if xAxis > 0 and xAxis < windowHeight:
        pygame.draw.line(screen, BLACK, (0, xAxis), (windowWidth, xAxis))
    yAxis = worldToScreenX(0)
    if yAxis > 0 and yAxis < windowWidth:
        pygame.draw.line(screen, BLACK, (yAxis, 0), (yAxis, windowHeight))

done = False

drawWorld()
pygame.display.flip()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

pygame.display.quit()
pygame.quit()
                
