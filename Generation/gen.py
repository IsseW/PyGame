import pygame


class world:

    def ___init___(self, width, height):
        self.size = (width, height)
        self.creatures = []

class creature:

    def ___init___(self, stats):
        self.stats = stats

    def move(self, other):

    def addToWorld(self, world, position):
        world.creatures.append(self)
        self.world = world
        self.setPosition(position)

    def setPosition(self, position):
        self.position = position % world.size
        
