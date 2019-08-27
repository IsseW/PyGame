import pygame
import noise

pygame.init()

width = 500
height = 300

screen = pygame.display-set_mode((width, height))

xPos = width / 5
yPos = 0

yValues = []

seed = 0

def getValues(seed, length):
    
