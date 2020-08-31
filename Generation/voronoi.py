import cv2
import random
import numpy as np
import math
from noise import perlin
noise = perlin.SimplexNoise()
def GetPoints(size):
    points = []
    for i in range(size):
        points.append([])
        for j in range(size):
            x = i / size
            y = j / size
            _x = random.random() / size
            _y = random.random() / size
            points[i].append((x + _x, y + _y))
    return points

def GetNoise(pos, distortion, offset):
    return (noise.noise2(pos[0] * distortion + offset, pos[1] * distortion + offset) + 1) / 2

def GetColor(position, distance, cell):
    
    t = math.sqrt(GetNoise(cell, 1, 0))
    t1 = math.sqrt(GetNoise(cell,2,10))
    t2 = math.sqrt(GetNoise(cell,4,20))
    #c = min(10 * distance / (distance+math.sqrt(distance)), 1)
    return [255 * t, 255 * t1, 255 * t2]

def DistanceSq(p1, p2):
    """
    p = ((abs(p1[0] - p2[0])), abs(p1[1] - p2[1]))

    #d = p[0] * p[0] + 2 * p[0] * p[1] + p[1] * p[1]
    d1 = p[1] * p[1]
    d2 = p[0] * p[0]
    d = 2 * d1 + 2 * d2 + 2 * p[0] * p[1]
    """
    p = (p1[0] - p2[0], p1[1] - p2[1])
    
    return p[0] * p[0] + p[1] * p[1] 

def GenerateVoronoi(points, imageSize):
    img = np.zeros((imageSize,imageSize,3), np.uint8)

    for i in range(imageSize):
        for j in range(imageSize):
            x  = i / imageSize
            y = j / imageSize
            pos = (x, y)
            _x = math.floor(len(points) * x)
            _y = math.floor(len(points) * y)
            
            check = [[points[abs(_x + 1) % len(points)][abs(_y + 1) % len(points[_x])], points[_x][abs(_y + 1) % len(points[_x])], points[(_x - 1) % len(points)][abs(_y + 1) % len(points[_x])]],
                     [points[abs(_x + 1) % len(points)][_y],                            points[_x][_y],                            points[(_x - 1) % len(points)][_y]],
                     [points[abs(_x + 1) % len(points)][(_y - 1) % len(points[_x])],    points[_x][(_y - 1) % len(points[_x])],    points[(_x - 1) % len(points)][(_y - 1) % len(points[_x])]]]
            
            
            minDist = 1
            iX = 0
            iY = 0
            for y_ in range(len(check)):
                for x_ in range(len(check[y_])):
                    c = DistanceSq(check[y_][x_], pos)
                    if c < minDist:
                        minDist = c
                        iX = x_
                        iY = y_
                    
                         
            
            img[i][j] = GetColor(pos, minDist, ((_x - (iX)), (_y - (iY))))
    
    cv2.imwrite('voronoi.png',img)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
points = GetPoints(10)
GenerateVoronoi(points, 1000)
