import sys
import pygame
from dfunction import DiffFunction

print('y\'=', end='')
inp = input()
function = DiffFunction(inp)
xstart = 0
ystart = 1
xmin = 0
xmax = 10
step = 0.01
val, ymin, ymax = function.getValues(xstart, ystart, xmin, xmax, step)
print(ymin, ymax)
W = 500
H = 500
screen = pygame.display.set_mode((W, H))
dX = W / (xmax - xmin)
dY = H / (ymax - ymin)
RED = (255, 0, 0)
def ScreenPoint(index):
    global val, dX, dY, step, ymin, H
    return dX * (index * step), H - dY * (val[index] - ymin)

def DrawFunction():
    lastpoint = ScreenPoint(0)
    for i in range(1, len(val)):
        point = ScreenPoint(i)
        pygame.draw.line(screen, RED, lastpoint, point)
        lastpoint = point
pygame.init();

white = (255, 255, 255)
clock = pygame.time.Clock()
drawn = False

while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
    if not drawn:
            screen.fill(white)
            DrawFunction()
            pygame.display.update()
            drawn = True
    clock.tick(30)

