import pygame
from noise import perlin
from sys import exit
noise = perlin.SimplexNoise()

screenWidth = 500
screenHeight = 500
width = 250
height = 250
blockWidth = float(screenWidth) / width
blockHeight = float(screenHeight) / height

screen = pygame.display.set_mode((screenWidth, screenHeight))


seedX = 0
seedY = 0
colors = [((0,0,0), -10), ((0, 191, 255), 0.1), ((0, 255, 0), 0), ((0, 255, 0), 0.5), ((255, 255, 255), 0.1), ((0, 0, 0), 10)]

def plotValue(value):
    if len(colors) == 0:
        return (0, 0, 0)
    for i in range(0, len(colors)):
        if i + 1 == len(colors):
            return colors[i][0]
        if value >= colors[i][1] and value < colors[i + 1][1]:
            part = float(value - colors[i][1]) / (colors[i + 1][1] - colors[i][1])
            other = 1 - part
            return (colors[i][0][0] * other + colors[i + 1][0][0] * part,
                    colors[i][0][1] * other + colors[i + 1][0][1] * part,
                    colors[i][0][2] * other + colors[i + 1][0][2] * part)
    return 0

smooth = 200
def getValue(x, y):
    return noise.noise2((seedX + x) / smooth, (seedY + y)  / smooth)
def draw():
    for x in range(width):
        for y in range(height):
            value = getValue(x, y)
            color = plotValue(value * abs(value))
            pygame.draw.rect(screen, color, (x * blockWidth, y * blockHeight, blockWidth, blockHeight))
    
    pygame.display.flip()
done = False

draw()
move = 10
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                seedX -= move
            elif event.key == pygame.K_d:
                seedX += move
            elif event.key == pygame.K_w:
                seedY -= move
            elif event.key == pygame.K_s:
                seedY += move
            draw()

print('Exiting')
pygame.quit()
exit()


