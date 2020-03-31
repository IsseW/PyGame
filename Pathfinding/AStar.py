import math
import pygame
W = 100
H = 100
sqrt2 = math.sqrt(2)
def GetNeighbors(point):
    return [(point[0] + 1, point[1]),
            (point[0], point[1] + 1),
            (point[0] + 1, point[1] + 1),
            (point[0] - 1, point[1]),
            (point[0], point[1] - 1),
            (point[0] - 1, point[1] - 1),
            (point[0] + 1, point[1] - 1),
            (point[0] - 1, point[1]) + 1]
class Node(object):
    def __init__(self, x, y):
        self.pos = (x, y)
    def x(self):
        return self.pos[0]
    def y(self):
        return self.pos[1]
    def id(self):
        return self.y() * W + self.x()
    def __lt__(self, other):
        return self.id() < other.id()
    def __gt__(self, other):
        return self.id() > other.id()
    def 
class AStar:
    
    def FindPath(self, grid, start, end):
        open = [(start, 0)]
        closed = []
        
        while True:
            current = open.pop(0)
            closed.append(current)
            if current == end:
                return

            for p in GetNeighbors(current[0]):
                
                
            
